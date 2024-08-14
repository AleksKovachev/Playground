"""Constants used throughout the library"""

from collections.abc import Sequence
from enum import Enum


Color = str | int | float | Sequence[int, int, int] | Sequence[float, float, float]
Color_geo = int | float | Sequence[int, int, int] | Sequence[float, float, float]
Color_seq = str | Sequence[int, int, int] | Sequence[float, float, float]
Color_out1 = str | tuple[int, int, int] | tuple[float, float, float]
Color_out_seq = tuple[int, int, int] | tuple[float, float, float]
Color_out_hsw = tuple[int, int, int] | tuple[float, float, float] | tuple[int, float, float]
Out = Enum

class Out1(Enum):
    """Defines the output type of a given function

    * `hex` returns a hex string color in the form of `decade`
    * `hexp` returns a hex string color in the form of `#facade`
    * `normalized` returns a tuple(R, G, B) where the values are floats in range 0-1
    * `round` returns a tuple(R, G, B) where the values are integers in range 0-255
    * `direct` returns a tuple(R, G, B) where the values are floats in range 0-255
    """
    HEX = 0
    HEXP = 1
    ROUND = 2
    NORMALIZED = 3
    DIRECT = 4


class Out2(Enum):
    """Defines the output type of a given function

    * `round` returns a tuple(R, G, B) where the values are integers in range 0-100
    * `normalized` returns a tuple(R, G, B) where the values are floats in range 0-1
    * `half-normalized` returns a tuple(R, G, B) where the first value is an int in range 0-359
                        and the rest are floats in range 0-1
    * `direct` returns a tuple(R, G, B) where the values are floats in range 0-100
    """
    ROUND = 0
    NORMALIZED = 1
    HALF_NORMALIZED = 2
    DIRECT = 3


class Out3(Enum):
    """Defines the output type of a given function

    * `round` returns a tuple(R, G, B) where the values are integers in range 0-100
    * `normalized` returns a tuple(R, G, B) where the values are floats in range 0-1
    * `direct` returns a tuple(R, G, B) where the values are floats in range 0-100
    """
    ROUND = 0
    NORMALIZED = 1
    DIRECT = 2
