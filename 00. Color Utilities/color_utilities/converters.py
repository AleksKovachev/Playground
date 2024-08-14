"""A collection of useful functions for converting colors between different types,
color representation, bit depth, color spaces, etc."""
# pylint: disable=invalid-name, unpacking-non-sequence, pointless-string-statement, too-many-lines
from enum import Enum
from math import acos, atan, cos, degrees, exp, pi, radians, sin, sqrt, tan

from . import internal_helpers as ih
from . import transfer_functions as tf
from . import color_utils as cu
from . import xyz
from .color_spaces import color_spaces as cs
from .constants import Color, Color_out1, Color_out_hsw, Color_geo, Out1, Out2, Out3


def rgb_to_web_safe(*color: Color, output: Enum = Out1.ROUND) -> Color_out1:
    """### Converts an 8-bit RGB color to its web safe version

    #### Args:
        `color` (Color): String "c0ffee", "#decaff", consecutive values \
                either int in range 0-255 or float in range 0-1 or an \
                RGB sequence(R, G, B) with the same values
        `output` (Enum, optional): Out1 enum options available

    #### Returns:
        Color_out1: Red, Green, Blue
    """
    # Check color integrity
    R, G, B = ih.check_color(color, normalized=True)
    # Convert to web safe
    R, G, B = (round(i * 5) * 51 for i in (R, G, B))

    return ih.return_rgb((R, G, B), output=output)


def hex_to_rgb(color: str, *, depth: int | float = 8, normalized: bool = False) -> list:
    """### Converts a hex color to RGB values
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `color` (str): A hex color in the form "dec0de" or "#0ff1ce"
        `depth` (int | float): The bit depth of the input RGB values. Defaults to 8-bit (range 0-255)
        `normalized` (bool, optional): True will return values in range 0-1. Defaults to False.

    ### Returns:
        list[int, int, int] | list[float, float, float]: Red, Green, Blue
    """
    max_value = (2 ** depth) - 1   # The number of possible values per channel for the given bit depth
    # Length of the stringified hexadecimal representation of the max possible value for an RGB element
    ch_length = len(hex(max_value)[2:])

    color = color.strip().strip("#").strip()
    if len(color) != ch_length * 3:    # Channel length * 3 channels (R, G, B) for the full color
        raise ValueError(f"Input color should be of length {ch_length * 3} for {depth}-bit color")

    if normalized:
        return [int(color[i:i+ch_length], 16) / max_value for i in range(0, ch_length * 3, ch_length)]
    return [int(color[i:i+ch_length], 16) for i in range(0, ch_length * 3, ch_length)]


def rgb_to_hex(*color: Color, depth: int | float = 8, pound: bool = True) -> str:
    """### Converts RGB values to a hexadecimal color string representation
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `color` (Color): String "decade", "#facade", consecutive values either \
                int in range 0-255 or float in range 0-1 or an RGB list/tuple(R, G, B) with the same values
        N/B: If a color is passed as a hex in a string form, the result will be the same string
        `depth` (int | float): The bit depth of the input RGB values. Defaults to 8-bit (range 0-255)
        `pound` (bool): Whether to return the result with a pound sign prefix "#c0ffed" instead of just "dec1de"

    ### Returns:
        str: Hex string in either `add1c7` | `#effec7` form
    """
    # Check color integrity
    R, G, B = ih.check_color(color, depth=depth)

    # The maximum acceptable value per element in given bit depth
    max_value = (2 ** depth) - 1
    length = len(hex(max_value)[2:])

    # Make the color in hex format
    hexed = ''.join(f"{'0' * (length - len(hex(i)[2:]))}{hex(i)[2:]}" for i in (R, G, B) if 0 <= i <= max_value)
    if len(hexed) != length * 3:
        raise ValueError(f"Elements of {depth}-bit color can't be negative or have values higher than {max_value}")

    pound_sign = "#" if pound else ""
    return f"{pound_sign}{hexed}"


def rgb_to_hsl(*color: Color, depth: int = 8, output: Enum = Out2.ROUND) -> Color_out_hsw:
    """### Takes an RGB color and returns its HSL (Hue, Saturation, Luminance) representation
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `color` (Color): String "c0ffee", "#decaff", consecutive values \
                either int in range 0-255 or float in range 0-1 or an \
                RGB list/tuple(R, G, B) with the same values
        `depth` (int | float): The bit depth of the input RGB values. Defaults to 8-bit (range 0-255)
        `output` (Enum, optional): Out2 enum options available

    #### N/B: Don't use round output if the output color is going to be used to further conversion!

    ### Returns:
        Color_out_hsw: Hue, Saturation, Lightness
    """
    # Check color integrity
    R, G, B = ih.check_color(color, normalized=True, depth=depth)

    # Get the minimum and maximum of the channels and their sum and delta
    Cmax = max(R, G, B)
    Cmin = min(R, G, B)
    sum_ = Cmax + Cmin
    delta = Cmax - Cmin

    # Find Lightness
    L = sum_ / 2

    # If all elements have the same values, then the color is in the grayscale
    if Cmin == Cmax:
        match output:
            case Out2.ROUND:
                return 0, 0, round(L * 100)
            case Out2.NORMALIZED | Out2.HALF_NORMALIZED:
                return 0, 0, L
            case Out2.DIRECT:
                return 0, 0, L * 100

    # Find Saturation and Hue
    S = 0 if delta == 0 else (delta / (1 - abs(2 * L - 1)))

    H = cu.get_hue(R, G, B, output=Out2.NORMALIZED)

    return ih.return_hsw((H, S, L), normalized_input=True, output=output)


def rgb_to_hls(*color: Color, depth: int = 8, output: Enum = Out2.ROUND) -> Color_out_hsw:
    """### Takes an RGB color and returns its HLS (Hue, Luminance, Saturation) representation
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `color` (Color): String "dec0de", "#0ff1ce", consecutive values \
                either int in range 0-255 or float in range 0-1 or an \
                RGB list/tuple(R, G, B) with the same values
        `depth` (int | float): The bit depth of the input RGB values. Defaults to 8-bit (range 0-255)
        `output` (Enum, optional): Out2 enum options available

    #### N/B: Don't use round output if the output color is going to be used to further conversion!

    ### Returns:
        Color_out_hsw: Hue, Lightness,  Saturation
    """
    RGB = ih.check_color(color, normalized=True, depth=depth)

    # Get the minimum and maximum of the channels and their sum and delta
    Cmax = max(RGB)
    Cmin = min(RGB)
    sum_ = Cmax + Cmin
    delta = Cmax - Cmin

    # Find Lightness
    L = sum_ / 2

    # If all elements have the same values, then the color is in the grayscale
    if Cmin == Cmax:
        match output:
            case Out2.ROUND:
                return 0, round(L * 100), 0
            case Out2.NORMALIZED | Out2.HALF_NORMALIZED:
                return 0, L, 0
            case Out2.DIRECT:
                return 0, L * 100, 0
            case _:
                raise TypeError("Wrong output type!")

    # Find Saturation
    S = delta / sum_ if L <= 0.5 else delta / (2 - sum_)

    # Find Hue (Alternative to the method used in the cu.get_hue() function)
    rc = (Cmax - RGB[0]) / delta
    gc = (Cmax - RGB[1]) / delta
    bc = (Cmax - RGB[2]) / delta

    if RGB[0] == Cmax:
        H = bc - gc
    elif RGB[1] == Cmax:
        H = 2 + rc - bc
    else:
        H = 4 + gc - rc
    H = (H / 6) % 1

    return ih.return_hsw((H, L, S), normalized_input=True, output=output)


def hls_to_rgb(*HLS: Color_geo, depth: int = 8, output: Enum = Out1.ROUND) -> Color_out1:
    """### Converts HLS values to RGB
    Reference: https://en.wikipedia.org/wiki/HSL_and_HSV#HSL_to_RGB

    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `HLS` (Color_geo): Hue, Lightness, Saturation in either int range H 0-360, LS range 0-100 \
                                    or float range 0-1 or a tuple/list with the same values
        `depth` (int | float): The bit depth of the input RGB values. Defaults to 8-bit (range 0-255)
        `output` (Enum, optional): Out1 enum options available

    #### N/B: Don't use round if the output color is going to be used to further conversion!

    ### Returns:
        Color_out1: Red, Green, Blue
    """
    if depth % 1 != 0:
        raise ValueError("Depth value must be an integer number passed either as int or float")

    # Check values integrity
    H, L, S = ih.check_hsw(HLS, output=Out2.NORMALIZED)

    def hue_to_rgb(m1, m2, H1):
        # sourcery skip: reintroduce-else
        H1 = H1 % 1
        if H1 < 1/6:
            return m1 + (m2 - m1) * H1 * 6
        if H1 < 0.5:
            return m2
        if H1 < 2/3:
            return m1 + (m2 - m1) * (2/3 - H1) * 6
        return m1

    if S == 0:
        return ih.return_rgb((L, L, L), normalized_input=True, depth=depth, output=output)

    m2 = L * (1 + S) if L < 0.5 else L + S - (L * S)
    m1 = 2 * L - m2

    res = hue_to_rgb(m1, m2, H + 1/3), hue_to_rgb(m1, m2, H), hue_to_rgb(m1, m2, H - 1/3)
    return ih.return_rgb((res), normalized_input=True, depth=depth, output=output)


def hsl_to_rgb(*HSL: int | float | tuple | list, depth: int = 8, output: Enum = Out1.ROUND):
    """### Converts HSL values to RGB
    #### Reference: https://en.wikipedia.org/wiki/HSL_and_HSV

    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `HSL` (int | float | tuple | list): hue, saturation, lightness either in int H range 0-359, SL range 0-100 \
                                    or float range 0-1 or a tuple/list with the same values
        `depth` (int | float): The bit depth of the input RGB values. Defaults to 8-bit (range 0-255)
        `output` (str, optional): Either "hex", "hexp", "normalized", "round" or "direct"
        *     hex returns a hex string color in the form of c0ffed
        *     hexp returns a hex string color in the form of #dec1de
        *     normalized returns a tuple(R, G, B) where the values are floats in range 0-1
        *     round returns a tuple(R, G, B) where the values are integers in range 0-255
        *     direct returns a tuple(R, G, B) where the values are floats in range 0-255
        *     In any invalid case the "direct" approach will be used

    #### N/B: Don't use round if the output color is going to be used to further conversion!

    ### Returns:
        str | tuple[int, int, int] | tuple[float, float, float]: Red, Green, Blue
    """
    if depth % 1 != 0:
        raise ValueError("Depth value must be an integer number passed either as int or float")

    # Check values integrity
    H, S, L = ih.check_hsw(HSL, output=Out2.HALF_NORMALIZED)

    # Find Chroma
    C = (1 - abs(2 * L - 1)) * S
    # Find a point (R1, G1, B1) along the bottom three faces of the RGB cube, with the same hue and chroma
    # as our color (using the intermediate value X for the second largest component of this color)
    X = C * (1 - abs((H / 60) % 2 - 1)) # 60 degrees
    m = L - C / 2

    if 0 <= H < 60:
        R, G, B = C, X, 0
    elif 60 <= H < 120:
        R, G, B = X, C, 0
    elif 120 <= H < 180:
        R, G, B = 0, C, X
    elif 180 <= H < 240:
        R, G, B = 0, X, C
    elif 240 <= H < 300:
        R, G, B = X, 0, C
    elif 300 <= H < 360:
        R, G, B = C, 0, X

    # Match lightness
    R, G, B = R + m, G + m, B + m

    return ih.return_rgb((R, G, B), normalized_input=True, depth=depth, output=output)


def rgb_to_hsv(*color: Color, depth: int = 8, output: Enum = Out2.ROUND) -> Color_out_hsw:
    """### Takes an RGB color and returns its HSV (Travis) representation
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `color` (int | float | str | tuple | list): String "add1c7", "#effec7", consecutive values either \
                int in range 0-255 or float in range 0-1 or an RGB list/tuple(R, G, B) with the same values
        `depth` (int | float): The bit depth of the input RGB values. Defaults to 8-bit (range 0-255)
        `output` (str, optional): Either "normalized", "half-normalized", "round" or "direct"
        *     normalized returns a tuple(H, S, V) where the values are floats in range 0-1
        *     half-normalized returns a tuple(H, S, V) where the values are H in range 0-359, SV in range 0-1
        *     round returns a tuple(H, S, V) where the values are integers. H in range 0-359, SV in range 0-100
        *     direct returns a tuple(H, S, V) where the values are floats. H in range 0-359, SV in range 0-100
        *     In any invalid case the "direct" approach will be returned

    #### N/B: Don't use round output if the output color is going to be used to further conversion!

    Returns:
        tuple[int, int, int] | tuple[float, float, float] | tuple[int, float, float]: Hue, Saturation, Value
    """
    # Check color integrity
    R, G, B = ih.check_color(color, normalized=True, depth=depth)

    # Get the minimum and maximum of the channels and their delta
    Cmax = max(R, G, B)
    Cmin = min(R, G, B)
    delta = Cmax - Cmin

    # Find Saturation and Value
    S = 0 if Cmax == 0 else (delta / Cmax) * 100
    V = Cmax * 100

    # If all elements have the same values, then the color is in the grayscale
    if Cmax == Cmin:
        match output:
            case Out2.ROUND:
                return 0, 0, round(V)
            case Out2.NORMALIZED | Out2.HALF_NORMALIZED:
                return 0, 0, V / 100
            case Out2.DIRECT:
                return 0, 0, V
            case _:
                raise ValueError("Wrong output type!")

    # Find Hue
    H = cu.get_hue(R, G, B)

    # H (degrees), S (%), V (%)
    return ih.return_hsw((H, S, V), output=output)


def hsv_to_rgb(*HSV: int | float | tuple | list, depth: int = 8, output: Enum = Out1.ROUND):
    """### Converts HSV values to RGB
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `HSV` (int | float | tuple | list): Hue, Saturation, Value either H in int range 0-360, SV range 0-100, \
            float range 0-1 or H in int range 0-359, SV in float range 0-1 or a tuple/list with the same values
        `depth` (int | float): The bit depth of the input RGB values. Defaults to 8-bit (range 0-255)
        `output` (str, optional): Either "hex", "hexp", "normalized", "round" or "direct"
        *     hex returns a hex string color in the form of c0ffee
        *     hexp returns a hex string color in the form of #decaff
        *     normalized returns a tuple(R, G, B) where the values are floats in range 0-1
        *     round returns a tuple(R, G, B) where the values are integers in range 0-255
        *     direct returns a tuple(R, G, B) where the values are floats in range 0-255
        *     In any invalid case the "direct" approach will be used

    #### N/B: Don't use round if the output color is going to be used to further conversion!

    ### Returns:
        str | tuple[int, int, int] | tuple[float, float, float]: Red, Green, Blue
    """
    if depth % 1 != 0:
        raise ValueError("Depth value must be an integer number passed either as int or float")

    # Check lavues integrity
    H, S, V = ih.check_hsw(HSV, output=Out2.NORMALIZED)

    # If all elements have the same values, then the color is in the grayscale
    if S == 0:
        return ih.return_rgb((V, V, V), normalized_input=True, depth=depth, output=output)

    # Find primary and secondary color on the color wheel
    primary_color = int(H * 6)  # Red, Green, Blue
    secondary_color = H * 6 - primary_color  # Cyan, Magenta, Yellow
    # Calculate R, G, B Values
    a = (1 - S) * V
    b = (1 - S * secondary_color) * V
    c = (1 - S * (1 - secondary_color)) * V

    if primary_color == 0:  # Red
        R, G, B = V, c, a
    elif primary_color == 1:  # Yellow
        R, G, B = b, V, a
    elif primary_color == 2:  # Green
        R, G, B = a, V, c
    elif primary_color == 3:  # Cyan
        R, G, B = a, b, V
    elif primary_color == 4:  # Blue
        R, G, B = c, a, V
    elif primary_color == 5:  # Magenta
        R, G, B = V, a, b

    return ih.return_rgb((R, G, B), normalized_input=True, output=output, depth=depth)


def hsv_to_hsl(*HSV: int | float | tuple | list, output: Enum = Out2.ROUND):
    """### Convert HSV values to HSL
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `HSV` (int | float | tuple | list): Hue, Saturation, Value either H in int range 0-359, SV range 0-100 \
                                    or float range 0-1 or a tuple/list with the same values
        `output` (str, optional): Either "normalized", "half-normalized", "round" or "direct"
        *     normalized returns a tuple(H, S, L) where the values are floats in range 0-1
        *     half-normalized returns a tuple(H, S, L) where the values are H in range 0-359, SL in range 0-1
        *     round returns a tuple(H, S, L) where the values are integers. H in range 0-359, SL in range 0-100
        *     direct returns a tuple(H, S, L) where the values are floats. H in range 0-359, SL in range 0-100
        *     In any invalid case the "direct" approach will be used

    #### N/B: Don't use round output if the output color is going to be used to further conversion!

    ### Returns:
        tuple[int, int, int] | tuple[float, float, float] | tuple[int, float, float]: Hue, Saturation, Lightness
    """
    # Check values integrity
    H, S, V = ih.check_hsw(HSV, output=Out2.NORMALIZED)

    # Find Lightness
    L = ((1/2) * V) * (2 - S)
    # Find Saturation for HSL using Saturation from HSV
    S = (V * S) / (1 - abs(2 * L - 1))

    return ih.return_hsw((H, S, L), normalized_input=True, output=output)


def hsl_to_hsv(*HSL: int | float | tuple | list, output: Enum = Out2.ROUND):
    """### Convert HSL to HSV values
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `HSL` (int | float | tuple | list): Hue, Saturation, Lightness either H in int range 0-359, SL range 0-100 \
                                    or float range 0-1 or a tuple/list with the same values
        `output` (str, optional): Either "normalized", "half-normalized", "round" or "direct"
        *     normalized returns a tuple(H, S, V) where the values are floats in range 0-1
        *     half-normalized returns a tuple(H, S, V) where the values are H in range 0-359, SV in range 0-1
        *     round returns a tuple(H, S, V) where the values are integers. H in range 0-359, SV in range 0-100
        *     direct returns a tuple(H, S, V) where the values are floats. H in range 0-359, SV in range 0-100
        *     In any invalid case the "direct" approach will be returned

    #### N/B: Don't use round output if the output color is going to be used to further conversion!

    Returns:
        tuple[int, int, int] | tuple[float, float, float] | tuple[int, float, float]: Hue, Saturation, Value
    """
    # Check values integrity
    H, S, L = ih.check_hsw(HSL, output=Out2.NORMALIZED)

    # Find Value
    V = ((2 * L) + S * (1 - abs(2 * L - 1))) / 2
    # Find Saturation for HSV using Saturation from HSL
    S = (2 * (V - L)) / V

    return ih.return_hsw((H, S, V), normalized_input=True, output=output)


def rgb_to_hsi(*color: int | float | str | tuple | list, depth: int = 8, output: Enum = Out2.ROUND):
    """### Takes an RGB color and returns its HSI (Hue Saturation Intensity) representation
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `color` (int | float | str | tuple | list): String "dec0de", "#0ff1ce", consecutive values either \
                int in range 0-255 or float in range 0-1 or an RGB list/tuple(R, G, B) with the same values
        `depth` (int | float): The bit depth of the input RGB values. Defaults to 8-bit (range 0-255)
        `output` (str, optional): Either "normalized", "half-normalized", "round" or "direct"
        *     normalized returns a tuple(H, S, I) where the values are floats in range 0-1
        *     half-normalized returns a tuple(H, S, I) where the values are H in range 0-359, SI in range 0-1
        *     round returns a tuple(H, S, I) where the values are integers. H in range 0-359, SI in range 0-100
        *     direct returns a tuple(H, S, I) where the values are floats. H in range 0-359, SI in range 0-100
        *     In any invalid case the "direct" approach will be returned

    #### N/B: Don't use round output if the output color is going to be used to further conversion!

    Returns:
        tuple[int, int, int] | tuple[float, float, float] | tuple[int, float, float]: Hue, Saturation, Intensity
    """
    # Check color integrity
    R, G, B = ih.check_color(color, normalized=True, depth=depth)

    # Find Hue, Saturation, Intensity
    I = (R + G + B) / 3
    S = 1 - 3 / (R + G + B) * min(R, G, B) if I > 0 else 0
    H = cu.get_hue(R, G, B, depth=depth, output=Out2.NORMALIZED)

    return ih.return_hsw((H, S, I), normalized_input=True, output=output)


def hsi_to_rgb(*HSI: int | float | tuple | list, depth: int = 8, output: Enum = Out1.ROUND):
    """### Converts HSI values to RGB
    #### Reference: https://en.wikipedia.org/wiki/HSL_and_HSV#HSI_to_RGB

    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `HSI` (int | float | tuple | list): Hue, Saturation, Intensity either H in int range 0-359, SL range 0-100 \
                                    or float range 0-1 or a tuple/list with the same values
        `depth` (int | float): The bit depth of the input RGB values. Defaults to 8-bit (range 0-255)
        `output` (str, optional): Either "hex", "hexp", "normalized", "round" or "direct"
        *     hex returns a hex string color in the form of decade
        *     hexp returns a hex string color in the form of #facade
        *     normalized returns a tuple(R, G, B) where the values are floats in range 0-1
        *     round returns a tuple(R, G, B) where the values are integers in range 0-255
        *     direct returns a tuple(R, G, B) where the values are floats in range 0-255
        *     In any invalid case the "direct" approach will be used

    #### N/B: Don't use round if the output color is going to be used to further conversion!

    ### Returns:
        str | tuple[int, int, int] | tuple[float, float, float]: Red, Green, Blue
    """
    if depth % 1 != 0:
        raise ValueError("Depth value must be an integer number passed either as int or float")

    # Check values integrity
    H, S, I = ih.check_hsw(HSI, output=Out2.NORMALIZED)

    H *= 6  # Get primary color
    Z = 1 - abs(H % 2 - 1)
    C = (3 * I * S) / (1 + Z) # Get Chroma
    X = C * Z

    if 0 <= H <= 1:
        R, G, B = C, X, 0
    elif 1 <= H <= 2:
        R, G, B = X, C, 0
    elif 2 <= H <= 3:
        R, G, B = 0, C, X
    elif 3 <= H <= 4:
        R, G, B = 0, X, C
    elif 4 <= H <= 5:
        R, G, B = X, 0, C
    elif 5 <= H <= 6:
        R, G, B = C, 0, X

    # Calculate R, G, B
    m = I * (1 - S)
    R, G, B = R + m, G + m, B + m

    return ih.return_rgb((R, G, B), normalized_input=True, depth=depth, output=output)


def rgb_to_hsp(*color: int | float | str | tuple | list, depth: int = 8, output: Enum = Out2.ROUND):
    """### Takes an sRGB color and returns its HSP (Hue, Saturation, Perceived brightness) representation.
    #### This is not an actual color representation! The Hue and Saturation are being calculated the same  \
            way as in HSV. The perceived brightness is being calculated using the Weighted Euclidean Norm of the R, G, B

    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `color` (int | float | str | tuple | list): String "c0ffed", "#dec1de", consecutive values either \
                int in range 0-255 or float in range 0-1 or an RGB list/tuple(R, G, B) with the same values
        `depth` (int | float): The bit depth of the input RGB values. Defaults to 8-bit (range 0-255)
        `output` (str, optional): Either "normalized", "half-normalized", "round" or "direct"
        *     normalized returns a tuple(H, S, P) where the values are floats in range 0-1
        *     half-normalized returns a tuple(H, S, P) where the values are H in range 0-359, SP in range 0-1
        *     round returns a tuple(H, S, P) where the values are integers. H in range 0-359, SP in range 0-100
        *     direct returns a tuple(H, S, P) where the values are floats. H in range 0-359, SP in range 0-100
        *     In any invalid case the "direct" approach will be used

    #### N/B: Don't use round output if the output color is going to be used to further conversion!

    Reference: http://alienryderflex.com/hsp.html

    ### Returns:
        tuple[int, int, int] | tuple[float, float, float] | tuple[int, float, float]: Hue, Saturation, Perceived brightness
    """
    # Check color integrity
    R, G, B = ih.check_color(color, depth=depth, normalized=True)

    # Calculate Weighted Euclidean Norm of the R, G, B Vector (Perceived brightness)
    P = (0.299 * R * R + 0.587 * G * G + 0.114 * B * B) ** 0.5

    # Check if color is in grayscale
    if R == G == B:
        return ih.return_hsw((0, 0, P), normalized_input=True, output=output)

    # Get Hue and Saturation
    H = cu.get_hue(R, G, B, depth=depth, output=Out2.NORMALIZED)
    S = (max(R, G, B) - min(R, G, B)) / max(R, G, B)

    return ih.return_hsw((H, S, P), normalized_input=True, output=output)


def hsp_to_rgb(*HSP: int | float | tuple | list, depth: int = 8, output: Enum = Out1.ROUND):
    """### Takes an HSP color and returns RGB values.

    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `color` (int | float | str | tuple | list): String "add1c7", "#effec7", consecutive values either \
                int in range 0-255 or float in range 0-1 or an RGB list/tuple(R, G, B) with the same values
        `depth` (int | float): The bit depth of the input RGB values. Defaults to 8-bit (range 0-255)
        `output` (str, optional): Either "hex", "hexp", "normalized", "round" or "direct"
        *     hex returns a hex string color in the form of c0ffee
        *     hexp returns a hex string color in the form of #decaff
        *     normalized returns a tuple(R, G, B) where the values are floats in range 0-1
        *     round returns a tuple(R, G, B) where the values are integers in range 0-255
        *     direct returns a tuple(R, G, B) where the values are floats in range 0-255
        *     In any invalid case the "direct" approach will be used

    #### N/B: Don't use round output if the output color is going to be used to further conversion!

    Reference: http://alienryderflex.com/hsp.html
    ITU BT.601 / Rec. 601

    ### Returns:
        str | tuple[int, int, int] | tuple[float, float, float]: Red, Green, Blue
    """
    if depth % 1 != 0:
        raise ValueError("Depth value must be an integer number passed either as int or float")

    # Check values integrity
    H, S, P = ih.check_hsw(HSP, output=Out2.NORMALIZED)

    def wrap(HSP: tuple | list, c1: float, c2: float, c3: float, S1: bool):
        """### This is an internal helper function for the hsp_to_rgb function to lift off some of the calculations.
        c1, c2, c3 - Pr, Pg, Pb in different order

        ### Args:
            `HSP` (tuple | list): Hue, Saturation, Perceived brightness in range 0-1
            `c1` (float): Constant. Either 0.299, 0.587 or 0.114
            `c2` (float): Constant. Either 0.299, 0.587 or 0.114
            `c3` (float): Constant. Either 0.299, 0.587 or 0.114
            `S1` (bool): Whether S (Saturation) is 1 (100%). Defaults to False

        ### Returns:
            tuple[float, float, float]: R, G, B values in different order depending on the constants.
        """
        if S1:
            ch1 = (HSP[2] ** 2 / (c1 + c2 * HSP[0] ** 2)) ** 0.5
            ch2 = ch1 * HSP[0]
            ch3 = 0
            return ch3, ch1, ch2

        min_over_max = 1 - HSP[1]
        part = 1 + HSP[0] * (1 / min_over_max - 1)
        ch1 = HSP[2] / (c1 / min_over_max ** 2 + c2 * part ** 2 + c3) ** 0.5
        ch2 = ch1 / min_over_max
        ch3 = ch1 + HSP[0] * (ch2 - ch1)
        return ch1, ch2, ch3

    # Get weights constants
    Pr, Pg, Pb = 0.299, 0.587, 0.114

    # Calculate R, G, B based on the Hue
    if H < 1 / 6:  # R > G > B
        H = 6 * H
        B, R, G = wrap((H, S, P), Pr, Pg, Pb, S >= 1)
    elif H < 2 / 6:  # G > R > B
        H = 6 * (-H + 2 / 6)
        B, G, R = wrap((H, S, P), Pg, Pr, Pb, S >= 1)
    elif H < 3 / 6:  # G > B > R
        H = 6 * (H - 2 / 6)
        R, G, B = wrap((H, S, P), Pg, Pb, Pr, S >= 1)
    elif H < 4 / 6:  # B > G > R
        H = 6 * (-H + 4 / 6)
        R, B, G = wrap((H, S, P), Pb, Pg, Pr, S >= 1)
    elif H < 5 / 6:  # B > R > G
        H = 6 * (H - 4 / 6)
        G, B, R = wrap((H, S, P), Pb, Pr, Pg, S >= 1)
    else:            # R > B > G
        H = 6 * (-H + 1)
        G, R, B = wrap((H, S, P), Pr, Pb, Pg, S >= 1)

    return ih.return_rgb((R, G, B), depth=depth, normalized_input=True, output=output)


def rgb_to_hcl(
    *color: int | float | str | tuple | list,
    gamma: int | float = 3,
    Y0: int | float = 100,
    depth: int = 8,
    output: Enum = Out2.DIRECT):
    """### Takes an RGB color and returns its HCL (Hue, Chroma, Luminance) representation according to \
    Sarifuddin and Missaoui (2005) method.
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `color` (int | float | str | tuple | list): String "c0ffee", "#decaff", consecutive values either \
                int in range 0-255 or float in range 0-1 or an RGB list/tuple(R, G, B) with the same values
        `gamma` (int, optional): Non-linear lightness exponent matching Lightness. Defaults to 3.
        `Y0` (int, optional): White reference luminance. Defaults to 100.
        `depth` (int | float): The bit depth of the input RGB values. Defaults to 8-bit (range 0-255)
        `output` (str, optional): Either "normalized", "half-normalized", "round" or "direct"
        *     normalized returns a tuple(H, C, L) where the values are floats in range 0-1
        *     half-normalized returns a tuple(H, C, L) where the values are H in range 0-359, CL in range 0-1
        *     round returns a tuple(H, C, L) where the values are integers. H in range 0-359, CL depend on gamma and Y0
        *     direct returns a tuple(H, C, L) where the values are floats. H in range 0-359, CL depend on gamma and Y0
        *     In any invalid case the "direct" approach will be used

    - Reference https://en.wikipedia.org/wiki/HCL_color_space
    - Reference https://web.archive.org/web/20190220074017/http://pdfs.semanticscholar.org/206c/a4c4bb4a5b6c7b614b8a8f4461c0c6b87710.pdf

    ### Returns:
        tuple(Hue (degrees), Chroma, Luminance)

    #### N/B : Don't compare the results with the colour science library! While the formula is the same, their return \
        value for Hue is in radians ~[-pi, pi] while this one is in degrees [0, 359]
    """
    # Check color integrity
    R, G, B = ih.check_color(color, depth=depth, normalized=output in {"normalized", "half-normalized"})

    min_ = min(R, G, B)
    max_ = max(R, G, B)
    alpha = 0 if min_ == max_ else (min_ / max_) / Y0
    Q = exp(alpha * gamma)

    H = 0 if R == G else atan((G - B) / (R - G)) # For angles between -90 and 90 degrees

    # To allow hue values to vary in a larger interval going from −180 to 180 degrees:
    if R < G:
        H = 2/3 * H - pi if G < B else pi + 4/3 * H
    else:
        H = 4/3 * H if G < B else 2/3 * H
    H = convert_range(degrees(H), (-180, 180), (0, 360))

    C = Q/3 * (abs(R - G) + abs(G - B) + abs(B - R))
    L = (Q * max_ + (Q - 1) * min_) / 2

    # if min_ == 0 and 0 < max_ < 256:
        # 0 < L <= 128
    # if max_ == 255 and 0 < min_  < 255:
        # if gamma == 1:
            # 128 < L <= 130
        # elif gamma == 10:
            # 128 < L <= 154.5
        # elif gamma == 30:
            # 128 < L <= 216.5

    match output:
        case "round":
            return round(H), round(C), round(L)
        case "normalized":
            return H/360, C, L
        case "half-normalized":
            return H, C, L
        case _:
            return H, C, L


def hcl_to_rgb(
    *HCL: int | float | tuple | list,
    gamma: int | float = 3,
    Y0: int | float = 100,
    depth: int = 8,
    big_float: bool = True,
    output: Enum = Out1.ROUND):
    """### Takes an HCL color (Sarifuddin and Missaoui (2005) method) and returns its RGB representation.
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `HCL` (int | float | tuple | list): Hue, Chroma, Luminance either H in int range 0-359, CL range 0-255, \
                H in int range 0-359, CL float in range 0-1 or floats range 0-1 or a tuple/list with the same values.
        `gamma` (int, optional): Non-linear lightness exponent matching Lightness. Defaults to 3.
        `Y0` (int, optional): White reference luminance. Defaults to 100.
        `depth` (int | float): The bit depth of the input RGB values. Defaults to 8-bit (range 0-255)
        `output` (str, optional): Either "hex", "hexp", "normalized", "round" or "direct"
        *     hex returns a hex string color in the form of decade
        *     hexp returns a hex string color in the form of #facade
        *     normalized returns a tuple(R, G, B) where the values are floats in range 0-1
        *     round returns a tuple(R, G, B) where the values are integers in range 0-255
        *     direct returns a tuple(R, G, B) where the values are floats in range 0-255
        *     In any invalid case the "direct" approach will be used

    Reference https://en.wikipedia.org/wiki/HCL_color_space
    Reference https://web.archive.org/web/20190220074017/http://pdfs.semanticscholar.org/206c/a4c4bb4a5b6c7b614b8a8f4461c0c6b87710.pdf

    ### Returns:
        tuple(Hue, Chroma, Luminance)
    """
    H, C, L = ih.check_hcl(*HCL, big_float=big_float)

    Q = exp((1 - (3*C) / (4*L)) * gamma/Y0)
    min_ = (4*L - 3*C) / (4*Q - 2)
    max_ = min_ + (3*C) / (2*Q)

    if 0 <= H <= radians(60):
        R = max_
        G = (max_ * (tan(3/2 * H)) + min_) / (1 + tan(3/2 * H))
        B = min_
    elif radians(60) < H <= radians(120):
        R = (max_ * (1 + tan(3/4 * (H - 180))) - min_) / tan(3/4 * (H - 180))
        G = max_
        B = min_
    elif 120 < H <= 180:
        R = min_
        G = max_
        B = max_ * (1 + tan(3/4 * (H - 180))) - min_ * tan(3/4 * (H - 180))
    elif radians(-60) <= H < 0:
        R = max_
        G = min_
        B = min_ * (1 + tan(3/4 * H)) - max_ * tan(3/4 * H)
    elif radians(-120) <= H < radians(-60):
        a, b = (min_ * (1 + tan(3/4 * H)) - max_), tan(3/4 * H)
        R = 0 if b == 0 else a / b
        G = min_
        B = max_
    elif radians(-180) < H < radians(120):
        R = min_
        G = (min_ * (tan(3/2 * (H + 180))) + B) / (1 + tan(3/2 * (H + 180)))
        B = max_

    return ih.return_rgb((R, G, B), normalized_input=True, depth=depth, output=output)


def rgb_to_ihls(*color: int | float | str | tuple | list, depth: int = 8, output: Enum = Out2.ROUND):
    """### Takes an RGB color and returns its IHLS (Improved Hue, Luminance, Saturation) representation
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `color` (int | float | str | tuple | list): String "dec0de", "#0ff1ce", consecutive values either \
                int in range 0-255 or float in range 0-1 or an RGB list/tuple(R, G, B) with the same values
        `depth` (int | float): The bit depth of the input RGB values. Defaults to 8-bit (range 0-255)

        `output` (str, optional): Either "normalized", "half-normalized", "round" or "direct"
        *     normalized returns a tuple(H, Y, S) where the values are floats in range 0-1
        *     half-normalized returns a tuple(H, Y, S) where the values are H in range 0-359, YS in range 0-1
        *     round returns a tuple(H, Y, S) where the values are integers. H in range 0-359, YS in range 0-100
        *     direct returns a tuple(H, Y, S) where the values are floats. H in range 0-359, YS in range 0-100
        *     In any invalid case the "direct" approach will be used

    #### N/B: Don't use round output if the output color is going to be used to further conversion!

    Reference 1 https://sites.google.com/site/mcvibot2011sep/Modules/IHLSNHS
    Reference 2 https://people.cmm.minesparis.psl.eu/users/serra/notes_internes_pdf/NI-230.pdf

    ### Returns:
        tuple[int, int, int] | tuple[float, float, float] | tuple[int, float, float]: Hue (degrees), Lightness,  Saturation

    #### N/B: The Hue value is slightly different than the one in the standard conversion to HSL/HSV/HSI and the get_hue
        function. In most cases the rounded value is the same but sometimes there's a difference.
    """
    # Check color integrity
    R, G, B = ih.check_color(color, normalized=True, depth=depth)

    Y, C1, C2 = ih.MATRIX_RGB_TO_YC1C2 @ (R, G, B)
    C = sqrt(C1**2 + C2**2)
    C1C = 0 if C == 0 else C1 / C
    acos_C1_C2 = 0 if C1C == 0 else acos(C1C)

    H = pi*2 - acos_C1_C2 if C2 > 0 else acos_C1_C2
    S = max(R, G, B) - min(R, G, B)

    #+ Alternative calculation method with similar results:
    # Reference https://academicjournals.org/journal/SRE/article-full-text-pdf/770C53228330
    # H = cu.get_hue(R, G, B, depth=depth)
    # Y = (0.213*R + 0.715*G + 0.072 * B) * 100
    # S = (max(R, G, B) - min(R, G, B)) * 100

    return ih.return_hsw((degrees(H), Y*100, S*100), output=output)


def ihls_to_rgb(*HYS: int | float | tuple | list, depth: int = 8, output: Enum = Out1.ROUND):
    """### Converts IHLS (Improved Hue, Luminance, Saturation) values to RGB
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `HYS` (int | float | tuple | list): Hue, Luminance, Saturation in either int range H 0-360, LS range 0-100 \
                                    or float range 0-1 or a tuple/list with the same values
        `depth` (int, optional): The bit depth of the input RGB values. Defaults to 8-bit (range 0-255)
        `output` (str, optional): Either "hex", "hexp", "normalized", "round" or "direct"
        *     hex returns a hex string color in the form of decade
        *     hexp returns a hex string color in the form of #facade
        *     normalized returns a tuple(R, G, B) where the values are floats in range 0-1
        *     round returns a tuple(R, G, B) where the values are integers in range 0-255
        *     direct returns a tuple(R, G, B) where the values are floats in range 0-255
        *     In any invalid case the "direct" approach will be used

    #### N/B: Don't use round if the output color is going to be used to further conversion!

    Reference 1 https://sites.google.com/site/mcvibot2011sep/Modules/IHLSNHS
    Reference 2 https://people.cmm.minesparis.psl.eu/users/serra/notes_internes_pdf/NI-230.pdf

    ### Returns:
        str | tuple[int, int, int] | tuple[float, float, float]: Red, Green, Blue
    """
    # Check values integrity
    H, Y, S = ih.check_hsw(HYS, output=Out2.HALF_NORMALIZED)
    H = radians(H)

    k = H // (pi/3)
    Hs = H - k * (pi/3)
    C = sqrt(3) * S / (2 * sin(2 * (pi/3) - Hs))
    C1 = C * cos(H)
    C2 = -C * sin(H)

    RGB = ih.MATRIX_YC1C2_TO_RGB @ (Y, C1, C2)
    return ih.return_rgb(RGB, normalized_input=True, depth=depth, output=output)


def rgb_to_xyz(
    *color: str | tuple | list,
    illuminant: str = "D65",
    observer: int | float | str = "2",
    adaptation: str = "bradford",
    output: Enum = Out3.DIRECT) -> tuple[int, int, int] | tuple[float, float, float]:
    """### Takes an 8-bit sRGB color and returns its XYZ values (where Y is Luminance)

    ### Args:
        `color` (str | tuple | list): String "dec0de", "#0ff1ce", consecutive values either \
                in int range 0-255 or in float range 0-1 or a list/tuple (r, g, b) in same ranges
        `illuminant` (str): The illuminant for the output XYZ values. Defaults to "D65"
        `observer` (str | int | float): The observer angle for the illuminant of the XYZ values. Defaults to "2"
        `adaptation` (str): The adaptation method to be used for illuminant conversions. Defaults to "bradford"
        `output` (str, optional): Either "normalized", "round" or "direct"
        * normalized returns a tuple(X, Y, Z) where the values are floats in range 0-1
        * round returns a tuple(X, Y, Z) where the values are integers in range 0-100
        * direct returns a tuple(X, Y, Z) where the values are floats in range 0-100
        * In any invalid case the "direct" approach will be returned

    ### Illuminants | Lighting type:

        `A`: Incandescent/tungsten
        `B`: Old direct sunlight at noon
        `C`: Old daylight
        `D50`: ICC profile PCS. Used for printing and used by Photoshop.
        `D55`: Mid-morning daylight
        `D65`: Daylight, sRGB, Adobe RGB. Simulates noon daylight with correlated color temperature of 6504 K.
        `D75`: North sky daylight
        `E`: Equal energy
        `F1`: Daylight Fluorescent
        `F2`: Cool fluorescent
        `F3`: White Fluorescent
        `F4`: Warm White Fluorescent
        `F5`: Daylight Fluorescent
        `F6`: Lite White Fluorescent
        `F7`: Daylight fluorescent, D65 simulator
        `F8`: Sylvania F40, D50 simulator
        `F9`: Cool White Fluorescent
        `F10`: Ultralume 50, Philips TL85
        `F11`: Ultralume 40, Philips TL84
        `F12`: Ultralume 30, Philips TL83

    ### Observers can either be `2`° or `10`°

    ### Available adaptation matrices:
        * xyz_scaling
        * bradford      >>> Considered to be the most accurate. Used in Photoshop.
        * von_kries
        * fairchild
        * cat02
        * sharp
        * cmccat97
        * cmccat2000
        * cat02_brill2008
        * cat16
        * bianco2010
        * pc_bianco2010

    #### N/B: Don't use round if the output color is going to be used to further conversion!

    ### Returns:
        tuple[float, float, float] | tuple[int, int, int]: XYZ
    """
    # Check color integrity
    R, G, B = ih.check_color(color, normalized=True)
    # Refine arguments to be the correct type and form
    illuminant, observer, adaptation = xyz.refine_args(illuminant=illuminant, observer=observer, adaptation=adaptation)

    # Convert sRGB to Linear RGB
    R, G, B = tf.srgb((R, G, B), decode=True, output=Out1.NORMALIZED)

    # Get the conversion matrix for sRGB, D65 illuminant, 2 degrees observer angle
    matrix = cs["SRGB"]["override_matrix"]["to_xyz"]

    # Get the dot product of the matrix and the RGB colors
    X, Y, Z = ((R * matrix[i][0]) + (G * matrix[i][1]) + (B * matrix[i][2]) for i in range(3))

    # Do chromatic adaptation if the output illuminant or observer aren't the same as the ones of the matrix
    if illuminant != "D65" or observer != "2":
        X, Y, Z = xyz.apply_chromatic_adaptation((X, Y, Z), orig_illum="D65", targ_illum=illuminant, observer=observer, adaptation=adaptation)

    match output:
        case Out3.ROUND:
            return round(X*100), round(Y*100), round(Z*100)
        case Out3.NORMALIZED:
            return X, Y, Z
        case Out3.DIRECT:
            return X*100, Y*100, Z*100
        case _:
            raise ValueError("Wrong output type!")


def rgb_to_xyz_alt(
    *color: str | tuple | list,
    illuminant: str = "D65",
    observer: str | int | int = "2",
    adaptation: str = "bradford",
    color_space: str = "sRGB",
    output: Enum = Out3.DIRECT,
    **kwargs) -> tuple[int, int, int] | tuple[float, float, float]:
    """### Takes an 8-bit sRGB color and returns its XYZ values (where Y is Luminance)

    #### This is an alternative way to convert from sRGB to XYZ color. The output of both methods \
        is roughly the same. It's the input that's different. The original function assumes the \
            input color is in sRGB space. This one allows for specifying a different input color space.

    ### Args:
        `color` (str | tuple | list): String "decade", "#facade", consecutive values either \
                in int range 0-255 or in float range 0-1 or a list/tuple (r, g, b) in same ranges
        `illuminant` (str): The illuminant for the output XYZ values. Defaults to "D65"
        `observer` (str | int | float): The observer angle for the illuminant of the XYZ values. Defaults to "2"
        `adaptation` (str): The adaptation method to be used for illuminant conversions. Defaults to "bradford"
        `color_space` (str): The color space of the input R, G, B values.
        `output` (str, optional): Either "normalized", "round" or "direct"
        * normalized returns a tuple(X, Y, Z) where the values are floats in range 0-1
        * round returns a tuple(X, Y, Z) where the values are integers in range 0-100
        * direct returns a tuple(X, Y, Z) where the values are floats in range 0-100
        * In any invalid case the "direct" approach will be returned

        `kwargs`: Additional arguments to pass to the transfer function of the given color space. Refer to
            the transfer_functions module to get the needed arguments for the specific color space

    ### Illuminants | Lighting type:

        `A`: Incandescent/tungsten
        `B`: Old direct sunlight at noon
        `C`: Old daylight
        `D50`: ICC profile PCS. Used for printing and used by Photoshop.
        `D55`: Mid-morning daylight
        `D65`: Daylight, sRGB, Adobe RGB. Simulates noon daylight with correlated color temperature of 6504 K.
        `D75`: North sky daylight
        `E`: Equal energy
        `F1`: Daylight Fluorescent
        `F2`: Cool fluorescent
        `F3`: White Fluorescent
        `F4`: Warm White Fluorescent
        `F5`: Daylight Fluorescent
        `F6`: Lite White Fluorescent
        `F7`: Daylight fluorescent, D65 simulator
        `F8`: Sylvania F40, D50 simulator
        `F9`: Cool White Fluorescent
        `F10`: Ultralume 50, Philips TL85
        `F11`: Ultralume 40, Philips TL84
        `F12`: Ultralume 30, Philips TL83

    ### Observers can either be `2`° or `10`°

    ### Available adaptation matrices:
        * xyz_scaling
        * bradford      >>> Considered to be the most accurate. Used in Photoshop.
        * von_kries
        * fairchild
        * cat02
        * sharp
        * cmccat97
        * cmccat2000
        * cat02_brill2008
        * cat16
        * bianco2010
        * pc_bianco2010

    #### N/B: Don't use round if the output color is going to be used to further conversion!

    ### Returns:
        tuple[float, float, float] | tuple[int, int, int]: XYZ
    """

    # Check color integrity
    R, G, B = ih.check_color(color, normalized=True)
    illuminant, observer, color_space, adaptation, _ = xyz.refine_args(
        illuminant=illuminant, observer=observer, color_space=color_space, adaptation=adaptation)

    # Convert to Linear RGB
    R, G, B = cs[color_space]["transfer function"]((R, G, B), decode=True, output="normalized", **kwargs)

    # Check if requested color space has an override matrix
    override_matrix = cs[color_space].get("override_matrix")
    if override_matrix and illuminant == "D65":
        matrix = override_matrix["to_xyz"]
    else:
        # Generate a conversion matrix if no override matrix exists
        matrix = xyz.working_space_matrix(color_space, illuminant, observer, adaptation)

    X, Y, Z = ((R * matrix[i][0]) + (G * matrix[i][1]) + (B * matrix[i][2]) for i in range(3))

    match output:
        case "round":
            return round(X*100), round(Y*100), round(Z*100)
        case "normalized":
            return X, Y, Z
        case _:
            return X*100, Y*100, Z*100


def xyz_to_rgb(
    *XYZ: int | float | tuple | list,
    big_float: bool = True,
    illuminant: str = "D65",
    observer: str | int | float = "2",
    adaptation: str = "bradford",
    color_space: str = "sRGB",
    output: Enum = Out1.ROUND):
    """### Takes XYZ color and returns its sRGB values

    ### Args:
        `XYZ` (int, float, tuple, list): XYZ value in 3 consecutive int(0, 100), float(0, 100) or float(0, 1)  \
            or list/tuple containing the same
        `big_float` (bool, optional): Wether the input XYZ values are floats in range 0-100. Defaults to True.
        `illuminant` (str, optional): The illuminant of the input XYZ color. Defaults to 'D65'
        `observer` (int[2 | 10] | str, optional): The observer viewing angle - 2° (CIE 1931) or 10° (CIE 1964). Defaults to "2".
        `adaptation` (str): The adaptation method to be used for illuminant conversions. Defaults to "bradford"
        `color_space` (str, optional): The target color space in which the XYZ color will be converted. Defaults to sRGB.
        `output` (str, optional): Either "hex", "hexp", "normalized", "round" or "direct"
        *     hex returns a hex string color in the form of c0ffed
        *     hexp returns a hex string color in the form of #dec1de
        *     normalized returns a tuple(R, G, B) where the values are floats in range 0-1
        *     round returns a tuple(R, G, B) where the values are integers in range 0-255
        *     direct returns a tuple(R, G, B) where the values are floats in range 0-255
        *     In any invalid case the "direct" approach will be used

    ### Illuminants | Lighting type:

        `A`: Incandescent/tungsten
        `B`: Old direct sunlight at noon
        `C`: Old daylight
        `D50`: ICC profile PCS `used for printing`
        `D55`: Mid-morning daylight
        `D65`: Daylight, sRGB, Adobe RGB. Simulates noon daylight with correlated color temperature of 6504 K.
        `D75`: North sky daylight
        `E`: Equal energy
        `F1`: Daylight Fluorescent
        `F2`: Cool fluorescent
        `F3`: White Fluorescent
        `F4`: Warm White Fluorescent
        `F5`: Daylight Fluorescent
        `F6`: Lite White Fluorescent
        `F7`: Daylight fluorescent, D65 simulator
        `F8`: Sylvania F40, D50 simulator
        `F9`: Cool White Fluorescent
        `F10`: Ultralume 50, Philips TL85
        `F11`: Ultralume 40, Philips TL84
        `F12`: Ultralume 30, Philips TL83

    ### Observers can either be `2`° or `10`°

    ### Available adaptation matrices:
        * xyz_scaling
        * bradford      >>> Considered to be the most accurate. Used in Photoshop.
        * von_kries
        * fairchild
        * cat02
        * sharp
        * cmccat97
        * cmccat2000
        * cat02_brill2008
        * cat16
        * bianco2010
        * pc_bianco2010

    #### N/B: Don't use round if the output color is going to be used to further conversion!

    ### Returns:
        str | tuple[int, int, int] | tuple[float, float, float]: Red, Green, Blue
    """
    # Refine arguments to be the correct type and form
    illuminant, observer, color_space, adaptation, _ = xyz.refine_args(
        illuminant=illuminant, observer=observer, color_space=color_space, adaptation=adaptation)

    # Check values integrity
    X, Y, Z = ih.check_xyz(XYZ, normalized=True, big_float=big_float)

    # Check if requested color space has an override matrix
    override_matrix = cs[color_space].get("override_matrix")
    if override_matrix and illuminant == "D65":
        matrix = override_matrix["to_rgb"]
    else:
        # Generate a conversion matrix if no override matrix exists
        matrix = xyz.working_space_matrix(color_space, illuminant, observer, adaptation, to_xyz=False)

    # Get the conversion matrix
    R, G, B = ((X * matrix[i][0]) + (Y * matrix[i][1]) + (Z * matrix[i][2]) for i in range(3))
    # R, G, B = matrix @ (X, Y, Z)
    R, G, B = ih.return_scale((R, G, B), min_max=(0.0, 1.0), clamp=True, normalized_input=True, output=Out3.NORMALIZED)

    # Apply gamma
    R, G, B = cs[color_space]["transfer function"]((R, G, B), output="normalized")

    return ih.return_rgb((R, G, B), normalized_input=True, output=output)


def xyz_to_rgb_alt(
    *XYZ: int | float | tuple | list,
    big_float: bool = True,
    illuminant: str = "D65",
    observer: int | float | str = "2",
    adaptation="bradford",
    output: Enum = Out1.ROUND) -> tuple:
    """### Takes XYZ color and returns its RGB values in the requested color space

    #### This is an alternative way to convert from XYZ to RGB color. The output of both methods \
        is roughly the same. It's the input that's different. The original function assumes the \
            output color is in sRGB space. This one allows for specifying a different input color space.

    ### Args:
        `XYZ` (int, float, tuple, list): XYZ value in 3 consecutive int(0, 100), float(0, 100) or float(0, 1) or \
            list/tuple containing the same
        `big_float` (bool, optional): Wether the input XYZ values are floats in range 0-100. Defaults to True.
        `illuminant` (str, optional): The iluminant of the input XYZ color. Defaults to 'D65'
        `observer` (int[2 | 10] | str, optional): The observer viewing angle - 2° (CIE 1931) or 10° (CIE 1964). Defaults to None (2).
        `adaptation` (str): The adaptation method to be used for illuminant conversions. Defaults to "bradford"
        `output` (str, optional): Either "hex", "hexp", "normalized", "round" or "direct"
        *     hex returns a hex string color in the form of add1c7
        *     hexp returns a hex string color in the form of #effec7
        *     normalized returns a tuple(R, G, B) where the values are floats in range 0-1
        *     round returns a tuple(R, G, B) where the values are integers in range 0-255
        *     direct returns a tuple(R, G, B) where the values are floats in range 0-255
        *     In any invalid case the "direct" approach will be used

    ### Illuminants | Lighting type:

        `A`: Incandescent/tungsten
        `B`: Old direct sunlight at noon
        `C`: Old daylight
        `D50`: ICC profile PCS `used for printing`
        `D55`: Mid-morning daylight
        `D65`: Daylight, sRGB, Adobe RGB. Simulates noon daylight with correlated color temperature of 6504 K.
        `D75`: North sky daylight
        `E`: Equal energy
        `F1`: Daylight Fluorescent
        `F2`: Cool fluorescent
        `F3`: White Fluorescent
        `F4`: Warm White Fluorescent
        `F5`: Daylight Fluorescent
        `F6`: Lite White Fluorescent
        `F7`: Daylight fluorescent, D65 simulator
        `F8`: Sylvania F40, D50 simulator
        `F9`: Cool White Fluorescent
        `F10`: Ultralume 50, Philips TL85
        `F11`: Ultralume 40, Philips TL84
        `F12`: Ultralume 30, Philips TL83

    ### Color spaces:

        - NTSC-J
        - NTSC, MUSE
        - Apple RGB
        - PAL / SECAM
        - sRGB
        - scRGB
        - HDTV
        - Adobe RGB
        - M.A.C
        - NTSC-FCC
        - PAL-M
        - eciRGB
        - DCI-P3
        - Display P3
        - UHDTV
        - Wide Gamut
        - RIMM
        - ProPhoto (ROMM)
        - CIE RGB
        - CIE XYZ

    ### Observers can either be `2`° or `10`°

    ### Available adaptation matrices:
        * xyz_scaling
        * bradford      >>> Considered to be the most accurate. Used in Photoshop.
        * von_kries
        * fairchild
        * cat02
        * sharp
        * cmccat97
        * cmccat2000
        * cat02_brill2008
        * cat16
        * bianco2010
        * pc_bianco2010

    #### N/B: Don't use round if the output color is going to be used to further conversion!

    ### Returns:
        str | tuple[int, int, int] | tuple[float, float, float]: Red, Green, Blue
    """
    # Refine arguments to be the correct type and form
    illuminant, observer, adaptation = xyz.refine_args(
        illuminant=illuminant, observer=observer, adaptation=adaptation)

    # Check values integrity
    X, Y, Z = ih.check_xyz(XYZ, normalized=True, big_float=big_float)

    # Do chromatic adaptation if the input illuminant or observer aren't the same as the ones of the color space's
    if illuminant != "D65" or observer != "2":
        X, Y, Z = xyz.apply_chromatic_adaptation((X, Y, Z), illuminant, "D65", observer=observer, adaptation=adaptation)

    # Get the conversion matrix
    matrix = cs["SRGB"]["override_matrix"]["to_rgb"]

    # Apply matrix to the X, Y, Z values
    R, G, B = ((X * matrix[i][0]) + (Y * matrix[i][1]) + (Z * matrix[i][2]) for i in range(3))

    # Apply gamma
    R, G, B = tf.srgb((R, G, B), output=Out1.NORMALIZED)

    return ih.return_rgb((R, G, B), normalized_input=True, output=output)


def xyz_to_lab(
    *XYZ: int | float | tuple | list,
    big_float : bool = True,
    xyz_illuminant: str = "D65",
    lab_illuminant: str = "D65",
    observer: str | int | float = "2",
    adaptation: str = "bradford",
    round_: bool = False) -> tuple[int, int, int] | tuple[float, float, float]:
    """### Takes XYZ color and returns its CIE L*ab values

    ### Args:
        `XYZ` (int, float, tuple, list): XYZ color in 3 consecutive int(0, 100), float(0, 100) or float(0, 1) or \
            list/tuple containing the same
        `big_float` (bool, optional): Wether the input XYZ values are floats in range 0-100. Defaults to True.
        `xyz_illuminant` (str, optional): The iluminant of the input XYZ color. Defaults to 'D65'
        `lab_illuminant` (str, optional): The iluminant of the output L*ab color. Defaults to 'D65'
        `observer` (int[2 | 10] | str, optional): The observer viewing angle - 2° (CIE 1931) or 10° (CIE 1964). Defaults to "2".
        `adaptation` (str): The adaptation method to be used for illuminant conversions. Defaults to "bradford"
        `round_` (bool, optional): Returns rounded values as integers. Defaults to False.

    ### Illuminants | Lighting type:

        `A`: Incandescent/tungsten
        `B`: Old direct sunlight at noon
        `C`: Old daylight
        `D50`: ICC profile PCS. Used for printing and used by Photoshop.
        `D55`: Mid-morning daylight
        `D65`: Daylight, sRGB, Adobe RGB. Simulates noon daylight with correlated color temperature of 6504 K.
        `D75`: North sky daylight
        `E`: Equal energy
        `F1`: Daylight Fluorescent
        `F2`: Cool fluorescent
        `F3`: White Fluorescent
        `F4`: Warm White Fluorescent
        `F5`: Daylight Fluorescent
        `F6`: Lite White Fluorescent
        `F7`: Daylight fluorescent, D65 simulator
        `F8`: Sylvania F40, D50 simulator
        `F9`: Cool White Fluorescent
        `F10`: Ultralume 50, Philips TL85
        `F11`: Ultralume 40, Philips TL84
        `F12`: Ultralume 30, Philips TL83

    ### Observers can either be `2`° or `10`°

    #### N/B: Don't use round if the output color is going to be used to further conversion!

    ### Returns:
        tuple[int, int, int] | tuple[float, float, float]: L in range(0, 100), ab in range(-128, 128)
    """
    # Refine arguments to be the correct type and form
    xyz_illuminant, observer = xyz.refine_args(illuminant=xyz_illuminant, observer=observer)
    lab_illuminant = next(xyz.refine_args(illuminant=lab_illuminant))

    # Check values integrity
    X, Y, Z = ih.check_xyz(XYZ, normalized=True, big_float=big_float)

    # Do chromatic adaptation if the output illuminant or observer aren't the same as the ones of the matrix
    if xyz_illuminant != lab_illuminant:
        X, Y, Z = xyz.apply_chromatic_adaptation((X, Y, Z), xyz_illuminant, lab_illuminant, observer, adaptation)

    # Calculate reference white
    X, Y, Z = (val / xyz.ILLUMINANTS[observer][lab_illuminant][i] for i, val in enumerate((X, Y, Z)))

    # Calculate function of X, Y, Z. That's f(x), f(y), f(z)
    X, Y, Z = (i ** (1/3) if i > xyz.CIE_E else ((xyz.CIE_K * i) + 16) / 116 for i in (X, Y, Z))
    # Alternative formula
    # X, Y, Z = (i ** (1/3) if i > xyz.CIE_E else (7.787 * i) + (16 / 116) for i in (X, Y, Z))
    # Alternative values
    # 7.787 is 841/108 or (1/3) * (29/6) ** 2 and 16 / 116 could be 4/29

    # Calculate L*ab based on functions
    L = (116 * Y) - 16
    A = 500 * (X - Y)
    B = 200 * (Y - Z)

    return (round(L), round(A), round(B)) if round_ else (L, A, B)


def lab_to_xyz(
    *LAB: tuple | list,
    lab_illuminant: str = "D65",
    xyz_illuminant: str = "D65",
    observer: int | float | str = "2",
    adaptation: str = "bradford",
    output: Enum = Out3.DIRECT) -> tuple[int, int, int] | tuple[float, float, float]:
    """### Converts CIE L*ab color ato XYZ.
    L* in range(0, 100), ab in range(-128, 128)

    ### Args:
        `LAB` (int, float, tuple, list): L*ab color in 3 consecutive int or float values in range
            L* (0, 100), ab (-128, 128) or list/tuple containing the same values
        `lab_illuminant` (str, optional): The iluminant of the input L*ab color. Defaults to 'D65'
        `xyz_illuminant` (str, optional): The iluminant of the output XYZ color. Defaults to 'D65'
        `observer` (int[2 | 10] | str, optional): The observer viewing angle - 2° (CIE 1931) or 10° (CIE 1964). Defaults to "2".
        `adaptation` (str): The adaptation method to be used for illuminant conversions. Defaults to "bradford"
        `output` (str, optional): Either "normalized", "round" or "direct"
        * normalized returns a tuple(X, Y, Z) where the values are floats in range 0-1
        * round returns a tuple(X, Y, Z) where the values are integers in range 0-100
        * direct returns a tuple(X, Y, Z) where the values are floats in range 0-100
        * In any invalid case the "direct" approach will be returned

    ### Return:
            tuple[int, int, int] | tuple[float, float, float]: X, Y, Z in range 0-100 or 0-1
    """
    # Check values integrity
    if isinstance(LAB, (tuple, list)) and len(LAB) == 1:
        LAB = LAB[0]
    if not 0 <= LAB[0] <= 100:
        raise ValueError("L* must be in range(0, 100)")
    for var in (LAB[1], LAB[2]):
        if not -128 <= var <= 128:
            raise ValueError("a and b must be in range(-128, 128)")

    # Refine arguments to be the correct type and form
    xyz_illuminant, observer = xyz.refine_args(illuminant=xyz_illuminant, observer=observer)
    lab_illuminant = next(xyz.refine_args(illuminant=lab_illuminant))

    # Calculate function of X, Y, Z. That's f(x), f(y), f(z)
    Y = (LAB[0] + 16) / 116
    X = LAB[1] / 500 + Y
    Z = Y - LAB[2] / 200
    # Reference: http://www.easyrgb.com/en/math.php
    X, Y, Z = [i**3 if i**3 > xyz.CIE_E else (i - 16 / 116) / 7.787 for i in (X, Y, Z)]

    # Alternative: http://brucelindbloom.com/
    # X = X ** 3 if X ** 3 > xyz.CIE_E else (116 * X - 16) / xyz.CIE_K
    # Y = ((LAB[0] + 16) / 116) ** 3 if LAB[0] > xyz.CIE_E * xyz.CIE_K else LAB[0] / xyz.CIE_K
    # Z = Z ** 3 if Z ** 3 > xyz.CIE_E else (116 * Z - 16) / xyz.CIE_K

    # Alternative 2: https://en.wikipedia.org/wiki/CIELAB_color_space#RGB_and_CMYK_conversions
    # X, Y, Z = [i**3 if i > 6/29 else 3 * (6/29)**2 * (i - 4/29) for i in (X, Fy, Z)]

    # Calculate reference white
    X, Y, Z = (val * xyz.ILLUMINANTS[observer][lab_illuminant][i] for i, val in enumerate((X, Y, Z)))

    # Do chromatic adaptation if the output illuminant or observer aren't the same as the ones of the matrix
    if xyz_illuminant != lab_illuminant:
        X, Y, Z = xyz.apply_chromatic_adaptation((X, Y, Z), lab_illuminant, xyz_illuminant, observer, adaptation)

    match output:
        case "round":
            return round(X*100), round(Y*100), round(Z*100)
        case "normalized":
            return X, Y, Z
        case _:
            return X*100, Y*100, Z*100


def xyz_to_yxy(
    *XYZ: int | float  | tuple | list,
    big_float: bool = True,
    output: Enum = Out3.DIRECT) -> tuple[int, int, int] | tuple[float, float, float]:
    """### Converts XYZ color to Yxy

    ### Args:
        `XYZ` (int, float, tuple, list): XYZ values in 3 consecutive int(0, 100), float(0, 100) or float(0, 1) or \
            list/tuple containing the same
        `big_float` (bool, optional): Wether the input XYZ values are floats in range 0-100. Defaults to True.
        `output` (str, optional): Either "normalized", "round" or "direct"
        * normalized returns a tuple(Y, x, y) where the values are floats in range 0-1
        * round returns a tuple(Y, x, y) where the values are integers in range 0-100
        * direct returns a tuple(Y, x, y) where the values are floats in range 0-100
        * In any invalid case the "direct" approach will be returned

    ### Returns:
        tuple[int, int, int] | tuple[float, float, float] : Yxy
    """
    # Watch out for black, where X=Y=Z=0. In that case, you may want to
    # set x and y to the chromaticity coordinates of your reference white
    X, Y, Z = ih.check_xyz(XYZ, big_float=big_float, normalized=True)
    x = X / (X + Y + Z)
    y = Y / (X + Y + Z)

    match output:
        case "round":
            return round(Y*100), round(x*100), round(y*100)
        case "normalized":
            return Y, x , y
        case _:
            return Y*100, x*100, y*100


def yxy_to_xyz(
    *Yxy: int | float | tuple | list,
    big_float: bool = True,
    output: Enum = Out3.DIRECT) -> tuple[int, int, int] | tuple[float, float, float]:
    """### Converts Yxy color to XYZ

    ### Args:
        `Yxy` (int, float, tuple, list): Yxy values in 3 consecutive int(0, 100), float(0, 100) or float(0, 1) or \
            list/tuple containing the same
        `big_float` (bool, optional): Wether the input Yxy values are floats in range 0-100. Defaults to True.
        `output` (str, optional): Either "normalized", "round" or "direct"
        * normalized returns a tuple(X, Y, Z) where the values are floats in range 0-1
        * round returns a tuple(X, Y, Z) where the values are integers in range 0-100
        * direct returns a tuple(X, Y, Z) where the values are floats in range 0-100
        * In any invalid case the "direct" approach will be returned

    ### Returns:
        tuple[int, int, int] | tuple[float, float, float] : XYZ
    """
    Y, x, y = ih.check_xyz(Yxy, big_float=big_float, normalized=True)
    X = x * (Y / y)
    Z = (1 - x - y) * (Y / y)

    match output:
        case "round":
            return round(X*100), round(Y*100), round(Z*100)
        case "normalized":
            return X, Y, Z
        case _:
            return X*100, Y*100, Z*100


def rgb_to_cmyk(*color: int| float | str | tuple | list, normalized: bool = False
                ) -> tuple[int, int, int] | tuple[float, float, float]:
    """### Takes a color and returns its CMYK (Cyan, Magenta, Yellow, Key) representation

    #### This function only calculates the CMYK in D65 illuminant. The result doesn't match Photoshop's \
        output because Photoshop uses D50 illuminant in the conversion

    ### Args:
        `color` (int | float | str | tuple | list): String "c0ffee", "#decaff", consecutive values either \
                int in range 0-255 or float in range 0-1 or an RGB list/tuple(R, G, B) with the same values
        `normalized` (bool, optional): Returns the values in float range 0-1 instead of the default int range 0-100

    ### Returns:
        tuple[int, int, int] | tuple[float, float, float]: Cyan, Magenta, Yellow, Key
    """
    # Check color integrity
    R, G, B = ih.check_color(color, normalized=True)

    # Calculate the black key
    K = 1 - max(R, G, B)

    # Calculate the cyan
    C = (1 - R - K) / (1 - K)

    # Calculate the magenta
    M = (1 - G - K) / (1 - K)

    # Calculate the yellow
    Y = (1 - B - K) / (1 - K)

    return (C, M, Y, K) if normalized else [round(i * 100) for i in (C, M, Y, K)]


def cmyk_to_rgb(*CMYK: int | float | tuple | list, output: Enum = Out1.ROUND):
    """### Converts CMYK to RGB values

    #### This function only calculates the CMYK in D65 illuminant. The result doesn't match Photoshop's
        output because Photoshop uses D50 illuminant in the conversion

    ### Args:
        `CMYK` (int | float | tuple | list): Consecutive values either int in range 0-100 or float in range 0-1 \
            or a CMYK list/tuple(C, M, Y, K) with the same values.
        `output` (str, optional): Either "hex", "hexp", "normalized", "round" or "direct"
        *     hex returns a hex string color in the form of dec0de
        *     hexp returns a hex string color in the form of #0ff1ce
        *     normalized returns a tuple(R, G, B) where the values are floats in range 0-1
        *     round returns a tuple(R, G, B) where the values are integers in range 0-255
        *     direct returns a tuple(R, G, B) where the values are floats in range 0-255
        *     In any invalid case the "direct" approach will be used

    ### Returns:
        str | tuple[int, int, int] | tuple[float, float, float]: Red, Green, Blue
    """
    # Check values integrity
    if len(CMYK) == 1:
        CMYK = CMYK[0]
    elif len(CMYK) != 4:
        raise ValueError("Invalid CMYK input!")

    for elem in CMYK:
        if not isinstance(elem, (int, float)):
            raise TypeError("All elements should be either integers or floats!")

    # Normalized values
    C, M, Y, K = (i / 100 for i in CMYK)

    # Calculate R, G, B
    R = (1 - C) * (1 - K)
    G = (1 - M) * (1 - K)
    B = (1 - Y) * (1 - K)

    return ih.return_rgb((R, G, B), normalized_input=True, output=output)


def srgb_to_adobe_rgb(*color: int | float | str | tuple | list, output: Enum = Out1.ROUND):
    """### Takes an sRGB color and returns its Adobe RGB representation

    ### Args:
        `color` (int | float | str | tuple | list): String "decade", "#facade", consecutive values either \
                int in range 0-255 or float in range 0-1 or an RGB list/tuple(R, G, B) with the same values
        `illuminant` (str, optional): The iluminant of the output Adobe R, G, B color. Defaults to 'D65'
        `output` (str, optional): Either "hex", "hexp", "normalized", "round" or "direct"
        *     hex returns a hex string color in the form of c0ffed
        *     hexp returns a hex string color in the form of #dec1de
        *     normalized returns a tuple(R, G, B) where the values are floats in range 0-1
        *     round returns a tuple(R, G, B) where the values are integers in range 0-255
        *     direct returns a tuple(R, G, B) where the values are floats in range 0-255
        *     In any invalid case the "direct" approach will be used

    ### Returns:
        str | tuple[int, int, int] | tuple[float, float, float]: Red, Green, Blue
    """
    # Check color integrity
    R, G, B = ih.check_color(color, normalized=True)
    # Convert RGB color to XYZ
    X, Y, Z = rgb_to_xyz(R, G, B, illuminant="D65", observer="2", adaptation="bradford", output=Out3.NORMALIZED)

    # Generate a conversion matrix for Adobe RGB
    matrix = xyz.working_space_matrix("ADOBE RGB", "D65", "2", "bradford", to_xyz=False)
    """matrix = (   # Wikipedia                         # Lindbloom
        ( 2.04159, -0.56501, -0.34473),  #  2.0413690 -0.5649464 -0.3446944
        (-0.96924,  1.87597,  0.04156),  # -0.9692660  1.8760108  0.0415560
        ( 0.01344, -0.11836,  1.01517))  #  0.0134474 -0.1183897  1.0154096"""

    # Apply conversion matrix
    R, G, B = ((X * matrix[i][0]) + (Y * matrix[i][1]) + (Z * matrix[i][2]) for i in range(3))

    # Apply gamma to get Adobe RGB
    R, G, B = (i **  (1 / (563/256)) if i > 0 else 0 for i in (R, G, B))

    return ih.return_rgb((R, G, B), normalized_input=True, output=output)


def adobe_rgb_to_srgb(*color: int | float | str | tuple | list, output: Enum = Out1.HEX):
    """### Takes an Adobe RGB color and returns its sRGB representation

    ### Args:
        `color` (int | float | str | tuple | list): String "add1c7", "#effec7", consecutive values either \
                int in range 0-255 or float in range 0-1 or an RGB list/tuple(R, G, B) with the same values
        `output` (str, optional): Either "hex", "hexp", "normalized", "round" or "direct"
        *     hex returns a hex string color in the form of c0ffee
        *     hexp returns a hex string color in the form of #decaff
        *     normalized returns a tuple(R, G, B) where the values are floats in range 0-1
        *     round returns a tuple(R, G, B) where the values are integers in range 0-255
        *     direct returns a tuple(R, G, B) where the values are floats in range 0-255
        *     In any invalid case the "direct" approach will be used

    ### Returns:
        str | tuple[int, int, int] | tuple[float, float, float]: Red, Green, Blue
    """
    # Convert to X, Y, Z and then to sRGB
    X, Y, Z = adobe_rgb_to_xyz(*color, illuminant="D65", observer="2", adaptation="bradford", output=Out3.NORMALIZED)
    return xyz_to_rgb(X, Y, Z, output=output)


def adobe_rgb_to_xyz(
    *color: str | tuple | list,
    illuminant: str = "D65",
    observer: str | int | float = "2",
    adaptation: str = "bradford",
    output: Enum = Out3.DIRECT) -> tuple | str:
    """### Takes an Adobe RGB color and returns its XYZ representation

    ### Args:
        `color` (int | float | str | tuple | list): String "dec0de", "#0ff1ce", consecutive values either \
                int in range 0-255 or float in range 0-1 or an RGB list/tuple(R, G, B) with the same values
        `illuminant` (str, optional): The iluminant of the output XYZ color. Defaults to 'D65'
        `observer` (str | int | float): The observer angle for the illuminant of the XYZ values. Defaults to "2"
        `adaptation` (str): The adaptation method to be used for illuminant conversions. Defaults to "bradford"
        `output` (str, optional): Either "normalized", "round" or "direct"
        * normalized returns a tuple(X, Y, Z) where the values are floats in range 0-1
        * round returns a tuple(X, Y, Z) where the values are integers in range 0-100
        * direct returns a tuple(X, Y, Z) where the values are floats in range 0-100
        * In any invalid case the "direct" approach will be returned

    ### Returns:
        tuple[int, int, int] | tuple[float, float, float]: X, Y, Z in range 0-100 | 0-1
    """
    # Check color integrity
    R, G, B = ih.check_color(color, normalized=True)

    # Convert Adobe RGB to Linear RGB
    R, G, B = (i  ** (563/256) for i in (R, G, B))
    # Multiply by 100 to get actual XYZ values
    R, G, B = (i * 100 for i in (R, G, B))

    # Generate conversion matrix for Adobe RGB
    matrix = xyz.working_space_matrix("ADOBE RGB", illuminant, observer, adaptation)
    """matrix = (   # Wikipedia                      # Lindbloom
        (0.57667, 0.18556, 0.18823),  # 0.5767309  0.1855540  0.1881852
        (0.29734, 0.62736, 0.07529),  # 0.2973769  0.6273491  0.0752741
        (0.02703, 0.07069, 0.99134))  # 0.0270343  0.0706872  0.9911085"""

    # Apply conversiion matrix
    X, Y, Z = ((R * matrix[i][0]) + (G * matrix[i][1]) + (B * matrix[i][2]) for i in range(3))

    match output:
        case "round":
            return round(X), round(Y), round(Z)
        case "normalized":
            return X / 100, Y / 100, Z / 100
        case _:
            return X, Y, Z


def convert_range(value: int | float, old_range: tuple | list, new_range: tuple | list) -> int | float:
    """### This function converts a number that's in a given range to one in a new range

    ### Args:
        `value` (int | float): The number to be converted from one range to another
        `old_range` (tuple | list): A tuple of 2 elements. The first element is the minimum and the
            second one - the maximum value of the range you want to convert from.
        `new_range` (tuple | list): A tuple of 2 elements. The first element is the minimum and the
            second one - the maximum value of the range you want to convert to.

    ### Returns:
        int | float: The number in the new range

    ### Example:
        >>> convert_range(10000, (-16000, 16000), (0, 100))
        81.25
    """
    old_min, old_max = min(old_range), max(old_range)
    new_min, new_max = min(new_range), max(new_range)
    old_delta = old_max - old_min
    new_delta = new_max - new_min
    if old_delta == 0 or new_delta == 0:
        raise ValueError("Neither range can be 0!")

    return (((value - old_min) * new_delta) / old_delta) + new_min


def rgb_to_ycbcr(*color, output: Enum = Out3.ROUND):
    """
    Reference https://en.wikipedia.org/wiki/YCbCr
    """
    WEIGHTS = {
        "ITU-R BT.601": (0.299, 0.114),
        "ITU-R BT.709": (0.2126, 0.0722),
        "ITU-R BT.2020": (0.2627, 0.0593),
        "ITU BT.470-6": (0.2220, 0.0713),
        "SMPTE-240M": (0.2122, 0.0865)}
    R, G, B = ih.check_color(color)

    if "ITU-R BT.601":
        Y = 16 + (65.738*R)/256 + (129.057*G)/256 + (25.064*B)/256
        Cb = 128 - (37.945*R)/256 - (74.494*G)/256 + (112.439*B)/256
        Cr = 128 + (112.439*R)/256 - (94.154*G)/256 - (18.285*B)/256

        # Using bitwise operators, below is an alternative calculation with integer output with nearest bitwise value output:
        # Y = 16 + (((R<<6) + (R<<1)+(G<<7) + G + (B<<4)+(B<<3) + B) >> 8)
        # Cb = 128 + ((-((R<<5) + (R<<2) + (R<<1)) - ((G<<6) + (G<<3)+ (G<<1)) + (B<<7) - (B<<4)) >> 8)
        # Cr = 128 + ((R<<7) - (R<<4) - (((G<<6) + (G<<5) - (G<<1)) - ((B<<4) + (B<<1))) >> 8)
    elif "ITU-R BT.709":
        matrix = ((0.2126, 0.7152, 0.0722), (-0.1146, -0.3854, 0.5), (0.5, -0.4542, -0.0458))
        Y, Cb, Cr = ((R * matrix[i][0]) + (G * matrix[i][1]) + (B * matrix[i][2]) for i in range(3))

    elif "SMPTE-240M":
        matrix = ((1, 0, 1.4746), (1, -0.16455312684366, -0.57135312684366), (1, 1.8814, 0))
        Y, Cb, Cr = ((R * matrix[i][0]) + (G * matrix[i][1]) + (B * matrix[i][2]) for i in range(3))


    match output:
        case "round":
            return round(Y), round(Cb), round(Cr)
        case "normalized":
            return Y/236, Cb/128, Cr/128
        case _:
            return Y, Cb, Cr


def ycbcr_to_rgb(*YCbCr, output:str = Out1.ROUND):
    """Reference https://en.wikipedia.org/wiki/YCbCr"""
    Y, Cb, Cr = YCbCr
    Kr, Kg, Kb = 0.299, 0.587, 0.114    # Constants

    R = (298.089*Y)/256 + (408.583*Cr)/256 - 222.921
    G = (298.082*Y)/256 - (100.291*Cb)/256 - (208.120*Cr)/256 + 135.576
    B = (298.082*Y)/256 + (516.412*Cb)/256 - 276.836

    # Alternative directly from ITU-R BT.601 without any roundings:
    # R = 255/219 * (Y - 16) + 255/224 * 1.402 * (Cr - 128)
    # G = 255/219 * (Y - 16) - 255/224 * 1.772 * (Kb/Kg) * (Cb - 128) - 255/224 * 1.402 * (Kr/Kg) * (Cr - 128)
    # B = 255/219 * (Y - 16) + 255/224 * 1.772 * (Cb - 128)

    # For Rec. 709 the constants are different
    # Kr = 0.2126
    # Kb = 0.0722
    # Kg = 1 - Kb - Kr = 0.7152
    # R, G, B = numpy.array((1, 0, 1.5748), (1, -0.1873, -0.4681), (1, 1.8556, 0)) @ (Y, Cb, Cr)






WEIGHTS = {
    "ITU-R BT.601": (0.299, 0.114),
    "ITU-R BT.709": (0.2126, 0.0722),
    "ITU-R BT.2020": (0.2627, 0.0593),
    "ITU BT.470-6": (0.2220, 0.0713),
    "SMPTE-240M": (0.2122, 0.0865)}

def RGB_to_YCbCr(
    *color,
    K = WEIGHTS["ITU-R BT.709"],
    in_depth: int = 10,
    in_legal: bool = False,
    out_depth: int = 8,
    out_legal: bool = True,
    clamp: bool = True,
    output: Enum = Out3.ROUND,
    **kwargs) -> tuple:
    """
    Convert an RGB color the corresponding Y'CbCr colour encoding values.

    Parameters
    ----------
    RGB
        Input *R'G'B'* array of floats or integer values.
    K
        Luma weighting coefficients of red and blue. See
        :attr:`colour.WEIGHTS_YCBCR` for presets. Default is
        *(0.2126, 0.0722)*, the weightings for *ITU-R BT.709*.
    in_bits
        Bit depth for integer input, or used in the calculation of the
        denominator for legal range float values, i.e. 8-bit means the float
        value for legal white is *235 / 255*. Default is *10*.
    in_legal
        Whether to treat the input values as legal range. Default is *False*.
    in_int
        Whether to treat the input values as ``in_bits`` integer code values.
        Default is *False*.
    out_bits
        Bit depth for integer output, or used in the calculation of the
        denominator for legal range float values, i.e. 8-bit means the float
        value for legal white is *235 / 255*. Ignored if ``out_legal`` and
        ``out_int`` are both *False*. Default is *8*.
    out_legal
        Whether to return legal range values. Default is *True*.
    out_int
        Whether to return values as ``out_bits`` integer code values. Default
        is *False*.
    clamp_int
        Whether to clamp integer output to allowable range for ``out_bits``.
        Default is *True*.

    Other Parameters
    ----------------
    in_range
        Array overriding the computed range such as
        *in_range = (RGB_min, RGB_max)*. If ``in_range`` is undefined,
        *RGB_min* and *RGB_max* will be computed using :func:`colour.CV_range`
        definition.
    out_range
        Array overriding the computed range such as
        *out_range = (Y_min, Y_max, C_min, C_max)`. If ``out_range`` is
        undefined, *Y_min*, *Y_max*, *C_min* and *C_max* will be computed
        using :func:`colour.models.rgb.ycbcr.ranges_YCbCr` definition.

    Returns
    -------
    :class:`numpy.ndarray`
        *Y'CbCr* colour encoding array of integer or float values.

    Warnings
    --------
    For *Recommendation ITU-R BT.2020*, :func:`colour.RGB_to_YCbCr` definition
    is only applicable to the non-constant luminance implementation.
    :func:`colour.RGB_to_YcCbcCrc` definition should be used for the constant
    luminance case as per :cite:`InternationalTelecommunicationUnion2015h`.

    Notes
    -----
    +----------------+-----------------------+---------------+
    | **Domain \\***  | **Scale - Reference** | **Scale - 1** |
    +================+=======================+===============+
    | ``RGB``        | [0, 1]                | [0, 1]        |
    +----------------+-----------------------+---------------+

    +----------------+-----------------------+---------------+
    | **Range \\***   | **Scale - Reference** | **Scale - 1** |
    +================+=======================+===============+
    | ``YCbCr``      | [0, 1]                | [0, 1]        |
    +----------------+-----------------------+---------------+

    \\* This definition has input and output integer switches, thus the
    domain-range scale information is only given for the floating point mode.

    -   The default arguments, ``**{'in_bits': 10, 'in_legal': False,
        'in_int': False, 'out_bits': 8, 'out_legal': True, 'out_int': False}``
        transform a float *R'G'B'* input array normalised to domain [0, 1]
        (``in_bits`` is ignored) to a float *Y'CbCr* output array where *Y'* is
        normalised to range [16 / 255, 235 / 255] and *Cb* and *Cr* are
        normalised to range [16 / 255, 240./255]. The float values are
        calculated based on an [0, 255] integer range, but no 8-bit
        quantisation or clamping are performed.

    References
    ----------
    :cite:`InternationalTelecommunicationUnion2011e`,
    :cite:`InternationalTelecommunicationUnion2015i`,
    :cite:`SocietyofMotionPictureandTelevisionEngineers1999b`,
    :cite:`Wikipedia2004d`

    Examples
    --------
    >>> RGB = np.array([1.0, 1.0, 1.0])
    >>> RGB_to_YCbCr(RGB)  # doctest: +ELLIPSIS
    array([ 0.9215686...,  0.5019607...,  0.5019607...])

    Matching the float output of *The Foundry Nuke*'s *Colorspace* node set to
    *YCbCr*:

    >>> RGB_to_YCbCr(
    ...     RGB, out_range=(16 / 255, 235 / 255, 15.5 / 255, 239.5 / 255)
    ... )
    ... # doctest: +ELLIPSIS
    array([ 0.9215686...,  0.5       ,  0.5       ])

    Matching the float output of *The Foundry Nuke*'s *Colorspace* node set to
    *YPbPr*:

    >>> RGB_to_YCbCr(RGB, out_legal=False, out_int=False)
    ... # doctest: +ELLIPSIS
    array([ 1.,  0.,  0.])

    Creating integer code values as per standard *10-bit SDI*:

    >>> RGB_to_YCbCr(RGB, out_legal=True, out_bits=10, out_int=True)
    ... # doctest: +ELLIPSIS
    array([940, 512, 512]...)

    For *JFIF JPEG* conversion as per *Recommendation ITU-T T.871*

    >>> RGB = np.array([102, 0, 51])
    >>> RGB_to_YCbCr(
    ...     RGB,
    ...     K=WEIGHTS_YCBCR["ITU-R BT.601"],
    ...     in_range=(0, 255),
    ...     out_range=(0, 255, 0.5, 255.5),
    ...     out_int=True,
    ... )
    ... # doctest: +ELLIPSIS
    array([ 36, 136, 175]...)

    Note the use of [0.5, 255.5] for the *Cb / Cr* range, which is required so
    that the *Cb* and *Cr* output is centered about 128. Using 255 centres it
    about 127.5, meaning that there is no integer code value to represent
    achromatic colours. This does however create the possibility of output
    integer codes with value of 256, which cannot be stored in 8-bit integer
    representation. *Recommendation ITU-T T.871* specifies these should be
    clamped to 255, which is applied with the default ``clamp_int=True``.

    These *JFIF JPEG* ranges are also obtained as follows:

    >>> RGB_to_YCbCr(
    ...     RGB,
    ...     K=WEIGHTS_YCBCR["ITU-R BT.601"],
    ...     in_bits=8,
    ...     in_int=True,
    ...     out_legal=False,
    ...     out_int=True,
    ... )
    ... # doctest: +ELLIPSIS
    array([ 36, 136, 175]...)
    """

    R, G, B = ih.check_color(color, normalized=True)
    max_value = 2**out_depth-1

    # Compared to the colour science library, if there we use the in_int=True argument, then here in
    # the in_scope calculation for legal range, we need to divide by 2**out_depth - 1 instead
    Kr, Kb, Kg = *K, 1 - K[0] - K[1]
    in_scope = (i * 2**(in_depth - 8) / (2**in_depth - 1) for i in (16, 235)) if in_legal else (0, 1)
    out_scope = tuple((i * 2 ** (out_depth - 8)) / max_value for i in (16, 235, 16, 240)) if out_legal else (0, 1, -0.5, 0.5)

    RGB_min, RGB_max = kwargs.get("in_range", in_scope)
    Y_min, Y_max, C_min, C_max = kwargs.get("out_range", out_scope)

    R, G, B = ((i - RGB_min) * 1 / (RGB_max - RGB_min) for i in (R, G, B))

    Y = Kr * R + Kg * G + Kb * B
    Cb = (0.5 * (B - Y) / (1 - Kb)) * (C_max - C_min) + (C_max + C_min) / 2
    Cr = (0.5 * (R - Y) / (1 - Kr)) * (C_max - C_min) + (C_max + C_min) / 2
    Y = Y * (Y_max - Y_min) + Y_min

    match output:
        case "normalized":
            return Y, Cb, Cr
        case "round":
            res = [round(Y*max_value), round(Cb*max_value), round(Cr*max_value)]
            if not out_legal:
                res[1], res[2] = round(Cb*max_value + (max_value + 1)/2), round(Cr*max_value + (max_value + 1)/2)
        case _:
            res = [Y*max_value, Cb*max_value, Cr*max_value]
            if not out_legal:
                res[1], res[2] = Cb*max_value + (max_value + 1)/2, Cr*max_value + (max_value + 1)/2
    return [max(min(max_value, i), 0) for i in res] if clamp else res
