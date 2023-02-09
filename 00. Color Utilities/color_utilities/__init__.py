"""This is a collection of useful functions for working with colors"""
from functools import partial

from color_utilities.internal_helpers import *
from color_utilities.transfer_functions import *
from color_utilities.color_spaces import color_spaces
from color_utilities.color_utils import *
from color_utilities.additionals import (ILLUMINANT_WHITEPOINTS, T4200K, T6800K, wp_4200K, wp_6800K,
                                        COLOR_SPACE_MATRICES, color_space_props, LIGHT_SOURCES)
from color_utilities.converters import *
from color_utilities.xyz import *

#* Combo functions
def hsv_to_hsi(*HSV, depth: int = 8, output: str = "round"):
    """### Convert HSV values to HSI
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `HSI` (int | float | tuple | list): Hue, Saturation, Intensity either H in int range 0-359, SV range 0-100
                                    or float range 0-1 or a tuple/list with the same values
        `output` (str, optional): Either "normalized", "half-normalized", "round" or "direct"
        *     normalized returns a tuple(H, S, I) where the values are floats in range 0-1
        *     half-normalized returns a tuple(H, S, I) where the values are H in range 0-359, SI in range 0-1
        *     round returns a tuple(H, S, I) where the values are integers. H in range 0-359, SI in range 0-100
        *     direct returns a tuple(H, S, I) where the values are floats in range 0-100
        *     In any invalid case the "direct" approach will be used

    #### N/B: Don't use round output if the output color is going to be used to further conversion!

    ### Returns:
        tuple[int, int, int] | tuple[float, float, float] | tuple[int, float, float]: Hue, Saturation, Intensity
    """
    return rgb_to_hsi(hsv_to_rgb(*HSV, output="normalized"), depth=depth, output=output)


def hsv_to_hsp(*HSV, depth: int = 8, output: str = "round"):
    """### Convert HSV values to HSI
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `HSI` (int | float | tuple | list): Hue, Saturation, Intensity either H in int range 0-359, SV range 0-100
                                    or float range 0-1 or a tuple/list with the same values
        `output` (str, optional): Either "normalized", "half-normalized", "round" or "direct"
        *     normalized returns a tuple(H, S, P) where the values are floats in range 0-1
        *     half-normalized returns a tuple(H, S, P) where the values are H in range 0-359, SP in range 0-1
        *     round returns a tuple(H, S, P) where the values are integers. H in range 0-359, SP in range 0-100
        *     direct returns a tuple(H, S, P) where the values are floats in range 0-100
        *     In any invalid case the "direct" approach will be used

    #### N/B: Don't use round output if the output color is going to be used to further conversion!

    ### Returns:
        tuple[int, int, int] | tuple[float, float, float] | tuple[int, float, float]: Hue, Saturation, Perceived brightness
    """
    return rgb_to_hsp(hsv_to_rgb(*HSV, output="normalized"), depth=depth, output=output)


def hsl_to_hsi(*HSL, depth: int = 8, output: str = "round"):
    """### Convert HSL values to HSI
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `HSI` (int | float | tuple | list): Hue, Saturation, Intensity either H in int range 0-359, SL range 0-100
                                    or float range 0-1 or a tuple/list with the same values
        `output` (str, optional): Either "normalized", "half-normalized", "round" or "direct"
        *     normalized returns a tuple(H, S, I) where the values are floats in range 0-1
        *     half-normalized returns a tuple(H, S, I) where the values are H in range 0-359, SI in range 0-1
        *     round returns a tuple(H, S, I) where the values are integers. H in range 0-359, SI in range 0-100
        *     direct returns a tuple(H, S, I) where the values are floats in range 0-100
        *     In any invalid case the "direct" approach will be used

    #### N/B: Don't use round output if the output color is going to be used to further conversion!

    ### Returns:
        tuple[int, int, int] | tuple[float, float, float] | tuple[int, float, float]: Hue, Saturation, Intensity
    """
    return rgb_to_hsi(hsl_to_rgb(*HSL, output="normalized"), depth=depth, output=output)


def hsl_to_hsp(*HSL, depth: int = 8, output: str = "round"):
    """### Convert HSV values to HSI
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `HSI` (int | float | tuple | list): Hue, Saturation, Intensity either H in int range 0-359, SL range 0-100
                                    or float range 0-1 or a tuple/list with the same values
        `output` (str, optional): Either "normalized", "half-normalized", "round" or "direct"
        *     normalized returns a tuple(H, S, P) where the values are floats in range 0-1
        *     half-normalized returns a tuple(H, S, P) where the values are H in range 0-359, SP in range 0-1
        *     round returns a tuple(H, S, P) where the values are integers. H in range 0-359, SP in range 0-100
        *     direct returns a tuple(H, S, P) where the values are floats in range 0-100
        *     In any invalid case the "direct" approach will be used

    #### N/B: Don't use round output if the output color is going to be used to further conversion!

    ### Returns:
        tuple[int, int, int] | tuple[float, float, float] | tuple[int, float, float]: Hue, Saturation, Perceived brightness
    """
    return rgb_to_hsp(hsl_to_rgb(*HSL, output="normalized"), depth=depth, output=output)


def hsi_to_hsv(*HSI, depth: int = 8, output: str = "round"):
    """### Convert HSI values to HSV
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `HSI` (int | float | tuple | list): Hue, Saturation, Intensity either H in int range 0-359, SI range 0-100
                                    or float range 0-1 or a tuple/list with the same values
        `output` (str, optional): Either "normalized", "half-normalized", "round" or "direct"
        *     normalized returns a tuple(H, S, V) where the values are floats in range 0-1
        *     half-normalized returns a tuple(H, S, V) where the values are H in range 0-359, SV in range 0-1
        *     round returns a tuple(H, S, V) where the values are integers. H in range 0-359, SV in range 0-100
        *     direct returns a tuple(H, S, V) where the values are floats in range 0-100
        *     In any invalid case the "direct" approach will be used

    #### N/B: Don't use round output if the output color is going to be used to further conversion!

    ### Returns:
        tuple[int, int, int] | tuple[float, float, float] | tuple[int, float, float]: Hue, Saturation, Value
    """
    return rgb_to_hsv(hsi_to_rgb(*HSI, output="normalized"), depth=depth, output=output)


def hsi_to_hsl(*HSI, depth: int = 8, output: str = "round"):
    """### Convert HSI values to HSL
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `HSI` (int | float | tuple | list): Hue, Saturation, Intensity either H in int range 0-359, SI range 0-100
                                    or float range 0-1 or a tuple/list with the same values
        `output` (str, optional): Either "normalized", "half-normalized", "round" or "direct"
        *     normalized returns a tuple(H, S, L) where the values are floats in range 0-1
        *     half-normalized returns a tuple(H, S, L) where the values are H in range 0-359, SL in range 0-1
        *     round returns a tuple(H, S, L) where the values are integers. H in range 0-359, SL in range 0-100
        *     direct returns a tuple(H, S, L) where the values are floats in range 0-100
        *     In any invalid case the "direct" approach will be used

    #### N/B: Don't use round output if the output color is going to be used to further conversion!

    ### Returns:
        tuple[int, int, int] | tuple[float, float, float] | tuple[int, float, float]: Hue, Saturation, Lightneses
    """
    return rgb_to_hsl(hsi_to_rgb(*HSI, output="normalized"), depth=depth, output=output)


def hsi_to_hsp(*HSI, depth: int = 8, output: str = "round"):
    """### Convert HSI values to HSL
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `HSI` (int | float | tuple | list): Hue, Saturation, Intensity either H in int range 0-359, SI range 0-100
                                    or float range 0-1 or a tuple/list with the same values
        `output` (str, optional): Either "normalized", "half-normalized", "round" or "direct"
        *     normalized returns a tuple(H, S, P) where the values are floats in range 0-1
        *     half-normalized returns a tuple(H, S, P) where the values are H in range 0-359, SP in range 0-1
        *     round returns a tuple(H, S, P) where the values are integers. H in range 0-359, SP in range 0-100
        *     direct returns a tuple(H, S, P) where the values are floats in range 0-100
        *     In any invalid case the "direct" approach will be used

    #### N/B: Don't use round output if the output color is going to be used to further conversion!

    ### Returns:
        tuple[int, int, int] | tuple[float, float, float] | tuple[int, float, float]: Hue, Saturation, Perceived brightness
    """
    return rgb_to_hsp(hsi_to_rgb(*HSI, output="normalized"), depth=depth, output=output)


def hsp_to_hsv(*HSP, depth: int = 8, output: str = "round"):
    """### Convert HSP values to HSV
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `HSI` (int | float | tuple | list): Hue, Saturation, Intensity either H in int range 0-359, SP range 0-100
                                    or float range 0-1 or a tuple/list with the same values
        `output` (str, optional): Either "normalized", "half-normalized", "round" or "direct"
        *     normalized returns a tuple(H, S, V) where the values are floats in range 0-1
        *     half-normalized returns a tuple(H, S, V) where the values are H in range 0-359, SV in range 0-1
        *     round returns a tuple(H, S, V) where the values are integers. H in range 0-359, SV in range 0-100
        *     direct returns a tuple(H, S, V) where the values are floats in range 0-100
        *     In any invalid case the "direct" approach will be used

    #### N/B: Don't use round output if the output color is going to be used to further conversion!

    ### Returns:
        tuple[int, int, int] | tuple[float, float, float] | tuple[int, float, float]: Hue, Saturation, Value
    """
    return rgb_to_hsv(hsp_to_rgb(*HSP, output="normalized"), depth=depth, output=output)


def hsp_to_hsl(*HSP, depth: int = 8, output: str = "round"):
    """### Convert HSI values to HSL
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `HSI` (int | float | tuple | list): Hue, Saturation, Intensity either H in int range 0-359, SP range 0-100
                                    or float range 0-1 or a tuple/list with the same values
        `output` (str, optional): Either "normalized", "half-normalized", "round" or "direct"
        *     normalized returns a tuple(H, S, L) where the values are floats in range 0-1
        *     half-normalized returns a tuple(H, S, L) where the values are H in range 0-359, SL in range 0-1
        *     round returns a tuple(H, S, L) where the values are integers. H in range 0-359, SL in range 0-100
        *     direct returns a tuple(H, S, L) where the values are floats in range 0-100
        *     In any invalid case the "direct" approach will be used

    #### N/B: Don't use round output if the output color is going to be used to further conversion!

    ### Returns:
        tuple[int, int, int] | tuple[float, float, float] | tuple[int, float, float]: Hue, Saturation, Lightneses
    """
    return rgb_to_hsl(hsp_to_rgb(*HSP, output="normalized"), depth=depth, output=output)


def hsp_to_hsi(*HSP, depth: int = 8, output: str = "round"):
    """### Convert HSP values to HSI
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `HSI` (int | float | tuple | list): Hue, Saturation, Intensity either H in int range 0-359, SP range 0-100
                                    or float range 0-1 or a tuple/list with the same values
        `output` (str, optional): Either "normalized", "half-normalized", "round" or "direct"
        *     normalized returns a tuple(H, S, I) where the values are floats in range 0-1
        *     half-normalized returns a tuple(H, S, I) where the values are H in range 0-359, SI in range 0-1
        *     round returns a tuple(H, S, I) where the values are integers. H in range 0-359, SI in range 0-100
        *     direct returns a tuple(H, S, I) where the values are floats in range 0-100
        *     In any invalid case the "direct" approach will be used

    #### N/B: Don't use round output if the output color is going to be used to further conversion!

    ### Returns:
        tuple[int, int, int] | tuple[float, float, float] | tuple[int, float, float]: Hue, Saturation, Intensity
    """
    return rgb_to_hsi(hsp_to_rgb(*HSP, output="normalized"), depth=depth, output=output)


def rgb_to_lab(
    *color: str | tuple | list,
    illuminant: str = "D65",
    observer: str | int | float = "2",
    adaptation: str = "bradford",
    round_: bool = False):
    """### Takes RGB color and returns its CIE L*ab values

    ### Args:
        `color` (str | tuple | list): String "dec0de", "#0ff1ce", consecutive values either
                in int range 0-255 or in float range 0-1 or a list/tuple (r, g, b) in same ranges
        `illuminant` (str, optional): The iluminant of the output L*ab color. Defaults to 'D65'
        `observer` (int[2 | 10] | str, optional): The observer viewing angle for the output L*ab. Defaults to "2".
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
    return xyz_to_lab(rgb_to_xyz(*color, output="direct"), lab_illuminant=illuminant, observer=observer, adaptation=adaptation, round_=round_)


def lab_to_rgb(
    *LAB: tuple | list,
    illuminant: str = "D65",
    observer: str | int | float = "2",
    adaptation: str = "bradford",
    output: str = "round"):
    """### Takes CIE L*ab color and returns its sRGB values

    ### Args:
        `LAB` (int, float, tuple, list): L*ab color in 3 consecutive int or float values in range
            L* (0, 100), ab (-128, 128) or list/tuple containing the same values
        `illuminant` (str, optional): The iluminant of the input L*ab color. Defaults to 'D65'
        `observer` (int[2 | 10] | str, optional): The observer viewing angle for the input L*ab. Defaults to "2".
        `adaptation` (str): The adaptation method to be used for illuminant conversions. Defaults to "bradford"
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
        str | tuple[int, int, int] | tuple[float, float, float]: Red, Green, Blue
    """
    return xyz_to_rgb(lab_to_xyz(*LAB), illuminant=illuminant, observer=observer, adaptation=adaptation, output=output)


# TODOs:
# Add HCL<->RGB - Hue, Chroma, Luminance
# Add IHLS<->RGB - Improved HLS


# TODOs:
# Include all illuminants from additionals.py in the code.
# Make xyz_to_rgb and rgb_to_xyz functions work with any color depth
# When reading strings (especially color_space_props), in refine_rgb()
    # make it delete empty space chars inside strings as well
# Make the CMYK calculations more accurate by going through XYZ values
