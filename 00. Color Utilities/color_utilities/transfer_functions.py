"""This module contains transfer functions for various color spaces"""
# pylint: disable=invalid-name, unsubscriptable-object
from math import log, log2, log10, exp, e

from . import internal_helpers as ih

def srgb(RGB: tuple | list, decode: bool = False, output="direct"):
    """### Converts between Linear and Gamma-corrected sRGB values. \
        This is the sRGB electro-optical transfer function (EOTF) and its inverse

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

    Reference https://www.itu.int/dms_pubrec/itu-r/rec/bt/R-REC-BT.709-6-201506-I!!PDF-E.pdf

    ### Returns:
        tuple[R, G, B]
    """
    RGB = ih.check_color(RGB, normalized=True)
    if decode:  # Linearize EOTF
        check = srgb((0.0031308, 0.0031308, 0.0031308), output="normalized")[0]    # ~0.04045
        R, G, B = (((i + 0.055) / 1.055) ** 2.4 if i > check else i / 12.92 for i in RGB)
        return ih.return_scale((R, G, B), normalized_input=True, output=output)
    # EOTF Inverse
    R, G, B = (1.055 * (i ** (1 / 2.4)) - 0.055 if i > 0.0031308 else i * 12.92 for i in RGB)
    return ih.return_scale((R, G, B), normalized_input=True, output=output)


def rec601(RGB: tuple | list, decode: bool = False, output="normalized") -> str | tuple:
    """### Converts between Linear and Gamma-corrected Rec. 601 / Rec.709 values \
        This is the Rec. 601 / Rec. 709 opto-electrical transfer function (OETF) and its inverse

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


def rec2020(RGB: tuple | list, decode: bool = False, depth: int = 10, output="normalized") -> str | tuple:
    """### Converts between Linear and Gamma-corrected Rec.2020 values \
        This is the Rec. 2020 opto-electrical transfer function (OETF) and its inverse

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

    Reference 1 https://en.wikipedia.org/wiki/Rec._2020
    Reference 2 https://www.color.org/chardata/rgb/BT2020.xalter

    NOTE: The reference electro-optical transfer function (EOTF) for a Rec.2020 display is defined in ITU-R BT.1886.
    Some implementors use the inverse of the (OETF) as defined in BT.2020 (BT.2087 case #2) in place of ITU-R BT.1886.

    ### Returns:
        tuple[R, G, B]
    """
    if depth not in (10, 10., 12, 12.):
        raise ValueError("The depth for Rec. 2020 can either be 8 or 12 bits!")
    RGB = ih.check_color(RGB, normalized=True)

    beta = 0.018053968510807
    alpha = 1 + 5.5 * beta # ~1.09929682680944 # 10 * BETA ** 0.55

    if decode:  # Linearize / OETF
        RGB = (i * 4.5 if i < beta else alpha * i ** 0.45 - (alpha - 1) for i in RGB)
        return ih.return_rgb(RGB, normalized_input=True, clamp=0, output=output)

    # OETF Inverse
    RGB = (i / 4.5 if i < rec2020((beta, beta, beta), decode=True)[0]
           else ((i + (alpha - 1)) / alpha) ** 1/0.45 for i in RGB)
    return ih.return_rgb(RGB, normalized_input=True, clamp=0, output=output)


def romm(RGB: tuple | list, decode: bool = False, depth: int = 8, output="normalized"):
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
    RGB = ih.check_color(RGB, normalized=True)
    if decode:  # Linearize / Decoding CCTF
        R, G, B = (i / 16 if i < 16 * (1/512) else i ** 1.8 for i in RGB)
        return ih.return_rgb((R, G, B), depth=depth, normalized_input=True, clamp=0, output=output)
    # Encoding CCTF
    R, G, B = (i * 16 if i < 1/512 else i ** (1/1.8) for i in RGB)
    return ih.return_rgb((R, G, B), depth=depth, normalized_input=True, clamp=0, output=output)


def rimm(RGB: tuple | list, decode: bool = False, exposure: int = 2, depth: int = 8, output="normalized"):
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
    RGB = ih.check_color(RGB, normalized=True)
    clip = 1.099 * exposure ** 0.45 - 0.099
    if decode:  # Linearize / Decoding CCTF
        check = rimm((0.018, 0.018, 0.018), depth=depth, exposure=exposure)[0]
        R, G, B = (i * clip / 4.5 if i < check else ((i * clip + 0.099) / 1.099) ** (1 / 0.45) for i in RGB)
        return ih.return_rgb((R, G, B), depth=depth, normalized_input=True, clamp=0, output=output)
    # Encoding CCTF
    out = [(i * 4.5) / clip if i < 0.018 else (1.099 * i ** 0.45 - 0.099) / clip for i in RGB]
    return ih.return_rgb(out, depth=depth, normalized_input=True, clamp=0, output=output)


def erimm(RGB: tuple | list, decode: bool = False, exp_min: float = 0.001, exp_max: float = 316.2, depth: int = 8, output="normalized"):
    """### Converts between Linear and Gamma-corrected ERIMM values \
        This is the ERIMM opto-electric transfer function (OETF).

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
    RGB = ih.check_color(RGB, normalized=True, limit=False)
    euler_min = e * exp_min
    lg = log(euler_min)
    exp_min = log(exp_min)
    exp_max = log(exp_max)

    if decode:  # Linearize / Decoding OETF
        check = ((lg - exp_min) / (exp_max - exp_min))
        RGB = (exp(i * (exp_max - exp_min) + exp_min) if i > check else
               ((exp_max - exp_min) / (lg - exp_min)) * (i * euler_min) for i in RGB)
        return ih.return_rgb(RGB, depth=depth, normalized_input=True, clamp=0, output=output)

    # Encoding OETF
    RGB = (max(0, min(i, 1)) for i in RGB)
    RGB = ((log(i) - exp_min) / (exp_max - exp_min) if i > euler_min else
           ((lg - exp_min) / (exp_max - exp_min)) * i / euler_min for i in RGB)
    # RGB = [16 * i if i < 0.001953 else i ** (1/1.8) for i in RGB]
    return ih.return_rgb(RGB, depth=depth, normalized_input=True, clamp=0, output=output)


def blackmagic(RGB: tuple | list, decode: bool = False):
    """### Converts between Linear and Gamma-corrected Blackmagic Film Gen 5 values \
        This is the Blackmagic Film Gen 5 opto-electric transfer function (OETF).

    ### Args:
        `RGB` (tuple | list): The R, G, B values to be converted
        `decode` (bool, optional): Decode, convert the values to linear. Defaults to False.

    Reference: https://drive.google.com/file/d/1FF5WO2nvI9GEWb4_EntrBoV9ZIuFToZd/view

    ### Returns:
        tuple[R, G, B]
    """
    RGB = ih.check_color(RGB, normalized=True, limit=False)
    A = 0.08692876065491224
    B = 0.005494072432257808
    C = 0.5300133392291939
    D = 8.283605932402494
    E = 0.09246575342465753
    LIN_CUT = 0.005

    if decode:  # Linearize / Decoding OETF
        LOG_CUT = D * LIN_CUT + E
        return [(i - E) / D if i < LOG_CUT else exp((i - C) / A) - B for i in RGB]

    # Encoding OETF
    return [D * i + E if i < LIN_CUT else A * log(i + B) + C for i in RGB]


def davinci(RGB: tuple | list, decode: bool = False):
    """### Converts between Linear and Gamma-corrected DaVinci values \
        This is the DaVinci opto-electric transfer function (OETF).

    ### Args:
        `RGB` (tuple | list): The R, G, B values to be converted
        `decode` (bool, optional): Decode, convert the values to linear. Defaults to False.

    Reference: https://documents.blackmagicdesign.com/InformationNotes/DaVinci_Resolve_17_Wide_Gamut_Intermediate.pdf?_v=1607414410000

    ### Returns:
        tuple[R, G, B]
    """
    RGB = ih.check_color(RGB, normalized=True, limit=False)
    DI_A = 0.0075
    DI_B = 7.0
    DI_C = 0.07329248
    DI_M = 10.44426855
    DI_LIN_CUT = 0.00262409

    if decode:  # Linearize / Decoding OETF
        DI_LOG_CUT = 0.02740668
        return [2 ** ((i / DI_C) - DI_B) - DI_A if i > DI_LOG_CUT else i / DI_M for i in RGB]

    # Encoding OETF
    return [DI_C * (log2(i + DI_A) + DI_B) if i > DI_LIN_CUT else i * DI_M for i in RGB]


def slog3(RGB: tuple | list, reflection: bool = True, decode: bool = False, depth: int = 10, norm_range: bool = True):
    """No documentation yet"""
    RGB = ih.check_color(RGB, normalized=True, limit=False)
    mult = 2 ** (depth - 8)
    scope = 16 * mult, 235 * mult
    max_value = 2 ** depth - 1


    if decode:  # Linearize / Decoding OETF
        RGB = [i if norm_range else ((scope[1] - scope[0]) * i + scope[0])/max_value for i in RGB]
        res = [(i * 1023 - 95) * 0.01125000 / (171.2102946929 - 95) if i < 171.2102946929 / 1023
                else ((10 ** ((i * 1023 - 420) / 261.5)) * (0.18 + 0.01) - 0.01) for i in RGB]

        return res if reflection else [i / 0.9 for i in res]

    RGB = RGB if reflection else [i * 0.9 for i in RGB]

    # Encoding OETF
    res = [(i * (171.2102946929 - 95) / 0.01125 + 95) / 1023 if i < 0.01125 else
            (420 + log10((i + 0.01) / (0.18 + 0.01)) * 261.5) / 1023 for i in RGB]

    return res if norm_range else [((i * max_value) - scope[0]) / (scope[1] - scope[0]) for i in res]


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
    RGB = ih.check_color(RGB, normalized=True)
    if decode:  # Linearize EOTF
        R, G, B = (i ** (1 / gamma) if i > 0 else 0 for i in RGB)
        return ih.return_rgb((R, G, B), normalized_input=True, depth=depth, output=output)
    # Apply gamma
    R, G, B = (i ** gamma if i > 0 else 0 for i in RGB)
    return ih.return_rgb((R, G, B), normalized_input=True, depth=depth, output=output)
