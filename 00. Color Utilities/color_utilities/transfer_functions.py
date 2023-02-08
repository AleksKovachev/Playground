"""This module contains transfer functions for various color spaces"""
# pylint: disable=invalid-name, unsubscriptable-object, unused-argument
from math import log, log2, log10, log1p, copysign, exp, e

from . import internal_helpers as ih
from . import alexa_transfer_function_helpers as atfh


def srgb(RGB: tuple | list, depth: int = 8, decode: bool = False, output="direct", **kwargs):
    """### Converts between Linear and Gamma-corrected sRGB values. \
        This is the sRGB electro-optical transfer function (EOTF) and its inverse

    ### Args:
        `RGB` (tuple | list): The R, G, B values to be converted
        `depth` (int | float): The bit depth of the input RGB values. Defaults to 8-bit (range 0-255)
        `decode` (bool, optional): Decode, convert the values to linear. Defaults to False.
        `output` (str, optional): Either "hex", "hexp", "normalized", "round" or "direct"
        *     hex returns a hex string color in the form of decade
        *     hexp returns a hex string color in the form of #facade
        *     normalized returns a tuple(R, G, B) where the values are floats in range 0-1
        *     round returns a tuple(R, G, B) where the values are integers in range 0-255
        *     direct returns a tuple(R, G, B) where the values are floats in range 0-255
        *     In any invalid case the "direct" approach will be used

    Reference https://www.itu.int/dms_pubrec/itu-r/rec/bt/R-REC-BT.709-6-201506-I!!PDF-E.pdf

    ### Returns:
        tuple[R, G, B]
    """
    RGB = ih.check_color(RGB, depth=depth, normalized=True)
    if decode:  # Linearize EOTF
        check = srgb((0.0031308, 0.0031308, 0.0031308), output="normalized")[0]    # ~0.04045
        R, G, B = (((i + 0.055) / 1.055) ** 2.4 if i > check else i / 12.92 for i in RGB)
        return ih.return_rgb((R, G, B), normalized_input=True, output=output)
    # EOTF Inverse
    R, G, B = (1.055 * (i ** (1 / 2.4)) - 0.055 if i > 0.0031308 else i * 12.92 for i in RGB)
    return ih.return_scale((R, G, B), normalized_input=True, output=output)


def rec601(RGB: tuple | list, decode: bool = False, output="normalized", **kwargs) -> str | tuple:
    """### Converts between Linear and Gamma-corrected Rec. 601 / Rec.709 values \
        This is the Rec. 601 / Rec. 709 opto-electronic transfer function (OETF) and its inverse

    ### Args:
        `RGB` (tuple | list): The R, G, B values to be converted
        `decode` (bool, optional): Decode, convert the values to linear. Defaults to False.
        `output` (str, optional): Either "hex", "hexp", "normalized", "round" or "direct"
        *     hex returns a hex string color in the form of decade
        *     hexp returns a hex string color in the form of #facade
        *     normalized returns a tuple(R, G, B) where the values are floats in range 0-1
        *     round returns a tuple(R, G, B) where the values are integers in range 0-255
        *     direct returns a tuple(R, G, B) where the values are floats in range 0-255
        *     In any invalid case the "direct" approach will be used

    Reference 1 https://www.itu.int/dms_pubrec/itu-r/rec/bt/R-REC-BT.709-6-201506-I!!PDF-E.pdf
    Reference 2 http://www.itu.int/dms_pubrec/itu-r/rec/bt/R-REC-BT.601-7-201103-I!!PDF-E.pdf
    Reference 3 https://en.wikipedia.org/wiki/Rec._709
    Reference 4 https://www.color.org/chardata/rgb/bt601.xalter

    For Rec. 709, RGB values should be clipped in range 16-235

    ### Returns:
        tuple[R, G, B]
    """
    RGB = ih.check_color(RGB, normalized=True)
    if decode:  # Linearize / OETF
        R, G, B = (i * 4.5 if i < 0.018 else 1.099 * i ** 0.45 - 0.099 for i in RGB)
        return ih.return_rgb((R, G, B), normalized_input=True, clamp=0, output=output)
    # OETF Inverse
    check = rec601((0.018, 0.018, 0.018), decode=True)[0]
    R, G, B = (i / 4.5 if i < check else ((i + 0.099) / 1.099) ** (1 / 0.45) for i in RGB)
    return ih.return_rgb((R, G, B), normalized_input=True, clamp=0, output=output)


def rec2020(RGB: tuple | list, decode: bool = False, depth: int = 10, output="normalized", **kwargs) -> str | tuple:
    """### Converts between Linear and Gamma-corrected Rec.2020 values \
        This is the Rec. 2020 opto-electronic transfer function (OETF) and its inverse

    ### Args:
        `RGB` (tuple | list): The R, G, B values to be converted
        `decode` (bool, optional): Decode, convert the values to linear. Defaults to False.
        `depth` (int | float): The bit depth of the input RGB values. Defaults to 10-bit (range 0-1023)
        `output` (str, optional): Either "hex", "hexp", "normalized", "round" or "direct"
        *     hex returns a hex string color in the form of decade
        *     hexp returns a hex string color in the form of #facade
        *     normalized returns a tuple(R, G, B) where the values are floats in range 0-1
        *     round returns a tuple(R, G, B) where the values are integers in range 0-255
        *     direct returns a tuple(R, G, B) where the values are floats in range 0-255
        *     In any invalid case the "direct" approach will be used

    Reference 1 https://en.wikipedia.org/wiki/Rec._2020
    Reference 2 https://www.color.org/chardata/rgb/BT2020.xalter

    NOTE: The reference electro-optical transfer function (EOTF) for a Rec.2020 display is defined in ITU-R BT.1886.
    Some implementors use the inverse of the (OETF) as defined in BT.2020 (BT.2087 case #2) in place of ITU-R BT.1886.

    ### Returns:
        tuple[R, G, B]
    """
    if depth not in (10, 10., 12, 12.):
        raise ValueError("The depth for Rec. 2020 can either be 10 or 12 bits!")
    RGB = ih.check_color(RGB, depth=depth, normalized=True)

    beta = 0.018053968510807
    alpha = 1 + 5.5 * beta # ~1.09929682680944 # 10 * BETA ** 0.55

    if decode:  # Linearize / OETF
        RGB = (i * 4.5 if i < beta else alpha * i ** 0.45 - (alpha - 1) for i in RGB)
        return ih.return_rgb(RGB, normalized_input=True, clamp=0, output=output)

    # OETF Inverse
    RGB = (i / 4.5 if i < rec2020((beta, beta, beta), decode=True)[0]
           else ((i + (alpha - 1)) / alpha) ** 1/0.45 for i in RGB)
    return ih.return_rgb(RGB, normalized_input=True, clamp=0, output=output)


def romm(RGB: tuple | list, decode: bool = False, depth: int = 8, output="normalized", **kwargs):
    """### Converts between Linear and Gamma-corrected ROMM (ProPhoto) values \
        This is the ROMM color component transfer function (CCTF).

    ### Args:
        `RGB` (tuple | list): The R, G, B values to be converted
        `decode` (bool, optional): Decode, convert the values to linear. Defaults to False.
        `depth` (int | float): The bit depth of the input RGB values. Defaults to 8-bit (range 0-255)
        `output` (str, optional): Either "hex", "hexp", "normalized", "round" or "direct"
        *     hex returns a hex string color in the form of decade
        *     hexp returns a hex string color in the form of #facade
        *     normalized returns a tuple(R, G, B) where the values are floats in range 0-1
        *     round returns a tuple(R, G, B) where the values are integers in range 0-255
        *     direct returns a tuple(R, G, B) where the values are floats in range 0-255
        *     In any invalid case the "direct" approach will be used

    Reference 1 http://www.color.org/ROMMRGB.pdf
    Reference 2 http://www.photo-lovers.org/pdf/color/romm.pdf

    ### Returns:
        tuple[R, G, B]
    """
    if depth not in (8, 8., 12, 12., 16, 16.):
        raise ValueError("The depth for Rec. 2020 can either be 10 or 12 bits!")
    RGB = ih.check_color(RGB, depth=depth, normalized=True)
    if decode:  # Linearize / Decoding CCTF
        R, G, B = (i / 16 if i < 16 * (1/512) else i ** 1.8 for i in RGB)
        return ih.return_rgb((R, G, B), depth=depth, normalized_input=True, clamp=0, output=output)
    # Encoding CCTF
    R, G, B = (i * 16 if i < 1/512 else i ** (1/1.8) for i in RGB)
    return ih.return_rgb((R, G, B), depth=depth, normalized_input=True, clamp=0, output=output)


def eci(RGB: tuple | list, decode: bool = False, depth: int = 8, output="normalized", **kwargs):
    """### Converts between Linear and Gamma-corrected ROMM (ProPhoto) values \
        This is the ROMM color component transfer function (CCTF).

    ### Args:
        `RGB` (tuple | list): The R, G, B values to be converted
        `decode` (bool, optional): Decode, convert the values to linear. Defaults to False.
        `depth` (int | float): The bit depth of the input RGB values. Defaults to 8-bit (range 0-255)
        `output` (str, optional): Either "hex", "hexp", "normalized", "round" or "direct"
        *     hex returns a hex string color in the form of decade
        *     hexp returns a hex string color in the form of #facade
        *     normalized returns a tuple(R, G, B) where the values are floats in range 0-1
        *     round returns a tuple(R, G, B) where the values are integers in range 0-255
        *     direct returns a tuple(R, G, B) where the values are floats in range 0-255
        *     In any invalid case the "direct" approach will be used

    Reference http://www.eci.org/_media/downloads/icc_profiles_from_eci/ecirgbv20.zip

    ### Returns:
        tuple[R, G, B]
    """
    if depth not in (8, 8., 16, 16.):
        raise ValueError("The depth for Rec. 2020 can either be 10 or 12 bits!")
    RGB = ih.check_color(RGB, depth=depth, normalized=True)
    CIE_E = 216 / 24389 # 0.008856  # epsilon
    CIE_K = 24389 / 27 # 903.3  # kappa

    if decode:  # Linearize / Decoding CCTF
        YYN = [(i*100 + 16) / 116 for i in RGB]
        R, G, B = [i**3 if i > 24 / 116 else (i - 16 / 116) * (108 / 841) for i in YYN]

        return ih.return_rgb((R, G, B), depth=depth, normalized_input=True, clamp=0, output=output)

    # Encoding CCTF
    R, G, B = ((116 * i** (1/3) - 16) / 100 if i > CIE_E else (i * CIE_K) / 100 for i in RGB)

    return ih.return_rgb((R, G, B), depth=depth, normalized_input=True, clamp=0, output=output)


def rimm(RGB: tuple | list, decode: bool = False, exposure: int = 2, depth: int = 8, output="normalized", **kwargs):
    """### Converts between Linear and Gamma-corrected RIMM values \
        This is the RIMM color component transfer function (CCTF).

    ### Args:
        `RGB` (tuple | list): The R, G, B values to be converted
        `decode` (bool, optional): Decode, convert the values to linear. Defaults to False.
        `exposure` (int, optional): Maximum exposure level.
        `depth` (int | float): The bit depth of the input RGB values. Defaults to 8-bit (range 0-255)
        `output` (str, optional): Either "hex", "hexp", "normalized", "round" or "direct"
        *     hex returns a hex string color in the form of decade
        *     hexp returns a hex string color in the form of #facade
        *     normalized returns a tuple(R, G, B) where the values are floats in range 0-1
        *     round returns a tuple(R, G, B) where the values are integers in range 0-255
        *     direct returns a tuple(R, G, B) where the values are floats in range 0-255
        *     In any invalid case the "direct" approach will be used

    Reference 1 http://www.photo-lovers.org/pdf/color/romm.pdf
    Reference 2 https://www.color.org/chardata/rgb/rimmrgb.xalter

    ### Returns:
        tuple[R, G, B]
    """
    if depth not in (8, 8., 12, 12., 16, 16.):
        raise ValueError("The depth for Rec. 2020 can either be 10 or 12 bits!")
    RGB = ih.check_color(RGB, depth=depth, normalized=True)
    clip = 1.099 * exposure ** 0.45 - 0.099
    if decode:  # Linearize / Decoding CCTF
        check = rimm((0.018, 0.018, 0.018), depth=depth, exposure=exposure)[0]
        R, G, B = (i * clip / 4.5 if i < check else ((i * clip + 0.099) / 1.099) ** (1 / 0.45) for i in RGB)
        return ih.return_rgb((R, G, B), depth=depth, normalized_input=True, clamp=0, output=output)
    # Encoding CCTF
    out = [(i * 4.5) / clip if i < 0.018 else (1.099 * i ** 0.45 - 0.099) / clip for i in RGB]
    return ih.return_rgb(out, depth=depth, normalized_input=True, clamp=0, output=output)


def erimm(RGB: tuple | list, decode: bool = False, exp_min: float = 0.001, exp_max: float = 316.2, depth: int = 8, output="normalized", **kwargs):
    """### Converts between Linear and Gamma-corrected ERIMM values \
        This is the ERIMM opto-electronic/electro-optical transfer function (OETF).

    ### Args:
        `RGB` (tuple | list): The R, G, B values to be converted
        `decode` (bool, optional): Decode, convert the values to linear. Defaults to False.
        `exp_min` (int, optional): Minimum exposure. Defaults to 0.001.
        `exp_max` (int, optional): Maximum exposure. Defaults to 316.2.
        `depth` (int | float): The bit depth of the input RGB values. Defaults to 8-bit (range 0-255)
        `output` (str, optional): Either "hex", "hexp", "normalized", "round" or "direct"
        *     hex returns a hex string color in the form of decade
        *     hexp returns a hex string color in the form of #facade
        *     normalized returns a tuple(R, G, B) where the values are floats in range 0-1
        *     round returns a tuple(R, G, B) where the values are integers in range 0-255
        *     direct returns a tuple(R, G, B) where the values are floats in range 0-255
        *     In any invalid case the "direct" approach will be used

    ```
    Relative exposure to Relative Log exposure
    0.001   -3.00
    0.01    -2.00
    0.10    -1.00
    0.18    -0.75
    1.00     0.00
    2.00     0.30
    8.00     0.90
    32.00    1.50
    316.23   2.50
    ```

    Reference 1 http://www.photo-lovers.org/pdf/color/romm.pdf
    Reference 2 https://www.color.org/chardata/rgb/erimmrgb.xalter

    ### Returns:
        tuple[R, G, B]
    """
    if depth not in (8, 8., 12, 12., 16, 16.):
        raise ValueError("The depth for Rec. 2020 can either be 10 or 12 bits!")
    RGB = ih.check_color(RGB, depth=depth, normalized=True, clamp=False)
    euler_min = e * exp_min
    lg = log(euler_min)
    exp_min = log(exp_min)
    exp_max = log(exp_max)

    if decode:  # Linearize / Decoding OETF
        check = ((lg - exp_min) / (exp_max - exp_min))
        RGB = (exp(i * (exp_max - exp_min) + exp_min) if i > check else
               ((exp_max - exp_min) / (lg - exp_min)) * (i * euler_min) for i in RGB)
        return ih.return_rgb(RGB, depth=depth, normalized_input=True, clamp=0, output=output)

    # Encoding EOTF
    RGB = (max(0, min(i, 1)) for i in RGB)
    RGB = ((log(i) - exp_min) / (exp_max - exp_min) if i > euler_min else
           ((lg - exp_min) / (exp_max - exp_min)) * i / euler_min for i in RGB)
    # RGB = [16 * i if i < 0.001953 else i ** (1/1.8) for i in RGB]
    return ih.return_rgb(RGB, depth=depth, normalized_input=True, clamp=0, output=output)


def blackmagic(RGB: tuple | list, decode: bool = False, **kwargs):
    """### Converts between Linear and Gamma-corrected Blackmagic Film Gen 5 values \
        This is the Blackmagic Film Gen 5 opto-electronic transfer function (OETF).

    ### Args:
        `RGB` (tuple | list): The R, G, B values to be converted
        `decode` (bool, optional): Decode, convert the values to linear. Defaults to False.

    Reference https://drive.google.com/file/d/1FF5WO2nvI9GEWb4_EntrBoV9ZIuFToZd/view

    ### Returns:
        tuple[R, G, B]
    """
    RGB = ih.check_color(RGB, depth=12, normalized=True, clamp=False)
    A = 0.08692876065491224
    B = 0.005494072432257808
    C = 0.5300133392291939
    D = 8.283605932402494
    E = 0.09246575342465753
    LIN_CUT = 0.005

    if decode:  # Linearize / Decoding OETF
        LOG_CUT = D * LIN_CUT + E
        return [(i - E) / D if i < LOG_CUT else exp((i - C) / A) - B for i in RGB]

    # Encoding OETF Inverse
    return [D * i + E if i < LIN_CUT else A * log(i + B) + C for i in RGB]


def davinci(RGB: tuple | list, decode: bool = False, **kwargs):
    """### Converts between Linear and Gamma-corrected DaVinci values \
        This is the DaVinci opto-electronic transfer function (OETF).

    ### Args:
        `RGB` (tuple | list): The R, G, B values to be converted
        `decode` (bool, optional): Decode, convert the values to linear. Defaults to False.

    Reference https://documents.blackmagicdesign.com/InformationNotes/DaVinci_Resolve_17_Wide_Gamut_Intermediate.pdf?_v=1607414410000

    ### Returns:
        tuple[R, G, B]
    """
    RGB = ih.check_color(RGB, depth=10, normalized=True, clamp=False)
    DI_A, DI_B, DI_C, DI_M, DI_LIN_CUT = 0.0075, 7.0, 0.07329248, 10.44426855, 0.00262409

    if decode:  # Linearize / Decoding OETF
        DI_LOG_CUT = 0.02740668
        return [2 ** ((i / DI_C) - DI_B) - DI_A if i > DI_LOG_CUT else i / DI_M for i in RGB]

    # Encoding OETF Inverse
    return [DI_C * (log2(i + DI_A) + DI_B) if i > DI_LIN_CUT else i * DI_M for i in RGB]


def dcdm(XYZ: tuple | list, decode: bool = False, normalized: bool = True, **kwargs):
    """### The DCDM electro-optical transfer function (EOTF). \
        Converts between standard and linear tristimulus values.

    ### Args:
        `XYZ` (tuple | list): The X, Y, Z tristimulus values to be converted
        `decode` (bool, optional): Decode, convert the values to linear. Defaults to False.
        `normalized` (bool, optional): Wether the input/output values are in normalized range (0-1). Defaults to True.

    Reference http://www.dcimovies.com/archives/spec_v1_1/DCI_DCinema_System_Spec_v1_1.pdf

    ### Returns:
        tuple[R, G, B]
    """
    depth = 12 if decode else 1
    XYZ = ih.check_color(XYZ, depth=depth, normalized=True, clamp=False)

    if decode:  # Linearize / Decoding EOTF
        return [52.37 * i ** 2.6 for i in XYZ]

    # Encoding EOTF Inverse
    XYZ = [(i / 52.37) ** (1 / 2.6) for i in XYZ]
    return XYZ if normalized else [round(i * 4095) for i in XYZ]


def slog(RGB: tuple | list, reflection: bool = True, decode: bool = False, depth: int = 10, norm_range: bool = True, **kwargs):
    """### Converts between Linear and Gamma-corrected S-Log values \
        This is the S-Log opto-electronic/electro-optical transfer function (OETF)/(EOTF).

    ### Args:
        `RGB` (tuple | list): The R, G, B values to be converted
        `reflection` (bool): Whether the light level to a camera is reflection. Defaults to True.
        `decode` (bool, optional): Decode, convert the values to linear. Defaults to False.
        `depth` (int | float): The bit depth of the input RGB values. Defaults to 10-bit (range 0-1023)
        `norm_range` (bool, optional): Whether the RGB values are encoded as normalised code values.

    Reference https://drive.google.com/file/d/1Q1RYri6BaxtYYxX0D4zVD6lAmbwmgikc/view?usp=sharing

    ### Returns:
        tuple[R, G, B]
    """
    RGB = ih.check_color(RGB, depth=depth, normalized=True, clamp=False)
    mult = 2 ** (depth - 8)
    scope = 16 * mult, 235 * mult
    max_value = 2 ** depth - 1

    if decode:  # Linearize / Decoding EOTF
        RGB = [((i * max_value) - scope[0]) / (scope[1] - scope[0]) for i in RGB] if norm_range else RGB
        check = slog((0, 0, 0), depth=depth, norm_range=norm_range)[0]
        RGB = [(i - 0.030001222851889303) / 5.0 if i < check else 10 ** ((i - 0.616596 - 0.03) / 0.432699) - 0.037584 for i in RGB]

        return [i * 0.9 for i in RGB] if reflection else RGB

    RGB = [i / 0.9 for i in RGB] if reflection else RGB
    # Encoding OETF
    RGB = [i * 5 + 0.030001222851889303 if i < 0 else ((0.432699 * log10(i + 0.037584) + 0.616596) + 0.03) for i in RGB]

    return [((scope[1] - scope[0]) * i + scope[0]) / max_value for i in RGB] if norm_range else RGB


def slog2(RGB: tuple | list, reflection: bool = True, decode: bool = False, depth: int = 10, norm_range: bool = True, **kwargs):
    """### Converts between Linear and Gamma-corrected S-Log2 values \
        This is the S-Log2 opto_electronic/electro-optical transfer function (OETF)/(EOTF).

    ### Args:
        `RGB` (tuple | list): The R, G, B values to be converted
        `reflection` (bool): Whether the light level to a camera is reflection. Defaults to True.
        `decode` (bool, optional): Decode, convert the values to linear. Defaults to False.
        `depth` (int | float): The bit depth of the input RGB values. Defaults to 10-bit (range 0-1023)
        `norm_range` (bool, optional): Whether the RGB values are encoded as normalised code values.

    Reference https://drive.google.com/file/d/1Q1RYri6BaxtYYxX0D4zVD6lAmbwmgikc/view?usp=sharing

    ### Returns:
        tuple[R, G, B]
    """
    RGB = ih.check_color(RGB, depth=depth, normalized=True, clamp=False)

    if decode:  # Linearize / Decoding EOTF
        return [219 * i / 155 for i in slog(RGB, reflection=reflection, decode=True, depth=depth, norm_range=norm_range)]

    # Encoding OETF
    return slog([i * 155 / 219 for i in RGB], reflection=reflection, depth=depth, norm_range=norm_range)


def slog3(RGB: tuple | list, reflection: bool = True, decode: bool = False, depth: int = 10, norm_range: bool = True, **kwargs):
    """### Converts between Linear and Gamma-corrected S-Log3 values \
        This is the S-Log3 opto-electronic/electro-optical transfer function (OETF)(EOTF).

    ### Args:
        `RGB` (tuple | list): The R, G, B values to be converted
        `reflection` (bool): Whether the light level to a camera is reflection. Defaults to True.
        `decode` (bool, optional): Decode, convert the values to linear. Defaults to False.
        `depth` (int | float): The bit depth of the input RGB values. Defaults to 10-bit (range 0-1023)
        `norm_range` (bool, optional): Whether the RGB values are encoded as normalised code values.

    Reference http://www.starcentral.ca/forums/TechnicalSummary_for_S-Gamut3Cine_S-Gamut3_S-Log3_V1_00.pdf

    ### Returns:
        tuple[R, G, B]
    """
    RGB = ih.check_color(RGB, depth=depth, normalized=True, clamp=False)
    mult = 2 ** (depth - 8)
    scope = 16 * mult, 235 * mult
    max_value = 2 ** depth - 1

    if decode:  # Linearize / Decoding EOTF
        RGB = RGB if norm_range else [((scope[1] - scope[0]) * i + scope[0]) / max_value for i in RGB]
        RGB = [(i * 1023 - 95) * 0.01125000 / (171.2102946929 - 95) if i < 171.2102946929 / 1023
                else ((10 ** ((i * 1023 - 420) / 261.5)) * (0.18 + 0.01) - 0.01) for i in RGB]

        return RGB if reflection else [i / 0.9 for i in RGB]

    RGB = RGB if reflection else [i * 0.9 for i in RGB]

    # Encoding OETF
    RGB = [(i * (171.2102946929 - 95) / 0.01125 + 95) / 1023 if i < 0.01125 else
            (420 + log10((i + 0.01) / (0.18 + 0.01)) * 261.5) / 1023 for i in RGB]

    return RGB if norm_range else [((i * max_value) - scope[0]) / (scope[1] - scope[0]) for i in RGB]


def vlog(RGB: tuple | list, reflection: bool = True, decode: bool = False, depth: int = 10, norm_range: bool = True, **kwargs):
    """### Converts between Linear and Gamma-corrected V-Log values \
        This is the V-Log opto-electronic/electro-optical transfer function (OETF)/(EOTF).

    ### Args:
        `RGB` (tuple | list): The R, G, B values to be converted
        `reflection` (bool): Whether the light level to a camera is reflection. Defaults to True.
        `decode` (bool, optional): Decode, convert the values to linear. Defaults to False.
        `depth` (int | float): The bit depth of the input RGB values. Defaults to 10-bit (range 0-1023)
        `norm_range` (bool, optional): Whether the RGB values are encoded as normalised code values.

    Reference https://pro-av.panasonic.net/en/cinema_camera_varicam_eva/support/pdf/VARICAM_V-Log_V-Gamut.pdf

    ### Returns:
        tuple[R, G, B]
    """
    RGB = ih.check_color(RGB, depth=depth, normalized=True, clamp=False)
    mult = 2 ** (depth - 8)
    scope = 16 * mult, 235 * mult
    max_value = 2 ** depth - 1

    b, c, d = 0.00873, 0.241514, 0.59820

    if decode:  # Linearize / Decoding EOTF
        RGB = [i if norm_range else ((scope[1] - scope[0]) * i + scope[0])/max_value for i in RGB]
        RGB = [(i - 0.125) / 5.6 if i < 0.181 else 10 ** ((i - d) / c) - b for i in RGB]

        return RGB if reflection else [i / 0.9 for i in RGB]

    RGB = RGB if reflection else [i * 0.9 for i in RGB]

    # Encoding OETF
    RGB = [5.6 * i + 0.125 if i < 0.01 else c * log10(i + b) + d for i in RGB]

    return RGB if norm_range else [((i * max_value) - scope[0]) / (scope[1] - scope[0]) for i in RGB]


def flog(RGB: tuple | list, reflection: bool = True, decode: bool = False, depth: int = 10, norm_range: bool = True, **kwargs):
    """### Converts between Linear and Gamma-corrected F-Log values \
        This is the F-Log opto-electronic/electro-optical transfer function (OETF)/(EOTF).

    ### Args:
        `RGB` (tuple | list): The R, G, B values to be converted
        `reflection` (bool): Whether the light level to a camera is reflection. Defaults to True.
        `decode` (bool, optional): Decode, convert the values to linear. Defaults to False.
        `depth` (int | float): The bit depth of the input RGB values. Defaults to 10-bit (range 0-1023)
        `norm_range` (bool, optional): Whether the RGB values are encoded as normalised code values.

    Reference https://www.fujifilm.com/support/digital_cameras/software/lut/pdf/F-Log_DataSheet_E_Ver.1.0.pdf

    ### Returns:
        tuple[R, G, B]
    """
    RGB = ih.check_color(RGB, depth=depth, normalized=True, clamp=False)
    mult = 2 ** (depth - 8)
    scope = 16 * mult, 235 * mult
    max_value = 2 ** depth - 1

    a, b, c, d, _e, f = 0.555556, 0.009468, 0.344676, 0.790453, 8.735631, 0.092864

    if decode:  # Linearize / Decoding EOTF
        RGB = [i if norm_range else ((scope[1] - scope[0]) * i + scope[0]) / max_value for i in RGB]
        RGB = [(i - f) / _e if i < 0.100537775223865 else (10 ** ((i - d) / c)) / a - b / a for i in RGB]

        return RGB if reflection else [i / 0.9 for i in RGB]

    RGB = RGB if reflection else [i * 0.9 for i in RGB]

    # Encoding OETF
    RGB = [_e * i + f if i < 0.00089 else c * log10(a * i + b) + d for i in RGB]
    return RGB if norm_range else [((i * max_value) - scope[0]) / (scope[1] - scope[0]) for i in RGB]


def nlog(RGB: tuple | list, reflection: bool = True, decode: bool = False, depth: int = 10, norm_range: bool = True, **kwargs):
    """### Converts between Linear and Gamma-corrected N-Log values \
        This is the N-Log opto-electronic/electro-optical transfer function (OETF)/(EOTF).

    ### Args:
        `RGB` (tuple | list): The R, G, B values to be converted
        `reflection` (bool): Whether the light level to a camera is reflection. Defaults to True.
        `decode` (bool, optional): Decode, convert the values to linear. Defaults to False.
        `depth` (int | float): The bit depth of the input RGB values. Defaults to 10-bit (range 0-1023)
        `norm_range` (bool, optional): Whether the RGB values are encoded as normalised code values.

    Reference http://download.nikonimglib.com/archive3/hDCmK00m9JDI03RPruD74xpoU905/N-Log_Specification_(En)01.pdf

    ### Returns:
        tuple[R, G, B]
    """
    RGB = ih.check_color(RGB, depth=depth, normalized=True, clamp=False)
    mult = 2 ** (depth - 8)
    scope = 16 * mult, 235 * mult
    max_value = 2 ** depth - 1

    a, b, c, d = 650 / 1023, 0.0075, 150 / 1023, 619 / 1023

    if decode:  # Linearize / Decoding EOTF
        RGB = [i if norm_range else ((scope[1] - scope[0]) * i + scope[0]) / max_value for i in RGB]
        RGB = [(i / a) ** 3 - b if i < 452 / 1023 else exp((i - d) / c) for i in RGB]

        return RGB if reflection else [i / 0.9 for i in RGB]

    RGB = RGB if reflection else [i * 0.9 for i in RGB]
    # Encoding OETF
    RGB = [a * (i + b) ** (1/3) if i < 0.328 else c * log(i) + d for i in RGB]
    return RGB if norm_range else [((i * max_value) - scope[0]) / (scope[1] - scope[0]) for i in RGB]


def djidlog(RGB: tuple | list, decode: bool = False, **kwargs):
    """### Converts between Linear and DJI D-Log values. This defines the DJI D-Log log encoding curve.

    ### Args:
        `RGB` (tuple | list): The R, G, B values to be converted
        `decode` (bool, optional): Decode, convert the values to linear. Defaults to False.

    Reference https://dl.djicdn.com/downloads/zenmuse+x7/20171010/D-Log_D-Gamut_Whitepaper.pdf

    ### Returns:
        tuple[R, G, B]
    """
    RGB = ih.check_color(RGB, depth=10, normalized=True, clamp=False)
    if decode:  # Linearize / Decoding
        return [(10 ** (3.89616 * i - 2.27752) - 0.0108) / 0.9892 if i > 0.14 else (i - 0.0929) / 6.025 for i in RGB]
    # Encoding
    return [(log10(i * 0.9892 + 0.0108)) * 0.256663 + 0.584555 if i > 0.0078 else 6.025 * i + 0.0929 for i in RGB]


def filmlighttlog(RGB: tuple | list, w: int = 128, g: int = 16, o: float = 0.075, decode: bool = False, **kwargs):
    """### Converts between Linear and Gamma-corrected FilmlightTLog values \
        This is the FilmlightTLog opto-electronic/electro-optical transfer function (OETF)/(EOTF).

    ### Args:
        `RGB` (tuple | list): The R, G, B values to be converted
        `w` (int, optional): x value for y = 1.0. Defaults to 128.
        `g` (int, optional): The gradient at x = 0. Defaults to 16.
        `o` (float, optional): y value for x = 0.0. Defaults to 0.075.
        `decode` (bool, optional): Decode, convert the values to linear. Defaults to False.

    T-Log, a cineon driven log tone-curve developed by FilmLight.
    The colour space is designed to be used as Working Colour Space.

    #### I don't have an exact solution but the formula for b gives an approximation. \
        The gradient is not g, but should be within a few percent for most sensible values of (w*g).

    Reference https://github.com/colour-science/colour/blob/develop/colour/models/rgb/transfer_functions/filmlight_t_log.py

    ### Returns:
        tuple[R, G, B]
    """
    b = 1 / (0.7107 + 1.2359 * log(w * g))
    gs = g / (1 - o)
    C = b / gs                              # A, B, C are constants calculated from
    a = 1 - b * log(w + C)                  # w = x value for y = 1.0
    s = (1 - o) / (1 - (a + b * log(C)))    # g = The gradient at x = 0
    A = 1 + (a - 1) * s                     # o = y value for x = 0.0
    B = b * s
    G = gs * s

    if decode:  # Linearize / Decoding
        return [(i - o) / G if i < o else exp((i - A) / B) - C for i in RGB]

    # Encoding
    return [G * i + o if i < 0 else log(i + C) * B + A for i in RGB]


def arri_log_c3(RGB: tuple | list, depth: int = 10, firmware: int = 3, linear: bool = True, EI: int = 800, decode: bool = False, **kwargs):
    """### Converts between Linear and ARRI LogC3 values \
        This is the ARRI LogC3 opto-electronic/electro-optical transfer function (OETF)/(EOTF).

    ### Args:
        `RGB` (tuple | list): The R, G, B values to be converted
        `depth` (int | float): The bit depth of the input RGB values [10 or 12]. Defaults to 10-bit (range 0-1023)
        `firmware` (int, optional): Alexa firmware version. Either 2 ("SUP 2.x") or 3 ("SUP 3.x"). Defaults to 3.
        `linear` (bool, optional): Conversion method. Either True ("Linear Scene Exposure Factor") or
                                                False ("Normalised Sensor Signal"). Defaults to True.
        `EI` (int, optional): Exposure index. One of (160, 200, 250, 320, 400, 500, 640, 800, 1000, 1280, 1600). Defaults to 800.
        `decode` (bool, optional): Decode, convert the values to linear. Defaults to False.

    Reference https://drive.google.com/open?id=1t73fAG_QpV7hJxoQPYZDWvOojYkYDgvn

    ### Returns:
        tuple[R, G, B]
    """
    RGB = ih.check_color(RGB, depth=depth, normalized=True, clamp=False)
    method = {True: "Linear Scene Exposure Factor", False: "Normalised Sensor Signal"}
    if firmware not in (2, 3):
        raise ValueError("Firmware version can only be either 2 or 3!")
    if EI not in (160, 200, 250, 320, 400, 500, 640, 800, 1000, 1280, 1600):
        raise ValueError("Exposure index can only be one of (160, 200, 250, 320, 400, 500, 640, 800, 1000, 1280, 1600)!")

    cut, a, b, c, d, _e, f, _ = atfh.DATA_ALEXA_LOG_C_CURVE_CONVERSION[firmware][method[linear]][EI]

    if decode:  # Linearize / Decoding EOTF
        return [(10 ** ((i - d) / c) - b) / a if i > _e * cut + f else (i - f) / _e for i in RGB]

    # Encoding OETF
    return [c * log10(a * i + b) + d if i > cut else _e * i + f for i in RGB]


def arri_log_c4(RGB: tuple | list, depth: int = 12, decode: bool = False, **kwargs):
    """### Converts between Linear and ARRI LogC4 values \
        This is the ARRI LogC4 opto-electronic/electro-optical transfer function (OETF)/(EOTF).

    ### Args:
        `RGB` (tuple | list): The R, G, B values to be converted
        `depth` (int | float): The bit depth of the input RGB values [10 or 12]. Defaults to 12-bit (range 0-4095)
        `decode` (bool, optional): Decode, convert the values to linear. Defaults to False.

    Reference https://www.arri.com/resource/blob/278790/bea879ac0d041a925bed27a096ab3ec2/2022-05-arri-logc4-specification-data.pdf

    ### Returns:
        tuple[R, G, B]
    """
    RGB = ih.check_color(RGB, depth=depth, normalized=True, clamp=False)

    a = (2**18 - 16) / 117.45
    b = (1023 - 95) / 1023
    c = 95 / 1023
    s = (7 * log(2) * 2 ** (7 - 14 * c / b)) / (a * b)
    t = (2 ** (14 * (-c / b) + 6) - 64) / a

    if decode:  # Linearize / Decoding EOTF
        return [i * s + t if i < 0 else (2 ** (14 * ((i - c) / b) + 6) - 64) / a for i in RGB]

    # Encoding OETF
    return [(i - t) / s if i < t else (log2(a * i + 64) - 6) / 14 * b + c for i in RGB]


def red_log(RGB: tuple | list, black_offset: float = 10 ** ((0 - 1023) / 511), decode: bool = False, **kwargs):
    """### Converts between Linear and Red Log values \
        This is the Red Log opto-electronic/electro-optical transfer function (OETF)/(EOTF).
    #### This is the same OETF/EOTFs as the ones for Cineon Log

    ### Args:
        `RGB` (tuple | list): The R, G, B values to be converted
        `black_offset` (float, optional): Black offet. Defaults to ~0.009955041
        `decode` (bool, optional): Decode, convert the values to linear. Defaults to False.

    Reference https://github.com/imageworks/OpenColorIO-Configs/blob/master/nuke-default/make.py

    ### Returns:
        tuple[R, G, B]
    """
    RGB = ih.check_color(RGB, depth=10, normalized=True, clamp=False)

    if decode:  # Linearize / Decoding EOTF
        return [((10 ** ((1023 * i - 1023) / 511)) - black_offset) / (1 - black_offset) for i in RGB]

    # Encoding OETF
    return [(1023 + 511 * log10(i * (1 - black_offset) + black_offset)) / 1023 for i in RGB]


def red_log_film(RGB: tuple | list, black_offset: float = 10 ** ((95 - 685) / 300), decode: bool = False, **kwargs):
    """### Converts between Linear and Red Log Film values \
        This is the Red Log Film opto-electronic/electro-optical transfer function (OETF)/(EOTF).
    #### This is the same OETF/EOTFs as the ones for Cineon Log

    ### Args:
        `RGB` (tuple | list): The R, G, B values to be converted
        `black_offset` (float, optional): Black offet. Defaults to ~0.01079775
        `decode` (bool, optional): Decode, convert the values to linear. Defaults to False.

    Reference https://github.com/imageworks/OpenColorIO-Configs/blob/master/nuke-default/make.py

    ### Returns:
        tuple[R, G, B]
    """
    RGB = ih.check_color(RGB, depth=10, normalized=True, clamp=False)

    if decode:  # Linearize / Decoding EOTF
        return [(10 ** ((1023 * i - 685) / 300) - black_offset) / (1 - black_offset) for i in RGB]

    # Encoding OETF
    return [(685 + 300 * log10(i * (1 - black_offset) + black_offset)) / 1023 for i in RGB]


def log3_g10(RGB: tuple | list, method: int = 3, decode: bool = False, **kwargs):
    """### Converts between Linear and Log3G10 values \
        This is the Log3G10 opto-electronic/electro-optical transfer function (OETF)/(EOTF).

    ### Args:
        `RGB` (tuple | list): The R, G, B values to be converted
        `method` (int, optional): Computation method. Either 1, 2 or 3 (version). Defaults to 3.
        `decode` (bool, optional): Decode, convert the values to linear. Defaults to False.

    -   The *Log3G10* *v1* log encoding curve is the one used in
        *REDCINE-X Beta 42*. *Resolve 12.5.2* also uses the *v1* curve. *RED*
        is planning to use the *Log3G10* *v2* log encoding curve in the release
        version of the *RED SDK*.
    -   The intent of the *Log3G10* *v1* log encoding curve is that zero maps
        to zero, 0.18 maps to 1/3, and 10 stops above 0.18 maps to 1.0.
        The name indicates this in a similar way to the naming conventions of
        *Sony HyperGamma* curves.

        The constants used in the functions do not in fact quite hit these
        values, but rather than use corrected constants, the functions here
        use the official *RED* values, in order to match the output of the
        *RED SDK*.

        Methods 2 and 3 usually give the same results!

    Reference https://www.red.com/download/white-paper-on-redwidegamutrgb-and-log3g10

    ### Returns:
        tuple[R, G, B]
    """
    if decode:  # Linearize / Decoding EOTF
        if method == 1:  # Used in REDCINE-X PRO Beta 42 and Resolve 12.5.2.
            return [copysign(1, i) * (10.0 ** (abs(i) / 0.222497) - 1) / 169.379333 for i in RGB]
        if method == 2:  # The current curve in REDCINE-X PRO
            return [(copysign(1, i) * (10.0 ** (abs(i) / 0.224282) - 1) / 155.975327) - 0.01 for i in RGB]
        if method == 3:  # The curve described in the RedLog3G10 whitepaper.
            a, b, c, g = 0.224282, 155.975327, 0.01, 15.1927
            return [(i / g) - c if i < 0.0 else copysign(1, i) * (10 ** (abs(i) / a) - 1.0) / b - c for i in RGB]

    # Encoding OETF
    if method == 1:  # Used in REDCINE-X PRO Beta 42 and Resolve 12.5.2.
        return [copysign(1, i) * 0.222497 * log10((abs(i) * 169.379333) + 1) for i in RGB]
    if method == 2:  # The current curve in REDCINE-X PRO
        return [(copysign(1, i + 0.01) * 0.224282 * log10((abs(i + 0.01) * 155.975327) + 1)) for i in RGB]
    if method == 3:  # The curve described in the RedLog3G10 whitepaper.
        a, b, c, g = 0.224282, 155.975327, 0.01, 15.1927
        return [(i + c) * g if i + c < 0.0 else copysign(1, i + c) * a * log10((abs(i + c) * b) + 1.0) for i in RGB]
    raise ValueError("Wrong method input. The method can only be an int number 1, 2 or 3!")


def log3_g12(RGB: tuple | list, decode: bool = False, **kwargs):
    """### Converts between Linear and Log3G12 values \
        This is the Log3G12 opto-electronic/electro-optical transfer function (OETF)/(EOTF).

    ### Args:
        `RGB` (tuple | list): The R, G, B values to be converted
        `decode` (bool, optional): Decode, convert the values to linear. Defaults to False.

    Reference https://www.red.com/download/white-paper-on-redwidegamutrgb-and-log3g10

    ### Returns:
        tuple[R, G, B]
    """
    if decode:  # Linearize / Decoding EOTF
        return [copysign(1, i) * (10.0 ** (abs(i) / 0.184904) - 1) / 347.189667 for i in RGB]

    # Encoding OETF
    return [copysign(1, i) * 0.184904 * log10((abs(i) * 347.189667) + 1) for i in RGB]


def acescc(RGB: tuple | list, decode: bool = False, **kwargs):
    """### Converts between Linear and ACEScc values \
        This is the ACEScc opto-electronic/electro-optical transfer function (OETF)/(EOTF).

    ### Args:
        `RGB` (tuple | list): The R, G, B values to be converted
        `decode` (bool, optional): Decode, convert the values to linear. Defaults to False.

    Reference http://j.mp/S-2014-003

    ### Returns:
        tuple[R, G, B]
    """
    if decode:  # Linearize / Decoding EOTF
        res = [(2 ** (i * 17.52 - 9.72) - 2** - 16) * 2 if i < (9.72 - 15) / 17.52 else 2 ** (i * 17.52 - 9.72) for i in RGB]
        return [res[i] if k < (log2(65504) + 9.72) / 17.52 else 65504 for i, k in enumerate(RGB)]

    # Encoding OETF
    res = [(log2(2** - 16) + 9.72) / 17.52 if i < 0 else (log2(2** - 16 + i * 0.5) + 9.72) / 17.52 for i in RGB]
    return [res[i] if k < 2** - 15 else (log2(k) + 9.72) / 17.52 for i, k in enumerate(RGB)]


def acescct(RGB: tuple | list, decode: bool = False, **kwargs):
    """### Converts between Linear and ACEScct values \
        This is the ACEScct opto-electronic/electro-optical transfer function (OETF)/(EOTF).

    ### Args:
        `RGB` (tuple | list): The R, G, B values to be converted
        `decode` (bool, optional): Decode, convert the values to linear. Defaults to False.

    Reference http://j.mp/S-2016-001

    ### Returns:
        tuple[R, G, B]
    """
    A = 10.5402377416545
    B = 0.0729055341958355

    if decode:  # Linearize / Decoding EOTF
        return [2 ** (i * 17.52 - 9.72) if i > 0.155251141552511 else (i - B) / A for i in RGB]

    # Encoding OETF
    return [(log2(i) + 9.72) / 17.52 if i > 0.0078125 else A * i + B for i in RGB]


def acesproxy(RGB: tuple | list, depth: int = 10, decode: bool = False, normalized: bool = True, **kwargs):
    """### Converts between Linear and ACESproxy values \
        This is the ACESproxy opto-electronic/electro-optical transfer function (OETF)/(EOTF).

    ### Args:
        `RGB` (tuple | list): The R, G, B values to be converted
        `depth` (int | float): The bit depth of the input RGB values [10 or 12]. Defaults to 10-bit (range 0-1023)
        `decode` (bool, optional): Decode, convert the values to linear. Defaults to False.
        `normalized` (bool, optional): Wether the values are in normalized range (0-1). Defaults to True.

    Reference http://j.mp/S-2013-001

    ### Returns:
        tuple[R, G, B]
    """
    RGB = ih.check_color(RGB, depth=depth, normalized=True, clamp=False)
    if depth not in (10, 12):
        raise ValueError("Depth must be integer [10 or 12]!")
    max_value = 2 ** depth - 1
    multiplier = 1 if depth == 10 else 4
    CV_min = 64 * multiplier
    CV_max = 940 * multiplier
    steps_per_stop = 50 * multiplier
    mid_CV_offset = 425 * multiplier

    if decode:  # Linearize / Decoding EOTF
        RGB = (i * max_value for i in RGB) if normalized else RGB
        return [2 ** ((i - mid_CV_offset) / steps_per_stop - 2.5) for i in RGB]

    # Encoding OETF
    res = ((max(CV_min, min(CV_max, ((log2(i) + 2.5) * steps_per_stop + mid_CV_offset)))) if i > 2** -9.72 else CV_min for i in RGB)
    return [i / max_value for i in res] if normalized else [round(i) for i in res]


def protune(RGB: tuple | list, depth: int = 10, decode: bool = False, **kwargs):
    """### Converts between Linear and Protune values \
        This is the Protune opto-electronic/electro-optical transfer function (OETF)/(EOTF).

    ### Args:
        `RGB` (tuple | list): The R, G, B values to be converted
        `depth` (int | float): The bit depth of the input RGB values [10 or 12]. Defaults to 10-bit (range 0-1023)
        `decode` (bool, optional): Decode, convert the values to linear. Defaults to False.

    Reference https://github.com/hpd/OpenColorIO-Configs/blob/master/aces_1.0.3/python/aces_ocio/colorspaces/gopro.py

    ### Returns:
        tuple[R, G, B]
    """
    RGB = ih.check_color(RGB, depth=depth, normalized=True, clamp=False)

    if decode:  # Linearize / Decoding EOTF
        return [(113**i - 1) / 112 for i in RGB]
    # Encoding OETF
    return [log1p(i * 112) / log(113) for i in RGB]


def smpte240m(RGB: tuple | list, decode: bool = False, **kwargs):
    """### Converts between Linear and SMPTE240M values \
        This is the SMPTE240M opto-electrical/electro-optical transfer function (OETF)/(EOTF).

    ### Args:
        `RGB` (tuple | list): The R, G, B values to be converted
        `decode` (bool, optional): Decode, convert the values to linear. Defaults to False.

    Reference http://car.france3.mars.free.fr/HD/INA-%2026%20jan%2006/SMPTE%20normes%20et%20confs/s240m.pdf

    ### Returns:
        tuple[R, G, B]
    """
    RGB = ih.check_color(RGB, normalized=True, clamp=False)

    if decode:  # Linearize / Decoding EOTF
        return [i / 4 if i < smpte240m((0.0228, 0.0228, 0.0228))[0] else (i + 0.1115) / 1.1115 ** (1 / 0.45) for i in RGB]

    # Encoding OETF
    return [4 * i if i < 0.0228 else 1.1115 * i** 0.45 - 0.1115 for i in RGB]


def gamma_function(RGB: tuple | list, gamma: int | float, decode: bool = False, depth: int = 8,  output: str = "normalized"):
    """### Converts between Linear and Gamma-corrected RGB values. \
        This is a typical gamma encoding/decoding function

    ### Args:
        `RGB` (tuple | list): The R, G, B values to be converted
        `gamma` (int | float): The gamma exponent of the RGB value's color space.
        `decode` (bool, optional): Decode, convert the values to linear. Defaults to False.
        `depth` (int | float): The bit depth of the input RGB values. Defaults to 8-bit (range 0-255)
        `output` (str, optional): Either "hex", "hexp", "normalized", "round" or "direct"
        *     hex returns a hex string color in the form of decade
        *     hexp returns a hex string color in the form of #facade
        *     normalized returns a tuple(R, G, B) where the values are floats in range 0-1
        *     round returns a tuple(R, G, B) where the values are integers in range 0-255
        *     direct returns a tuple(R, G, B) where the values are floats in range 0-255
        *     In any invalid case the "direct" approach will be used

    ### Returns:
        tuple[R, G, B]
    """
    RGB = ih.check_color(RGB, depth=depth, normalized=True)
    if decode:  # Linearize
        R, G, B = (i ** (1 / gamma) if i > 0 else 0 for i in RGB)
        return ih.return_rgb((R, G, B), normalized_input=True, depth=depth, output=output)
    # Apply gamma
    R, G, B = (i ** gamma if i > 0 else 0 for i in RGB)
    return ih.return_rgb((R, G, B), normalized_input=True, depth=depth, output=output)
