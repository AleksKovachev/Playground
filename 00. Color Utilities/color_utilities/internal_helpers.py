"""A collection of useful reusable internal functions"""
# pylint: disable=invalid-name
from enum import Enum
from math import radians, sqrt
from numpy import array
from numpy.linalg import inv

from . import converters as co
from .constants import Out1, Out2, Out3, Color_seq, Color_out_seq, Color_out_hsw

MATRIX_RGB_TO_YC1C2 = array((
    (0.2126, 0.7152, 0.0722),
    (1, -0.5, -0.5),
    (0, -sqrt(3) / 2, sqrt(3) / 2)))
MATRIX_YC1C2_TO_RGB = inv(MATRIX_RGB_TO_YC1C2)


def check_color(
    color: Color_seq,
    depth: int = 8,
    normalized: bool = False,
    clamp: bool = True) -> Color_out_seq:
    """### Checks the type of the color input and returns R, G, B values
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `color` (Color_seq): String "c0ffee", "#decaff" or a list/tuple (R, G, B)
                where the values should be either int in range 0-255 or float in range 0-1.
        `depth` (int | float): The bit depth of the input RGB values. Defaults to 8-bit (range 0-255).
        `normalized` (bool, optional): Return R, G, B as floats in range 0-1. Defaults to False.
        `clamp` (bool, optional): Clamps the values in a given range.

    ### Returns:
        tuple(R, G, B): R, G, B int in range 0-255 or R, G, B float in range 0-1
    """
    if depth % 1 != 0:
        raise ValueError("Depth value must be an integer number!")
    max_value = (2 ** depth) - 1

    # If color is a tuple with length == 1, assume the element is a tuple/list and assign it as color
    if isinstance(color, (tuple, list)) and len(color) == 1:
        color = color[0]
    if isinstance(color, (tuple, list)):
        # The tuple/list can only be len(3)
        if len(color) != 3:
            raise ValueError("Color list/tuple can only contain 3 values!")
        R, G, B = color
    # If color is given as a hex color, return it as R, G, B tuple
    elif isinstance(color, str):
        R, G, B = co.hex_to_rgb(color, normalized=normalized, depth=depth)
    # The input color can't be any other type
    else:
        raise TypeError("Argument must be either a type str | list | tuple")

    # Check if all R, G, B elements are the same type and in the correct range
    if all(isinstance(i, int) for i in (R, G, B)):
        if not (0 <= R <= max_value and 0 <= G <= max_value and 0 <= B <= max_value) and clamp:
            raise ValueError(f"{depth}-bit integer types should be in range 0-{max_value}")
    elif all(isinstance(i, float) for i in (R, G, B)):
        if not (0 <= R <= 1 and 0 <= G <= 1 and 0 <= B <= 1) and clamp:
            raise ValueError("Float types should be in range 0-1")
        # Convert to 0-max_value range if not normalized
        return (R, G, B) if normalized else tuple(round(i * max_value) for i in (R, G, B))
    else:
        raise TypeError("All elements must be the same type (int | float)")

    # Convert to 0-1 range if normalized
    return (R / max_value, G / max_value, B / max_value) if normalized else (R, G, B)


def check_hsw(vals: tuple | list, output: Enum = Out2.ROUND) -> Color_out_hsw:
    """### Checks if 3-element values HSW (W-wildcard, could be Lightness, Value, etc.) have correct type of elements

    ### Args:
        `vals` (tuple | list): Tuple/list of 3 values or tuple/list containing 1 tuple/list with 3 values
        `output` (str, optional): Either "normalized", "round" or "half-normalized"
        * "normalized" returns values in range 0-1
        * "half-normalized" returns Hue in range 0-360, Saturation and Wildcard in range 0-1
        * "round" returns Hue in range 0-360, Saturation and Wildcard in range 0-100

    ### Returns:
        tuple[H, S, W]
    """
    # If there's only one element in vals, assume it's a tuple and make vals the first element of vals
    if len(vals) == 1:
        vals = vals[0]
    # The tuple can't contain other than 3 elements
    if len(vals) != 3:
        raise ValueError("Invalid input format!")

    H, S, W = vals  # Hue, Saturation, Wildcard (Value, Lightness, Intensity, etc)

    # Check if all H, S, W elements are the same type and in the correct range
    if isinstance(H, int) and isinstance(S, int) and isinstance(W, int):
        if not 0 <= H < 360:
            raise ValueError("Hue must be in range 0-359 degrees!")
        if not (0 <= S <= 100 and 0 <= W <= 100):
            raise ValueError("The value must be in range 0-100%!")

        match output:
            case Out2.NORMALIZED:
                return H / 360, S / 100, W / 100
            case Out2.HALF_NORMALIZED:
                return H, S / 100, W / 100
            case Out2.ROUND | Out2.DIRECT:
                return vals

    if isinstance(H, float) and isinstance(S, float) and isinstance(W, float):
        if not 0 <= H <= 1:
            raise ValueError("Hue must be in range 0-1!")
        if not (0 <= S <= 1 and 0 <= W <= 1):
            raise ValueError("The value must be in range 0-1!")

        match output:
            case Out2.NORMALIZED:
                return vals
            case Out2.HALF_NORMALIZED:
                return H * 360, S, W
            case Out2.ROUND | Out2.DIRECT:
                return H * 360, S * 100, W * 100

    if isinstance(H, int) and isinstance(S, float) and isinstance(W, float):
        if not 0 <= H < 360:
            raise ValueError("Hue must be in range 0-359 degrees!")
        if not (0 <= S <= 1 and 0 <= W <= 1):
            raise ValueError("The value must be in range 0-1!")

        match output:
            case Out2.NORMALIZED:
                return vals[0] / 360, S, W
            case Out2.HALF_NORMALIZED:
                return vals
            case Out2.ROUND | Out2.DIRECT:
                return H, S * 100, W * 100

    raise TypeError("All elements must be the same type (int | float) \
        or Hue - int, the rest - float")


def check_hcl(HCL, big_float):
    """### Checks if an HCL color is valid and outputs the values in a specific H range(0-360), CL range(0-255)

    ### Args:
        `HCL` (tuple | list): Tuple/list of 3 values (Hue, Chroma, Luminosity)
        `big_float` (bool, optional): Wether the input HCL values are floats in range 0-100

    ### Returns:
        tuple[H, C, L]
    """
    # If there's only one element in vals, assume it's a tuple and make vals the first element of vals
    if len(HCL) == 1:
        HCL = HCL[0]
    # The tuple can't contain other than 3 elements
    if len(HCL) != 3:
        raise ValueError("Invalid input format!")
    H, C, L = HCL
    if isinstance(H, int) and isinstance(C, int) and isinstance(L, int):
        C /= 255
        L /= 255
    elif isinstance(H, int) and isinstance(C, float) and isinstance(L, float):
        if big_float:
            C /= 255
            L /= 255
    elif isinstance(H, float) and isinstance(C, float) and isinstance(L, float):
        if big_float:
            C /= 255
            L /= 255
        else:
            H *= 360
    else:
        raise ValueError("Invalid input format!")
    # Chroma range - 255 with defauts.#! Test with different gamma and Y0
    # Luminance range - 255 with defauts.#! Test with different gamma and Y0
    H = radians(co.convert_range(H, (0, 360), (-180, 180)))
    return H, C, L


def integers_floats(ints_floats: list, element: int | float):
    """### Internal function for managing consecutive integers and floats passed to a function
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `ints_floats` (list): A list containing 3-element pairs of integers or floats
        `element` (int | float): An RGB element. Integer in range 0-255 or float in range 0-1
    """
    # Put the element as the first one in the first RGB pair
    if not ints_floats:
        ints_floats.append([element])
    else:
        # Add to the pair with less than 3 values or create a new one
        for count, lst in enumerate(ints_floats):
            if len(lst) != 3:
                lst.append(element)
                break
            if count == len(ints_floats) - 1:
            #* if not len(ints_floats[-1]) % 3: # Alternative
                ints_floats.append([element])
                break


def check_xyz(XYZ, normalized: bool = False, big_float: bool = True):
    """### Checks XYZ values for errors and returns the requested type

    ### Args:
        `normalized` (bool, optional): Whether to return the result in range 0-1 rather than the default range 0-100
        `big_float` (bool, optional): Whether the input XYZ values are floats in range 0-100

    ### Returns:
        tuple: X, Y, Z
    """
    if not isinstance(XYZ, (tuple, list)):
        raise TypeError("Argument must be either a type str | list | tuple")

    # If XYZ is a tuple with length == 1, assume the element is a tuple/list and assign it as color
    if len(XYZ) == 1:
        XYZ = XYZ[0]
    # The tuple/list can only be len(3)
    if len(XYZ) != 3:
        raise ValueError("Incorrect XYZ input!")

    X, Y, Z = XYZ

    # Check if all X, Y, Z elements are the same type and in the correct range
    if isinstance(X, int) and isinstance(Y, int) and isinstance(Z, int):
        if not (0 <= X <= 95 and 0 <= Y <= 100 and 0 <= Z <= 109):
            raise ValueError("Integer types should be in the range 0-100")
    elif isinstance(X, float) and isinstance(Y, float) and isinstance(Z, float):
        if big_float:
            if not (0 <= X <= 95.05 and 0 <= Y <= 100 and 0 <= Z <= 109):
                raise ValueError("Color should be in the range 0-100")
            return (X/100, Y/100, Z/100) if normalized else (X, Y, Z)
        if not (0 <= X <= 0.9505 and 0 <= Y <= 1 and 0 <= Z <= 1.09):
            raise ValueError("Float types should be in the range 0-1")
        return (X, Y, Z) if normalized else (X*100, Y*100, Z*100)
    else:
        raise TypeError("All elements in the list/tuple must be the same type (int | float)")

    # Convert to 0-1 range if normalized
    return (X/100, Y/100, Z/100) if normalized else (X, Y, Z)


def return_rgb(
    RGB: tuple | list,
    output: Enum,
    depth: int = 8,
    clamp: bool = True,
    normalized_input: bool = False) -> str | tuple[int, int, int] | tuple [float, float, float]:
    """### Determines what to return based on input parameters
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `RGB` (tuple[R, G, B] | list[R, G, B]): The input color
        `output` (str): The desired type of output in: "hex", "hexp", "round", "normalized", "direct"
        `depth` (int | float): The bit depth of the input RGB values. Defaults to 8-bit (range 0-255)
        `clamp` (bool, optional): Clamps the values in valid range. Ex. -1 to 0, 262 to 255 for range 0-255. Defaults to True.
        `normalized_input` (bool): Whether the R, G, B values are in range 0-1 or the default range 0-255

    ### Returns:
        tuple[R, G, B]
    """
    if depth % 1 != 0:
        raise ValueError("Depth value must be an integer number passed either as int or float")

    # Get the max value for the chosen bit depth
    length = (2 ** depth) - 1
    R, G, B = RGB

    # Clamp the values to a valid range
    if clamp:
        R, G, B = (max(min(i, 1.0), 0.0) if normalized_input else max(min(i, float(length)), 0.0) for i in (R, G, B))

    # Return desired output type based on input
    match output:
        case Out1.HEX | Out1.HEXP:
            if normalized_input:
                R, G, B = (round(i * length) for i in (R, G, B))

            # Return new color in hex color format
            pound_sign = output == Out1.HEXP
            return co.rgb_to_hex(R, G, B, depth=depth, pound=pound_sign)
        case Out1.ROUND:
            return (round(R * length), round(G * length), round(B * length)) if normalized_input else (round(R), round(G), round(B))
        case Out1.NORMALIZED:
            return (R, G, B) if normalized_input else (R / length, G / length, B / length)
        case Out1.DIRECT:
            return (R * length, G * length, B * length) if normalized_input else (R, G, B)
        case _:
            raise TypeError("Wrong output type!")


def return_hsw(
    HSW: tuple | list,
    output: Enum,
    normalized_input: bool = False) -> tuple[int, int, int] | tuple[float, float, float] | tuple[int, float, float]:
    """### Determines what to return based on input parameters

    ### Args:
        `HSW` (tuple | list): Hue, Saturation, Wildcard (Either Value, Lightness or Intensity)
        `output` (str): The desired type of output
        `normalized_input` (bool): Whether the H, S, W values are in range 0-1 or the default range 0-100

    ### Returns:
        tuple[H, S, W]
    """
    H, S, W = HSW
    match output:
        case Out2.ROUND:
            return (min(round(H * 360), 359), round(S * 100), round(W * 100)) if normalized_input else (min(round(H), 359), round(S), round(W))
        case Out2.NORMALIZED:
            return (H, min(S, 1.0), min(W, 1.0)) if normalized_input else (H / 360, S / 100, W / 100)
        case Out2.HALF_NORMALIZED:
            return (min(round(H * 360), 359), S, W) if normalized_input else (min(round(H), 359), S / 100, W / 100)
        case Out2.DIRECT:
            return (H * 360, min(S * 100, 100.0), min(W * 100, 100.0)) if normalized_input else (H, S, W)
        case _:
            raise ValueError("Wrong output type!")

def return_scale(
    vals: tuple | list,
    output: Enum,
    min_max: tuple | list = (0, 100),
    clamp: bool = False,
    normalized_input: bool = False) -> tuple[int, int, int] | tuple[float, float, float]:
    """### Determines what to return based on input parameters

    ### Args:
        `vals` (tuple | list): The values to be returned as the requested type
        `output` (str): The desired type of output
        `min_max` (tuple | list, optional): The minimum and maximum allowed values before clamping. Defaults to (0, 100).
        `clamp` (bool, optional): Clamps the values in the specified in `min_max` range. Defaults to False.
        `normalized_input` (bool): Whether the input values are in range 0-1 or the default range 0-100

    ### Returns:
        tuple: Three values in the requested range and type.
    """
    clamp = min_max if clamp else (float('-inf'), float('inf'))

    match output:
        case Out3.ROUND:
            return [max(min(round(i * min_max[1]), clamp[1]), clamp[0]) for i in vals] if normalized_input \
                else [max(min(round(i), clamp[1]), clamp[0]) for i in vals]
        case Out3.NORMALIZED:
            if clamp == min_max:
                clamp = (0.0, 1.0) if 0 in min_max else (-1.0, 1.0)
            return [max(min(i, clamp[1]), clamp[0]) for i in vals] if normalized_input \
                else [max(min(i / min_max[1], clamp[1]), clamp[0]) for i in vals]
        case Out3.DIRECT | _:
            return [max(min(i * min_max[1], clamp[1]), clamp[0]) for i in vals] if normalized_input \
                else [max(min(i, clamp[1]), clamp[0]) for i in vals]
