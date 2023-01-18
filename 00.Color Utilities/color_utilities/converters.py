"""A collection of useful functions for converting colors between different types,
color representation, bit depth, color spaces, etc."""
# pylint: disable=invalid-name, unpacking-non-sequence, pointless-string-statement, too-many-lines

from . import internal_helpers as ih
from . import color_utils as cu
from . import xyz


def hex_to_rgb(color: str, *, depth: int | float = 8, normalized: bool = False) -> list:
    """### Converts a hex color to RGB values
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `color` (str): A hex color in the form "c0ffee" or "#decaff"
        `depth` (int | float): The bit depth of the input RGB values. Defaults to 8-bit (range 0-255)
        `normalized` (bool, optional): True will return values in range 0-1. Defaults to False.

    ### Returns:
        list: (R, G, B) either in range 0-1 or 0-255
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


def rgb_to_hex(*color: int | float | tuple | list | str, depth: int | float = 8, pound: bool = True):
    """### Converts RGB values to a hexadecimal color string representation
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `color` (int | float | str | tuple | list): String "dec0de", "#0ff1ce", consecutive values either
                int in range 0-255 or float in range 0-1 or an RGB list/tuple(R, G, B) with the same values
            N/B: If a color is passed as a hex in a string form, the result will be the same string
        `depth` (int | float): The bit depth of the input RGB values. Defaults to 8-bit (range 0-255)
        `pound` (bool): Wether to return the result with a pound sign prefix "#decade" instead of just "facade"

    ### Returns:
        str: Hex string in either `c0ffed` | `#dec1de` form
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


def rgb_to_hsl(*color: int | float | str | tuple | list, depth: int = 8, output: str = "round"):
    """### Takes an RGB color and returns its HSL (Hue, Saturation, Luminance) representation
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `color` (int | float | str | tuple | list): String "add1c7", "#effec7", consecutive values either
                int in range 0-255 or float in range 0-1 or an RGB list/tuple(R, G, B) with the same values
        `depth` (int | float): The bit depth of the input RGB values. Defaults to 8-bit (range 0-255)
        `output` (str, optional): Either "normalized", "half-normalized", "round" or "direct"
        *     normalized returns a tuple(H, S, L) where the values are floats in range 0-1
        *     half-normalized returns a tuple(H, S, L) where the values are H in range 0-359, SL in range 0-1
        *     round returns a tuple(H, S, L) where the values are integers. H in range 0-359, SL in range 0-100
        *     direct returns a tuple(H, S, L) where the values are floats in range 0-100
        *     In any invalid case the "direct" approach will be used

    #### N/B: Don't use round output if the output color is going to be used to further conversion!

    ### Returns:
        tuple: (H, S, L)
    """
    # Check color integrity
    R, G, B = ih.check_color(color, normalized=True, depth=depth)

    # Get the minimum and maximum of the channels and their sum and delta
    Cmax = max(R, G, B)
    Cmin = min(R, G, B)
    sum_ = Cmax + Cmin
    delta = Cmax - Cmin

    # Find Lightness
    L = (sum_ / 2)

    # If all elements have the same values, then the color is in the grayscale
    if Cmin == Cmax:
        match output:
            case "round":
                return 0, 0, round(L * 100)
            case "normalized":
                return 0, 0, L
            case _:
                return 0, 0, L * 100

    # Find Saturation and Hue
    S = 0 if delta == 0 else (delta / (1 - abs(2 * L - 1)))
    H = cu.get_hue(R, G, B, output="normalized")

    match output:
        case "round":
            return round(H * 360), round(S * 100), round(L * 100)
        case "normalized":
            return H, S , L
        case _:
            return H * 360, S * 100, L * 100


def rgb_to_hls(*color: int | float | str | tuple | list, depth: int = 8, output: str = "round") -> tuple:
    """### Takes an RGB color and returns its HLS (Hue, Luminance, Saturation) representation
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `color` (int | float| str | tuple | list): String "c0ffee", "#decaff", consecutive values either
                int in range 0-255 or float in range 0-1 or an RGB list/tuple(R, G, B) with the same values
        `depth` (int | float): The bit depth of the input RGB values. Defaults to 8-bit (range 0-255)

        `output` (str, optional): Either "normalized", "round" or "direct"
        *     normalized returns a tuple(H, L, S) where the values are floats in range 0-1
        *     half-normalized returns a tuple(H, S, L) where the values are H in range 0-359, SL in range 0-1
        *     round returns a tuple(H, L, S) where the values are integers. H in range 0-359, LS in range 0-100
        *     direct returns a tuple(H, L, S) where the values are floats in range 0-100
        *     In any invalid case the "direct" approach will be used

    #### N/B: Don't use round output if the output color is going to be used to further conversion!

    ### Returns:
        tuple: (H, L, S)
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
            case "round":
                return 0, round(L * 100), 0
            case "normalized":
                return 0, L, 0
            case _:
                return 0, L * 100, 0

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

    match output:
        case "round":
            return round(H * 360), round(L * 100), round(S * 100)
        case "normalized":
            return H, L, S
        case _:
            return H * 360, L * 100, S * 100


def hls_to_rgb(*HLS: int | float | tuple | list, depth: int = 8, output="round"):
    """### Converts HLS values to RGB
    Reference: https://en.wikipedia.org/wiki/HSL_and_HSV#HSL_to_RGB

    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `HLS` (int | float | tuple | list): Hue, Lightness, Saturation in either int range H 0-360, LS range 0-100
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
        str | tuple[int, int, int] | tuple[float, float, float]: RGB
    """
    if depth % 1 != 0:
        raise ValueError("Depth value must be an integer number passed either as int or float")

    # Check values integrity
    H, L, S = ih.check_hsw(HLS, output="normalized")

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


def hsl_to_rgb(*HSL: int | float | tuple | list, depth: int = 8, output: str = "round") -> tuple[int, int, int]:
    """### Converts HSL values to RGB
    #### Reference: https://en.wikipedia.org/wiki/HSL_and_HSV

    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `HSL` (int | float | tuple | list): hue, saturation, lightness either in int H range 0-359, SL range 0-100
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
        str | tuple[int, int, int] | tuple[float, float, float]: RGB
    """
    if depth % 1 != 0:
        raise ValueError("Depth value must be an integer number passed either as int or float")

    # Check values integrity
    H, S, L = ih.check_hsw(HSL, output="half-normalized")

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


def rgb_to_hsv(
    *color: int | float | str | tuple | list,
    depth: int = 8,
    output: str = "round") -> tuple[int, int, int] | tuple[float, float, float]:
    """### Takes an RGB color and returns its HSV (Travis) representation
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `color` (int | float| str | tuple | list): String "add1c7", "#effec7", consecutive values either
                int in range 0-255 or float in range 0-1 or an RGB list/tuple(R, G, B) with the same values
        `depth` (int | float): The bit depth of the input RGB values. Defaults to 8-bit (range 0-255)
        `output` (str, optional): Either "normalized", "round" or "direct"
        *     normalized returns a tuple(H, S, V) where the values are floats in range 0-1
        *     half-normalized returns a tuple(H, S, V) where the values are H in range 0-359, SV in range 0-1
        *     round returns a tuple(H, S, V) where the values are integers. H in range 0-359, SV in range 0-100
        *     direct returns a tuple(H, S, V) where the values are floats in range 0-100
        *     In any invalid case the "direct" approach will be returned

    #### N/B: Don't use round output if the output color is going to be used to further conversion!

    Returns:
        tuple: Hue, Saturation, Value
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
            case "round":
                return 0, 0, round(V)
            case "normalized":
                return 0, 0, V / 100
            case _:
                return 0, 0, V

    # Find Hue
    H = cu.get_hue(R, G, B)

    # H (degrees), S (%), V (%)
    return ih.return_hsw((H, S, V), output=output)


def hsv_to_rgb(*HSV: int | float | tuple | list, depth: int = 8, output: str = "round"):
    """### Converts HSV values to RGB
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `HSV` (int | float | tuple | list): Hue, Saturation, Value either H in int range 0-360, SV range 0-100,
            float range 0-1 or H in int range 0-359, SV in float range 0-1 or a tuple/list with the same values
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
        str | tuple[int, int, int] | tuple[float, float, float]: RGB
    """
    if depth % 1 != 0:
        raise ValueError("Depth value must be an integer number passed either as int or float")

    # Check lavues integrity
    H, S, V = ih.check_hsw(HSV, output="normalized")

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

    return ih.return_rgb((R, G, B), normalized_input=True, output=output)


def hsv_to_hsl(*HSV: int | float | tuple | list, output: str = "round"):
    """### Convert HSV values to HSL
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `HSV` (int | float | tuple | list): Hue, Saturation, Value either H in int range 0-359, SV range 0-100
                                    or float range 0-1 or a tuple/list with the same values
        `output` (str, optional): Either "normalized", "half-normalized", "round" or "direct"
        *     normalized returns a tuple(H, S, L) where the values are floats in range 0-1
        *     half-normalized returns a tuple(H, S, L) where the values are H in range 0-359, SL in range 0-1
        *     round returns a tuple(H, S, L) where the values are integers. H in range 0-359, SL in range 0-100
        *     direct returns a tuple(H, S, L) where the values are floats in range 0-100
        *     In any invalid case the "direct" approach will be used

    #### N/B: Don't use round output if the output color is going to be used to further conversion!

    ### Returns:
        tuple: Hue Saturation Lightness
    """
    # Check values integrity
    H, S, V = ih.check_hsw(HSV, output="normalized")

    # Find Lightness
    L = ((1/2) * V) * (2 - S)
    # Find Saturation for HSL using Saturation from HSV
    S = (V * S) / (1 - abs(2 * L - 1))

    return ih.return_hsw((H, S, L), normalized_input=True, output=output)


def hsl_to_hsv(*HSL: int | float | tuple | list, output: str = "round"):
    """### Convert HSL to HSV values
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `HSL` (int | float | tuple | list): Hue, Saturation, Lightness either H in int range 0-359, SL range 0-100
                                    or float range 0-1 or a tuple/list with the same values
        `output` (str, optional): Either "normalized", "half-normalized", "round" or "direct"
        *     normalized returns a tuple(H, S, V) where the values are floats in range 0-1
        *     half-normalized returns a tuple(H, S, V) where the values are H in range 0-359, SV in range 0-1
        *     round returns a tuple(H, S, V) where the values are integers. H in range 0-359, SV in range 0-100
        *     direct returns a tuple(H, S, V) where the values are floats in range 0-100
        *     In any invalid case the "direct" approach will be returned

    #### N/B: Don't use round output if the output color is going to be used to further conversion!

    Returns:
        tuple: Hue Saturation Value
    """
    # Check values integrity
    H, S, L = ih.check_hsw(HSL, output="normalized")

    # Find Value
    V = ((2 * L) + S * (1 - abs(2 * L - 1))) / 2
    # Find Saturation for HSV using Saturation from HSL
    S = (2 * (V - L)) / V

    return ih.return_hsw((H, S, V), normalized_input=True, output=output)


def rgb_to_hsi(*color: int | float | str | tuple | list, depth: int = 8, output: str = "round"):
    """### Takes an RGB color and returns its HSI (Hue Saturation Intensity) representation
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `color` (int | float| str | tuple | list): String "add1c7", "#effec7", consecutive values either
                int in range 0-255 or float in range 0-1 or an RGB list/tuple(R, G, B) with the same values
        `depth` (int | float): The bit depth of the input RGB values. Defaults to 8-bit (range 0-255)
        `output` (str, optional): Either "normalized", "round" or "direct"
        *     normalized returns a tuple(H, S, I) where the values are floats in range 0-1
        *     half-normalized returns a tuple(H, S, I) where the values are H in range 0-359, SI in range 0-1
        *     round returns a tuple(H, S, I) where the values are integers. H in range 0-359, SI in range 0-100
        *     direct returns a tuple(H, S, I) where the values are floats in range 0-100
        *     In any invalid case the "direct" approach will be returned

    #### N/B: Don't use round output if the output color is going to be used to further conversion!

    Returns:
        tuple: Hue, Saturation, Intensity
    """
    # Check color integrity
    R, G, B = ih.check_color(color, normalized=True, depth=depth)

    # Find Hue, Saturation, Intensity
    I = (R + G + B) / 3
    S = 1 - 3 / (R + G + B) * min(R, G, B) if I > 0 else 0
    H = cu.get_hue(R, G, B, depth=depth, output="normalized")

    return ih.return_hsw((H, S, I), normalized_input=True, output=output)


def hsi_to_rgb(*HSI, depth: int = 8, output: str = "round"):
    """### Converts HSI values to RGB
    #### Reference: https://en.wikipedia.org/wiki/HSL_and_HSV#HSI_to_RGB

    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `HSI` (int | float | tuple): Hue, Saturation, Intensity either H in int range 0-359, SL range 0-100
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
        str | tuple[int, int, int] | tuple[float, float, float]: RGB
    """
    if depth % 1 != 0:
        raise ValueError("Depth value must be an integer number passed either as int or float")

    # Check values integrity
    H, S, I = ih.check_hsw(HSI, output="normalized")

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


def rgb_to_xyz(
    *color: str | tuple | list,
    illuminant: str = "D65",
    observer: int | float | str = "2",
    adaptation: str = "bradford",
    output: str = "round"):
    """### Takes an 8-bit sRGB color and returns its XYZ values (where Y is Luminance)

    ### Args:
        `color` (str | tuple | list): String "add1c7", "#effec7", consecutive values either
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
    R, G, B = convert_to_linear((R, G, B), "SRGB")

    # Get the conversion matrix for sRGB, D65 illuminant, 2 degrees observer angle
    matrix = xyz.color_space_props["SRGB"]["override_matrix"]["D65"]["to_xyz"]

    # Get the dot product of the matrix and the RGB colors
    X, Y, Z = ((R * matrix[i][0]) + (G * matrix[i][1]) + (B * matrix[i][2]) for i in range(3))

    # Do chromatic adaptation if the output illuminant or observer aren't the same as the ones of the matrix
    if illuminant != "D65" or observer != "2":
        X, Y, Z = xyz.apply_chromatic_adaptation((X, Y, Z), orig_illum="D65", targ_illum=illuminant, observer=observer, adaptation=adaptation)

    match output:
        case "round":
            return round(X), round(Y), round(Z)
        case "normalized":
            return X / 100, Y / 100, Z / 100
        case _:
            return X, Y, Z


def rgb_to_xyz_alt(
    *color: str | tuple | list,
    illuminant: str = "D65",
    observer: str | int | int = "2",
    adaptation: str = "bradford",
    color_space: str = "sRGB",
    output: str = "round"):
    """### Takes an 8-bit sRGB color and returns its XYZ values (where Y is Luminance)

    #### This is an alternative way to convert from sRGB to XYZ color. The output of both methods \
        is roughly the same. It's the input that's different. The original function assumes the \
            input color is in sRGB space. This one allows for specifying a different input color space.

    ### Args:
        `color` (str | tuple | list): String "add1c7", "#effec7", consecutive values either
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
    R, G, B = convert_to_linear((R, G, B), color_space)

    # Check if requested color space has an override matrix
    override_matrix = xyz.color_space_props[color_space].get("override_matrix")
    if override_matrix and override_matrix.get(illuminant):
        matrix = override_matrix[illuminant]["to_xyz"]
    else:
        # Generate a conversion matrix if no override matrix exists
        matrix = xyz.working_space_matrix(color_space, illuminant, observer, adaptation)

    X, Y, Z = ((R * matrix[i][0]) + (G * matrix[i][1]) + (B * matrix[i][2]) for i in range(3))

    match output:
        case "round":
            return round(X), round(Y), round(Z)
        case "normalized":
            return X / 100, Y / 100, Z / 100
        case _:
            return X, Y, Z


def xyz_to_rgb(
    *XYZ: int | float | tuple | list,
    big_float: bool = True,
    illuminant: str = "D65",
    observer: str | int | float = "2",
    adaptation: str = "bradford",
    output: str = "round") -> tuple:
    """### Takes XYZ color and returns its sRGB values

    ### Args:
        `XYZ` (int, float, tuple, list): XYZ value in 3 consecutive int(0, 100), float(0, 100) or float(0, 1) or
            list/tuple containing the same
        `big_float` (bool, optional): Wether the input XYZ values are floats in range 0-100. Defaults to True.
        `illuminant` (str, optional): The iluminant of the input XYZ color. Defaults to 'D65'
        `observer` (int[2 | 10] | str, optional): The observer viewing angle - 2° (CIE 1931) or 10° (CIE 1964). Defaults to None (2).
        `adaptation` (str): The adaptation method to be used for illuminant conversions. Defaults to "bradford"
        `output` (str, optional): Either "hex", "hexp", "normalized", "round" or "direct"
        *     hex returns a hex string color in the form of decade
        *     hexp returns a hex string color in the form of #facade
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
        str | tuple[int, int, int] | tuple[float, float, float]: RGB
    """
    # Refine arguments to be the correct type and form
    illuminant, observer, adaptation = xyz.refine_args(
        illuminant=illuminant, observer=observer, adaptation=adaptation)

    # Check values integrity
    X, Y, Z = ih.check_xyz(XYZ, normalized=True, big_float=big_float)

    # Check if requested color space has an override matrix
    override_matrix = xyz.color_space_props["SRGB"]["override_matrix"].get(illuminant)

    # Generate a conversion matrix if no override matrix exists
    matrix = override_matrix["to_rgb"] if override_matrix \
        else xyz.working_space_matrix("SRGB", illuminant, observer, adaptation, to_xyz=False)

    # Get the conversion matrix
    R, G, B = ((X * matrix[i][0]) + (Y * matrix[i][1]) + (Z * matrix[i][2]) for i in range(3))

    # Apply gamma
    R, G, B = convert_linear_to((R, G, B), "SRGB")

    return ih.return_rgb((R, G, B), normalized_input=True, output=output)


def xyz_to_rgb_alt(
    *XYZ: int | float | tuple | list,
    big_float: bool = True,
    illuminant: str = "D65",
    observer: int | float | str = "2",
    adaptation="bradford",
    color_space: str = "sRGB",
    output: str = "round") -> tuple:
    """### Takes XYZ color and returns its RGB values in the requested color space

    #### This is an alternative way to convert from XYZ to RGB color. The output of both methods \
        is roughly the same. It's the input that's different. The original function assumes the \
            output color is in sRGB space. This one allows for specifying a different input color space.

    ### Args:
        `XYZ` (int, float, tuple, list): XYZ value in 3 consecutive int(0, 100), float(0, 100) or float(0, 1) or
            list/tuple containing the same
        `big_float` (bool, optional): Wether the input XYZ values are floats in range 0-100. Defaults to True.
        `illuminant` (str, optional): The iluminant of the input XYZ color. Defaults to 'D65'
        `observer` (int[2 | 10] | str, optional): The observer viewing angle - 2° (CIE 1931) or 10° (CIE 1964). Defaults to None (2).
        `adaptation` (str): The adaptation method to be used for illuminant conversions. Defaults to "bradford"
        `color_space` (str, optional): The target color space in which the XYZ color will be converted. Defaults to sRGB.
        `output` (str, optional): Either "hex", "hexp", "normalized", "round" or "direct"
        *     hex returns a hex string color in the form of decade
        *     hexp returns a hex string color in the form of #facade
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
        str | tuple[int, int, int] | tuple[float, float, float]: RGB
    """
    # Refine arguments to be the correct type and form
    illuminant, observer, color_space, adaptation, rgb_illum = xyz.refine_args(
        illuminant=illuminant, observer=observer, color_space=color_space, adaptation=adaptation)

    # Check values integrity
    X, Y, Z = ih.check_xyz(XYZ, normalized=True, big_float=big_float)

    # Do chromatic adaptation if the input illuminant or observer aren't the same as the ones of the color space's
    if rgb_illum != illuminant or observer != "2":
        X, Y, Z = xyz.apply_chromatic_adaptation((X, Y, Z), illuminant, rgb_illum, observer=observer, adaptation=adaptation)

    # Get the conversion matrix
    matrix = xyz.color_space_props["SRGB"]["override_matrix"]["D65"]["to_rgb"]

    # Apply matrix to the X, Y, Z values
    R, G, B = ((X * matrix[i][0]) + (Y * matrix[i][1]) + (Z * matrix[i][2]) for i in range(3))

    # Apply gamma
    R, G, B = convert_linear_to((R, G, B), color_space)

    return ih.return_rgb((R, G, B), normalized_input=True, output=output)


def xyz_to_lab(
    *XYZ: int | float | tuple | list,
    big_float : bool = True,
    xyz_illuminant: str = "D65",
    lab_illuminant: str = "D65",
    observer: str | int | float = "2",
    adaptation: str = "bradford",
    round_: bool = False):
    """### Takes XYZ color and returns its L*ab values

    ### Args:
        `XYZ` (int, float, tuple, list): XYZ color in 3 consecutive int(0, 100), float(0, 100) or float(0, 1) or
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
    X, Y, Z = (i ** (1/3) if i > xyz.CIE_E else ((xyz.CIE_K * X) + 16) / 116 for i in (X, Y, Z))
    # Alternative formula
    # X, Y, Z = (i ** (1/3) if i > xyz.CIE_E else (7.787 * X) + (16 / 116) for i in (X, Y, Z))
    # Alternative values
    # 7.787 is 841/108 or (1/3) * (29/6) ** 2 and 16 / 116 could be 4/29

    # Calculate L*ab based on functions
    L = (116 * Y) - 16
    A = 500 * (X - Y)
    B = 200 * (Y - Z)

    return (round(L), round(A), round(B)) if round_ else (L, A, B)


def lab_to_xyz(
    *LAB,
    lab_illuminant="D65",
    xyz_illuminant="D65",
    observer="2",
    adaptation: str = "bradford",
    output="direct"):
    """### Converts L*ab color ato XYZ.
    L* in range(0, 100), a in range(-128, 128)

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

    """
    # Check values integrity
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


def convert_to_linear(RGB: tuple | list, color_space: str, normalized: bool = False):
    """Takes R, G, B values and converts them to Linear R, G, B values based on their color space

    Args:
        RGB (tuple | list): The R, G, B values to be converted
        color_space (str): The color space that the R, G, B values are in
        normalized (bool, optional): Returns the output in range 0-1 instead of 0-100

    Returns:
        tuple[R, G, B]
    """
    if color_space == "SRGB":
        R, G, B = (((i + 0.055) / 1.055) ** 2.4 if i > 0.04045 else i / 12.92 for i in RGB)
    elif color_space == "PROPHOTO":
        R, G, B = (i ** 1.8 if i > 16 * (1/512) else i / 16 for i in RGB)
    elif color_space == "REC 2020":
        R, G, B = (i / 4.5 if abs(i) < xyz.BETA * 4.5 else ((abs(i) + xyz.ALPHA - 1) / xyz.ALPHA) ** 1 / 0.45 for i in RGB)
    elif xyz.color_space_props[color_space]["gamma"] == "L*":
        R, G, B = (((i + 0.16) / 1.16) ** 3 if i < 0.08 else (100 * i) / xyz.CIE_K for i in RGB)
    else:
        R, G, B = (i **  xyz.color_space_props[color_space]["gamma"] if i > 0 else 0 for i in RGB)

    return (R, G, B) if normalized else (R * 100, G * 100, B * 100)


def convert_linear_to(RGB, color_space):
    """Takes linear R, G, B values and applies gamma to them based on the desired color space

    Args:
        RGB (tuple | list): The R, G, B values to be converted
        color_space (str): The color space that the R, G, B will be converted to

    Returns:
        tuple[R, G, B]
    """
    # Apply gamma
    if color_space == "SRGB":
        R, G, B = (1.055 * (i ** (1 / 2.4)) - 0.055 if i > 0.0031308 else i * 12.92 for i in RGB)
    elif color_space == "PROPHOTO":
        R, G, B = (i ** (1/1.8) if i > (1/512) else 16 * i for i in RGB)
    elif color_space == "REC 2020":
        R, G, B = (4.5 * i if i < xyz.BETA else xyz.ALPHA * i ** 0.45 - (xyz.ALPHA - 1) for i in RGB)
    elif xyz.color_space_props[color_space]["gamma"] == "L*":
        R, G, B = (1.16 * i ** (1/3) if i > xyz.CIE_E else (i * xyz.CIE_K) / 100 for i in RGB)
    else:
        R, G, B = (i **  (1 / xyz.color_space_props[color_space]["gamma"]) if i > 0 else 0 for i in RGB)

    return R, G, B


#######################################################################
# From this point on the functions aren't documented
# They work, but will soon be reworked to be more flexible
#######################################################################

def rgb_to_cmyk(*color: str | tuple | list, normalized=False) -> tuple:
    """Takes a color and returns its CMYK (Cyan, Magenta, Yellow, Key) representation

    #### This function only calculates the CMYK in D65 illuminant. The result doesn't match Photoshop's
        output because Photoshop uses D50 illuminant in the conversion

    Args:
        normalized (bool, optional): Wether to return the values in float range 0-1 instead of the default int range 0-100

    Returns:
        tuple: CMYK
    """

    R, G, B = ih.check_color(color, normalized=True)

    # Calculate the black key
    K = 1 - max(R, G, B)

    # Calculate the cyan
    C = (1 - R - K) / (1 - K)

    # Calculate the magenta
    M = (1 - G - K) / (1 - K)

    # Calculate the yellow
    Y = (1 - B - K) / (1 - K)

    return (C, M, Y, K) if normalized else tuple(round(i * 100) for i in (C, M, Y, K))


def cmyk_to_rgb(*CMYK, normalized: bool = False):
    """Converts CMYK to RGB values"""

    if len(CMYK) == 1:
        CMYK = CMYK[0]
    elif len(CMYK) != 4:
        raise ValueError("Invalid CMYK input!")

    for elem in CMYK:
        if not isinstance(elem, (int, float)):
            raise TypeError("All elements should be either integers or floats!")

    C, M, Y, K = (i / 100 for i in CMYK)

    R = (1 - C) * (1 - K)
    G = (1 - M) * (1 - K)
    B = (1 - Y) * (1 - K)

    return (R, G, B) if normalized else (round(R * 255), round(G * 255), round(B * 255))


def srgb_to_adobe_rgb(
    *color: str | tuple | list,
    illuminant: str = "D65",
    observer: str | int | float = "2",
    adaptation: str = "bradford",
    output: str = "round") -> tuple:
    """Takes an sRGB color and returns its Adobe RGB representation

    Args:
        color
        illuminant
        observer
        adaptation
        output

    Returns:
        tuple: R, G, B
    """
    # Check color integrity
    R, G, B = ih.check_color(color, normalized=True)
    # Convert RGB color to XYZ
    X, Y, Z = rgb_to_xyz(R, G, B, illuminant="D65", observer="2", adaptation="bradford", output="normalized")

    # Generate a conversion matrix for Adobe RGB
    matrix = xyz.working_space_matrix("ADOBE RGB", illuminant, observer, adaptation, to_xyz=False)
    """matrix = (   # Wikipedia                         # Lindbloom
        ( 2.04159, -0.56501, -0.34473),  #  2.0413690 -0.5649464 -0.3446944
        (-0.96924,  1.87597,  0.04156),  # -0.9692660  1.8760108  0.0415560
        ( 0.01344, -0.11836,  1.01517))  #  0.0134474 -0.1183897  1.0154096"""

    R, G, B = ((X * matrix[i][0]) + (Y * matrix[i][1]) + (Z * matrix[i][2]) for i in range(3))
    # Apply gamma to get Adobe RGB
    R, G, B = (i **  (1 / xyz.color_space_props["ADOBE RGB"]["gamma"]) if i > 0 else 0 for i in (R, G, B))

    match output:
        case "round":
            return round(R * 255), round(G * 255), round(B * 255)
        case "normalized":
            return R, G, B
        case _:
            return R * 255, G * 255, B * 255


def adobe_rgb_to_xyz(
    *color: str | tuple | list,
    illuminant: str = "D65",
    observer: str | int | float = "2",
    adaptation: str = "bradford",
    round_: bool = True):
    """Takes an Adobe RGB color and returns its XYZ representation

    Args:
        color
        illuminant (str, optional): _description_. Defaults to "D65".
        observer (str | int | float, optional): _description_. Defaults to "2".
        adaptation (str, optional): _description_. Defaults to "bradford".
        round_ (bool, optional): _description_. Defaults to True.

    Returns:
        tuple: X, Y, Z
    """
    # Check color integrity
    R, G, B = ih.check_color(color, normalized=True)

    # Convert Adobe RGB to Linear RGB
    R, G, B = (i  ** xyz.color_space_props["ADOBE RGB"]["gamma"] for i in (R, G, B))
    # Multiply by 100 to get actual XYZ values
    R, G, B = (i * 100 for i in (R, G, B))

    # Generate conversion matrix for Adobe RGB
    matrix = xyz.working_space_matrix("ADOBE RGB", illuminant, observer, adaptation)
    """matrix = (   # Wikipedia                      # Lindbloom
        (0.57667, 0.18556, 0.18823),  # 0.5767309  0.1855540  0.1881852
        (0.29734, 0.62736, 0.07529),  # 0.2973769  0.6273491  0.0752741
        (0.02703, 0.07069, 0.99134))  # 0.0270343  0.0706872  0.9911085"""

    # Calculate XYZ
    X, Y, Z = ((R * matrix[i][0]) + (G * matrix[i][1]) + (B * matrix[i][2]) for i in range(3))

    return (round(X), round(Y), round(Z)) if round_ else (X, Y, Z)


def adobe_rgb_to_srgb(
    *color: str | tuple | list,
    illuminant: str = "D65",
    observer: str | int | float = "2",
    adaptation: str = "bradford",
    output: str = "hex") -> str | tuple:
    """Takes an Adobe RGB color and returns its sRGB representation

    Args:
        illuminant (str, optional): _description_. Defaults to "D65".
        observer (str | int | float, optional): _description_. Defaults to "2".
        adaptation (str, optional): _description_. Defaults to "bradford".
        output (str, optional): _description_. Defaults to "hex".

    Returns:
        str | tuple: _description_
    """
    X, Y, Z = adobe_rgb_to_xyz(*color, illuminant=illuminant, observer=observer, adaptation=adaptation, round_=False)
    return xyz_to_rgb(X, Y, Z, output=output)


def xyz_to_yxy(*XYZ):
    """TEST"""
    # Watch out for black, where X=Y=Z=0. In that case, you may want to set x and y to the chromaticity coordinates of your reference white
    X, Y, Z = XYZ
    x = X / (X + Y + Z)
    y = Y / (X + Y + Z)
    return Y, x, y


def yxy_to_xyz(*Yxy):
    """TEST"""
    Y, x, y = Yxy
    X = x * (Y / y)
    Z = (1 - x - y) * (Y / y)
    return X, Y, Z


def rgb_to_web_safe(*color):
    """TEST"""
    R, G, B = ih.check_color(color)
    R, G, B = (int(round((i / 255) * 5) * 51) for i in (R, G, B))

    return (R, G, B)



######################################################


def rgb_to_hsp(*color, apply_gamma=True, output="round"):
    """TEST"""
    # Source: http://alienryderflex.com/hsp.html
    R, G, B = ih.check_color(color, normalized=True)
    if apply_gamma:
        R, G, B = (((i + 0.055) / 1.055) ** 2.4 if i > 0.04045 else i / 12.92 for i in (R, G, B))

    P = (0.299 * R * R + 0.587 * G * G + 0.114 * B * B) ** 0.5

    if R == G == B:
        return 0, 0, P

    H = cu.get_hue(R, G, B, output="normalized")
    S = (max(R, G, B) - min(R, G, B)) / max(R, G, B)

    return ih.return_hsw((H, S, P), normalized_input=True, output=output)


def hsp_to_rgb(*HSP, apply_gamma=True, output="round"):
    """TEST"""
    # Source: http://alienryderflex.com/hsp.html
    H, S, P = ih.check_hsw(HSP, output="normalized")
    # ITU BT.601 / Rec. 601

    min_over_max = 1 - S
    Pr, Pg, Pb = 0.299, 0.587, 0.114

    if S < 1:
        if H < 1 / 6:  # R > G > B
            H = 6 * H
            part = 1 + H * (1 / min_over_max - 1)
            B = P / (Pr / min_over_max ** 2 + Pg * part ** 2 + Pb) ** 0.5
            R = B / min_over_max
            G = B + H * (R - B)
        elif H < 2 / 6:  # G > R > B
            H = 6 * (-H + 2 / 6)
            part = 1 + H * (1 / min_over_max - 1)
            B = P / (Pg / min_over_max **2 + Pr * part **2 + Pb) ** 0.5
            G = B / min_over_max
            R = B + H * (G - B)
        elif H < 3 / 6:  # G > B > R
            H = 6 * (H - 2 / 6)
            part = 1 + H * (1 / min_over_max - 1)
            R = P / (Pg / min_over_max **2 + Pb * part ** 2 + Pr) ** 0.5
            G = R / min_over_max
            B = R + H * (G - R)
        elif H < 4 / 6:  # B > G > R
            H = 6 * (-H + 4 / 6)
            part = 1 + H * (1 / min_over_max - 1)
            R = P / (Pb / min_over_max ** 2 + Pg * part ** 2 + Pr) ** 0.5
            B = R / min_over_max
            G = R + H * (B - R)
        elif H < 5 / 6:  # B > R > G
            H = 6 * ( H - 4 / 6)
            part = 1 + H * (1 / min_over_max - 1)
            G = P / (Pb / min_over_max ** 2 + Pr * part ** 2 + Pg) ** 0.5
            B = G / min_over_max
            R = G + H * (B - G)
        else:              # R > B > G
            H = 6 * (-H + 1)
            part = 1 + H * (1 / min_over_max - 1)
            G = P / (Pr / min_over_max ** 2 + Pb * part ** 2 + Pg) ** 0.5
            R = G / min_over_max
            B = G + H * (R - G)
    elif H < 1 / 6:  # R > G > B
        H = 6 * H
        R = (P ** 2 / (Pr + Pg * H ** 2)) ** 0.5
        G = R * H
        B = 0
    elif H < 2 / 6:  # G > R > B
        H = 6 * (-H + 2 / 6)
        G = (P ** 2 / (Pg + Pr * H ** 2)) ** 0.5
        R = G * H
        B = 0
    elif H < 3 / 6:  # G > B > R
        H = 6 * ( H - 2 / 6)
        G = (P ** 2 / (Pg + Pb * H ** 2)) ** 0.5
        B = G * H
        R = 0
    elif H < 4 / 6:  # B > G > R
        H = 6 * (-H + 4 / 6)
        B = (P ** 2 / (Pb + Pg * H ** 2)) ** 0.5
        G = B * H
        R = 0
    elif H < 5 / 6:  # B > R > G
        H = 6 * ( H - 4 / 6)
        B = (P ** 2 / (Pb + Pr * H ** 2)) ** 0.5
        R = B * H
        G = 0
    else:  # R > B > G
        H = 6 * (-H + 1)
        R = (P ** 2 / (Pr + Pb * H ** 2)) ** 0.5
        B = R * H
        G = 0
    if apply_gamma:
        R, G, B = (1.055 * (i ** (1 / 2.4)) - 0.055 if i > 0.0031308 else i * 12.92 for i in (R, G, B))

    return ih.return_rgb((R, G, B), normalized_input=True, output=output)
