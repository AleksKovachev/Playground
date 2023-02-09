"""A collection of useful reusable internal functions"""
# pylint: disable=invalid-name
from . import converters as co


def check_color(
    color: str | tuple | list,
    depth: int | float = 8,
    normalized: bool = False,
    clamp: bool = True) -> tuple[int, int, int] | tuple[float, float, float]:
    """### Checks the type of the color input and returns r, g, b values
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `color` (str | tuple | list): String "c0ffee", "#decaff" or a list/tuple (r, g, b)
                where the values should be either int in range 0-255 or float in range 0-1.
        `depth` (int | float): The bit depth of the input RGB values. Defaults to 8-bit (range 0-255).
        `normalized` (bool, optional): Return r, g, b as floats in range 0-1. Defaults to False.
        `clamp` (bool, optional): Clamps the values in a given range.

    ### Returns:
        tuple(r, g, b): r, g, b int in range 0-255 or r, g, b float in range 0-1
    """
    if depth % 1 != 0:
        raise ValueError("Depth value must be an integer number passed either as int or float")
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
        R, G, B = co.hex_to_rgb(color, normalized=normalized)
    # The input color can't be any other type
    else:
        raise TypeError("Argument must be either a type str | list | tuple")

    # Check if all R, G, B elements are the same type and in the correct range
    if isinstance(R, int) and isinstance(G, int) and isinstance(B, int):
        if not (0 <= R <= max_value and 0 <= G <= max_value and 0 <= B <= max_value) and clamp:
            raise ValueError(f"{depth}-bit integer types should be in range 0-{max_value}")
    elif isinstance(R, float) and isinstance(G, float) and isinstance(B, float):
        if not (0 <= R <= 1 and 0 <= G <= 1 and 0 <= B <= 1) and clamp:
            raise ValueError("Float types should be in range 0-1")
        # Convert to 0-max_value range if not normalized
        return (R, G, B) if normalized else tuple(round(i * max_value) for i in (R, G, B))
    else:
        raise TypeError("All elements must be the same type (int | float)")

    # Convert to 0-1 range if normalized
    return (R / max_value, G / max_value, B / max_value) if normalized else (R, G, B)


def check_hsw(vals: tuple | list, output: str = "round") -> tuple[int, int, int] | tuple[float, float, float] | tuple[int, float, float]:
    """### Checks if 3-element values HSW (W-wildcard, could be Lightness, Value, etc.) \
    have correct type of elements

    ### Args:
        `vals` (tuple | list): Tuple/list of 3 values or tuple/list containing 1 tuple/list with 3 values
        `output` (str, optional): Either "normalized", "round" or "half-normalized"
        * "normalized" returns values in range 0-1
        * "half-normalized" returns Hue in range 0-360, Saturation and Wildcard in range 0-1
        * "round" returns Hue in range 0-360, Saturation and Wildcard in range 0-100

    ### Returns:
        tuple[h, s, w]
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
            case "normalized":
                return H / 360, S / 100, W / 100
            case "half-normalized":
                return H, S / 100, W / 100
            case _:
                return vals

    if isinstance(H, float) and isinstance(S, float) and isinstance(W, float):
        if not 0 <= H <= 359 / 360:
            raise ValueError("Hue must be in range 0-0.9972!")
        if not (0 <= S <= 1 and 0 <= W <= 1):
            raise ValueError("The value must be in range 0-1!")

        match output:
            case "normalized":
                return vals
            case "half-normalized":
                return H * 360, S, W
            case _:
                return H * 360, S * 100, W * 100

    if isinstance(H, int) and isinstance(S, float) and isinstance(W, float):
        if not 0 <= H < 360:
            raise ValueError("Hue must be in range 0-359 degrees!")
        if not (0 <= S <= 1 and 0 <= W <= 1):
            raise ValueError("The value must be in range 0-1!")

        match output:
            case "normalized":
                return vals[0] / 360, S, W
            case "half-normalized":
                return vals
            case _:
                return H, S * 100, W * 100

    raise TypeError("All elements must be the same type (int | float) \
        or Hue - int, the rest - float")


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
        `normalized` (bool, optional): Wether to return the result in range 0-1 rather than the default range 0-100
        `big_float` (bool, optional): Wether the input XYZ values are floats in range 0-100

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
    output: str,
    depth: int = 8,
    clamp: bool = True,
    normalized_input: bool = False) -> str | tuple[int, int, int] | tuple [float, float, float]:
    """### Determines what to return based on input parameters
    #### N/B: All examples below are given for 8-bit color depth that has range 0-255. \
        If you want to use this function with a different depth the actual range is 0-(max value for bit depth).

    ### Args:
        `RGB` (tuple[r, g, b] | list[r, g, b]): The input color
        `output` (str): The desired type of output in: "hex", "hexp", "normalized", "direct" (Any)
        `depth` (int | float): The bit depth of the input RGB values. Defaults to 8-bit (range 0-255)
        `clamp` (bool, optional): Clamps the values in valid range. Ex. -1 to 0, 262 to 255 for range 0-255. Defaults to Ture.
        `normalized_input` (bool): Whether the R, G, B values are in range 0-1 or the default range 0-255

    ### Returns:
        tuple[r, g, b]
    """
    if depth % 1 != 0:
        raise ValueError("Depth value must be an integer number passed either as int or float")

    # Get the max value for the chosen bit depth
    length = (2 ** depth) - 1
    R, G, B = RGB

    # Clamp the values to a valid range
    if clamp:
        R, G, B = (max(min(i, 1.0), 0.0) if normalized_input else max(min(i, 255.0), 0.0) for i in (R, G, B))

    # Return desired output type based on input
    match output.lower().strip():
        case "hex" | "hexp":
            if normalized_input:
                R, G, B = (round(i * length) for i in (R, G, B))

            # Return new color in hex color format
            pound_sign = output.lower().strip() == "hexp"
            return co.rgb_to_hex(R, G, B, depth=depth, pound=pound_sign)
        case "round":
            return (round(R * length), round(G * length), round(B * length)) if normalized_input else (round(R), round(G), round(B))
        case "normalized":
            return (R, G, B) if normalized_input else (R / length, G / length, B / length)
        case _:
            return (R * length, G * length, B * length) if normalized_input else (R, G, B)


def return_hsw(
    HSW: tuple | list,
    output,
    normalized_input: bool = False) -> tuple[int, int, int] | tuple[float, float, float] | tuple[int, float, float]:
    """### Determines what to return based on input parameters

    ### Args:
        `HSW` (tuple | list): Hue, Saturation, Wildcard (Either Value, Lightness or Intensity)
        `output` (str): The desired type of output
        `normalized_input` (bool): Whether the H, S, W values are in range 0-1 or the default range 0-100

    ### Returns:
        tuple[h, s, w]
    """
    H, S, W = HSW
    match output.lower():
        case "round":
            return (min(round(H * 360), 359), round(S * 100), round(W * 100)) if normalized_input else (min(round(H), 359), round(S), round(W))
        case "normalized":
            return (H, S, W) if normalized_input else (H / 360, S / 100, W / 100)
        case "half-normalized":
            return (min(round(H * 360), 359), S, W) if normalized_input else (min(round(H), 359), S / 100, W / 100)
        case _:
            return (H * 360, S * 100, W * 100) if normalized_input else (H, S, W)


def return_scale(
    vals: tuple | list,
    output,
    min_max: tuple | list = (0, 100),
    clamp: bool = False,
    normalized_input: bool = False) -> tuple[int, int, int] | tuple[float, float, float]:
    """### Determines what to return based on input parameters

    ### Args:
        `HSW` (tuple | list): Hue, Saturation, Wildcard (Either Value, Lightness or Intensity)
        `output` (str): The desired type of output
        `normalized_input` (bool): Whether the H, S, W values are in range 0-1 or the default range 0-100

    ### Returns:
        tuple[h, s, w]
    """
    clamp = min_max if clamp else (-9999999999999, 9999999999999)

    match output.lower():
        case "round":
            return [max(min(round(i * min_max[1]), clamp[1]), clamp[0]) for i in vals] if normalized_input \
                else [max(min(round(i), clamp[1]), clamp[0]) for i in vals]
        case "normalized":
            if clamp == min_max:
                clamp = (0, 1) if 0 in min_max else (-1, 1)
            return [max(min(i, clamp[1]), clamp[0]) for i in vals] if normalized_input \
                else [max(min(i / min_max[1], clamp[1]), clamp[0]) for i in vals]
        case _:
            return [max(min(i * min_max[1], clamp[1]), clamp[0]) for i in vals] if normalized_input \
                else [max(min(i, clamp[1]), clamp[0]) for i in vals]
