"""A collection of useful functions for working with colors"""
# pylint: disable=invalid-name, unpacking-non-sequence, unsubscriptable-object
import random
from . import internal_helpers as ih
from . import converters as co


def get_color_brightness(
    *color: int | float | str | tuple | list,
    depth: int = 8,
    method: int = None,
    output: str = "direct") -> int | float:
    """### Get the brightness value of a color
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `color` (int | float | str | tuple | list): String "c0ffee", "#decaff", consecutive values either
                int in range 0-255 or float in range 0-1 or an RGB list/tuple(R, G, B) with the same values
        `depth` (int | float): The bit depth of the input RGB values. Defaults to 8-bit (range 0-255)
        `apply_gamma` (bool): Wether to apply gamma before calculation for accurate results. Defaults to True.
        `method` (int | None): If None, a dialog appears to ask which method should be used
        `output` (str, optional): Either "normalized", "round" or "direct"
        *     normalized returns a tuple(H, S, V) where the values are floats in range 0-1
        *     round returns a tuple(H, S, V) where the values are integers. H in range 0-359, SV in range 0-100
        *     direct returns a tuple(H, S, V) where the values are floats in range 0-100
        *     In any invalid case the "direct" approach will be used, which in this case is percentage

    ### Available methods:\n
        1. The Maximum of the RGB Values (Value in HSV)
        2. The Average of the RGB Values (Intensity in HSI)
        3. The Average of the Smallest and Largest RGB Values (Lightness in HSL)
        4. Perceived brightness (P in HSP). Weighted Euclidean Norm of the [R, G, B] Vector
        5. Perceived brightness. Weighted Euclidean Norm of the [R, G, B] Vector (Linearized)
        6. Perceived brightness old (P in HSP in Darel Rex Finley's formula)
        7. Perceived brightness old (Linearized)
        8. Euclidean Norm of the [R, G, B] Vector
        9. Geometric Mean of the R, G, B Components
        10. Luma, Adobe
        11. Luma, Rec709/sRGB (HDTV)
        12. Luma, Rec2020 (UHDTV, HDR)
        13. Luminance (Y) sRGB
        14. Perceived Lightness (L*) from L*ab

    ### Returns:
        int | float: How bright the color is on the scale 0-100 | 0-1
    """

    if method not in (None, *range(15)):
        raise ValueError("Wrong method input!")

    # Display message if no method was given
    if not method:
        msg='\n'.join(("Please choose a method (1-9):",
        "1. The Maximum of the RGB Values (Value in HSV)",
        "2. The Average of the RGB Values (Intensity in HSI)",
        "3. The Average of the Smallest and Largest RGB Values (Lightness in HSL)",
        "4. Perceived brightness (P in HSP). Weighted Euclidean Norm of the [R, G, B] Vector",
        "5. Perceived brightness. Weighted Euclidean Norm of the [R, G, B] Vector (Linearized)",
        "6. Perceived brightness old (P in HSP in Darel Rex Finley's formula)",
        "7. Perceived brightness old (Linearized)",
        "8. Euclidean Norm of the [R, G, B] Vector",
        "9. Geometric Mean of the R, G, B Components",
        "10. Luma, Adobe",
        "11. Luma, Rec709/sRGB (HDTV)",
        "12. Luma, Rec2020 (UHDTV, HDR)"
        "13. Luminance (Y) sRGB"
        "14. Perceived Lightness (L*) from L*ab\n"))
        method = int(input(msg))

    # Check if the input color is valid
    R, G, B = ih.check_color(color, depth=depth)

    # The maximum acceptable value per element in given bit depth
    max_value = (2 ** depth) - 1

    # Brightness calculation methods comparison:
    #+ https://medium.com/random-noise/methods-for-measuring-color-lightness-in-python-84df593d0786
    #+ HSP system: http://alienryderflex.com/hsp.html
    match method:
        case 1: #= V (value) from HSV
            brightness = max((R, G, B)) / max_value
        case 2: #= I (intensity) from HSI
            brightness = sum((R, G, B)) / (3 * max_value)
        case 3: #= L (lightness) from HSL
            brightness = sum((min((R, G, B)), max((R, G, B)))) / (2 * max_value)
        case 4: #= P (perceived brightness) from HSP. Weighted Euclidean Norm
            brightness = ((0.299 * (R / max_value) ** 2) + (0.587 * (G / max_value) ** 2) + (0.114 * (B / max_value) ** 2)) ** 0.5

            #+ Alternative calculation. The one above is slightly faster.
            # denominator = max_value * (0.299 + 0.587 + 0.114) ** 0.5
            # brightness = (0.299 * R**2 + 0.587 * G**2 + 0.114 * B**2) ** 0.5 / denominator
        case 5: #= P (perceived brightness) from HSP. Weighted Euclidean Norm (Linearized)
            R, G, B = co.convert_to_linear((R / max_value, R / max_value, B / max_value), "SRGB", normalized=True)
            brightness = ((0.299 * R ** 2) + (0.587 * G ** 2) + (0.114 * B ** 2)) ** 0.5
        case 6: #= P (perceived brightness) from HSP old
            brightness = ((0.241 * (R / max_value) ** 2) + (0.691 * (G / max_value) ** 2) + (0.068 * (B / max_value) ** 2)) ** 0.5
        case 7: #= P (perceived brightness) from HSP old (Linearized)
            R, G, B = co.convert_to_linear((R / max_value, R / max_value, B / max_value), "SRGB", normalized=True)
            brightness = ((0.241 * R ** 2) + (0.691 * G ** 2) + (0.068 * B ** 2)) ** 0.5
        case 8:
            denominator = max_value * (3 ** 0.5)
            brightness = (R**2 + G**2 + B**2) ** 0.5 / denominator
        case 9:
            brightness = ((R * G * B) ** (1/3)) / max_value
        case 10: #= Luma, Adobe
            brightness = ((0.2126 * R) + (0.7152 * G) + (0.0722 * B)) / max_value
        case 11: #= Luma, Rec709/sRGB (HDTV)
            brightness = ((0.212 * R) + (0.701 * G) + (0.087 * B)) / max_value
        case 12: #= Luma, Rec2020 (UHDTV. HDR)
            brightness = ((0.2627 * R) + (0.6780 * G) + (0.0593 * B)) / max_value
        case 13: #= Luminocity
            # Apply gamma before doing calculations
            R, G, B = (((i + 0.055) / 1.055) ** 2.4 if i > 0.04045 else i / 12.92 for i in (R/max_value, G/max_value, B/max_value))
            brightness = (0.2126 * R) + (0.7152 * G) + (0.0722 * B)
        case 14: #= L* from L*ab
            # Apply gamma before doing calculations
            R, G, B = (((i + 0.055) / 1.055) ** 2.4 if i > 0.04045 else i / 12.92 for i in (R/max_value, G/max_value, B/max_value))
            Y = (0.2126 * R) + (0.7152 * G) + (0.0722 * B)
            brightness = Y * (24389 / 27) if Y <= 216 / 24389 else Y ** (1 / 3) * 116 - 16
            brightness /= 100

    return ih.return_hsw((brightness, brightness, brightness), normalized_input=True, output=output)[1]


def get_median_color(*colors: int| float | str | tuple | list, depth: int = 8, output: str = "hex"):
    """### Calculates the average color between multiple RGB colors
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `colors` (int | float | str | tuple | list): Input colors as string "c0ffee", "#decaff", consecutive values
            either int in range 0-255 or float in range 0-1 or an RGB list/tuple(R, G, B) with the same values
        `depth` (int | float): The bit depth of the input RGB values. Defaults to 8-bit (range 0-255)
        `output` (str, optional): Either "hex", "hexp", "normalized", "round" or "direct"
        *     hex returns a hex string color in the form of decade
        *     hexp returns a hex string color in the form of #facade
        *     normalized returns a tuple(R, G, B) where the values are floats in range 0-1
        *     round returns a tuple(R, G, B) where the values are integers in range 0-255
        *     direct returns a tuple(R, G, B) where the values are floats in range 0-255
        *     In any invalid case the "direct" approach will be used

    ### Returns:
        str | tuple[r, g, b]: Returns a tuple with colors in one of the following formats:
        >>>   "c0ffed" | "#dec1de" | (192, 255, 237) | (0.8705882, 0.7568627, 0.8705882)
    """
    rgb_colors  = []    # The final colors to be processed
    ints_floats = []    # Collecting ints and floats in pairs of 3 to be added to rgb_colors

    # Collect the colors
    for color in colors:
        if isinstance(color, (str, tuple, list)):
            rgb_colors.append(ih.check_color(color, depth=depth))
        elif isinstance(color, (int, float)):
            ih.integers_floats(ints_floats, color)
        else:
            raise ValueError("Incorrect colors input!")

    # Add the ints/floats pairs to the rgb_colors list
    if ints_floats:
        for lst in ints_floats:
            if len(lst) == 3:
                rgb_colors.append(ih.check_color(lst, depth=depth))
            else:
                print(f"{lst} is not a valid color input! Skipped...")

    # Collect all Reds, Greens, Blues in separate lists
    R, G, B = zip(*rgb_colors)
    #! Using round() doesn't match the output compared to results from Photoshop. Floor division works.
    R, G, B = [sum(i) // len(i) for i in (R, G, B)]

    return ih.return_rgb((R, G, B), depth=depth, output=output)


def interpolate_color(
    color1: str | tuple | list,
    color2: str | tuple | list,
    depth: int = 8,
    factor: int | float = 50,
    output: str = "hex"):
    """### Creates a median color between color1 and color2 based on the factor
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `color1, color2` (str | tuple | list):
        *       `str`: Strings should be passed in the form of a hex color "add1c7" or "#effec7"
        *       `tuple | list`: These shuold be passed ordered as (R, G, B) where all elements
                                are either int in range 0-255 or float in range 0-1

        `depth` (int | float): The bit depth of the input RGB values. Defaults to 8-bit (range 0-255)
        `factor` (int | float, optional): Range 0-100. 0 == color1, 100 == color2. Defaults to 50.
        `output` (str, optional): Either "hex", "hexp", "normalized", "round" or "direct"
        *     hex returns a hex string color in the form of c0ffee
        *     hexp returns a hex string color in the form of #decaff
        *     normalized returns a tuple(R, G, B) where the values are floats in range 0-1
        *     round returns a tuple(R, G, B) where the values are integers in range 0-255
        *     direct returns a tuple(R, G, B) where the values are floats in range 0-255
        *     In any invalid case the "direct" approach will be used

    ### Returns:
        str | tuple[r, g, b]: Returns a tuple with colors in one of the following formats:
        >>>   "dec0de" | "#0ff1ce" | (222, 192, 222) | (0.0705882, 0.94509803, 0.8078431)
    """
    if not 0 <= factor <= 100:  # Check factor validity
        raise ValueError("factor must be int | float in range 0-100")
    if depth % 1 != 0:
        raise ValueError("Depth value must be an integer number passed either as int or float")

    # Check color integrity
    color1 = ih.check_color(color1, depth=depth)
    color2 = ih.check_color(color2, depth=depth)

    percent = factor / 100  # Get the factor as e percentage value
    return ih.return_rgb((round(color1[i] + percent * (color2[i] - color1[i])) for i in range(3)), depth=depth, output=output)

# TODO: Make it so that instead of passing color1 and color2, any number of colors can be passed and the function
    #= would generate len(steps) number of colors between all input colors
def get_gradient(
    color1: str | tuple | list,
    color2: str | tuple | list,
    depth: int = 8,
    steps: int = 4,
    include_inputs: bool = False,
    output: str = "hex"):
    """### Calculates len(steps) number of equaly spaced RGB colors between color1 and color2
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `color1, color2` (str | tuple | list):
        *       `str`: Strings should be passed in the form of a hex color "c0ffee" or "#decaff"
        *       `tuple | list`: These shuold be passed ordered as (R, G, B) where all elements
                                are either int in range 0-255 or float in range 0-1

        `depth` (int | float): The bit depth of the input RGB values. Defaults to 8-bit (range 0-255)
        `steps` (int, optional): The number of new colors to be generated. Defaults to 4
        `include_inputs` (bool, optional): If true, the input colors will be included in the final color tuple.
            `N/B`: Using this option will make the final tuple length `number of steps + 2`

        `output` (str, optional): Either "hex", "hexp", "normalized", "round" or "direct"
        *     hex returns a hex string color in the form of dec0de
        *     hexp returns a hex string color in the form of #0ff1ce
        *     normalized returns a tuple(R, G, B) where the values are floats in range 0-1
        *     round returns a tuple(R, G, B) where the values are integers in range 0-255
        *     direct returns a tuple(R, G, B) where the values are floats in range 0-255
        *     In any invalid case the "direct" approach will be used

    ### Returns:
        list: Returns a list with colors in one of the following formats:
        >>>   "decade" | "#facade" | (222, 202, 222) | (0.9803921, 0.7921568, 0.8705882)
    """
    # Check color integrity
    RGB1 = ih.check_color(color1, normalized=1, depth=depth)
    RGB2 = ih.check_color(color2, normalized=1, depth=depth)

    steps += 1  # Add 1 to the steps because the input color1 is included in 'gradient' by default
    start = 0 if include_inputs else 1  # Make the range start from 1 if input colors are not included

    # Calculate color delta and divide it by the number of new colors that will be generated
    R = (RGB2[0] - RGB1[0]) / steps
    G = (RGB2[1] - RGB1[1]) / steps
    B = (RGB2[2] - RGB1[2]) / steps

    # Get all new colors
    gradient = [(RGB1[0] + (R * i), RGB1[1] + (G * i), RGB1[2] + (B * i)) for i in range(start, steps)]
    if include_inputs:
        gradient.append(RGB2)

    return [ih.return_rgb(i, normalized_input=True, depth=depth, output=output) for i in gradient]


def get_gradient_alt(
    color1: str | tuple | list,
    color2: str | tuple | list,
    depth: int = 8,
    steps: int = 4,
    include_inputs: bool = False,
    output: str = "hex"):
    """### Calculates len(steps) number of equaly spaced RGB colors between color1 and color2
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `color1, color2` (str | tuple | list):
        *       `str`: Strings should be passed in the form of a hex color "c0ffed" or "#dec1de"
        *       `tuple | list`: These shuold be passed ordered as (R, G, B) where all elements
                                are either int in range 0-255 or float in range 0-1

        `depth` (int | float): The bit depth of the input RGB values. Defaults to 8-bit (range 0-255)
        `steps` (int, optional): The number of new colors to be generated. Defaults to 4
        `include_inputs` (bool, optional): If true, the input colors will be included in the final color tuple.
            `N/B`: Using this option will make the final tuple length `number of steps + 2`

        `output` (str, optional): Either "hex", "hexp", "normalized", "round" or "direct"
        *     hex returns a hex string color in the form of add1c7
        *     hexp returns a hex string color in the form of #effec7
        *     normalized returns a tuple(R, G, B) where the values are floats in range 0-1
        *     round returns a tuple(R, G, B) where the values are integers in range 0-255
        *     direct returns a tuple(R, G, B) where the values are floats in range 0-255
        *     In any invalid case the "direct" approach will be used

    ### Returns:
        str | tuple[r, g, b]: Returns a tuple with colors in one of the following formats:
        >>>   "c0ffee" | "#decaff" | (192, 255, 238) | (0.8705882, 0.7921568, 1.0)

    ### N/B: Although this function is much simpler than get_gradient, it runs ~3.23 times slower
    """
    steps += 2  # Add 2 steps to compensate for input colors
    factor = (1 / (steps - 1)) * 100

    grads = [interpolate_color(color1, color2, factor=min(factor * i, 100), depth=depth, output=output) for i in range(steps)]

    return grads if include_inputs else grads[1:-1]


def half_color(
    *color: int | float | str | tuple | list,
    depth: int = 8,
    operation: str = "darken",
    output: str = "hex"):
    """### Takes a color and returns twise as bright/dark color
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `color` (int | float | str | tuple | list): String "dec0de", "#0ff1ce", consecutive values either
                int in range 0-255 or float in range 0-1 or an RGB list/tuple(R, G, B) with the same values
        `depth` (int | float): The bit depth of the input RGB values. Defaults to 8-bit (range 0-255)
        `operation` (str, optional): Use either 'darken', "dark" or "dim" to get twice as dak color.
                    Otherwise you get twice as bright color. Defaults to "darken"
        `output` (str, optional): Either "hex", "hexp", "normalized", "round" or "direct"
        *     hex returns a hex string color in the form of decade
        *     hexp returns a hex string color in the form of #facade
        *     normalized returns a tuple(R, G, B) where the values are floats in range 0-1
        *     round returns a tuple(R, G, B) where the values are integers in range 0-255
        *     direct returns a tuple(R, G, B) where the values are floats in range 0-255
        *     In any invalid case the "direct" approach will be used

    ### Returns:
        str | tuple[r, g, b]: Returns a tuple with colors in one of the following formats:
        >>>   "c0ffed" | "#dec1de" | (192, 255, 237) | (0.8705882, 0.7568627, 0.8705882)
    """
    if depth % 1 != 0:
        raise ValueError("Depth value must be an integer number passed either as int or float")
    # The maximum acceptable value per element in given bit depth
    max_value = (2 ** depth) - 1

    color = ih.check_color(color, depth=depth)   # Check color integrity
    darken = operation.strip().lower() in {"dark", "darken", "dim"}  # Acceptable values for darkening

    new_color = [i // 2 if darken else min(i + i // 2, max_value) for i in color]   # Calculate new color
    #= Alternatives that are more literal to the title of the function but less usefull
    # new_color = [i // 2 if darken else min(i * 2, max_value) for i in color]   # Calculate new color
    # new_color = [max(i - max_value // 2, 0) if darken else min(i + max_value // 2, max_value) for i in color]   # Calculate new color

    return ih.return_rgb(new_color, depth=depth, output=output)


def get_hue(*color: int | float | str | tuple | list, depth: int = 8, output: str = "direct") -> int | float:
    """### Takes a color and returns its Hue
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `color` (int | float | str | tuple | list): String "add1c7", "#effec7", consecutive values either
                int in range 0-255 or float in range 0-1 or an RGB list/tuple(R, G, B) with the same values
        `depth` (int | float): The bit depth of the input RGB values. Defaults to 8-bit (range 0-255)
        `output` (str, optional): Either "normalized", "round" or "direct"
        *     normalized returns a tuple(H, S, V) where the values are floats in range 0-1
        *     round returns a tuple(H, S, V) where the values are integers. H in range 0-359, SV in range 0-100
        *     direct returns a tuple(H, S, V) where the values are floats in range 0-100
        *     In any invalid case the "direct" approach will be used

    ### Returns:
        int | float: Hue in range 0-359
    """
    # Check color integrity
    R, G, B = ih.check_color(color, normalized=True, depth=depth)

    # Get the minimum, maximum and thir delta
    Cmax = max(R, G, B)
    Cmin = min(R, G, B)
    delta = Cmax - Cmin

    if delta == 0:
        return 0

    # Calculate Hue depending on the color wheel degree of the given color
    if R == Cmax:
        H = 60 * (((G - B) / delta) % 6)
    elif G == Cmax:
        H = 60 * (((B - R) / delta) + 2)
    else:
        H = 60 * (((R - G) / delta) + 4)

    return ih.return_hsw((H, H, H), output=output)[0]


def color_change(
    *color: int | float | str | tuple | list,
    depth: int = 8,
    value: int = 5,
    operation: str = "darken",
    mode: str = "rgb",
    output: str = "hex"):
    """### Takes an RGB color and brightens/darkens it based on the value and mode
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `color` (int | float | str | tuple | list): String "c0ffee", "#decaff", consecutive values either
                int in range 0-255 or float in range 0-1 or an RGB list/tuple(R, G, B) with the same values
        `depth` (int | float): The bit depth of the input RGB values. Defaults to 8-bit (range 0-255)
        `value` (int, optional): How much to brighten/darken the color. Defaults to 5.
            The value should be in range 0-255 for "rgb" mode and in range 0-100 for the others
        `operation` (str, optional): Use either 'darken', "dark" or "dim" to get twice as dak color.
                    Otherwise you get twice as bright color. Defaults to "darken"
        `mode` (str, optional): Available modes: "rgb", "hsl", "hsv", "hsp. Defaults to "rgb".
                HSL and HSV change the color using the standards. RGB changes it by adding/subtracting
                    the "value" from all components (R, G, B) until reaching the min/max
        `output` (str, optional): Either "hex", "hexp", "normalized", "round" or "direct"
        *     hex returns a hex string color in the form of dec0de
        *     hexp returns a hex string color in the form of #0ff1ce
        *     normalized returns a tuple(R, G, B) where the values are floats in range 0-1
        *     round returns a tuple(R, G, B) where the values are integers in range 0-255
        *     direct returns a tuple(R, G, B) where the values are floats in range 0-255
        *     In any invalid case the "direct" approach will be used

    ### Returns:
        str | tuple[r, g, b]: Returns a tuple with colors in one of the following formats:
        >>>   "decade" | "#facade" | (222, 202, 222) | (0.9803921, 0.7921568, 0.8705882)
    """
    darken = operation.strip().lower() in {"dark", "darken", "dim"}

    # Get the new values depending on the mode and operation type
    match mode:
        case "hsl":
            H, S, L = co.rgb_to_hsl(*color)
            L = max(L - value, 0) if darken else min(L + value, 100)
            R, G, B = co.hsl_to_rgb(H, S, L)
        case "hsv":
            H, S, V = co.rgb_to_hsv(*color)
            V = max(V - value, 0) if darken else min(V + value, 100)
            R, G, B = co.hsv_to_rgb(H, S, V)
        case "hsp":
            H, S, P = co.rgb_to_hsp(*color)
            P = max(P - value, 0) if darken else min(P + value, 100)
            R, G, B = co.hsp_to_rgb(H, S, P)
        case _:
            # Check color integrity
            R, G, B = ih.check_color(color, depth=depth)
            if darken:
                # For every color get the next brighter/darker color based on value. Use 0 if result < 0 and 255 if result > 255
                R, G, B = [max((R, G, B)[i] - value, 0) for i in range(3)]
            else:
                R, G, B = [min((R, G, B)[i] + value, 255) for i in range(3)]

    return ih.return_rgb((R, G, B), depth=depth, output=output)


def saturate(
    *color: int | float | str | tuple | list,
    depth: int = 8,
    value: int = 5,
    mode: str = "hsv",
    output: str = "round"):
    """### Get a more saturated version of given color.
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `color` (int | float | str | tuple | list): String "c0ffed", "#dec1de", consecutive values either
                int in range 0-255 or float in range 0-1 or an RGB list/tuple(R, G, B) with the same values
        `depth` (int | float): The bit depth of the input RGB values. Defaults to 8-bit (range 0-255)
        `value` (int, optional): How much to saturate the color in range 0-100. Defaults to 5.
        `mode` (str, optional): Either "hsv" or "hsl". Defaults to "hsv".
        `output` (str, optional): Either "hex", "hexp", "normalized", "round" or "direct"
        *     hex returns a hex string color in the form of add1c7
        *     hexp returns a hex string color in the form of #effec7
        *     normalized returns a tuple(R, G, B) where the values are floats in range0-1
        *     round returns a tuple(R, G, B) where the values are integers in range 0-255
        *     direct returns a tuple(R, G, B) where the values are floats in range 0-255
        *     In any invalid case the "direct" approach will be used

    ### Returns:
        str | tuple[r, g, b]: Returns a tuple with colors in one of the following formats:
        >>>   "c0ffee" | "#decaff" | (192, 255, 238) | (0.8705882, 0.7921568, 1.0)
    """

    # Check mode, calculate new saturation
    if mode.strip().lower() == "hsl":
        H, S, L = co.rgb_to_hsl(*color, depth=depth)
        S = min(S + value, 100)
        return co.hsl_to_rgb(H, S, L, depth=depth, output=output)

    H, S, V = co.rgb_to_hsv(*color, depth=depth)
    S = min(S + value, 100)
    return co.hsv_to_rgb(H, S, V, depth=depth, output=output)


def desaturate(
    *color: int | float | str | tuple | list,
    depth: int = 8,
    value: int = 5,
    mode: str = "hsv",
    output: str = "hex"):
    """### Get a more desaturated version of a given color.
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `color` (int | float | str | tuple | list): String "dec0de", "#0ff1ce", consecutive values either
                int in range 0-255 or float in range 0-1 or an RGB list/tuple(R, G, B) with the same values
        `depth` (int | float): The bit depth of the input RGB values. Defaults to 8-bit (range 0-255)
        `value` (int, optional): How much to desaturate the color in range 0-100. Defaults to 5.
        `mode` (str, optional): Either "hsv" or "hsl". Defaults to "hsv".
        `output` (str, optional): Either "hex", "hexp", "normalized", "round" or "direct"
        *     hex returns a hex string color in the form of decade
        *     hexp returns a hex string color in the form of #facade
        *     normalized returns a tuple(R, G, B) where the values are floats in range 0-1
        *     round returns a tuple(R, G, B) where the values are integers in range 0-255
        *     direct returns a tuple(R, G, B) where the values are floats in range 0-255
        *     In any invalid case the "direct" approach will be used

    ### Returns:
        str | tuple[r, g, b]: Returns a tuple with colors in one of the following formats:
        >>>   "c0ffed" | "#dec1de" | (192, 255, 237) | (0.8705882, 0.7568627, 0.8705882)
    """
    # Check mode, calculate new saturation
    if mode.strip().lower() == "hsl":
        H, S, L = co.rgb_to_hsl(*color, depth=depth)
        S = max(S - value, 0)
        return co.hsl_to_rgb(H, S, L, depth=depth, output=output)

    H, S, V = co.rgb_to_hsv(*color, depth=depth)
    S = max(S - value, 0)
    return co.hsv_to_rgb(H, S, V, depth=depth, output=output)


def complementary_color(*color: int | float | str | tuple | list, depth: int = 8, output: str = "hex"):
    """### Create the complementary color of "color".
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `color` (int | float | str | tuple | list): String "add1c7", "#effec7", consecutive values either
                int in range 0-255 or float in range 0-1 or an RGB list/tuple(R, G, B) with the same values
        `depth` (int | float): The bit depth of the input RGB values. Defaults to 8-bit (range 0-255)
        `output` (str, optional): Either "hex", "hexp", "normalized", "round" or "direct"
        *     hex returns a hex string color in the form of c0ffee
        *     hexp returns a hex string color in the form of #decaff
        *     normalized returns a tuple(R, G, B) where the values are floats in range 0-1
        *     round returns a tuple(R, G, B) where the values are integers in range 0-255
        *     direct returns a tuple(R, G, B) where the values are floats in range 0-255
        *     In any invalid case the "direct" approach will be used

    ### Returns:
        str | tuple[r, g, b]: Returns a tuple with colors in one of the following formats:
        >>>   "dec0de" | "#0ff1ce" | (222, 192, 222) | (0.0705882, 0.94509803, 0.8078431)
    """
    # Get the color at the opposite side of the color wheel
    H, S, L = co.rgb_to_hsl(*color, depth=depth)
    H = (H + 180) % 360

    return co.hsl_to_rgb(H, S, L, depth=depth, output=output)


def monochrome_scheme(
    *color: int | float | str | tuple | list,
    depth: int = 8,
    new_colors: int = 4,
    seed: int = None,
    mode: str = "hsl",
    output: str = "hex"):
    """### Return len(new_colors) colors in the same hue with varying saturation/lightness.
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `color` (int | float | str | tuple | list): String "decade", "#facade", consecutive values either
                int in range 0-255 or float in range 0-1 or an RGB list/tuple(R, G, B) with the same values
        `depth` (int | float): The bit depth of the input RGB values. Defaults to 8-bit (range 0-255)
        `new_colors` (int, optional): How many new colors to be generated. Defaults to 4.
        `seed` (int, optional): Use if you want to get the same colors every time. Defaults to None (different).
        `mode` (str, optional): Either "hsl", "hsv" or "hsp" method for calculating. Defaults to "hsl".
        `output` (str, optional): Either "hex", "hexp", "normalized", "round" or "direct"
        *     hex returns a hex string color in the form of c0ffed
        *     hexp returns a hex string color in the form of #dec1de
        *     normalized returns a tuple(R, G, B) where the values are floats in range 0-1
        *     round returns a tuple(R, G, B) where the values are integers in range 0-255
        *     direct returns a tuple(R, G, B) where the values are floats in range 0-255
        *     In any invalid case the "direct" approach will be used

    ### Returns:
        tuple: Returns a tuple containing colors in one of the following formats:
        >>>   "add1c7" | "#AABBCC" | (173, 209, 199) | (0.9372549, 0.9960784, 0.7803921)
    """

    # Get the hue of the color
    H = get_hue(*color, depth=depth, output="round")

    # Set the seed
    random.seed(seed)
    # Get values for the saturation and the lightness of the new colors
    values_s = random.sample(range(5, 100), new_colors)
    values_l = random.sample(range(5, 100), new_colors)

    # If the saturation/lightness value is too low, give a chance for that value to be replaced
    # If change_chance is higher than 3 - change the value to a higher one
    for ind, val in enumerate(values_s):
        change_chance = random.randint(0, 10)
        if val < 30 and change_chance > 3:
            values_s[ind] = random.randint(30, 100)

    for ind, val in enumerate(values_l):
        change_chance = random.randint(0, 10)
        if val < 15 and change_chance > 3:
            values_l[ind] = random.randint(15, 100)

    # Pack the saturation and lightness values into pairs
    values = tuple(zip(values_s, values_l))

    # Use the hue and unpacked values to get the new RGB colors
    if mode.strip().lower() == "hsv":
        rgb_colors = [co.hsv_to_rgb(H, *values[i], depth=depth) for i in range(new_colors)]
    elif mode.strip().lower() == "hsp":
        rgb_colors = [co.hsp_to_rgb(H, *values[i], depth=depth) for i in range(new_colors)]
    else:
        rgb_colors = [co.hsl_to_rgb(H, *values[i], depth=depth) for i in range(new_colors)]

    return [ih.return_rgb(rgb_colors[i], depth=depth, output=output) for i in range(new_colors)]


def monochrome_scheme_alt(*color: int | float | str | tuple | list, depth: int = 8, output: str = "hex"):
    """### Return 4 colors with the same Hue and varying Saturation and Lightness.
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `color` (int | float | str | tuple | list): String "c0ffee", "#decaff", consecutive values either
                int in range 0-255 or float in range 0-1 or an RGB list/tuple(R, G, B) with the same values
        `depth` (int | float): The bit depth of the input RGB values. Defaults to 8-bit (range 0-255)
        `output` (str, optional): Either "hex", "hexp", "normalized", "round" or "direct"
        *     hex returns a hex string color in the form of dec0de
        *     hexp returns a hex string color in the form of #0ff1ce
        *     normalized returns a tuple(R, G, B) where the values are floats in range 0-1
        *     round returns a tuple(R, G, B) where the values are integers in range 0-255
        *     direct returns a tuple(R, G, B) where the values are floats in range 0-255
        *     In any invalid case the "direct" approach will be used

    ### Returns:
        list: Returns a tuple containing colors in one of the following formats:
        >>>   "decade" | "#facade" | (222, 202, 222) | (0.9803921, 0.7921568, 0.8705882)
    """
    def wrap(x: float, _min: float, thres: float, plus: float) -> float:
        """Internal function to calculate the change in Saturation and Lightness

        Args:
            x (float): The value to be changed. Either Saturation or Lightness
            _min (float): A minimum value to use for changing x
            thres (float): Threshhold that determines how the value of x will be changed
            plus (float): The value that will be added to x

        Returns:
            float: The new saturation | lightness value
        """
        return x + plus if (x - _min) < thres else x - _min

    # Get the HSL values of the input color
    HSL = co.rgb_to_hsl(*color, depth=depth, output="normalized")

    # Calculate the new Saturation and lightness values
    s1 = wrap(HSL[1], 0.3, 0.1, 0.3)
    l1 = wrap(HSL[2], 0.5, 0.2, 0.3)

    s2 = HSL[1]
    l2 = wrap(HSL[2], 0.2, 0.2, 0.6)

    s3 = s1
    l3 = max(0.2, HSL[2] + (1 - HSL[2]) * 0.2)

    s4 = HSL[1]
    l4 = wrap(HSL[2], 0.5, 0.2, 0.3)

    # Combine everything into a tuple of tuples
    res = (HSL[0], s1,  l1), (HSL[0], s2,  l2), (HSL[0], s3,  l3), (HSL[0], s4,  l4)

    return [ih.return_rgb([co.hsl_to_rgb(i, depth=depth) for i in res][j], output=output) for j in range(4)]


def triadic_scheme(
    *color: int | float | str | tuple | list,
    depth: int = 8,
    angle: int = 120,
    complementary: bool = True,
    output: str = "hex"):
    """### Return two colors forming a triad or a split complementary with the input color.
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `color` (int | float | str | tuple | list): String "c0ffed", "#dec1de", consecutive values either
                int in range 0-255 or float in range 0-1 or an RGB list/tuple(R, G, B) with the same values
        `depth` (int | float): The bit depth of the input RGB values. Defaults to 8-bit (range 0-255)
        `angle` (int, optional): If no angle is specified, 120 degree angle will be used which will generate the
            triadic scheme. If angle != 120, 2 new colors will be generated equally distanced from the input color.
        `complementary` (bool, optional): If True, the new colors will be split complementary (on the opposite
            side of the color wheel) of the input color. Otherwise, the new colors will be analogous. Defaults to True.
        `output` (str, optional): Either "hex", "hexp", "normalized", "round" or "direct"
        *     hex returns a hex string color in the form of add1c7
        *     hexp returns a hex string color in the form of #effec7
        *     normalized returns a tuple(R, G, B) where the values are floats in range 0-1
        *     round returns a tuple(R, G, B) where the values are integers in range 0-255
        *     direct returns a tuple(R, G, B) where the values are floats in range 0-255
        *     In any invalid case the "direct" approach will be used

    ### Returns:
        tuple: A tuple containing the 2 new colors in one of the following formats:
        >>>   "c0ffee" | "#decaff" | (192, 255, 238) | (0.8705882, 0.7921568, 1.0)
    """
    # Convert color to HSL
    H, S, L = co.rgb_to_hsl(*color, depth=depth)
    angle = min(angle, 120)   # Get the angle, which can't be more than 120 degrees.

    if complementary:
        angle /= 2
        H += 180    # Go to opposite side of the color wheel

    # Calculate Hues with equal distance from H in opposite directions
    h1 = round((H - angle) % 360)
    h2 = round((H + angle) % 360)

    return [ih.return_rgb(i, depth=depth, output=output) for i in (co.hsl_to_rgb(i, S, L, depth=depth) for i in (h1, h2))]


def tetradic_scheme(*color: int | float | str | tuple | list, depth: int = 8, angle: int = 30, output: str = "hex"):
    """### Return three colors froming a tetrad with the input color. \
        Tetradic scheme is basically a double split complementary color scheme.
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `color` (int | float | str | tuple | list): String "dec0de", "#0ff1ce", consecutive values either
                int in range 0-255 or float in range 0-1 or an RGB list/tuple(R, G, B) with the same values
        `depth` (int | float): The bit depth of the input RGB values. Defaults to 8-bit (range 0-255)
        `angle` (int, optional): The angle to subtract from the adjacent colors hues [-90...90].
            You can use an angle of zero to generate a square tetrad.

    ### Returns:
        tuple: A tuple containing the 3 new colors in one of the following formats:
        >>>   "decade" | "#facade" | (222, 202, 222) | (0.9803921, 0.7921568, 0.8705882)
    """
    # Convert color to HSL
    H, S, L = co.rgb_to_hsl(*color, depth=depth)

    # Calculate the 3 new Hues
    h1 = (H + 90 - angle) % 360
    h2 = (H + 180) % 360
    h3 = (H + 270 - angle) % 360

    return [ih.return_rgb(i, depth=depth, output=output) for i in (co.hsl_to_rgb(i, S, L, depth=depth) for i in (h1, h2, h3))]


def convert_bit_depth(
    *color: int | float | str | tuple | list,
    base_depth: int | float,
    target_depth: int | float,
    output: str = "hex"):
    """### Converts a color to a different bit depth. Ex. 8-bit color in range 0-255 to 10-bit in range 0-1023

    Args:
        `color` (int | float | str | tuple | list): String "c0ffed", "#dec1de", consecutive values either
                int in range 0-255 or float in range 0-1 or an RGB list/tuple(R, G, B) with the same values
        `base_depth` (int | float): The bit depth of the input color
        `target_depth` (int | float): The target bit depth

    Returns:
        tuple[r, g, b]: A tuple with the values of the input color in the requested bit depth
    """
    color = ih.check_color(color, depth=base_depth)
    return ih.return_rgb([round((2 ** target_depth - 1) / (2 ** base_depth - 1) * i) for i in color], depth=target_depth, output=output)


def alpha_blend(color1, color2, color1_alpha, color2_alpha):
    '''Alpha-blend this color on the other one.
    Args:
        :other:
            The grapefruit.Color to alpha-blend with this one.
    Returns:
        A grapefruit.Color instance which is the result of alpha-blending
        this color on the other one.
    >>> c1 = Color.NewFromRgb(1, 0.5, 0, 0.2)
    >>> c2 = Color.NewFromRgb(1, 1, 1, 0.8)
    >>> c3 = c1.AlphaBlend(c2)
    >>> str(c3)
    '(1, 0.875, 0.75, 0.84)'
    '''
    color1 = ih.check_color(color1)
    color2 = ih.check_color(color2)

    # get final alpha channel
    fa = color1_alpha + color2_alpha - (color1_alpha * color2_alpha)

    # get percentage of source alpha compared to final alpha
    if fa == 0:
        sa = 0
    else:
        sa = min(1.0, color1_alpha/color2_alpha)

    # destination percentage is just the additive inverse
    da = 1 - sa

    sr, sg, sb = [v * sa for v in color1]
    dr, dg, db = [v * da for v in color2]

    return (sr + dr, sg + dg, sb + db)


def blend(color1, color2, color1_alpha=100, color2_alpha=100, percent=0.5):
    '''Blend this color with the other one.
    Args:
        :other:
            the grapefruit.Color to blend with this one.
    Returns:
        A grapefruit.Color instance which is the result of blending
        this color on the other one.
    >>> c1 = Color.NewFromRgb(1, 0.5, 0, 0.2)
    >>> c2 = Color.NewFromRgb(1, 1, 1, 0.6)
    >>> c3 = c1.Blend(c2)
    >>> str(c3)
    '(1, 0.75, 0.5, 0.4)'
    '''
    color1 = ih.check_color(color1)
    color2 = ih.check_color(color2)

    dest = 1.0 - percent
    rgb = tuple(((u * percent) + (v * dest) for u, v in zip(color1, color2)))
    a = (color1_alpha * percent) + (color2_alpha * dest)
    return rgb, a