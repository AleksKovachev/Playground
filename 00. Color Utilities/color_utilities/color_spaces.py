"""This module conly contains dictionaries full of information about different color spaces"""
# More: http://brucelindbloom.com/index.html?WorkingSpaceInfo.html
# More: https://en.wikipedia.org/wiki/RGB_color_spaces

from functools import partial
from . import transfer_functions as tf


#! The primaries only have x and y values because z = 1 - x - y
#! The primary Yr, Yg, Yb (Luminance) can be found by using the res = working_space_matrix() function for
    #! the desired color space and using the second row of the output res[1]
#! For reference and more infor use additionals.py

#+ The ones that start with "__" aren't checked yet. Their gamma should be checked and
#!  the matrix calculation should be checked if it calculates the same as override (so the override could be removed)
#! Note that 525-line and 625-line encodings were previously designated NTSC and PAL respectively in ITU-R BT.1700.
#! An override matrix is one rounded by the color space inventor. It's different of the one calculated by any formula.
#! Display gamma = EOTF
color_spaces = {
    "ACES2065-1": {
        "illuminant": "ACES",
        "primaries": {
            "xr": 0.7347, "yr":  0.2653,
            "xg": 0,      "yg":  1,
            "xb": 0.0001, "yb": -0.077,
        },
        "whitepoint": (0.32168, 0.33767),
        "override_matrix": {  # Uses CAT_02 for conversion
            "to_rgb": ((1.04981102, 0.0, -0.00009748), (-0.49590302, 1.37331305, 0.09824004), (0.0, 0.0, 0.99125202)),
            "to_xyz": ((0.9525524, 0.0,  0.00009368), (0.34396645, 0.7281661, -0.07213255), (0.0, 0.0, 1.00882518))
        }, #+ Calculation should be the same as override
        "transfer function": lambda x: x},  # http://j.mp/TB-2014-004

    "ACEScc": {
        "illuminant": "ACES",
        "primaries": {
            "xr": 0.713, "yr": 0.293,
            "xg": 0.165, "yg": 0.83,
            "xb": 0.128, "yb": 0.044,
        },
        "whitepoint": (0.32168, 0.33767),
        "override_matrix": {  # Uses CAT_02 for conversion
            "to_rgb": ((1.64102338, -0.32480329, -0.2364247), (-0.66366286, 1.61533159, 0.01675635), (0.01172189, -0.00828444, 0.98839486)),
            "to_xyz": ((0.66245418, 0.13400421, 0.15618769), (0.27222872, 0.67408177, 0.05368952), (-0.00557465, 0.00406073, 1.0103391))
        }, #+ Calculation should be the same as override
        "transfer function": tf.acescc},

    "ACEScct": {
        "illuminant": "ACES",
        "primaries": {
            "xr": 0.713, "yr": 0.293,
            "xg": 0.165, "yg": 0.83,
            "xb": 0.128, "yb": 0.044,
        },
        "whitepoint": (0.32168, 0.33767),
        "override_matrix": {  # Uses CAT_02 for conversion
            "to_rgb": ((1.64102338, -0.32480329, -0.2364247), (-0.66366286, 1.61533159, 0.01675635), (0.01172189, -0.00828444, 0.98839486)),
            "to_xyz": ((0.66245418, 0.13400421, 0.15618769), (0.27222872, 0.67408177, 0.05368952), (-0.00557465, 0.00406073, 1.0103391))
        }, #+ Calculation should be the same as override
        "transfer function": tf.acescct},

    "ACEScg": {
        "illuminant": "",
        "primaries": {
            "xr": 0.713, "yr": 0.293,
            "xg": 0.165, "yg": 0.83,
            "xb": 0.128, "yb": 0.044,
        },
        "whitepoint": (0.32168, 0.33767),
        "override_matrix": {  # Uses CAT_02 for conversion
            "to_rgb": ((1.64102338, -0.32480329, -0.2364247), (-0.66366286, 1.61533159, 0.01675635), (0.01172189, -0.00828444, 0.98839486)),
            "to_xyz": ((0.66245418, 0.13400421, 0.15618769), (0.27222872, 0.67408177, 0.05368952), (-0.00557465, 0.00406073, 1.0103391))
        }, #+ Calculation should be the same as override
        "transfer function": lambda x: x},  # http://j.mp/S-2014-004

    "ACESproxy": {
        "illuminant": "ACES",
        "primaries": {
            "xr": 0.713, "yr": 0.293,
            "xg": 0.165, "yg": 0.83,
            "xb": 0.128, "yb": 0.044,
        },
        "whitepoint": (0.32168, 0.33767),
        "override_matrix": {  # Uses CAT_02 for conversion
            "to_rgb": ((1.64102338, -0.32480329, -0.2364247), (-0.66366286, 1.61533159, 0.01675635), (0.01172189, -0.00828444, 0.98839486)),
            "to_xyz": ((0.66245418, 0.13400421, 0.15618769), (0.27222872, 0.67408177, 0.05368952), (-0.00557465, 0.00406073, 1.0103391))
        }, #+ Calculation should be the same as override
        "transfer function": tf.acesproxy},

    "ARRI WIDE GAMUT 3": {
        "illuminant": "D65",
        "primaries": {
            "xr": 0.684,  "yr":  0.313,
            "xg": 0.221,  "yg":  0.848,
            "xb": 0.0861, "yb": -0.102,
        },
        "whitepoint": (0.3127, 0.329),
        "override_matrix": {
            "to_rgb": ((1.789066, -0.482534, -0.200076), (-0.639849, 1.3964, 0.194432), (-0.041532, 0.082335, 0.878868)),
            "to_xyz": ((0.638008, 0.214704, 0.097744), (0.291954, 0.823841, -0.115795), (0.002798, -0.067034, 1.153294)),
            "to_aces": ((0.680205, 0.236137, 0.083658), (0.085415, 1.017471, -0.102886), (0.002057, -0.062563, 1.060506))
        }, #+ Actual override matrix
        "transfer function": tf.arri_log_c3},

    "ARRI WIDE GAMUT 4": {
        "illuminant": "D65",
        "primaries": {
            "xr": 0.7347, "yr":  0.2653,
            "xg": 0.1424, "yg":  0.8576,
            "xb": 0.0991, "yb": -0.0308,
        },
        "whitepoint": (0.3127, 0.329),
        "override_matrix": { # Uses CAT_02 for conversion
            "to_rgb": ((1.50921547, -0.25059735, -0.16881148), (-0.49154545, 1.36124555, 0.09728294), (0.0, 0.0, 0.91822495)),
            "to_xyz": ((0.704858320407232064, 0.129760295170463003, 0.115837311473976537),
                        (0.254524176404027025, 0.781477732712002049, -0.036001909116029039),
                        (0.0, 0.0, 1.089057750759878429)),
            "aces_to": ((0.750957362824734131, 0.144422786709757084, 0.104619850465508965),
                        (0.000821837079380207, 1.007397584885003194, -0.008219421964383583),
                        (-0.000499952143533471, -0.000854177231436971, 1.001354129374970370))
        }, #+ Actual override matrix
        "transfer function": tf.arri_log_c4},

    "ADOBE RGB": {  # Source: http://brucelindbloom.com/index.html?WorkingSpaceInfo.html
        "illuminant": "D65",
        "primaries": {
            "xr": 0.64, "yr": 0.33,
            "xg": 0.21, "yg": 0.71,
            "xb": 0.15, "yb": 0.06,
        },
        "whitepoint": (0.3127, 0.329),
        "override_matrix": {
            "to_rgb": ((2.04159, -0.56501, -0.34473), (-0.96924, 1.87597, 0.04156), (0.01344, -0.11836, 1.01517)),
            "to_xyz": ((0.57667, 0.18556, 0.18823), (0.29734, 0.62736, 0.07529), (0.02703, 0.07069, 0.99134))
        }, #+ Actual override matrix
        "transfer function": partial(tf.gamma_function, gamma=563/256)},  # gamma = 563/256 = 2.19921875 rounded to 2.2

    "ADOBE WIDE GAMUT RGB": {  # Source: http://brucelindbloom.com/index.html?WorkingSpaceInfo.html
        "illuminant": "D50",
        "primaries": {
            "xr": 0.7347, "yr": 0.2653,
            "xg": 0.1152, "yg": 0.8264,
            "xb": 0.1566, "yb": 0.0177,
        },
        "whitepoint": (0.3457, 0.3585),
        "override_matrix": {
            "to_rgb": ((1.46230418, -0.18452564, -0.27338105), (-0.52286828, 1.4479884, 0.06812617), (0.03460045, -0.09581963, 1.28766046)),
            "to_xyz": ((0.71650072, 0.10102057, 0.14677439), (0.25872824, 0.72468231, 0.01658944), (0.0, 0.05121182, 0.77389278))
        }, #+ Calculation should be the same as override
        "transfer function": partial(tf.gamma_function, gamma=563/256)},  # gamma = 563/256 = 2.19921875 rounded to 2.2

    "APPLE RGB": {  # Source: http://brucelindbloom.com/index.html?WorkingSpaceInfo.html
        "illuminant": "D65",
        "primaries": {
            "xr": 0.625, "yr": 0.34,
            "xg": 0.28,  "yg": 0.595,
            "xb": 0.155, "yb": 0.07,
        },
        "whitepoint": (0.3127, 0.329),
        "override_matrix": {
            "to_rgb": ((2.95197848, -1.2896043, -0.47391531), (-1.08508357, 1.99080934, 0.03720168), (0.08547221, -0.26942971, 1.09102767)),
            "to_xyz": ((0.44966162, 0.31625612, 0.18453819), (0.24461592, 0.67204425, 0.08333983), (0.02518105, 0.14118577, 0.92269093))
        }, #+ Calculation should be the same as override
        "transfer function": partial(tf.gamma_function, gamma=1.8)},

    "BEST RGB": {  # Source: http://brucelindbloom.com/index.html?WorkingSpaceInfo.html
        "illuminant": "D50",
        "primaries": {
            "xr": 0.7347, "yr": 0.2653,  # "xr": 0.73519164, "yr": 0.26480836,
            "xg": 0.215,  "yg": 0.775,   # "xg": 0.21533613, "yg": 0.77415966,
            "xb": 0.13,   "yb": 0.035,   # "xb": 0.13012295, "yb": 0.03483607,
        },
        "whitepoint": (0.3457, 0.3585),
        "override_matrix": {
            "to_rgb": ((1.75737181, -0.48538023, -0.25359913), (-0.54199672, 1.50475404, 0.02168337), (0.00666215, -0.01849623, 1.22659836)),
            "to_xyz": ((0.6318944, 0.20538793, 0.12701335), (0.22760177, 0.73839465, 0.03400357), (0.0, 0.01001892, 0.81508568))
        }, #+ Calculation should be the same as override
        "transfer function": partial(tf.gamma_function, gamma=2.2)},

    "BETA RGB": {  # Source: http://brucelindbloom.com/index.html?WorkingSpaceInfo.html
        "illuminant": "D50",
        "primaries": {
            "xr": 0.6888, "yr": 0.3112,
            "xg": 0.1986, "yg": 0.7551,
            "xb": 0.1265, "yb": 0.0352,
        },
        "whitepoint": (0.3457, 0.3585),
        "override_matrix": {
            "to_rgb": ((1.68297071, -0.42817109, -0.23598255), (-0.77107152, 1.70666472, 0.04469277), (0.04000653, -0.08854917, 1.27253082)),
            "to_xyz": ((0.6713559, 0.17457238, 0.11836739), (0.30331875, 0.66374423, 0.03293701), (0.0, 0.04069839, 0.78440621))
        }, #+ Calculation should be the same as override
        "transfer function": partial(tf.gamma_function, gamma=2.2)},

    "BLACKMAGIC WIDE GAMUT": {
        "illuminant": "Blackmagic Wide Gamut",
        "primaries": {
            "xr": 0.7177215, "yr":  0.3171181,
            "xg": 0.228041,  "yg":  0.861569,
            "xb": 0.1005841, "yb": -0.0820452,
        },
        "whitepoint": (0.312717, 0.3290312),
        "override_matrix": {
            "to_rgb": ((1.866382, -0.518397, -0.23461), (-0.600342, 1.378149, 0.176732), (0.002452, 0.0864, 0.836943)),
            "to_xyz": ((0.60653, 0.220408, 0.123479), (0.267989, 0.832731, -0.10072), (-0.029442, -0.086611, 1.204861))
        }, #+ Actual override matrix. Don't USE!
        "transfer function": tf.blackmagic},

    "BRUCE RGB": {  # Source: http://brucelindbloom.com/index.html?WorkingSpaceInfo.html
        "illuminant": "D65",
        "primaries": {
            "xr": 0.64, "yr": 0.33,
            "xg": 0.28, "yg": 0.65,
            "xb": 0.15, "yb": 0.06,
        },
        "whitepoint": (0.3127, 0.329),
        "transfer function": partial(tf.gamma_function, gamma=2.2)}, #! Not confirmed, no info about transfer function

    "CIE RGB": {  # Source: http://brucelindbloom.com/index.html?WorkingSpaceInfo.html & https://en.wikipedia.org/wiki/RGB_color_spaces
        "illuminant": "E",
        "primaries": {
            "xr": 0.73474284, "yr": 0.26525716,
            "xg": 0.27377903, "yg": 0.7174777,
            "xb": 0.16655563, "yb": 0.00891073,
        },
        "whitepoint": (1/3, 1/3),
        "override_matrix": {
            "to_rgb": ((2.36449012, -0.89655263, -0.46793749), (-0.51493525, 1.42633279, 0.08860245), (0.00514883, -0.01426189, 1.00911305)),
            "to_xyz": ((0.49, 0.31, 0.2), (0.1769, 0.8124, 0.0107), (0.0, 0.0099, 0.9901))
        }, #+ Calculation should be the same as override
        "transfer function": partial(tf.gamma_function, gamma=2.2)},

    "CINEMA GAMUT": {
        "illuminant": "D65",
        "primaries": {
            "xr": 0.74, "yr":  0.27,
            "xg": 0.17, "yg":  1.14,
            "xb": 0.08, "yb": -0.1,
        },
        "whitepoint": (0.3127, 0.329),
        "override_matrix": {
            "to_rgb": ((1.48981827, -0.2608959, -0.14242652), (-0.45816657, 1.26162778, 0.15962363), (-0.07034967, 0.22155767, 0.7761816)),
            "to_xyz": ((0.71604965, 0.12968348, 0.1047228), (0.26126136, 0.86964215, -0.1309035), (-0.00967635, -0.23648164, 1.33521573))
        }, #+ Calculation should be the same as override
        "transfer function": lambda x: x},

    "COLORMATCH RGB": {  # Source: http://brucelindbloom.com/index.html?WorkingSpaceInfo.html
        "illuminant": "D50",
        "primaries": {
            "xr": 0.63,  "yr": 0.34,
            "xg": 0.295, "yg": 0.605,
            "xb": 0.15,  "yb": 0.075,
        },
        "whitepoint": (0.3457, 0.3585),
        "override_matrix": {
            "to_rgb": ((2.64164976, -1.22313179, -0.39291946), (-1.11207173, 2.05919502, 0.01596275), (0.08218196, -0.28076676, 1.45620209)),
            "to_xyz": ((0.5094668, 0.32087954, 0.13394933), (0.27495034, 0.658075, 0.06697467), (0.02426032, 0.10877273, 0.69207155))
        }, #+ Calculation should be the same as override
        "transfer function": partial(tf.gamma_function, gamma=1.8)},

    "DAVINCI WIDE GAMUT": {
        "illuminant": "D65",
        "primaries": {
            "xr": 0.8,    "yr":  0.313,
            "xg": 0.1682, "yg":  0.9877,
            "xb": 0.079,  "yb": -0.1155
        },
        "whitepoint": (0.3127, 0.329),
        "override_matrix": {
            "to_rgb": ((1.51667204, -0.28147805, -0.14696363), (-0.4649171, 1.25142378, 0.17488461), (0.06484905, 0.10913934, 0.76141462)),
            "to_xyz": ((0.70062239, 0.14877482, 0.10105872), (0.27411851, 0.8736319, -0.14775041), (-0.09896291, -0.13789533, 1.32591599))
        }, #+ Calculation should be the same as override
        "transfer function": tf.davinci},

    "__DCDM": {
        "illuminant": "E",
        "primaries": {
            "xr": 1,   "yr": 0,
            "xg": 0,   "yg": 1,
            "xb": 0,   "yb": 0
        },
        "whitepoint": (1/3, 1/3),
        "override_matrix": {
            "to_rgb": ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
            "to_xyz": ((1, 0, 0), (0, 1, 0), (0, 0, 1))
        }, #+ Calculation should be the same as override
        "transfer function": tf.dcdm},  #TODO Implement in XYZ functions that this works with tristimulus rathar than RGB values

    "DCI-P3": {
        "illuminant": "DCI-P3", # or either D65: https://www.color.org/chardata/rgb/DCIP3.xalter (changes the white point too)
        "primaries": {
            "xr": 0.68,  "yr": 0.32,
            "xg": 0.265, "yg": 0.69,
            "xb": 0.15,  "yb": 0.06
        },
        "whitepoint": (0.314, 0.351),
        "override_matrix": {
            "to_rgb": ((2.72539403, -1.01800301, -0.4401632), (-0.79516803, 1.68973205, 0.02264719), (0.04124189, -0.08763902, 1.10092938)),
            "to_xyz": ((0.44516982, 0.27713441, 0.17228267), (0.20949168, 0.72159525, 0.06891307), (-0, 0.04706056, 0.90735539))
        }, #+ Calculation should be the same as override
        "transfer function": partial(tf.gamma_function, gamma=2.6)},

    "DCI-P3-P": {
        "illuminant": "DCI-P3",
        "primaries": {
            "xr": 0.74, "yr":  0.27,
            "xg": 0.22, "yg":  0.78,
            "xb": 0.09, "yb": -0.09
        },
        "whitepoint": (0.314, 0.351),
        "override_matrix": {
            "to_rgb": ((1.99040349, -0.56139586, -0.22966194), (-0.45849279, 1.262346, 0.15487549), (0.01563207, -0.00440904, 1.03772867)),
            "to_xyz": ((0.55907356, 0.24893595, 0.08657739), (0.2039863, 0.88259109, -0.08657739), (-0.00755505, 0, 0.961971))
        }, #+ Calculation should be the same as override
        "transfer function": partial(tf.gamma_function, gamma=2.6)},

    "DJI D-GAMUT": {
        "illuminant": "D65",
        "primaries": {
            "xr": 0.71, "yr":  0.31,
            "xg": 0.21, "yg":  0.88,
            "xb": 0.09, "yb": -0.08
        },
        "whitepoint": (0.3127, 0.329),
        "override_matrix": {
            "to_rgb": ((1.7257, -0.4314, -0.1917), (-0.6025, 1.3906, 0.1671), (-0.0156, 0.0905, 0.8489)),
            "to_xyz": ((0.6482, 0.194, 0.1082), (0.283, 0.8132, -0.0962), (-0.0183, -0.0832, 1.1903)),
            "d_to_rec709": ((1.6746, -0.5797, -0.0949), (-0.0981, 1.3340, -0.2359), (-0.0410, -0.2430, 1.2840)),
            "rec709_to_d": ((0.6163, 0.2857, 0.0980), (0.0505, 0.7990, 0.1505), (0.0292, 0.1604, 0.8104))
        }, #+ Actual override matrix
        "transfer function": tf.djidlog},

    "DISPLAY P3": {  # Source: https://en.wikipedia.org/wiki/RGB_color_spaces
        "illuminant": "D65",
        "primaries": {
            "xr": 0.68,  "yr": 0.32,
            "xg": 0.265, "yg": 0.69,
            "xb": 0.15,  "yb": 0.06
        },
        "whitepoint": (0.3127, 0.329),
        "override_matrix": {
            "to_rgb": ((2.49349691, -0.93138362, -0.40271078), (-0.82948897, 1.76266406, 0.02362469), (0.03584583, -0.07617239, 0.95688452)),
            "to_xyz": ((0.48657095, 0.26566769, 0.19821729), (0.22897456, 0.69173852, 0.07928691), (0, 0.04511338, 1.04394437))
        }, #+ Calculation should be the same as override
        "transfer function": tf.srgb},  # gamma = 2.2 | decoding gamma = 2.4

    "DON RGB": {  # Source: http://brucelindbloom.com/index.html?WorkingSpaceInfo.html
        "illuminant": "D50",
        "primaries": {
            "xr": 0.69612069, "yr": 0.29956897,
            "xg": 0.21468298, "yg": 0.76529477,
            "xb": 0.12993763, "yb": 0.03534304,
        },
        "whitepoint": (0.3457, 0.3585),
        "override_matrix": {
            "to_rgb": ((1.75819127, -0.48659205, -0.25308814), (-0.7112839, 1.65225302, 0.04076449), (0.00717743, -0.03459953, 1.24551283)),
            "to_xyz": ((0.64631888, 0.19296024, 0.12501655), (0.27813723, 0.68785827, 0.0340045), (0.00400197, 0.01799629, 0.80310634))
        }, #+ Calculation should be the same as override
        "transfer function": partial(tf.gamma_function, gamma=2.2)},

    "DRAGONCOLOR": {
        "illuminant": "D65",
        "primaries": {
            "xr": 0.75865589, "yr":  0.33035535,
            "xg": 0.29492362, "yg":  0.70805324,
            "xb": 0.0859616,  "yb": -0.04587944,
        },
        "whitepoint": (0.3127, 0.329),
        "override_matrix": {
            "to_rgb": ((2.41407671, -1.00664042, -0.26429553), (-0.61715986, 1.45087355, 0.12461203), (0.12073206, -0.04669048, 0.85573054)),
            "to_xyz": ((0.49831915, 0.34905932, 0.10307746), (0.21699218, 0.83802234, -0.05501452), (-0.05846657, -0.00352329, 1.15104761))
        }, #+ Calculation should be the same as override
        "transfer function": tf.red_log_film},

    "DRAGONCOLOR2": {
        "illuminant": "D65",
        "primaries": {
            "xr": 0.75865621, "yr": 0.33035584,
            "xg": 0.29492389, "yg": 0.70805336,
            "xb": 0.14416873, "yb": 0.05035738,
        },
        "whitepoint": (0.3127, 0.329),
        "override_matrix": {
            "to_rgb": ((2.72655873, -1.13744045, -0.41690486), (-0.71770143, 1.654923, 0.02499461), (0.12073281, -0.04669036, 0.85572978)),
            "to_xyz": ((0.43856251, 0.30720212, 0.2046913), (0.19097146, 0.73753094, 0.0714976), (-0.05145591, -0.0031012, 1.14361486))
        }, #+ Calculation should be the same as override
        "transfer function": tf.red_log_film},

    "EBU TECH. 3213-E": {
        "illuminant": "D65",
        "primaries": {
            "xr": 0.64, "yr": 0.33,
            "xg": 0.29, "yg": 0.6,
            "xb": 0.15, "yb": 0.06
        },
        "whitepoint": (0.313, 0.329),
        "override_matrix": {
            "to_rgb": ((3.05350675, -1.38890786, -0.47429309), (-0.97013781, 1.87769818, 0.04159339), (0.06792306, -0.22900835, 1.07006656)),
            "to_xyz": ((0.43194331, 0.341235, 0.17818948), (0.22272077, 0.70600344, 0.07127579), (0.02024734, 0.12943396, 0.93846459))
        }, #+ Calculation should be the same as override
        "transfer function": lambda x: x},

    "ECI RGB": {  # Source: http://brucelindbloom.com/index.html?WorkingSpaceInfo.html
        "illuminant": "D50",
        "primaries": {
            "xr": 0.670103092783505, "yr": 0.329896907216495,
            "xg": 0.209905660377358, "yg": 0.709905660377358,
            "xb": 0.140061791967044, "yb": 0.080329557157570
        },
        "whitepoint": (0.3457, 0.3585),
        "override_matrix": {
            "to_rgb": ((1.78215602, -0.49656317, -0.26901095), (-0.95923427, 1.94844461, -0.02843173), (0.08612755, -0.17494658, 1.32334029)),
            "to_xyz": ((0.65032438, 0.177949, 0.13602229), (0.3201597, 0.60182752, 0.07801279), (0, 0.06798052, 0.75712409)),
            # For D50, XYZ are normalized Y=1, RGB values outside 0-1 range are clipped. RGB = i**(1/1.8) for i in ReGeBe
            "d50_to_regebe": ((1.8951, -0.5943, -0.2824), (-0.9666, 1.9783, -0.0561), (0.0768, -0.1523, 1.3072))
        }, #+ Calculation should be the same as override
        "transfer function": tf.eci},

    "EKTA SPACE PS 5": {  # Source: http://brucelindbloom.com/index.html?WorkingSpaceInfo.html
        "illuminant": "D50",
        "primaries": {
            "xr": 0.695, "yr": 0.305,
            "xg": 0.26,  "yg": 0.7,
            "xb": 0.11,  "yb": 0.005,
        },
        "whitepoint": (0.3457, 0.3585),
        "override_matrix": {
            "to_rgb": ((2.00336603, -0.73013869, -0.24445204), (-0.71215462, 1.62076569, 0.07994372), (0.03818663, -0.08690749, 1.27266809)),
            "to_xyz": ((0.59433686, 0.27294481, 0.09701401), (0.26114801, 0.73485141, 0.00400058), (0, 0.04199151, 0.78311309))
        }, #+ Calculation should be the same as override
        "transfer function": partial(tf.gamma_function, gamma=2.2)},

    "ERIMM": {
        "illuminant": "D50",
        "primaries": {
            "xr": 0.7977, "yr": 0.2653,
            "xg": 0.288,  "yg": 0.8404,
            "xb": 0,      "yb": 0.0001,
        },
        "whitepoint": (0.3457, 0.3585),
        "override_matrix": {
            "to_rgb": ((1.346, -0.2556, -0.0511), (-0.5446, 1.5082, 0.0205), (0, 0, 1.2123)),
            "to_xyz": ((0.7977, 0.1352, 0.0313), (0.288, 0.7119, 0.0001), (0, 0, 0.8249))
        }, #+ Actual override matrix
        "transfer function": tf.erimm},

    "F-GAMUT": {  #~ FUJI
        "illuminant": "D65",
        "primaries": {
            "xr": 0.708, "yr": 0.292,
            "xg": 0.17,  "yg": 0.797,
            "xb": 0.131, "yb": 0.046,
        },
        "whitepoint": (0.3127, 0.329),
        "override_matrix": {
            "to_rgb": ((1.71665119, -0.35567078, -0.25336628), (-0.66668435, 1.61648124, 0.01576855), (0.01763986, -0.04277061, 0.94210312)),
            "to_xyz": ((0.63695805, 0.1446169, 0.16888098), (0.26270021, 0.67799807, 0.05930172), (0, 0.02807269, 1.06098506))
        }, #+ Calculation should be the same as override
        "transfer function": tf.flog},

    "FILMLIGHT E-GAMUT": {
        "illuminant": "D65",
        "primaries": {
            "xr": 0.8,   "yr":  0.3177,
            "xg": 0.18,  "yg":  0.9,
            "xb": 0.065, "yb": -0.0805,
        },
        "whitepoint": (0.3127, 0.329),
        "override_matrix": {
            "to_rgb": ((1.52505277, -0.31591351, -0.12265826), (-0.50915256, 1.33332741, 0.13828437), (0.09571535, 0.05089744, 0.78795577)),
            "to_xyz": ((0.70539685, 0.16404133, 0.08101775), (0.28013072, 0.82020664, -0.10033737), (-0.10378151, -0.07290726, 1.26574652))
        }, #+ Calculation should be the same as override
        "transfer function": tf.filmlighttlog},

    "ITU-T H.273 - 22 Unspecified": {
        "illuminant": "D65",
        "primaries": {
            "xr": 0.63,  "yr": 0.34,
            "xg": 0.295, "yg": 0.605,
            "xb": 0.155, "yb": 0.077,
        },
        "whitepoint": (0.3127, 0.329),
        "override_matrix": {
            "to_rgb": ((3.13288278, -1.44707454, -0.48720324), (-1.08850877, 2.01538781, 0.01762239), (0.05941301, -0.20297883, 1.05275352)),
            "to_xyz": ((0.42942013, 0.3277917, 0.1932441), (0.23175055, 0.67225077, 0.09599868), (0.02044858, 0.11111583, 0.95749334))
        }, #+ Calculation should be the same as override
        "transfer function": lambda x: x},

    "ITU-T H.273 - GENERIC FILM": {
        "illuminant": "C",
        "primaries": {
            "xr": 0.681, "yr": 0.319,
            "xg": 0.243, "yg": 0.692,
            "xb": 0.145, "yb": 0.049,
        },
        "whitepoint": (0.31, 0.316),
        "override_matrix": {
            "to_rgb": ((2.19248548, -0.73706449, -0.34962064), (-0.82433417, 1.75978548, 0.04131385), (0.04690337, -0.10012914, 0.89064375)),
            "to_xyz": ((0.54135308, 0.23820172, 0.20145785), (0.25358536, 0.67833578, 0.06807886), (-0, 0.06371651, 1.11982779))
        }, #+ Calculation should be the same as override
        "transfer function": lambda x: x},

    "M.A.C": {  # Source: https://en.wikipedia.org/wiki/RGB_color_spaces | https://en.wikipedia.org/wiki/Multiplexed_Analogue_Components
        "illuminant": "D65",
        "primaries": {
            "xr": 0.67, "yr": 0.33,
            "xg": 0.21, "yg": 0.71,
            "xb": 0.14, "yb": 0.08
        },
        "whitepoint": (0.313, 0.329),
        "transfer function": tf.rec601},  # gamma = 2.8

    "MAX RGB": {
        "illuminant": "D50",
        "primaries": {
            "xr": 0.73413379, "yr": 0.26586621,
            "xg": 0.10039113, "yg": 0.89960887,
            "xb": 0.03621495, "yb": 0
        },
        "whitepoint": (0.3457, 0.3585),
        "override_matrix": {
            "to_rgb": ((1.2169928, -0.13580933, -0.04572942), (-0.54704638, 1.51055387, 0.02055568), (0, 0, 1.21196755)),
            "to_xyz": ((0.85630404, 0.07698771, 0.03100393), (0.31011011, 0.68988989, 0), (0, 0, 0.8251046))
        }, #+ Calculation should be the same as override
        "transfer function": partial(tf.gamma_function, gamma=2.2)},

    "N-GAMUT": {  #~ NIKON
        "illuminant": "D65",
        "primaries": {
            "xr": 0.708, "yr": 0.292,
            "xg": 0.17,  "yg": 0.797,
            "xb": 0.131, "yb": 0.046,
        },
        "whitepoint": (0.3127, 0.329),
        "override_matrix": {
            "to_rgb": ((1.71665119, -0.35567078, -0.25336628), (-0.66668435, 1.61648124, 0.01576855), (0.01763986, -0.04277061, 0.94210312)),
            "to_xyz": ((0.63695805, 0.1446169, 0.16888098), (0.26270021, 0.67799807, 0.05930172), (0, 0.02807269, 1.06098506))
        }, #+ Calculation should be the same as override
        "transfer function": tf.nlog},

    "NTSC (1953)": {
        "illuminant": "C", # Source: http://brucelindbloom.com/index.html?WorkingSpaceInfo.html , https://en.wikipedia.org/wiki/RGB_color_spaces
        "primaries": {
            "xr": 0.67, "yr": 0.33,
            "xg": 0.21, "yg": 0.71,
            "xb": 0.14, "yb": 0.08,
        },
        "whitepoint": (0.31006, 0.31616),
        "override_matrix": {
            "to_rgb": ((1.91008143, -0.53247794, -0.28822201), (-0.98463135, 1.99910001, -0.02830719), (0.05830945, -0.11838584, 0.89761208)),
            "to_xyz": ((0.60686381, 0.17350728, 0.20033488), (0.29890307, 0.58661985, 0.11447708), (-0, 0.06609801, 1.11615148))
        }, #+ Calculation should be the same as override
        "transfer function": partial(tf.gamma_function, gamma=2.8)},

    "NTSC (1987)": {
        "illuminant": "D65", # Source: http://brucelindbloom.com/index.html?WorkingSpaceInfo.html | SMPTE C
        "primaries": {       # Source: https://en.wikipedia.org/wiki/RGB_color_spaces
            "xr": 0.63,  "yr": 0.34,
            "xg": 0.31,  "yg": 0.595,
            "xb": 0.155, "yb": 0.07,
        },
        "whitepoint": (0.3127, 0.329),
        "override_matrix": {
            "to_rgb": ((3.50600328, -1.73979073, -0.54405827), (-1.06904756, 1.97777888, 0.03517142), (0.05630659, -0.19697565, 1.04995233)),
            "to_xyz": ((0.3935209, 0.36525808, 0.19167695), (0.21237636, 0.70105986, 0.08656378), (0.01873909, 0.11193393, 0.95838473))
        }, #+ Calculation should be the same as override
        "transfer function": partial(tf.gamma_function, gamma=2.2)},

    "P3-D65": {  # Source: http://brucelindbloom.com/index.html?WorkingSpaceInfo.html
        "illuminant": "D65",
        "primaries": {
            "xr": 0.68,  "yr": 0.32,
            "xg": 0.265, "yg": 0.69,
            "xb": 0.15,  "yb": 0.06,
        },
        "whitepoint": (0.3127, 0.329),
        "override_matrix": {
            "to_rgb": ((2.49349691, -0.93138362, -0.40271078), (-0.82948897, 1.76266406, 0.02362469), (0.03584583, -0.07617239, 0.95688452)),
            "to_xyz": ((0.48657095, 0.26566769, 0.19821729), (0.22897456, 0.69173852, 0.07928691), (-0, 0.04511338, 1.04394437))
        }, #+ Calculation should be the same as override
        "transfer function": partial(tf.gamma_function, gamma=2.6)},

    "PAL": {  # Source: http://brucelindbloom.com/index.html?WorkingSpaceInfo.html
        "illuminant": "D65",  # Source: https://www.color.org/chardata/rgb/bt601.xalter | https://en.wikipedia.org/wiki/RGB_color_spaces
        "primaries": {
            "xr": 0.64, "yr": 0.33,
            "xg": 0.29, "yg": 0.6,
            "xb": 0.15, "yb": 0.06,
        },
        "whitepoint": (0.3127, 0.329),
        "override_matrix": {
            "to_rgb": ((3.06336109, -1.39339017, -0.47582374), (-0.96924364, 1.8759675, 0.04155506), (0.06786105, -0.22879927, 1.06908962)),
            "to_xyz": ((0.43055381, 0.3415498, 0.17835231), (0.22200431, 0.70665477, 0.07134092), (0.02018221, 0.12955337, 0.93932217))
        }, #+ Calculation should be the same as override
        "transfer function": partial(tf.gamma_function, gamma=2.8)},  # gamma = 2.4 tf | 2.8 wiki | 2.2 bruce

    "PROPHOTO": {  # Source: http://brucelindbloom.com/index.html?WorkingSpaceInfo.html
        "illuminant": "D50",
        "primaries": {
            "xr": 0.734699, "yr": 0.265301,
            "xg": 0.159597, "yg": 0.840403,
            "xb": 0.036598, "yb": 0.000105,
        },
        "whitepoint": (0.3457, 0.3585),
        "override_matrix": {
            "to_rgb": ((1.346, -0.2556, -0.0511), (-0.5446, 1.5082, 0.0205), (0, 0, 1.2123)),
            "to_xyz": ((0.7977, 0.1352, 0.0313), (0.288, 0.7119, 0.0001), (0, 0, 0.8249))
        }, #+ Actual override matrix
        "transfer function": tf.romm},  # gamma = 1.8

    "PROTUNE NATIVE": {  #~ GoPro
        "illuminant": "D65",
        "primaries": {
            "xr": 0.69848046, "yr":  0.19302645,
            "xg": 0.32955538, "yg":  1.02459662,
            "xb": 0.10844263, "yb": -0.03467857,
        },
        "whitepoint": (0.3127, 0.329),
        "override_matrix": {
            "to_rgb": ((2.2668965, -0.83163359, -0.29654225), (-0.35733783, 1.24337315, 0.08838899), (-0.21823445, 0.34417515, 0.79265501)),
            "to_xyz": ((0.50225719, 0.29296671, 0.15523203), (0.13879976, 0.91084146, -0.04964122), (0.07801426, -0.31483251, 1.325876))
        },#+ Calculation should be the same as override
        "transfer function": tf.protune},

    "REC. 601 - 525": {
        "illuminant": "D65",    # Source: https://www.color.org/chardata/rgb/bt601.xalter
        "primaries": {          # Source: https://en.wikipedia.org/wiki/Rec._601
            "xr": 0.63,  "yr": 0.34,
            "xg": 0.31,  "yg": 0.595,
            "xb": 0.155, "yb": 0.07,
        },
        "whitepoint": (0.3127, 0.329),
        "override_matrix": {},
        "transfer function": tf.rec601},  # gamma = 2.4

    "REC. 709": {  # Source: https://en.wikipedia.org/wiki/RGB_color_spaces
        "illuminant": "D65",
        "primaries": {
            "xr": 0.64, "yr": 0.33,
            "xg": 0.3,  "yg": 0.6,
            "xb": 0.15, "yb": 0.06,
        },
        "whitepoint": (0.3127, 0.329),
        "override_matrix": {
            "to_rgb": ((3.24096994, -1.53738318, -0.49861076), (-0.96924364, 1.8759675, 0.04155506), (0.05563008, -0.20397696, 1.05697151)),
            "to_xyz": ((0.4123908, 0.35758434, 0.18048079), (0.21263901, 0.71516868, 0.07219232), (0.01933082, 0.11919478, 0.95053215))
        }, #+ Calculation should be the same as override
        "transfer function": tf.rec601},  # gamma = 2.4 | decoding gamma = 20/9

    "REC. 2020": {  # Source: http://www.russellcottrell.com/photo/matrixCalculator.htm
        "illuminant": "D65",  # Source: https://en.wikipedia.org/wiki/RGB_color_spaces (UHDTV)
        "primaries": {
            "xr": 0.708, "yr": 0.292, # "xr": 0.708499, "yr": 0.293541,
            "xg": 0.17,  "yg": 0.797, # "xg": 0.190188, "yg": 0.775391,
            "xb": 0.131, "yb": 0.046, # "xb": 0.129244, "yb": 0.049140
        },
        "whitepoint": (0.3127, 0.329),
        "override_matrix": {
            "to_rgb": ((1.71665119, -0.35567078, -0.25336628), (-0.66668435, 1.61648124, 0.01576855), (0.01763986, -0.04277061, 0.94210312)),
            "to_xyz": ((0.63695805, 0.1446169, 0.16888098), (0.26270021, 0.67799807, 0.05930172), (0, 0.02807269, 1.06098506))
        }, #+ Calculation should be the same as override
        "transfer function": tf.rec2020},   # Color component transfer function: C'= C1/2.4 | gamma = 2.4

    "__REC. 2100": {  # Source: https://en.wikipedia.org/wiki/Rec._2100
        "illuminant": "D65",  # Source: https://en.wikipedia.org/wiki/RGB_color_spaces (UHDTV)
        "primaries": {
            "xr": 0.708, "yr": 0.292,
            "xg": 0.17,  "yg": 0.797,
            "xb": 0.131, "yb": 0.046,
        },
        "whitepoint": (0.3127, 0.329),
        "override_matrix": {
            "to_rgb": ((1.71665119, -0.35567078, -0.25336628), (-0.66668435, 1.61648124, 0.01576855), (0.01763986, -0.04277061, 0.94210312)),
            "to_xyz": ((0.63695805, 0.1446169, 0.16888098), (0.26270021, 0.67799807, 0.05930172), (0, 0.02807269, 1.06098506))
        }, #+ Calculation should be the same as override
        "gamma": 2.4}, #= Rec. 2100 defines two sets of HDR transfer functions which are perceptual quantization (PQ) and hybrid log-gamma
                        # (HLG).[3] HLG is supported in Rec. 2100 with a nominal peak luminance of 1,000 cd/m2 and a system gamma value
                        # that can be adjusted depending on background luminance.

    "REDCOLOR": {
        "illuminant": "D65",
        "primaries": {
            "xr": 0.70105856, "yr": 0.33018098,
            "xg": 0.29881132, "yg": 0.62516925,
            "xb": 0.13503868, "yb": 0.03526178,
        },
        "whitepoint": (0.3127, 0.329),
        "override_matrix": {
            "to_rgb": ((2.99433635, -1.37906534, -0.42873703), (-0.79472663, 1.69283865, 0.0574019), (0.12764085, -0.17911636, 0.97129776)),
            "to_xyz": ((0.42302331, 0.36210731, 0.16532531), (0.19923335, 0.75759632, 0.04317033), (-0.01885014, 0.09212233, 1.01578557))
        }, #+ Calculation should be the same as override
        "transfer function": tf.red_log_film},

    "REDCOLOR2": {
        "illuminant": "D65",
        "primaries": {
            "xr": 0.89740722, "yr":  0.33077623,
            "xg": 0.29602209, "yg":  0.68463555,
            "xb": 0.09979951, "yb": -0.02300051,
        },
        "whitepoint": (0.3127, 0.329),
        "override_matrix": {
            "to_rgb": ((2.55060735, -1.09426927, -0.30298724), (-0.48063394, 1.36324834, 0.0859211), (0.2572561, -0.13431523, 0.81704083)),
            "to_xyz": ((0.44957762, 0.3734296, 0.12744871), (0.16571026, 0.86366248, -0.02937275), (-0.11431396, 0.02440023, 1.17897148))
        }, #+ Calculation should be the same as override
        "transfer function": tf.red_log_film},

    "REDCOLOR3": {
        "illuminant": "D65",
        "primaries": {
            "xr": 0.70259866, "yr":  0.33018559,
            "xg": 0.29578224, "yg":  0.68974826,
            "xb": 0.11109053, "yb": -0.00433232,
        },
        "whitepoint": (0.3127, 0.329),
        "override_matrix": {
            "to_rgb": ((2.58673915, -1.10240102, -0.32705386), (-0.74762558, 1.6008681, 0.10074495), (0.06405867, -0.04645456, 0.90497461)),
            "to_xyz": ((0.47986312, 0.33439883, 0.13619398), (0.22551123, 0.77980008, -0.00531131), (-0.02239109, 0.01635861, 1.09509023))
        }, #+ Calculation should be the same as override
        "transfer function": tf.red_log_film},

    "REDCOLOR4": {
        "illuminant": "D65",
        "primaries": {
            "xr": 0.70259815, "yr": 0.3301851,
            "xg": 0.29578233, "yg": 0.68974825,
            "xb": 0.14445924, "yb": 0.05083772,
        },
        "whitepoint": (0.3127, 0.329),
        "override_matrix": {
            "to_rgb": ((2.58673915, -1.10240102, -0.32705386), (-0.74762558, 1.6008681, 0.10074495), (0.06405867, -0.04645456, 0.90497461)),
            "to_xyz": ((0.44431783, 0.30962925, 0.19650885), (0.20880659, 0.72203852, 0.06915489), (-0.02073188, 0.0151468, 1.09464284))
        }, #+ Calculation should be the same as override
        "transfer function": tf.red_log_film},

    "REDWIDEGAMUTRGB": {
        "illuminant": "D65",
        "primaries": {
            "xr": 0.780308, "yr":  0.304253,
            "xg": 0.121595, "yg":  1.493994,
            "xb": 0.095612, "yb": -0.084589,
        },
        "whitepoint": (0.3127, 0.329),
        "override_matrix": {
            "to_rgb": ((1.41280661, -0.17752237, -0.15177038), (-0.48620319, 1.29069621, 0.15740028), (-0.03713878, 0.28637576, 0.68767961)),
            "to_xyz": ((0.735275, 0.068609, 0.146571), (0.286694, 0.842979, -0.129673), (-0.079681, -0.347343, 1.516082)),
            "rwg_to_aces_ap0": ((0.785043, 0.083844, 0.131118), (0.023172, 1.087892, -0.111055), (-0.073769, -0.314639, 1.388537)),
            "aces_ap0_to_rwg": ((1.265561, -0.135228, -0.130321), (-0.020568, 0.943172, 0.077377), (0.062575, 0.206536, 0.730792)),
            "rwg_to_rec709": ((1.981880, -0.900388, -0.081540), (-0.178143, 1.500467, -0.322325), (-0.101811, -0.535343, 1.637304)),
            "rec709_to_rwg": ((0.541973, 0.360148, 0.097891), (0.076993, 0.767969, 0.155019), (0.058875, 0.273495, 0.667533)),
            "rwg_to_rec2020": ((1.180431, -0.094040, -0.086391), (-0.028017, 1.311442, -0.283425), (-0.074360, -0.362078, 1.436437)),
            "rec2020_to_rwg": ((0.853263, 0.079695, 0.067042), (0.029375, 0.809195, 0.161430), (0.051575, 0.208097, 0.740329))
        },  #+ Actual override matrix
        "transfer function": tf.log3_g10},

    "RIMM": {  # Source: https://en.wikipedia.org/wiki/RGB_color_spaces
        "illuminant": "D50",
        "primaries": {
            "xr": 0.7347, "yr": 0.2653,
            "xg": 0.1596, "yg": 0.8404,
            "xb": 0.0366, "yb": 0.0001
        },
        "whitepoint": (0.3457, 0.3585),
        "override_matrix": {
            "to_rgb": ((1.346, -0.2556, -0.0511), (-0.5446, 1.5082, 0.0205), (0, 0, 1.2123)),
            "to_xyz": ((0.7977, 0.1352, 0.0313), (0.288, 0.7119, 0.0001), (0, 0, 0.8249))
        },  #+ Actual override matrix
        "transfer function": tf.rimm},  # gamma =  2.222 | 20/9

    "RUSSELL RGB": {
        "illuminant": "D55",
        "primaries": {
            "xr": 0.69, "yr": 0.31,
            "xg": 0.18, "yg": 0.77,
            "xb": 0.1,  "yb": 0.02
        },
        "whitepoint": (0.33243, 0.34744),
        "override_matrix": {
            "to_rgb": ((1.58699918, -0.35980738, -0.17216338), (-0.75352154, 1.67719311, 0.04750942), (0.03704107, -0.08244626, 1.13632451)),
            "to_xyz": ((0.70158375, 0.15541622, 0.09979833), (0.31520429, 0.66483604, 0.01995967), (0, 0.04317117, 0.87822533))
        },  #+ Actual override matrix
        "transfer function": partial(tf.gamma_function, gamma=2.2)},

    "S-GAMUT": {  #~ SONY
        "illuminant": "D65",
        "primaries": {
            "xr": 0.73, "yr":  0.28,
            "xg": 0.14, "yg":  0.855,
            "xb": 0.1,  "yb": -0.05,
        },
        "whitepoint": (0.3127, 0.329),
        "override_matrix": {
            "to_rgb": ((1.5073999, -0.24582214, -0.17161168), (-0.51815173, 1.35539124, 0.12587867), (0.0155117, -0.00787277, 0.91191637)),
            "to_xyz": ((0.70648271, 0.12880105, 0.11517216), (0.27097967, 0.78660641, -0.05758608), (-0.00967785, 0.00460004, 1.09413556))
        }, #+ Calculation should be the same as override
        "transfer function": tf.slog2},

    "S-GAMUT3": {  #~ SONY
        "illuminant": "D65",
        "primaries": {
            "xr": 0.73, "yr":  0.28,
            "xg": 0.14, "yg":  0.855,
            "xb": 0.1,  "yb": -0.05,
        },
        "whitepoint": (0.3127, 0.329),
        "override_matrix": {
            "to_rgb": ((1.5073999, -0.24582214, -0.17161168), (-0.51815173, 1.35539124, 0.12587867), (0.0155117, -0.00787277, 0.91191637)),
            "to_xyz": ((0.70648271, 0.12880105, 0.11517216), (0.27097967, 0.78660641, -0.05758608), (-0.00967785, 0.00460004, 1.09413556))
        }, #+ Calculation should be the same as override
        "transfer function": tf.slog3},

    "S-GAMUT3.CINE": {  #~ SONY
        "illuminant": "D65",
        "primaries": {
            "xr": 0.766, "yr":  0.275,
            "xg": 0.255, "yg":  0.8,
            "xb": 0.089, "yb": -0.087,
        },
        "whitepoint": (0.3127, 0.329),
        "override_matrix": {
            "to_rgb": ((1.84677897, -0.52598612, -0.21054521), (-0.44415326, 1.2594429, 0.14939997), (0.04085542, 0.01564089, 0.86820725)),
            "to_xyz": ((0.59908392, 0.24892552, 0.10244649), (0.21507582, 0.8850685, -0.10014432), (-0.03206585, -0.02765839, 1.14878199))
        }, #+ Calculation should be the same as override
        "transfer function": tf.slog3},

    "__SCRGB": {  # Source: https://en.wikipedia.org/wiki/RGB_color_spaces , https://en.wikipedia.org/wiki/ScRGB
        "illuminant": "D65",
        "primaries": {
            "xr": 0.64, "yr": 0.33, # Either 16bits linear or 12bits non-linear
            "xg": 0.30, "yg": 0.60, # 64bit = 16 bit + alpha, 48bit = 12bit + alpha
            "xb": 0.15, "yb": 0.06, # scRGB range(-0.5, 7.4999). 16bit scRGB  encoding is linear RGB by 8192x + 4096
        },                          # 5x + 1024 sRGB color = 12bit scRGB color, 12bit uses sRGB OETF for positive and
        "gamma": 2.2},  # 12/5      # -f(-x), then converted by 1280x + 1024 for negative values

    "SHARP RGB": {
        "illuminant": "E",
        "primaries": {
            "xr": 0.6898, "yr": 0.3206,
            "xg": 0.0736, "yg": 0.9003,
            "xb": 0.1166, "yb": 0.0374,
        },
        "whitepoint": (1/3, 1/3),
        "override_matrix": {
            "to_rgb": ((1.26941888, -0.09883024, -0.17058864), (-0.83638581, 1.80071706, 0.03566876), (0.02973006, -0.03147126, 1.0017412)),
            "to_xyz": ((0.8156226, 0.0471626, 0.1372148), (0.37907887, 0.57690884, 0.04401229), (-0.01229701, 0.01672478, 0.99557223))
        }, #+ Calculation should be the same as override
        "transfer function": lambda x: x},

    "SMPTE 240M": {
        "illuminant": "D65",
        "primaries": {
            "xr": 0.63,  "yr": 0.34,
            "xg": 0.31,  "yg": 0.595,
            "xb": 0.155, "yb": 0.07,
        },
        "whitepoint": (0.3127, 0.329),
        "override_matrix": {
            "to_rgb": ((3.50600328, -1.73979073, -0.54405827), (-1.06904756, 1.97777888, 0.03517142), (0.05630659, -0.19697565, 1.04995233)),
            "to_xyz": ((0.3935209, 0.36525808, 0.19167695), (0.21237636, 0.70105986, 0.08656378), (0.01873909, 0.11193393, 0.95838473))
        }, #+ Calculation should be the same as override
        "transfer function": tf.smpte240m},

    "SRGB": {  # Source: http://brucelindbloom.com/index.html?WorkingSpaceInfo.html & https://en.wikipedia.org/wiki/RGB_color_spaces
        "illuminant": "D65",
        "primaries": {
            "xr": 0.64, "yr": 0.33,
            "xg": 0.30, "yg": 0.60,
            "xb": 0.15, "yb": 0.06,
        },
        "whitepoint": (0.3127, 0.329),
        "override_matrix": {
            "to_rgb": ((3.2406, -1.5372, -0.4986), (-0.9689, 1.8758, 0.0415), (0.0557, -0.2040, 1.0570)),
            "to_xyz": ((0.4124, 0.3576, 0.1805), (0.2126, 0.7152, 0.0722), (0.0193, 0.1192, 0.9505))
        },  #+ Actual override matrix
        "transfer function": tf.srgb},  # The gamma is ~2.2 but the calculations are made using 2.4 due to old standards

    "V-GAMUT": {  #~ PANASONIC
        "illuminant": "D65",
        "primaries": {
            "xr": 0.73,  "yr":  0.28,
            "xg": 0.165, "yg":  0.84,
            "xb": 0.1,   "yb": -0.03,
        },
        "whitepoint": (0.3127, 0.329),
        "override_matrix": {
            "to_rgb": ((1.589012, -0.313204, -0.180965), (-0.534053, 1.396011, 0.102458), (0.011179, 0.003194, 0.905535)),
            "to_xyz": ((0.679644, 0.152211, 0.1186), (0.260686, 0.774894, -0.03558), (-0.00931, -0.004612, 1.10298))
        },  #+ Actual override matrix
        "transfer function": tf.vlog},

    "VENICE S-GAMUT3": {
        "illuminant": "D65",
        "primaries": {
            "xr": 0.74046426, "yr":  0.27936437,
            "xg": 0.08924115, "yg":  0.89380953,
            "xb": 0.11048824, "yb": -0.05257933,
        },
        "whitepoint": (0.3127, 0.329),
        "override_matrix": {
            "to_rgb": ((1.39026398, -0.13557353, -0.17061639), (-0.49777193, 1.32876782, 0.13253885), (0.03205319, -0.02043803, 0.9090178)),
            "to_xyz": ((0.74422299, 0.07790652, 0.12832642), (0.28078248, 0.78028572, -0.0610682), (-0.01992929, 0.01479657, 1.09419047))
        }, #+ Calculation should be the same as override
        "transfer function": tf.slog3},

    "VENICE S-GAMUT3.CINE": {
        "illuminant": "D65",
        "primaries": {
            "xr": 0.77590187, "yr":  0.27450239,
            "xg": 0.1886829,  "yg":  0.82868494,
            "xb": 0.10133738, "yb": -0.08918752,
        },
        "whitepoint": (0.3127, 0.329),
        "override_matrix": {
            "to_rgb": ((1.70701129, -0.39308248, -0.21060088), (-0.42750858, 1.23694441, 0.1555323), (0.05417788, 0.00580601, 0.86561094)),
            "to_xyz": ((0.63226084, 0.20037001, 0.11782508), (0.22368436, 0.88001406, -0.10369842), (-0.04107303, -0.01844361, 1.14857439))
        }, #+ Calculation should be the same as override
        "transfer function": tf.slog3},

    "XTREME RGB": {
        "illuminant": "D50",
        "primaries": {
            "xr": 1, "yr": 0,
            "xg": 0, "yg": 1,
            "xb": 0, "yb": 0,
        },
        "whitepoint": (0.3457, 0.3585),
        "override_matrix": {
            "to_rgb": ((1.03702632, 0, 0), (0, 1, 0), (0, 0, 1.21196755)),
            "to_xyz": ((0.96429568, 0, 0), (0, 1, 0), (0, 0, 0.8251046))
        }, #+ Calculation should be the same as override
        "transfer function": partial(tf.gamma_function, gamma=2.2)},
}

#! https://stackoverflow.com/questions/2974022/is-it-possible-to-assign-the-same-value-to-multiple-keys-in-a-dict-object-at-onc
color_spaces.update(
    {
        "ACES": color_spaces["ACES2065-1"],
        "ALEXA WIDE GAMUT": color_spaces["ARRI WIDE GAMUT 3"],
        "ADOBE": color_spaces["ADOBE RGB"],
        "ADOBE 1998": color_spaces["ADOBE RGB"],
        "ADOBE1998": color_spaces["ADOBE RGB"],
        "DON RGB 4": color_spaces["DON RGB"],
        "ECI RGB V2": color_spaces["ECI RGB"],
        "ECI RGB 2": color_spaces["ECI RGB"],
        "MAC": color_spaces["M.A.C"],
        "ITU-R BO.650-2": color_spaces["M.A.C"],
        "NTSC 1953": color_spaces["NTSC (1953)"],
        "NTSC 1987": color_spaces["NTSC (1987)"],
        "SMPTE C": color_spaces["NTSC (1987)"],
        "SMPTE-C": color_spaces["NTSC (1987)"],
        "SMPTE C RGB": color_spaces["NTSC (1987)"],
        "SMPTE-C RGB": color_spaces["NTSC (1987)"],
        "ITU-R BT 470": color_spaces["NTSC (1987)"],
        "ITU-R BT 470-7": color_spaces["NTSC (1987)"],
        "ITU-R BT 470 - 525": color_spaces["NTSC (1987)"],
        "MUSE": color_spaces["NTSC (1987)"],
        "HI-VISION": color_spaces["NTSC (1987)"],
        "HI VISION": color_spaces["NTSC (1987)"],
        "ITU-R BO.786": color_spaces["NTSC (1987)"],
        "SECAM": color_spaces["PAL"],
        "PAL/SECAM": color_spaces["PAL"],
        "ITU-R BT.470-6": color_spaces["PAL"],
        "ITU-R BT.470 - 625": color_spaces["PAL"],
        "PROPHOTO RGB": color_spaces["PROPHOTO"],
        "ROMM": color_spaces["PROPHOTO"],
        "ROMM RGB": color_spaces["PROPHOTO"],
        "REC.601 - 525": color_spaces["REC. 601 - 525"],
        "BT.601 - 525": color_spaces["REC. 601 - 525"],
        "BT. 601 - 525": color_spaces["REC. 601 - 525"],
        "ITU 601 - 525": color_spaces["REC. 601 - 525"],
        "REC. 601 - 625": color_spaces["PAL"],
        "REC.601 - 625": color_spaces["PAL"],
        "BT.601 - 625": color_spaces["PAL"],
        "BT. 601 - 625": color_spaces["PAL"],
        "ITU 601 - 625": color_spaces["PAL"],
        "REC.709": color_spaces["REC. 709"],
        "ITU-R BT.709": color_spaces["REC. 709"],
        "BT.709": color_spaces["REC. 709"],
        "ITU 709": color_spaces["REC. 709"],
        "BT.2020": color_spaces["REC. 2020"],
        "ITU-R BT.2020": color_spaces["REC. 2020"],
        "__BT.2100": color_spaces["__REC. 2100"],
        "__ITU-R BT.2100": color_spaces["__REC. 2100"],
    }
)
