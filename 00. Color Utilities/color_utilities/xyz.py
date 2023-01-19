"""
This module contains some information about converting from and to XYZ color space.
It contains a few functions and a number of constants regarding different color spaces.
"""
# pylint: disable=invalid-name, unsubscriptable-object

# More information: https://ninedegreesbelow.com/photography/srgb-color-space-to-profile.html
# More information: https://www.easyrgb.com/en/math.php


import numpy
from numpy.linalg import pinv

# Make it so that every floating point number numpy returns is displayed to the 15th digit after the decimal point
numpy.set_printoptions(formatter={'float': '{:0.15f}'.format}, suppress=True)


# TODO: Move this to a separate module or a JSON file
# More: http://brucelindbloom.com/index.html?WorkingSpaceInfo.html
# More: https://en.wikipedia.org/wiki/RGB_color_spaces
color_space_props = {
    #! The primaries only have x and y values because z = 1 - x - y
    #! The primary Yr, Yg, Yb (Luminance) can be found by using the res = working_space_matrix() function for
        #! the desired color space and using the second row of the output res[1]
    #! For reference and more infor use additionals.py
    "NTSC": {  # Source: http://brucelindbloom.com/index.html?WorkingSpaceInfo.html
        "illuminant": "C",  # D65 according to: https://en.wikipedia.org/wiki/RGB_color_spaces
        "primaries": {
            "xr": 0.67,   "yr": 0.33,
            "xg": 0.21,   "yg": 0.71,
            "xb": 0.14,   "yb": 0.08,
        },
        "gamma": 2.2,
        "decoding gamma": 20/9},
    "MUSE": {  # Source: https://en.wikipedia.org/wiki/RGB_color_spaces
        "illuminant": "D65",
        "primaries": {
            "xr": 0.63,   "yr": 0.34,
            "xg": 0.31,   "yg": 0.595,
            "xb": 0.155,  "yb": 0.07
        },
        "gamma": 2.5,
        "decoding gamma": 20/9},

    "APPLE RGB": {  # Source: http://brucelindbloom.com/index.html?WorkingSpaceInfo.html
        "illuminant": "D65",
        "primaries": {
            "xr": 0.625,  "yr": 0.34,
            "xg": 0.28,   "yg": 0.595,
            "xb": 0.155,  "yb": 0.07,
        },
        "gamma": 1.8},

    "PAL": {  # Source: http://brucelindbloom.com/index.html?WorkingSpaceInfo.html
        "illuminant": "D65",
        "primaries": {
            "xr": 0.64,   "yr": 0.33,
            "xg": 0.29,   "yg": 0.60,
            "xb": 0.15, "yb": 0.06,
        },
        "gamma": 2.8,
        "decoding gamma": 14/5},
    "SECAM": {  # Source: http://brucelindbloom.com/index.html?WorkingSpaceInfo.html
        "illuminant": "D65",
        "primaries": {
            "xr": 0.64,   "yr": 0.33,
            "xg": 0.29,   "yg": 0.60,
            "xb": 0.15,   "yb": 0.06,
        },
        "gamma": 2.8,
        "decoding gamma": 14/5},

    "SRGB": {  # Source: http://brucelindbloom.com/index.html?WorkingSpaceInfo.html & https://en.wikipedia.org/wiki/RGB_color_spaces
        "illuminant": "D65",
        "primaries": {
            "xr": 0.64,   "yr": 0.33,
            "xg": 0.30,   "yg": 0.60,
            "xb": 0.15,   "yb": 0.06,
        },
        "override_matrix": { #! An override matrix is one rounded by the color space inventor.
            "D65": {         #! It's different of the one calculated by any formula.
                "to_rgb": ((3.2406, -1.5372, -0.4986), (-0.9689, 1.8758, 0.0415), (0.0557, -0.2040, 1.0570)),
                "to_xyz": ((0.4124, 0.3576, 0.1805), (0.2126, 0.7152, 0.0722), (0.0193, 0.1192, 0.9505))
            }
        },
        "gamma": 2.2,  # The gamma is ~2.2 but the calculations are made using 2.4 due to old standards
        "decoding gamma": 12/5},
    "SCRGB": {  # Source: https://en.wikipedia.org/wiki/RGB_color_spaces
        "illuminant": "D65",
        "primaries": {
            "xr": 0.64,   "yr": 0.33,
            "xg": 0.30,   "yg": 0.60,
            "xb": 0.15,   "yb": 0.06,
        },
        "gamma": 2.2,
        "decoding gamma": 12/5},

    "HDTV": {  # Source: https://en.wikipedia.org/wiki/RGB_color_spaces
        "illuminant": "D65",
        "primaries": {
            "xr": 0.64,   "yr": 0.33,
            "xg": 0.30,   "yg": 0.60,
            "xb": 0.15,   "yb": 0.06
        },
        "gamma": 2.4,
        "decoding gamma": 20/9},
    "ADOBE RGB": {  # Source: http://brucelindbloom.com/index.html?WorkingSpaceInfo.html
        "illuminant": "D65",
        "primaries": {
            "xr": 0.64,   "yr": 0.33,
            "xg": 0.21,   "yg": 0.71,
            "xb": 0.15,   "yb": 0.06,
        },
        "gamma": 563/256, # 2.19921875 rounded to 2.2
        "decoding gamma": 563/256},
    "M.A.C": {  # Source: https://en.wikipedia.org/wiki/RGB_color_spaces
        "illuminant": "D65",
        "primaries": {
            "xr": 0.67,   "yr": 0.33,
            "xg": 0.21,   "yg": 0.71,
            "xb": 0.14,   "yb": 0.08
        },
        "gamma": 2.8},
    "NTSC-FCC": {  # Source: https://en.wikipedia.org/wiki/RGB_color_spaces
        "illuminant": "C",
        "primaries": {
            "xr": 0.67,   "yr": 0.33,
            "xg": 0.21,   "yg": 0.71,
            "xb": 0.14,   "yb": 0.08
        },
        "gamma": 2.5,
        "decoding gamma": 11/5},
    "PAL-M": {  # Source: https://en.wikipedia.org/wiki/RGB_color_spaces
        "illuminant": "C",
        "primaries": {
            "xr": 0.67,   "yr": 0.33,
            "xg": 0.21,   "yg": 0.71,
            "xb": 0.14,   "yb": 0.08
        },
        "gamma": 2.2},
    "ECI RGB": {  # Source: http://brucelindbloom.com/index.html?WorkingSpaceInfo.html
        "illuminant": "D50",
        "primaries": {
            "xr": 0.67,   "yr": 0.33,
            "xg": 0.21,   "yg": 0.71,
            "xb": 0.14,   "yb": 0.08
        },
        "gamma": 1.8,
        "decoding gamma": 3},

    "DISPLAY P3": {  # Source: https://en.wikipedia.org/wiki/RGB_color_spaces
        "illuminant": "D65",
        "primaries": {
            "xr": 0.68,   "yr": 0.32,
            "xg": 0.265,  "yg": 0.69,
            "xb": 0.15,   "yb": 0.06
        },
        "gamma": 2.2,
        "decoding gamma": 12/5},
    "UHDTV": {  # Source: https://en.wikipedia.org/wiki/RGB_color_spaces
        "illuminant": "D65",
        "primaries": {
            "xr": 0.708,  "yr": 0.292,
            "xg": 0.170,  "yg": 0.797,
            "xb": 0.131,  "yb": 0.046
        },
        "gamma": 2.4},
    "WIDE GAMUT": {  # Source: http://brucelindbloom.com/index.html?WorkingSpaceInfo.html
        "illuminant": "D50",
        "primaries": {
            "xr": 0.735,  "yr": 0.265,
            "xg": 0.115,  "yg": 0.826,
            "xb": 0.157, "yb": 0.018,
        },
        "gamma": 2.2,
        "decoding gamma": 563/256},
    "RIMM" : {  # Source: https://en.wikipedia.org/wiki/RGB_color_spaces
        "illuminant": "D50",
        "primaries": {
            "xr": 0.7347, "yr": 0.2653,
            "xg": 0.1596, "yg": 0.8404,
            "xb": 0.0366, "yb": 0.0001
        },
        "gamma": 2.222,
        "decoding gamma": 20/9},

    "PROPHOTO" : {  # Source: http://brucelindbloom.com/index.html?WorkingSpaceInfo.html
        "illuminant": "D50",
        "primaries": {
            "xr": 0.734699, "yr": 0.265301,
            "xg": 0.159597, "yg": 0.840403,
            "xb": 0.036598, "yb": 0.000105,
        },
        "gamma": 1.8,
        "decoding gamma": 9/5},
    "ROMM ": {
        "illuminant": "D50",
        "primaries": {
            "xr": 0.7347, "yr": 0.2653,
            "xg": 0.1596, "yg": 0.8404,
            "xb": 0.0366, "yb": 0.0001
        },
        "gamma": 1.8},

    "CIE RGB": {  # Source: http://brucelindbloom.com/index.html?WorkingSpaceInfo.html & https://en.wikipedia.org/wiki/RGB_color_spaces
        "illuminant": "E",
        "primaries": {
            "xr": 0.7347, "yr": 0.2653,
            "xg": 0.2738, "yg": 0.7174,
            "xb": 0.1666, "yb": 0.0089,
        },
        "gamma": 2.2},
    "BEST RGB": {  # Source: http://brucelindbloom.com/index.html?WorkingSpaceInfo.html
        "illuminant": "D50",
        "primaries": {
            "xr": 0.7347, "yr": 0.2653,
            "xg": 0.215,  "yg": 0.775,
            "xb": 0.13,   "yb": 0.035,
        },
        "gamma": 2.2},
    "BETA RGB": {  # Source: http://brucelindbloom.com/index.html?WorkingSpaceInfo.html
        "illuminant": "D50",
        "primaries": {
            "xr": 0.6888, "yr": 0.3112,
            "xg": 0.1986, "yg": 0.7551,
            "xb": 0.1265, "yb": 0.0352,
        },
        "gamma": 2.2},
    "BRUCE RGB": {  # Source: http://brucelindbloom.com/index.html?WorkingSpaceInfo.html
        "illuminant": "D65",
        "primaries": {
            "xr": 0.64,   "yr": 0.33,
            "xg": 0.28,   "yg": 0.65,
            "xb": 0.15,   "yb": 0.06,
        },
        "gamma": 2.2},
    "COLORMATCH RGB": {  # Source: http://brucelindbloom.com/index.html?WorkingSpaceInfo.html
        "illuminant": "D50",
        "primaries": {
            "xr": 0.63,   "yr": 0.34,
            "xg": 0.295,  "yg": 0.605,
            "xb": 0.15,   "yb": 0.075,
        },
        "gamma": 1.8},
    "DON RGB": {  # Source: http://brucelindbloom.com/index.html?WorkingSpaceInfo.html
        "illuminant": "D50",
        "primaries": {
            "xr": 0.696,  "yr": 0.3,
            "xg": 0.215,  "yg": 0.765,
            "xb": 0.13,   "yb": 0.035,
        },
        "gamma": 2.2},
    "EKTA SPACE PS5": {  # Source: http://brucelindbloom.com/index.html?WorkingSpaceInfo.html
        "illuminant": "D50",
        "primaries": {
            "xr": 0.695,  "yr": 0.305,
            "xg": 0.26,   "yg": 0.7,
            "xb": 0.11,   "yb": 0.005,
        },
        "gamma": 2.2},
    "SMPTE-C RGB": {  # Source: http://brucelindbloom.com/index.html?WorkingSpaceInfo.html
        "illuminant": "D65",
        "primaries": {
            "xr": 0.63,   "yr": 0.34,
            "xg": 0.31,   "yg": 0.595,
            "xb": 0.155,  "yb": 0.07,
        },
        "gamma": 2.2},
    "REC 2020": {  # Source: http://www.russellcottrell.com/photo/matrixCalculator.htm
        "illuminant": "D65",
        "primaries": {
            "xr": 0.708,   "yr": 0.292,
            "xg": 0.170,   "yg": 0.797,
            "xb": 0.131,   "yb": 0.046,
        },
        "gamma": 2.4},
    }


#= More info: http://www.brucelindbloom.com/index.html?Eqn_XYZ_to_Lab.html
#= More info: https://en.wikipedia.org/wiki/CIELAB_color_space
#= More info: http://www.russellcottrell.com/photo/matrixCalculator.htm
#+ ϵ = 0.008856 # Actual CIE standard
#+ ϵ = 216 / 24389 # Intent of the CIE standard
#+ κ = 903.3 # Actual CIE standard
#+ κ = 24389 / 27 # Intent of the CIE standard
CIE_E = 216 / 24389 # 0.008856  # epsilon
CIE_K = 24389 / 27 # 903.3  # kappa
KODAK_E = 1/512 # 0.001953 # Actual Kodak standard
BETA = 0.018053968510807
ALPHA = 1.09929682680944 // 10 * BETA ** 0.55

# http://brucelindbloom.com/index.html?Eqn_ChromAdapt.html
# https://ninedegreesbelow.com/photography/srgb-color-space-to-profile.html
# https://en.wikipedia.org/wiki/Illuminant_D65
# Tristimulus values for different illuminants and observers
ILLUMINANTS = {
    # 2° Observer angle
    '2': {
        'A':   (1.09850, 1.00000, 0.35585),
        'B':   (0.99072, 1.00000, 0.85223),
        'C':   (0.98074, 1.00000, 1.18232),
        'D50': (0.96422, 1.0000,  0.82521),
        'D55': (0.95682, 1.00000, 0.92149),
        'D65': (0.95047, 1.00000, 1.08883),  # Calculated from primaries
        'D75': (0.94972, 1.00000, 1.22638),
        'E':   (1.00000, 1.00000, 1.00000),
        'F1':  (0.92834, 1.00000, 1.03665),
        'F2':  (0.99186, 1.00000, 0.67393),
        'F3':  (1.03754, 1.00000, 0.49861),
        'F4':  (1.09147, 1.00000, 0.38813),
        'F5':  (0.90872, 1.00000, 0.98723),
        'F6':  (0.97309, 1.00000, 0.60191),
        'F7':  (0.95041, 1.00000, 1.08747),
        'F8':  (0.96413, 1.00000, 0.82333),
        'F9':  (1.00365, 1.00000, 0.67868),
        'F10': (0.96174, 1.00000, 0.81712),
        'F11': (1.00962, 1.00000, 0.64350),
        'F12': (1.08046, 1.00000, 0.39228),
        'CIE D65': (0.9504,  1.0000,  1.0889 ),  # From CIE 15.2
        'ICC D50': (0.9642, 1.0000, 0.8249) # Not rounded, from actual ICC spec values
    },
    # 10° Observer angle
    '10': {
        'A':   (1.11144,  1.00000, 0.35200),
        'B':   (0.990927, 1.00000, 0.35200),
        'C':   (0.97285,  1.00000, 1.16145),
        'D50': (0.96720,  1.00000, 0.81427),
        'D55': (0.95799,  1.00000, 0.90926),
        'D65': (0.94811,  1.00000, 1.07304),
        'D75': (0.94416,  1.00000, 1.20641),
        'E':   (1.00000,  1.00000, 1.00000),
        'F1':  (0.94791,  1.00000, 1.03191),
        'F2':  (1.03280,  1.00000, 0.69026),
        'F3':  (1.08968,  1.00000, 0.51965),
        'F4':  (1.14961,  1.00000, 0.40963),
        'F5':  (0.93369,  1.00000, 0.98636),
        'F6':  (1.02148,  1.00000, 0.62074),
        'F7':  (0.95792,  1.00000, 1.07687),
        'F8':  (0.97115,  1.00000, 0.81135),
        'F9':  (1.02116,  1.00000, 0.67826),
        'F10': (0.99001,  1.00000, 0.83134),
        'F11': (1.03866,  1.00000, 0.65627),
        'F12': (1.11428,  1.00000, 0.40353)
    }
}

# Monitor tristimulus values
# DXX = (0.95105, 1.00000, 1.085480)

# Chromatic Adaptation Matrices
# http://brucelindbloom.com/Eqn_ChromAdapt.html
# More about CATs: https://colorjs.io/docs/adaptation.html
# [Ma] #~ Used for RGB to XYZ. Invert for the other way around
ADAPTATION_MATRICES = { # Also known as CATs (Chromatic Adaptation Tables)
    "xyz_scaling": numpy.array((
        (1.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        (0.0, 0.0, 1.0))),
    "bradford": numpy.array((
        ( 0.8951,  0.2664, -0.1614),
        (-0.7502,  1.7135,  0.0367),
        ( 0.0389, -0.0685,  1.0296))),
    "von_kries": numpy.array((
        ( 0.40024, 0.70760, -0.08081),
        (-0.22630, 1.16532,  0.04570),
        ( 0.00000, 0.00000,  0.91822))),
    "fairchild" : numpy.array((
        ( 0.8562,  0.3372, -0.1934),
        (-0.8360,  1.8327,  0.0033),
        ( 0.0357, -0.0469,  1.0112))),
    "ciecat02": numpy.array((
        ( 0.7328, 0.4296, -0.1624),
        (-0.7036, 1.6975,  0.0061),
        ( 0.0030, 0.0136,  0.9834))),
    "sharp": numpy.array((
        ( 1.2694, -0.0988, -0.1706),
        (-0.8364,  1.8006,  0.0357),
        ( 0.0297, -0.0315,  1.0018))),
    "cmccat97": numpy.array((   # Like a rearranged bradford matrix
        ( 0.8951, -0.7502, -0.0389),
        ( 0.2664,  1.7135,  0.0685),
        (-0.1614,  0.0367,  1.0296))),
    "cmccat2000": numpy.array((
        ( 0.7982, 0.3389, -0.1371),
        (-0.5918, 1.5512,  0.0406),
        ( 0.0008, 0.0239,  0.9753))),
    "cat02_brill2008": numpy.array((
        ( 0.7328, 0.4296, -0.1624),
        (-0.7036, 1.6975,  0.0061),
        ( 0.000,  0.0000,  1.0000))),
    "cat16": numpy.array((
        ( 0.401288, 0.650173, -0.051461),
        (-0.250268, 1.204414,  0.045854),
        (-0.002079, 0.048952,  0.953127))),
    "bianco2010": numpy.array((
        ( 0.8752, 0.2787, -0.1539),
        (-0.8904, 1.8709,  0.0195),
        (-0.0061, 0.0162,  0.9899))),
    "pc_bianco2010": numpy.array((
        ( 0.6489, 0.3915, -0.0404),
        (-0.3775, 1.3055,  0.0720),
        (-0.0271, 0.0888,  0.9383))),
    "hun-pointer-estevez": numpy.array((
        ( 0.38971, 0.68898, -0.07868),
        (-0.22981, 1.18340,  0.04641),
        ( 0.00000, 0.00000,  1.00000)))
}


def get_adaptation_matrix(wp_src: tuple | list, wp_dst: tuple | list, adaptation: str = "bradford"):
    """### Calculate the correct transformation matrix based on origin and target
    illuminants. The observer angle must be the same between illuminants.

    ### Args:
        `wp_src` (tuple | list): The tristimulus values for the source illuminant
        `wp_dst` (tuple | list): The tristimulus values for the target illuminant
        `adaptation` (str): The adaptation matrix to be used for the conversion. Defaults to "bradford"

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

    ### Detailed conversion documentation is available at:
    http://brucelindbloom.com/Eqn_ChromAdapt.html

    ### Returns:
        numpy.ndarray: 3x3 matrix for calculating values between illuminants
    """

    # Get the appropriate transformation matrix, [MsubA].
    Ma = ADAPTATION_MATRICES[adaptation]

    # Sharpened cone responses ~ rho gamma beta ~ sharpened r g b
    rgb_src = Ma @ wp_src
    rgb_dst = Ma @ wp_dst

    # Ratio of whitepoint sharpened responses
    m_rat = numpy.diag(rgb_dst / rgb_src)

    #= Manual calculation mathod
    # diag_matrix = ((rgb_dst[0] / rgb_src[0], 0, 0),
    #               (0, rgb_dst[1] / rgb_src[1], 0),
    #               (0, 0, rgb_dst[2] / rgb_src[2]))

    # Final transformation matrix
    return pinv(Ma) @ m_rat @ Ma


def apply_chromatic_adaptation(
    XYZ: tuple | list,
    orig_illum: str,
    targ_illum: str,
    observer: str = "2",
    adaptation="bradford"):
    """### Applies a chromatic adaptation matrix to convert XYZ values between
    illuminants. It is important to recognize that color transformation results
    in color errors, determined by how far the original illuminant is from the
    target illuminant. For example, D65 to A could result in very high maximum
    deviance.

    ### An informative article with estimate average Delta E values for each
    illuminant conversion may be found at: http://brucelindbloom.com/ChromAdaptEval.html

    ### Args:
        `XYZ` (tuple | list): The X, Y, Z values we want to apply the chromatic adaptation to
        `orig_illum` (str): The illuminant of the XYZ color
        `targ_illum` (str): The illuminant we want to convert the XYZ values to
        `observer` (str, optional): The observer angle of the illuminants. Defaults to "2".
        `adaptation` (str, optional): The adaptation method (matrix) to be used for the conversion. Defaults to "bradford".

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

    Available adaptation matrices:
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

    ### Returns:
        numpy.ndarray: 1x3 matrix (array) containing the new X, Y, Z values
    """
    # It's silly to have to do this, but some people may want to call this
    # function directly, so we'll protect them from messing up upper/lower case.
    adaptation = adaptation.lower()

    # Get white-points for illuminant
    wp_src = ILLUMINANTS[observer][orig_illum]
    wp_dst = ILLUMINANTS[observer][targ_illum]

    # Retrieve the appropriate transformation matrix from the constants.
    transform_matrix = get_adaptation_matrix(wp_src, wp_dst, adaptation)

    # Perform the adaptation via matrix multiplication.
    return transform_matrix @ XYZ


def refine_args(
    *,
    illuminant: str = None,
    observer: str | int | float = None,
    color_space: str = None,
    adaptation: str = None) -> tuple:
    """### Makes sure the input arguments are the correct type. Appropriate errors are raised otherwise

    ### Args:
        `illuminant` (str): The illuminant should be an all caps string
        `observer` (int | float | str): The observer angle should be a string
        `color_space` (str): The color space should be an all caps string
        `adaptation` (str): The adaptation method should be all lowercase string

    ### All arguments default to None so the function can be used for any combination of them

    ### Returns:
        tuple: All taken arguments + rgb_illum which is the default illuminant for the chosen color_space
    """
    # Check if illuminant is correct type and among of available illuminants
    if illuminant:
        if not isinstance(illuminant, str):
            raise TypeError("Iluminant must be a string type!")
        illuminant = illuminant.upper().strip()
        acc_tristimulus = list(ILLUMINANTS['2'])
        if illuminant not in acc_tristimulus:
            raise ValueError(f'Illuminant "{illuminant}" is not supported! Please choose from:\n{acc_tristimulus}')

    # Check (and fix) the observer angle type
    if observer:
        if not isinstance(observer, (str, int, float)) and observer is not None:
            raise TypeError("Observer must be str | int | float type!")
        if isinstance(observer, (int, float)):
            observer = str(int(observer))

    # Create an empty variable in case there's no color space input
    rgb_illum = None

    # Check adaptation input
    if adaptation:
        adaptation = adaptation.lower().strip()

    # Check color space input
    if color_space:
        color_space = color_space.upper().strip()

        # Find the iluminant of the requested color space
        if rgb_illum := color_space_props.get(color_space):
            rgb_illum = rgb_illum["illuminant"]
        else:
            raise ValueError(f'The "{color_space}" color space is not supported! '
                            f'Please choose one of the following:\n{list(color_space_props)}')

    return (i for i in (illuminant, observer, color_space, adaptation, rgb_illum) if i)


def working_space_matrix(
    color_space: str,
    illuminant: str = None,
    observer: str | int | float = "2",
    adaptation: str = "bradford",
    to_xyz: bool = True):
    """### Calculates (Generates) the working space matrix for a given color_space

    #### In every matrix converting to XYZ, the sum of all values in a row equals the illuminant's corresponding value
    * Example: ((0.4124564, 0.3575761, 0.1804375), (0.2126729, 0.7151522, 0.0721750), (0.0193339, 0.1191920, 0.9503041))
    * D65, observer2 = (0.95047, 1.00000, 1.08883)

    ### Args:
        `color_space` (str): The color space that the values will be calculated for
        `illuminant` (str, optional): The illuminant of the X, Y, Z values we want to convert to/from
        `observer` (str | int | float, optional): The observer angle of the X, Y, Z values we want to
                                                convert to/from. Defaults to "2".
        `adaptation` (str, optional): The adaptation method (matrix) to be used for the conversion. Defaults to "bradford".
        `to_xyz` (bool, optional): If the generated matrix will be used for converting to XYZ values or
                                    from XYZ values to something else. Defaults to True (Converting to XYZ).

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

    Available adaptation matrices:
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

    ### References:
    http://www.brucelindbloom.com/index.html?Eqn_RGB_XYZ_Matrix.html
    http://brucelindbloom.com/index.html?Eqn_ChromAdapt.html
    https://www.color.org/chadtag.xalter

    ### Returns:
        tuple[tuple[float, float, float], tuple[float, float, float], tuple[float, float, float]]:
        A 3x3 conversion matrix in the form of a tuple
    """

    # It target illuminant isn't specified, assume it's the color space's default illuminant
    if not illuminant:
        illuminant = color_space_props[color_space]["illuminant"]

    illuminant, observer, color_space, adaptation, rgb_illum = refine_args(
        illuminant=illuminant, observer=observer, color_space=color_space, adaptation=adaptation)

    # Get the primary values for the requested color space
    xr, yr, xg, yg, xb, yb = tuple(color_space_props[color_space]["primaries"].values())

    # Get the reference white for the color space's illuminant at observer 2
    Xw, Yw, Zw = ILLUMINANTS["2"][rgb_illum]

    # Calculate XYZ for the RGB using primaries
    (Xr, Yr, Zr), (Xg, Yg, Zg), (Xb, Yb, Zb) = [(i / j, 1, (1 - i - j) / j) for  i, j in ((xr, yr), (xg, yg), (xb, yb))]

    # Compose a 3x3 matrix with X, Y, Z values for the RGB and invert it
    m = pinv(((Xr, Xg, Xb), (Yr, Yg, Yb), (Zr, Zg, Zb)))

    # Calculate Sr, Sg, Sb later used for the final matrix
    Sr, Sg, Sb = m @ (Xw, Yw, Zw)
    # Calculate the final matrix
    M = ((Sr*Xr, Sg*Xg, Sb*Xb), (Sr*Yr, Sg*Yg, Sb*Yb), (Sr*Zr, Sg*Zg, Sb*Zb))

    # Return the proper matrix if the requested illuminant is the same as the color space's default
    if illuminant == rgb_illum:
        return M if to_xyz else tuple(tuple(i) for i in pinv(M))

    # Get the chromatic adaptation matrix for the requested illuminant
    adaptation = get_adaptation_matrix(
        ILLUMINANTS[observer][rgb_illum],
        ILLUMINANTS[observer][illuminant],
        adaptation)

    # Apply the chromatic adaptation matrix to the final matrix
    convert_to_illum = adaptation @ M

    # Return the proper matrix
    return tuple(tuple(i) for i in convert_to_illum) if to_xyz else tuple(tuple(i) for i in pinv(convert_to_illum))
