"""
This module contains all kinds of alternatives to the values used throughout the package.

These alternatives exist because the different references used for this package use different
    constants and different methods for calculating a given value

This module also contains information and constants NOT used in the package
"""
from . import internal_helpers as ih
from . import converters as co

# pylint: disable=invalid-name, unpacking-non-sequence, unsubscriptable-object

#= Reading material and references
# More info: https://blender.stackexchange.com/questions/173981/integrating-cg-imagery-with-footage-from-cameras-using-aces
# More info: https://stackoverflow.com/questions/2612361/convert-rgb-values-to-equivalent-hsv-values-using-python
# Luma: https://en.wikipedia.org/wiki/Luma_(video)
    # Rec 709 (sRGB):      Yr = 0.2126, Yg = 0.7152, Yb = 0.0722
    # Rec 601 (NTSC):      Yr = 0.299,  Yg = 0.587,  Yb = 0.114
    # Rec 240 (Adobe RGB): Yr = 0.212,  Yg = 0.701,  Yb = 0.087

# More: https://en.wikipedia.org/wiki/HSL_and_HSV | in the Lightness section
    # Rec 2020 (UHDTV, HDR): Yr = 0.2627, Yg = 0.6780, Yb = 0.0593
    # Rec 709  (sRGB):       Yr = 0.2126, Yg = 0.7152, Yb = 0.0722
    # Rec 601  (SDTV, NTSC): Yr = 0.2989  Yg = 0.5870, Yb = 0.1140
    # Rec 240  (sRGB):       Yr = 0.212,  Yg = 0.701,  Yb = 0.087

#! This Luma is the Y value in xyY and in primaries
Rec601Luma = '0.298839R + 0.586811G + 0.114350B'
Rec709Luma = '0.212656R + 0.715158G + 0.072186B'
Rec2020Luma = '0.2627R + 0.678G + 0.0593B'
Rec2100Luma = '0.2627R + 0.678G + 0.0593B'

# BT.470-625 (PAL) = '0.299R + 0.587G + 0.114B'


""" #! According to Wikipedia, the D65 matrix for sRGB to XYZ
#* The matrix has infinite precision, any change in its values or adding not zeroes is not allowed:
#= The reason this is here is that by generating a matrix via the
#= working_space_matrix() function, even after rounding, the values are different,
#= no matter which variant of D65 tristimulus values is used
# ((0.4124, 0.3576, 0.1805),
# ( 0.2126, 0.7152, 0.0722),
# ( 0.0193, 0.1192, 0.9505))

#! The numerical values below match those in the official sRGB specification,
# which corrected small rounding errors in the original publication by sRGB's creators,
# and assume the 2° standard colorimetric observer for CIE XYZ. #= This matrix depends on the bitdepth.
# ((3.2406, -1.5372, -0.4986),
# (-0.9689,  1.8758,  0.0415),
# ( 0.0557, -0.2040,  1.0570))
"""

bit_values = """
#? Digital 8-bit per channel	(255, 0, 0)
#? #FF0000 (hexadecimal)
#? Digital 12-bit per channel	(4095, 0, 0)
#? #FFF000000
#? Digital 16-bit per channel	(65535, 0, 0)
#? #FFFF00000000
#? Digital 24-bit per channel	(16777215, 0, 0)
#? #FFFFFF000000000000
#? Digital 32-bit per channel	(4294967295, 0, 0)
#? #FFFFFFFF0000000000000000
"""


# Reference: https://github.com/jsvine/spectra/blob/master/spectra/grapefruit.py
ILLUMINANTS = {
    "2": {
        'A':   (1.09847, 1.00000, 0.35582),
        'B':   (0.99093, 1.00000, 0.85313),
        'C':   (0.98071, 1.00000, 1.18225),
        'D50': (0.96421, 1.00000, 0.82519),
        'D55': (0.95680, 1.00000, 0.92148),
        'D65': (0.95043, 1.00000, 1.08890),
        'D75': (0.94972, 1.00000, 1.22639),
        'E':   (1.00000, 1.00000, 1.00000),
        'F1':  (0.92834, 1.00000, 1.03665),
        'F2':  (0.99145, 1.00000, 0.67316),
        'F3':  (1.03753, 1.00000, 0.49861),
        'F4':  (1.09147, 1.00000, 0.38813),
        'F5':  (0.90872, 1.00000, 0.98723),
        'F6':  (0.97309, 1.00000, 0.60191),
        'F7':  (0.95017, 1.00000, 1.08630),
        'F8':  (0.96413, 1.00000, 0.82333),
        'F9':  (1.00365, 1.00000, 0.67868),
        'F10': (0.96174, 1.00000, 0.81712),
        'F11': (1.00899, 1.00000, 0.64262),
        'F12': (1.08046, 1.00000, 0.39228)
    },
    "10": {
        'A':   (1.11142, 1.00000, 0.35200),
        'B':   (0.99178, 1.00000, 0.84349),
        'C':   (0.97286, 1.00000, 1.16145),
        'D50': (0.96721, 1.00000, 0.81428),
        'D55': (0.95797, 1.00000, 0.90925),
        'D65': (0.94810, 1.00000, 1.07305),
        'D75': (0.94417, 1.00000, 1.20643),
        'E':   (1.00000, 1.00000, 1.00000),
        'F1':  (0.94791, 1.00000, 1.03191),
        'F2':  (1.03245, 1.00000, 0.68990),
        'F3':  (1.08968, 1.00000, 0.51965),
        'F4':  (1.14961, 1.00000, 0.40963),
        'F5':  (0.93369, 1.00000, 0.98636),
        'F6':  (1.02148, 1.00000, 0.62074),
        'F7':  (0.95780, 1.00000, 1.07618),
        'F8':  (0.97115, 1.00000, 0.81135),
        'F9':  (1.02116, 1.00000, 0.67826),
        'F10': (0.99001, 1.00000, 0.83134),
        'F11': (1.03820, 1.00000, 0.65555),
        'F12': (1.11428, 1.00000, 0.40353)
    }
}

ILLUMINANTS2 = {
    #* Reference: http://masm32.com/board/index.php?topic=7640.0
    #* "calculate white reference, illuminants, tristimulus.asm"
    #* http://www.easyrgb.com/en/math.php
    # D65 is the most used one among color spaces including sRGB and Adobe RGB but D50 is the ICC standard
    "2": {
        'A':   (1.09850,  1.00000, 0.35585),  # Incandescent/tungsten
        'B':   (0.990927, 1.00000, 0.85313),  # Old direct sunlight at noon
        'C':   (0.98074,  1.00000, 1.18232),  # Old daylight
        'D50': (0.96422,  1.00000, 0.82521),  # ICC profile PCS
        'D55': (0.95682,  1.00000, 0.92149),  # Mid-morning daylight
        'D65': (0.95047,  1.00000, 1.08883),  # Daylight, sRGB, Adobe-RGB   # Lindbloom
        'D75': (0.94972,  1.00000, 1.22638),  # North sky daylight
        'E':   (1.00000,  1.00000, 1.00000),  # Equal energy
        'F1':  (0.92834,  1.00000, 1.03665),  # Daylight Fluorescent
        'F2':  (0.99187,  1.00000, 0.67395),  # Cool fluorescent
        'F3':  (1.03754,  1.00000, 0.49861),  # White Fluorescent
        'F4':  (1.09147,  1.00000, 0.38813),  # Warm White Fluorescent
        'F5':  (0.90872,  1.00000, 0.98723),  # Daylight Fluorescent
        'F6':  (0.97309,  1.00000, 0.60191),  # Lite White Fluorescent
        'F7':  (0.95044,  1.00000, 1.08755),  # Daylight fluorescent, D65 simulator
        'F8':  (0.96413,  1.00000, 0.82333),  # Sylvania F40, D50 simulator
        'F9':  (1.00365,  1.00000, 0.67868),  # Cool White Fluorescent
        'F10': (0.96174,  1.00000, 0.81712),  # Ultralume 50, Philips TL85
        'F11': (1.00966,  1.00000, 0.64370),  # ltralume 40, Philips TL84
        'F12': (1.08046,  1.00000, 0.39228)   # Ultralume 30, Philips TL83
    },
    "10": {
        'A':   (1.11144, 1.00000, 0.35200),  # Incandescent/tungsten
        'B':   (0.99178, 1.00000, 0.843493), # Old direct sunlight at noon
        'C':   (0.97285, 1.00000, 1.16145),  # Old daylight
        'D50': (0.96720, 1.00000, 0.81427),  # ICC profile PCS
        'D55': (0.95799, 1.00000, 0.90926),  # Mid-morning daylight
        'D65': (0.94811, 1.00000, 1.07304),  # Daylight, sRGB, Adobe-RGB
        'D75': (0.94416, 1.00000, 1.20641),  # North sky daylight
        'E':   (1.00000, 1.00000, 1.00000),  # Equal energy
        'F1':  (0.94791, 1.00000, 1.03191),  # Daylight Fluorescent
        'F2':  (1.03280, 1.00000, 0.69026),  # Cool fluorescent
        'F3':  (1.08968, 1.00000, 0.51965),  # White Fluorescent
        'F4':  (1.14961, 1.00000, 0.40963),  # Warm White Fluorescent
        'F5':  (0.93369, 1.00000, 0.98636),  # Daylight Fluorescent
        'F6':  (1.02148, 1.00000, 0.62074),  # Lite White Fluorescent
        'F7':  (0.95792, 1.00000, 1.07687),  # Daylight fluorescent, D65 simulator
        'F8':  (0.97115, 1.00000, 0.81135),  # Sylvania F40, D50 simulator
        'F9':  (1.02116, 1.00000, 0.67826),  # Cool White Fluorescent
        'F10': (0.99001, 1.00000, 0.83134),  # Ultralume 50, Philips TL85
        'F11': (1.03866, 1.00000, 0.65627),  # ltralume 40, Philips TL84
        'F12': (1.11428, 1.00000, 0.40353)   # Ultralume 30, Philips TL83
    }
}

# Reference: https://ninedegreesbelow.com/photography/linux-icc-profiles.html#variants
# Search: "Selected D50 and D65 profile white point xyY values" table
# https://github.com/ellelstone/elles_icc_profiles/blob/master/code/make-elles-profiles.c
# More: http://www.brucelindbloom.com/index.html?Eqn_ChromAdapt.html
ILLUMINANT_VARIANTS = {
    "D50": {
        "LCMS, ArgyllCMS profiles": (0.96420288, 1.00000000, 0.82490540),
        "More": (
            (0.96422, 1.00000, 0.82521),    # Lindbloom
            (0.964295676, 1.0, 0.825104603),
            (0.964199999, 1.000000000, 0.824899998),
            (0.9642, 1.000, 0.82491),
            (0.9642, 1.0000, 0.8251)) # https://www.mathworks.com/help/images/ref/whitepoint.html
    },
    "D65": {
        (0.950455927, 1.000000000, 1.089057751),
        (0.95045, 1.000, 1.08905),
        (0.9504,  1.0000,  1.0888), # https://www.mathworks.com/help/images/ref/whitepoint.html
        (0.9505, 1.0000, 1.089), # https://en.wikipedia.org/wiki/SRGB
        (0.95045593,  1.00000000, 1.08905775) # Colour science package
    }
}

#* *CIE Illuminant D Series D50* illuminant and *CIE Standard Illuminant D Series D65*
#* chromaticity coordinates are rounded to 4 decimals as given in the typical RGB colourspaces
#* litterature. Their chromaticity coordinates as given in :cite:`CIETC1-482004h` are
#* D50 = (0.34567, 0.35851) and D65 = (0.31272, 0.32903).
# More: https://en.wikipedia.org/wiki/Standard_illuminant
# More: https://en.wikipedia.org/wiki/SRGB
ILLUM_WHITEPOINTS = {# CIE 1931 2°       CIE 1964 10°     CCT (K)
    #                X        Y          X        Y
    "A":        ((0.44757, 0.40745), (0.45117, 0.40594), "2856K"), # Incandescent / Tungsten
    "B":        ((0.34842, 0.35161), (0.34980, 0.35270), "4874K"), # Obsolete, direct sunlight at noon
    "C":        ((0.31006, 0.31616), (0.31039, 0.31905), "6774K"), # Obsolete, average / North sky daylight
    "D50":      ((0.34567, 0.35850), (0.34773, 0.35952), "5003K"), # Horizon light, ICC profile PCS
    "D55":      ((0.33242, 0.34743), (0.33411, 0.34877), "5503K"), # Mid-morning / Mid-afternoon daylight
    "D65":      ((0.31271, 0.32902), (0.31382, 0.33100), "6504K"), # Noon daylight: television, sRGB color space
    "D75":      ((0.29902, 0.31485), (0.29968, 0.31740), "7504K"), # North sky daylight
    "D93":      ((0.28315, 0.29711), (0.28327, 0.30043), "9305K"), # High-efficiency blue phosphor monitors, BT.2035
    "E":        ((0.33333, 0.33333), (0.33333, 0.33333), "5454K"), # Equal energy
    "F1":       ((0.31310, 0.33727), (0.31811, 0.33559), "6430К"), # Daylight fluorescent
    "F2":       ((0.37208, 0.37529), (0.37925, 0.36733), "4230К"), # Cool white fluorescent
    "F3":       ((0.40910, 0.39430), (0.41761, 0.38324), "3450K"), # White fluorescent
    "F4":       ((0.44018, 0.40329), (0.44920, 0.39074), "2940K"), # Warm white fluorescent
    "F5":       ((0.31379, 0.34531), (0.31975, 0.34246), "6350K"), # Daylight fluorescent
    "F6":       ((0.37790, 0.38835), (0.38660, 0.37847), "4150K"), # Light white fluorescent
    "F7":       ((0.31292, 0.32933), (0.31569, 0.32960), "6500K"), # D65 simulator, daylight simulator
    "F8":       ((0.34588, 0.35875), (0.34902, 0.35939), "5000K"), # D50 simulator, Sylvania F40 Design 50
    "F9":       ((0.37417, 0.37281), (0.37829, 0.37045), "4150K"), # Cool white deluxe fluorescent
    "F10":      ((0.34609, 0.35986), (0.35090, 0.35444), "5000K"), # Philips TL85, Ultralume 50
    "F11":      ((0.38052, 0.37713), (0.38541, 0.37123), "4000K"), # Philips TL84, Ultralume 40
    "F12":      ((0.43695, 0.40441), (0.44256, 0.39717), "3000K"), # Philips TL83, Ultralume 30
                #   CIE 1931 2°     CCT (K)
    "LED-B1":   ((0.4560, 0.4078), "2733K"), # Phosphor-converted blue
    "LED-B2":   ((0.4357, 0.4012), "2998K"), # Phosphor-converted blue
    "LED-B3":   ((0.3756, 0.3723), "4103K"), # Phosphor-converted blue
    "LED-B4":   ((0.3422, 0.3502), "5109K"), # Phosphor-converted blue
    "LED-B5":   ((0.3118, 0.3236), "6598K"), # Phosphor-converted blue
    "LED-BH1":  ((0.4474, 0.4066), "2851K"), # Mixing of phosphor-converted blue LED and red LED (blue-hybrid)
    "LED-RGB1": ((0.4557, 0.4211), "2840K"), # Mixing of red, green, and blue LEDs
    "LED-V1":   ((0.4560, 0.4548), "2724K"), # Phosphor-converted violet
    "LED-V2":   ((0.3781, 0.3775), "4070K"), # Phosphor-converted violet
}

ILLUMINANT_WHITEPOINTS = { # According to colour science library: https://github.com/colour-science/colour
        "A":        ((0.44758, 0.40745), (0.45117, 0.40594)),
        "B":        ((0.34842, 0.35161), (0.34980, 0.35270)),
        "C":        ((0.31006, 0.31616), (0.31039, 0.31905)),
        "D50":      ((0.34570, 0.35850), (0.34773, 0.35952)),
        "D50_alt":  ((0.345704, 0.358540)), # http://www.russellcottrell.com/photo/matrixCalculator.htm
        "D55":      ((0.33243, 0.34744), (0.33412, 0.34877)),
        "D60":      ((0.321616709705268, 0.337619916550817), (0.322986926715820, 0.339275732345997)),
        "D65":      ((0.31270, 0.32900), (0.31382, 0.33100)),
        "D75":      ((0.29903, 0.31488), (0.29968, 0.31740)),
        "E":        ((1/3, 1/3), (1/3, 1/3)),
        "FL1":      ((0.31310, 0.33710), (0.31811, 0.33559)),
        "FL2":      ((0.37210, 0.37510), (0.37925, 0.36733)),
        "FL3":      ((0.40910, 0.39410), (0.41761, 0.38324)),
        "FL4":      ((0.44020, 0.40310), (0.44920, 0.39074)),
        "FL5":      ((0.31380, 0.34520), (0.31975, 0.34246)),
        "FL6":      ((0.37790, 0.38820), (0.38660, 0.37847)),
        "FL7":      ((0.31290, 0.32920), (0.31569, 0.32960)),
        "FL8":      ((0.34580, 0.35860), (0.34902, 0.35939)),
        "FL9":      ((0.37410, 0.37270), (0.37829, 0.37045)),
        "FL10":     ((0.34580, 0.35880), (0.35090, 0.35444)),
        "FL11":     ((0.38050, 0.37690), (0.38541, 0.37123)),
        "FL12":     ((0.43700, 0.40420), (0.44256, 0.39717)),
        "FL3.1":    ((0.44070, 0.40330), (0.449830684010003, 0.390231404321266)),
        "FL3.2":    ((0.38080, 0.37340), (0.386924116672933, 0.365756034732821)),
        "FL3.3":    ((0.31530, 0.34390), (0.321176986855865, 0.340501092654981)),
        "FL3.4":    ((0.44290, 0.40430), (0.448121275113995, 0.397077112142482)),
        "FL3.5":    ((0.37490, 0.36720), (0.377814166608895, 0.366625766963060)),
        "FL3.6":    ((0.34880, 0.36000), (0.351976478983504, 0.361094432889677)),
        "FL3.7":    ((0.43840, 0.40450), (0.444309208810922, 0.396791387314871)),
        "FL3.8":    ((0.38200, 0.38320), (0.387588931999771, 0.376305569410173)),
        "FL3.9":    ((0.34990, 0.35910), (0.354688990710449, 0.353445033593383)),
        "FL3.10":   ((0.34550, 0.35600), (0.349344792334400, 0.354984421140869)),
        "FL3.11":   ((0.32450, 0.34340), (0.329267975695120, 0.338865386643537)),
        "FL3.12":   ((0.43770, 0.40370), (0.442252080438001, 0.401220551071252)),
        "FL3.13":   ((0.38300, 0.37240), (0.386275268780817, 0.374283190950586)),
        "FL3.14":   ((0.34470, 0.36090), (0.347255078638291, 0.366808242504180)),
        "FL3.15":   ((0.31270, 0.32880), (0.314613997909246, 0.333377149377113)),
        "HP1":      ((0.53300, 0.4150), (0.543334600247307, 0.405289298480431)),
        "HP2":      ((0.47780, 0.41580), (0.482647330648721, 0.410815644179685)),
        "HP3":      ((0.43020, 0.40750), (0.435560034503954, 0.398801084399711)),
        "HP4":      ((0.38120, 0.37970), (0.385193641123543, 0.368275479241015)),
        "HP5":      ((0.37760, 0.37130), (0.380316415606638, 0.366617114797851)),
        "LED-B1":   ((0.45600, 0.40780), (0.462504966271043, 0.403041801546906)),
        "LED-B2":   ((0.43570, 0.40120), (0.442119475258745, 0.396633702892576)),
        "LED-B3":   ((0.37560, 0.37230), (0.380851979328052, 0.368518548904765)),
        "LED-B4":   ((0.34220, 0.35020), (0.348371362473402, 0.345065503264192)),
        "LED-B5":   ((0.31180, 0.32360), (0.316916877024753, 0.322060276350364)),
        "LED-BH1":  ((0.44740, 0.40660), (0.452772610754910, 0.400032462750000)),
        "LED-RGB1": ((0.45570, 0.42110), (0.457036370583652, 0.425381348780888)),
        "LED-V1":   ((0.45480, 0.40440), (0.453602699414564, 0.398199587905174)),
        "LED-V2":   ((0.37810, 0.37750), (0.377728483834020, 0.374512315539769)),
        "ID65":     ((0.310656625403120, 0.330663091836953), (0.312074043269908, 0.332660121024630)),
        "ID50":     ((0.343211370103531, 0.360207541805137), (0.345621427535976, 0.361228962209198)),
        "ACES":     ((0.32168, 0.33767)),  # This standard only has values for 2 degrees
        "Blackmagic Wide Gamut": ((0.312717, 0.3290312)),  # This standard only has values for 2 degrees
        "DCI-P3":   ((0.314, 0.351)),  # This standard only has values for 2 degrees
        "ICC D50":  ((0.34570291, 0.3585386)),  # This standard only has values for 2 degrees
        "ISO 7589 Photographic Daylight": ((0.3320391, 0.34726389), (0.33371691, 0.34859249)),
        "ISO 7589 Sensitometric Daylight": ((0.33381831, 0.35343623), (0.33612591, 0.35499706)),
        "ISO 7589 Studio Tungsten": ((0.43094409, 0.40358544), (0.43457593, 0.40221969)),
        "ISO 7589 Sensitometric Studio Tungsten": ((0.43141822, 0.40747144), (0.43560767, 0.40612924)),
        "ISO 7589 Photoflood": ((0.41114602, 0.39371938), (0.41414465, 0.39245859)),
        "ISO 7589 Sensitometric Photoflood": ((0.41202478, 0.39817741), (0.41562582, 0.39700229)),
        "ISO 7589 Sensitometric Printer": ((0.41208797, 0.42110498), (0.41884105, 0.41869513))
}

#= The Olympus E-M1 characterization matrices for the 4200 and 6800 K calibration illuminants
T4200K = ((0.868, 0.3395, 0.2133), (0.2883, 0.8286, -0.0216), (0.0425, -0.2647, 1.7637))
T6800K = ((1.2105, 0.2502, 0.1882), (0.4586, 0.8772, -0.1328), (0.0936, -0.2788, 1.9121))
#= These matrices are normalized such that the WP of the characterization illuminant maps to
#= raw values where the green raw channel just reaches saturation
wp_4200K = (0.6337, 1.0000, 0.5267)
wp_6800K = (0.4793, 1.0000, 0.7312)

# This is a set of matrices for conversion to and from a given color space using its default illuminant
# TO50 and FROM50 are matrices to convert to/from given color space in illuminant D50 without it being the default one
COLOR_SPACE_MATRICES = {
    #! These are not included in the actual code because the working_space_matrix function in the xyz.py module generates these and more
    "TO": {
        "ADOBE RGB":      ((2.041369,  -0.5649464, -0.3446944), (-0.969266,  1.8760108,  0.041556 ), (0.0134474, -0.1183897, 1.0154096)),   # D65
        "APPLE RGB":      ((2.9515373, -1.2894116, -0.4738445), (-1.0851093, 1.9908566,  0.0372026), (0.0854934, -0.2694964, 1.0912975)),   # D65
        "BEST RGB":       ((1.7552599, -0.4836786, -0.253    ), (-0.5441336, 1.5068789,  0.0215528), (0.0063467, -0.0175761, 1.2256959)),   # D50
        "BETA RGB":       ((1.683227 , -0.4282363, -0.2360185), (-0.7710229, 1.7065571,  0.04469  ), (0.0400013, -0.0885376, 1.272364 )),   # D50
        "BRUCE RGB":      ((2.7454669, -1.1358136, -0.4350269), (-0.969266,  1.8760108,  0.041556 ), (0.0112723, -0.1139754, 1.0132541)),   # D65
        "CIE RGB":        ((2.3706743, -0.9000405, -0.4706338), (-0.513885,  1.4253036,  0.0885814), (0.0052982, -0.0146949, 1.0093968)),   # E
        "COLORMATCH RGB": ((2.6422874, -1.223427,  -0.3930143), (-1.1119763, 2.0590183,  0.0159614), (0.0821699, -0.2807254, 1.4559877)),   # D50
        "DON RGB 4":      ((1.7603902, -0.4881198, -0.2536126), (-0.7126288, 1.6527432,  0.0416715), (0.0078207, -0.0347411, 1.2447743)),   # D50
        "ECI RGB":        ((1.7827618, -0.4969847, -0.2690101), (-0.9593623, 1.9477962, -0.0275807), (0.0859317, -0.1744674, 1.3228273)),   # D50
        "EKTA SPACE PS5": ((2.0043819, -0.7304844, -0.2450052), (-0.7110285, 1.6202126,  0.0792227), (0.0381263, -0.086878,  1.2725438)),   # D50
        "NTSC":           ((1.9099961, -0.5324542, -0.2882091), (-0.9846663, 1.999171,  -0.0283082), (0.0583056, -0.1183781, 0.8975535)),   # C
        "PAL":            ((3.0628971, -1.3931791, -0.4757517), (-0.969266,  1.8760108,  0.041556 ), (0.0678775, -0.2288548, 1.069349 )),   # D65
        "SECAM":          ((3.0628971, -1.3931791, -0.4757517), (-0.969266,  1.8760108,  0.041556 ), (0.0678775, -0.2288548, 1.069349 )),   # D65
        "PROPHOTO":       ((1.3459433, -0.2556075, -0.0511118), (-0.5445989, 1.5081673,  0.0205351), (0,          0,         1.2118128)),   # D50
        "SMPTE-C RGB":    ((3.505396,  -1.7394894, -0.543964 ), (-1.0690722, 1.9778245,  0.0351722), (0.05632,   -0.1970226, 1.0502026)),   # D65
        "SRGB":           ((3.2404542, -1.5371385, -0.4985314), (-0.969266,  1.8760108,  0.041556 ), (0.0556434, -0.2040259, 1.0572252)),   # D65
        "WIDE GAMUT":     ((1.4628067, -0.1840623, -0.2743606), (-0.5217933, 1.4472381,  0.0677227), (0.0349342, -0.096893,  1.2884099))},  # D50

    "FROM": {
        "ADOBE RGB":      ((0.5767309,  0.185554,   0.1881852), ( 0.2973769, 0.6273491,  0.0752741), (0.0270343,  0.0706872, 0.9911085)),   # D65
        "APPLE RGB":      ((0.4497288,  0.3162486,  0.1844926), ( 0.2446525, 0.6720283,  0.0833192), (0.0251848,  0.1411824, 0.9224628)),   # D65
        "BEST RGB":       ((0.6326696,  0.2045558,  0.1269946), ( 0.2284569, 0.7373523,  0.0341908), (0,          0.0095142, 0.8156958)),   # D50
        "BETA RGB":       ((0.6712537,  0.1745834,  0.1183829), ( 0.3032726, 0.6637861,  0.0329413), (0,          0.040701,  0.784509 )),   # D50
        "BRUCE RGB":      ((0.4674162,  0.2944512,  0.1886026), ( 0.2410115, 0.6835475,  0.075441 ), (0.0219101,  0.0736128, 0.9933071)),   # D65
        "CIE RGB":        ((0.488718,   0.3106803,  0.2006017), ( 0.1762044, 0.8129847,  0.0108109), (0,          0.0102048, 0.9897952)),   # E
        "COLORMATCH RGB": ((0.5093439,  0.3209071,  0.1339691), ( 0.274884,  0.6581315,  0.0669845), (0.0242545,  0.1087821, 0.6921735)),   # D50
        "DON RGB 4":      ((0.6457711,  0.1933511,  0.1250978), ( 0.2783496, 0.6879702,  0.0336802), (0.0037113,  0.0179861, 0.8035125)),   # D50
        "ECI RGB":        ((0.6502043,  0.1780774,  0.1359384), ( 0.3202499, 0.6020711,  0.0776791), (0,          0.067839,  0.757371 )),   # D50
        "EKTA SPACE PS5": ((0.5938914,  0.2729801,  0.0973485), ( 0.2606286, 0.7349465,  0.0044249), (0,          0.0419969, 0.7832131)),   # D50
        "NTSC":           ((0.6068909,  0.1735011,  0.200348 ), ( 0.2989164, 0.586599,   0.1144845), (0,          0.0660957, 1.1162243)),   # C
        "PAL":            ((0.430619,   0.3415419,  0.1783091), ( 0.2220379, 0.7066384,  0.0713236), (0.0201853,  0.1295504, 0.9390944)),   # D65
        "SECAM":          ((0.430619,   0.3415419,  0.1783091), ( 0.2220379, 0.7066384,  0.0713236), (0.0201853,  0.1295504, 0.9390944)),   # D65
        "PROPHOTO":       ((0.7976749,  0.1351917,  0.0313534), ( 0.2880402, 0.7118741,  0.0000857), (0,          0,         0.82521  )),   # D50
        "SMPTE-C RGB":    ((0.3935891,  0.3652497,  0.1916313), ( 0.2124132, 0.7010437,  0.0865432), (0.0187423,  0.1119313, 0.9581563)),   # D65
        "SRGB":           ((0.4124564,  0.3575761,  0.1804375), ( 0.2126729, 0.7151522,  0.072175 ), (0.0193339,  0.119192,  0.9503041)),   # D65
        "WIDE GAMUT":     ((0.7161046,  0.1009296,  0.1471858), ( 0.2581874, 0.7249378,  0.0168748), (0,          0.0517813, 0.7734287))},  # D50

    "TO50": {
        "ADOBE RGB":      ((1.9624274, -0.6105343, -0.3413404), (-0.9787684, 1.9161415,  0.033454 ), (0.0286869, -0.1406752, 1.3487655)),   # D50
        "APPLE RGB":      ((2.8510695, -1.3605261, -0.4708281), (-1.092768,  2.0348871,  0.0227598), (0.1027403, -0.2964984, 1.4510659)),   # D50
        "BRUCE RGB":      ((2.6502856, -1.2014485, -0.4289936), (-0.9787684, 1.9161415,  0.033454 ), (0.026457,  -0.1361227, 1.3458542)),   # D50
        "CIE RGB":        ((2.3638081, -0.867603,  -0.4988161), (-0.500594,  1.3962369,  0.1047562), (0.0141712, -0.03064,   1.2323842)),   # D50
        "NTSC RGB":       ((1.8464881, -0.5521299, -0.2766458), (-0.982663,  2.0044755, -0.0690396), (0.0736477, -0.145302,  1.3018376)),   # D50
        "PAL":            ((2.9603944, -1.4678519, -0.4685105), (-0.9787684, 1.9161415,  0.033454 ), (0.0844874, -0.2545973, 1.4216174)),   # D50
        "SECAM":          ((2.9603944, -1.4678519, -0.4685105), (-0.9787684, 1.9161415,  0.033454 ), (0.0844874, -0.2545973, 1.4216174)),   # D50
        "SMPTE-C RGB":    ((3.392194,  -1.8264027, -0.5385522), (-1.0770996, 2.0213975,  0.0207989), (0.0723073, -0.2217902, 1.3960932)),   # D50
        "SRGB":           ((3.1338561, -1.6168667, -0.4906146), (-0.9787684, 1.9161415,  0.033454 ), (0.0719453, -0.2289914, 1.4052427))},  # D50

    "FROM50": {
        "ADOBE RGB":      ((0.6097559,  0.2052401,  0.149224 ), ( 0.3111242, 0.625656,   0.0632197), ( 0.0194811, 0.0608902, 0.7448387)),   # D50
        "APPLE RGB":      ((0.4755678,  0.3396722,  0.14898  ), ( 0.2551812, 0.6725693,  0.0722496), ( 0.0184697, 0.1133771, 0.6933632)),   # D50
        "BRUCE RGB":      ((0.4941816,  0.3204834,  0.149555 ), ( 0.2521531, 0.6844869,  0.06336  ), ( 0.0157886, 0.0629304, 0.7464909)),   # D50
        "CIE RGB":        ((0.486887,   0.3062984,  0.1710347), ( 0.1746583, 0.8247541,  0.0005877), (-0.0012563, 0.0169832, 0.8094831)),   # D50
        "NTSC":           ((0.6343706,  0.1852204,  0.144629 ), ( 0.3109496, 0.5915984,  0.097452 ), (-0.0011817, 0.0555518, 0.7708399)),   # D50
        "PAL":            ((0.4552773,  0.36755,    0.1413926), ( 0.2323025, 0.7077956,  0.0599019), ( 0.0145457, 0.1049154, 0.7057489)),   # D50
        "SECAM":          ((0.4552773,  0.36755,    0.1413926), ( 0.2323025, 0.7077956,  0.0599019), ( 0.0145457, 0.1049154, 0.7057489)),   # D50
        "SMPTE-C RGB":    ((0.416329,   0.3931464,  0.1547446), ( 0.2216999, 0.7032549,  0.0750452), ( 0.0136576, 0.0913604, 0.720192 )),   # D50
        "SRGB":           ((0.4360747,  0.3850649,  0.1430804), ( 0.2225045, 0.7168786,  0.0606169), ( 0.0139322, 0.0971045, 0.7141733))},  # D50

    "EXTRA": {
        "FROM SRGB D65": {1 : ((0.412390799265959, 0.357584339383878, 0.180480788401834),
                        (0.212639005871510, 0.715168678767756, 0.072192315360734),
                        (0.019330818715592, 0.119194779794626, 0.950532152249661)),
                        "2 Easy RGB": ((0.4124, 0.3576, 0.1805),
                        (0.2126, 0.7152, 0.0722),
                        (0.0193, 0.1192, 0.9505)),
                        "3 Lindbloom": ((0.4124564, 0.3575761, 0.1804375),
                        (0.2126729, 0.7151522, 0.0721750),
                        (0.0193339, 0.1191920, 0.9503041))},
        "FROM SRGB D50": ((0.4360747, 0.3850649, 0.1430804),
                        (0.2225045, 0.7168786, 0.0606169),
                        (0.0139322, 0.0971045, 0.7141733)),
        "TO SRGB D65": {1: ((3.240969941904523, -1.537383177570094, -0.498610760293003),
                            (-0.969243636280880,  1.875967501507721,  0.041555057407176),
                            ( 0.055630079696994, -0.203976958888977,  1.056971514242879)),
                        2: ((3.2406255, -1.5372080, -0.4986286),
                            (-0.9689307, 1.8757561, 0.0415175),
                            (0.0557101, -0.2040211, 1.0569959)),
                        3: ((3.2407100, -1.537260, -0.4985710),
                            (-0.9692580, 1.875990, 0.0415557),
                            (0.0556352, -0.203996, 1.0570700)),
                        4: ((3.2404542, -1.5371385, -0.4985314),
                            (-0.9692660, 1.8760108, 0.0415560),
                            (0.0556434, -0.2040259, 1.0572252))},
        "TO SRGB D50": ((3.1338561, -1.6168667, -0.4906146),
                        (-0.9787684, 1.9161415, 0.0334540),
                        (0.0719453, -0.2289914, 1.4052427))
    }
}


color_space_props = {
    #! The primaries only have x and y values because z = 1 - x - y
    #! The primary Yr, Yg, Yb can be found by using the res = working_space_matrix() function for
        #! the desired color space and using the second row of the output res[1]
    "NTSC": {  # Source: http://brucelindbloom.com/index.html?WorkingSpaceInfo.html
        "illuminant": "C",  # D65 according to: https://en.wikipedia.org/wiki/RGB_color_spaces
        "primaries": {
            "xr": 0.67,   "yr": 0.33,
            "xg": 0.21,   "yg": 0.71,
            "xb": 0.14,   "yb": 0.08,
        },
        "primaries Yz": {
            "Yr": 0.298839,
            "Yg": 0.586811,
            "Yb": 0.11435,
            "zr": 0,
            "zg": 0.08,
            "zb": 0.78
        },
        "primaries d50": {
            "xr": 0.67191,  "yr": 0.32934,
            "xg": 0.222591, "yg": 0.710647,
            "xb": 0.142783, "yb": 0.096145
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
        "primaries Yz": {
            "Yr": 0.244634,
            "Yg": 0.672034,
            "Yb": 0.083332,
            "zr": 0.035,
            "zg": 0.125,
            "zb": 0.775
        },
        "primaries d50": {
            "xr": 0.634756,   "yr": 0.340596,
            "xg": 0.301775,   "yg": 0.597511,
            "xb": 0.162897,   "yb": 0.079001
        },
        "gamma": 1.8},

    "PAL": {  # Source: http://brucelindbloom.com/index.html?WorkingSpaceInfo.html
        "illuminant": "D65",
        "primaries": {
            "xr": 0.64,   "yr": 0.33,
            "xg": 0.29,   "yg": 0.60,
            "xb": 0.15, "yb": 0.06,
        },
        "primaries Yz": {
            "Yr": 0.222021,
            "Yg": 0.706645,
            "Yb": 0.071334,
            "zr": 0.03,
            "zg": 0.11,
            "zb": 0.79
        },
        "primaries d50": {
            "xr": 0.648431,   "yr": 0.330856,
            "xg": 0.311424,   "yg": 0.599693,
            "xb": 0.155886,   "yb": 0.066044
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
        "primaries Yz": {
            "Yr": 0.222021,
            "Yg": 0.706645,
            "Yb": 0.071334,
            "zr": 0.03,
            "zg": 0.11,
            "zb": 0.79
        },
        "primaries d50": {
            "xr": 0.648431,   "yr": 0.330856,
            "xg": 0.311424,   "yg": 0.599693,
            "xb": 0.155886,   "yb": 0.066044
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
        "primaries Yz": {
            "Yr": 0.2126,      # https://en.wikipedia.org/wiki/Rec._709 / Luma coefficients
            # "Yr": 0.212656,  # http://brucelindbloom.com/index.html?WorkingSpaceInfo.html
            "Yg": 0.7152,
            # "Yg": 0.715158,
            "Yb": 0.0722,
            # "Yb": 0.0721856
            "zr": 0.03,
            "zg": 0.1,
            "zb": 0.79
        },
        "primaries d50": {
            "xr": 0.648431,   "yr": 0.330856,
            "xg": 0.321152,   "yg": 0.597871,
            "xb": 0.155886,   "yb": 0.066044
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
        "primaries Yz": {
            "zr": 0.03,
            "zg": 0.1,
            "zb": 0.79
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
            # "Yr": 0.297361,
            "xg": 0.21,   "yg": 0.71,
            # "Yg": 0.627355,
            "xb": 0.15,   "yb": 0.06,
            # "Yb": 0.075285
        },
        "primaries d50": {
            "xr": 0.648431,   "yr": 0.330856,
            "xg": 0.230154,   "yg": 0.701572,
            "xb": 0.155886,   "yb": 0.066044
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
        "primaries Yz": {

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
            # "Yr": 0.258187,
            "xg": 0.115,  "yg": 0.826,
            # "Yg": 0.724938,
            "xb": 0.157, "yb": 0.018,
            # "Yb": 0.016875
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
            "xr": 0.7347, "yr": 0.2653,
            # "Yr": 0.288040,
            "xg": 0.1596, "yg": 0.8404,
            # "Yg": 0.711874,
            "xb": 0.0366, "yb": 0.0001,
            # "Yb": 0.000086
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
            "xr": 0.7347, "yr": 0.2653, # Many sources
            # "Yr": 0.176204,
            "xg": 0.2738, "yg": 0.7174, # Many sources
            # "Yg": 0.812985,
            "xb": 0.1666, "yb": 0.0089, # Many sources
            # "Yb": 0.010811
        },
        "primaries d50": { # Lindbloom
            "xr": 0.737385,   "yr": 0.264518,
            "xg": 0.266802,   "yg": 0.718404,
            "xb": 0.174329,   "yb": 0.000599
        },
        "gamma": 2.2},
    "BEST RGB": {  # Source: http://brucelindbloom.com/index.html?WorkingSpaceInfo.html
        "illuminant": "D50",
        "primaries": {
            "xr": 0.7347, "yr": 0.2653,
            # "Yr": 0.228457,
            "xg": 0.215,  "yg": 0.775,
            # "Yg": 0.737352,
            "xb": 0.13,   "yb": 0.035,
            # "Yb": 0.034191
        },
        "gamma": 2.2},
    "BETA RGB": {  # Source: http://brucelindbloom.com/index.html?WorkingSpaceInfo.html
        "illuminant": "D50",
        "primaries": {
            "xr": 0.6888, "yr": 0.3112,
            # "Yr": 0.303273,
            "xg": 0.1986, "yg": 0.7551,
            # "Yg": 0.663786,
            "xb": 0.1265, "yb": 0.0352,
            # "Yb": 0.032941
        },
        "gamma": 2.2},
    "BRUCE RGB": {  # Source: http://brucelindbloom.com/index.html?WorkingSpaceInfo.html
        "illuminant": "D65",
        "primaries": {
            "xr": 0.64,   "yr": 0.33,
            # "Yr": 0.240995,
            "xg": 0.28,   "yg": 0.65,
            # "Yg": 0.683554,
            "xb": 0.15,   "yb": 0.06,
            # "Yb": 0.075452
        },
        "primaries d50": {
            "xr": 0.648431,   "yr": 0.330856,
            "xg": 0.300115,   "yg": 0.64096,
            "xb": 0.155886,   "yb": 0.066044
        },
        "gamma": 2.2},
    "COLORMATCH RGB": {  # Source: http://brucelindbloom.com/index.html?WorkingSpaceInfo.html
        "illuminant": "D50",
        "primaries": {
            "xr": 0.63,   "yr": 0.34,
            # "Yr": 0.274884,
            "xg": 0.295,  "yg": 0.605,
            # "Yg": 0.658132,
            "xb": 0.15,   "yb": 0.075,
            # "Yb": 0.066985
        },
        "gamma": 1.8},
    "DON RGB": {  # Source: http://brucelindbloom.com/index.html?WorkingSpaceInfo.html
        "illuminant": "D50",
        "primaries": {
            "xr": 0.696,  "yr": 0.3,
            # "Yr": 0.27835,
            "xg": 0.215,  "yg": 0.765,
            # "Yg": 0.68797,
            "xb": 0.13,   "yb": 0.035,
            # "Yb": 0.03368
        },
        "gamma": 2.2},
    "EKTA SPACE PS5": {  # Source: http://brucelindbloom.com/index.html?WorkingSpaceInfo.html
        "illuminant": "D50",
        "primaries": {
            "xr": 0.695,  "yr": 0.305,
            # "Yr": 0.260629,
            "xg": 0.26,   "yg": 0.7,
            # "Yg": 0.734946,
            "xb": 0.11,   "yb": 0.005,
            # "Yb": 0.004425
        },
        "gamma": 2.2},
    "SMPTE-C RGB": {  # Source: http://brucelindbloom.com/index.html?WorkingSpaceInfo.html
        "illuminant": "D65",
        "primaries": {
            "xr": 0.63,   "yr": 0.34,
            # "Yr": 0.212395,
            "xg": 0.31,   "yg": 0.595,
            # "Yg": 0.701049,
            "xb": 0.155,  "yb": 0.07,
            # "Yb": 0.086556
        },
        "primaries d50": {
            "xr": 0.638852,   "yr": 0.340194,
            "xg": 0.331007,   "yg": 0.592082,
            "xb": 0.162897,   "yb": 0.079001
        },
        "gamma": 2.2},
    "NTSC-J": {  # Source: https://en.wikipedia.org/wiki/RGB_color_spaces
        "illuminant": "D93",
        "primaries": {
            "xr": 0.63,   "yr": 0.34,
            "xg": 0.31,   "yg": 0.595,
            "xb": 0.155,  "yb": 0.07
        },
        "gamma": 2.5},  # Can't be used because no tristimulus values can be found for D93 (No value in ILLUMINANTS)
    "DCI-P3": {  # Source: https://en.wikipedia.org/wiki/RGB_color_spaces
        "illuminant": "6300K",
        "primaries": {
            "xr": 0.68,   "yr": 0.32,
            "xg": 0.265,  "yg": 0.69,
            "xb": 0.15,   "yb": 0.06
        },
        "gamma": 2.6,
        "decoding gamma": 13/5},  # Commented because it uses 6300K instead of standard illuminant
    "ECI RGB V2": { # v2, Source: http://brucelindbloom.com/index.html?WorkingSpaceInfo.html
        "illuminant": "D50",
        "primaries": {
            "xr": 0.67,   "yr": 0.33,
            # "Yr": 0.32025,
            "xg": 0.21,   "yg": 0.71,
            # "Yg": 0.602071,
            "xb": 0.14,   "yb": 0.08,
            # "Yb": 0.077679
        },
        "gamma": "L*"},  # ECI RGB v2, this is commented because it doesn't use gamma but L* instead which is the L from LAB
    "BLACKMAGIC WIDE GAMUT": { # BLACKMAGIC WIDE GAMUT COLOR SPACE: #= https://drive.google.com/file/d/1FF5WO2nvI9GEWb4_EntrBoV9ZIuFToZd/view
        "illuminant": "",
        "primaries": {
            "xr": 0.7177215,   "yr": 0.3171181,
            "xg": 0.2280410,   "yg": 0.8615690,
            "xb": 0.1005841,   "yb": -0.0820452,
        },
        "white point": {
            "x": 0.3127170,
            "y": 0.3290312,
        }
    },
}


def get_hue(*color, round_: bool = False) -> int | float:
    """### Takes a color and returns its Hue

    ### Args:
        `round_` (bool, optional): Wether to round the final output. Defaults to False.

    ### Returns:
        int | float: Hue
    """
    R, G, B = ih.check_color(color, normalized=True)

    Cmax = max(R, G, B)
    Cmin = min(R, G, B)
    delta = Cmax - Cmin

    if Cmax - Cmin == 0:
        return 0

    #+ Different method, same results
    # if R == Cmax:
    #     H = (60 * ((G - B) / delta) + 360) % 360
    # elif G == Cmax:
    #     H = (60 * ((B - R) / delta) + 120) % 360
    # elif B == Cmax:
    #     H = (60 * ((R - G) / delta) + 240) % 360

    r = (Cmax - R) / delta
    g = (Cmax - G) / delta
    b = (Cmax - B) / delta

    if R == Cmax and G == Cmin:
        H = (5 + b) * 60
    elif R == Cmax:
        H = (1 - g) * 60
    elif G == Cmax and B == Cmin:
        H = (r + 1) * 60
    elif G == Cmax:
        H = (3 - b) * 60
    elif B == Cmax and G == Cmin:
        H = (5 - r) * 60
    else: # B == Cmax
        H = (3 + g) * 60

    return round(H) if round_ else H


# Thanks to: https://chase-seibert.github.io/blog/2011/07/29/python-calculate-lighterdarker-rgb-colors.html
def color_change_old(color: str, /,  value: int = 1, *, brighten: bool = False, pound: bool = True) -> str:
    """### Takes a hex color and brightens/darkens it based on the value. \
    Converts the hex color to r, g, b integers and increases/decreases the number by <value>

    ### Args:
        `color` (str): A hex color in the for of "AABBCC" or "#AABBCC"
        `value` (int, optional): How much the color will brighten/darken. Defaults to 1.
        `brighten` (bool, False): If we want to brighten or darnek the color
        `pound` (bool): Wether to return the result with a pound sign prefix (#AABBCC)

    ### Returns:
        str: A hex color in the form of "#AABBCC"
    """
    color = color.strip("#")
    if len(color) != 6:
        raise ValueError("Incorrect color input")

    # For every color get the next brighter/darker color based on value. Use 0 if result < 0 and 255 if result > 255
    if brighten:
        new_color_int = [min(int(color[i:i+2], base=16) + value, 255) for i in (0, 2, 4)]
    else:
        new_color_int = [max(int(color[i:i+2], base=16) - value, 0) for i in (0, 2, 4)]

    # Make the new color in hex color format
    hexed = ''.join((f"0{hex(i)[2:]}" if len(hex(i)[2:]) == 1 else hex(i)[2:] for i in new_color_int))

    pound_sign = "#" if pound else ""
    return f"{pound_sign}{hexed}"


def darker_color(*color, level, mode: str = "hsv", normalized: bool = False):
    '''### Create a darker color based "color".

    ### Args:
        `colors` (str | tuple | list | int | float):
        *       `str`: If a string is passed, it should be in the form of a hex color "FFFFFF" or "#FFFFFF"
        *       `tuple | list`: If any of these is passed, it shuold be ordered as (R, G, B)
                    where all elements are either in int range(0, 255) or in float range(0, 1)
        *       `int | float`: Integers and floats can only be passed in pairs of 3 consecutive values of the same kind
                        Ex. 128, 84, 31 | Ex2. 0.34, 0.14, 0.78

        `level` (int): Range  0-100. How darker the new color should be
        `mode` (str): Either "hsl" or "hsv". Method for calculating the new color. Defaults to "hsv".
        `normalized` (bool): Wether the return color shuold have normalized values (in range 0-1). Defaults to False.

    ### Returns:
        tuple[r, g, b]
    '''
    normalized = "normalized" if normalized else "round"
    R, G, B = ih.check_color(color)
    if mode.lower() == "hsl":
        H, S, L = co.rgb_to_hsl(R, G, B)
        L = max(L - level, 0)
        return co.hsl_to_rgb(H, S, L, output=normalized)

    H, S, V = co.rgb_to_hsv(R, G, B)
    V = max(V - level, 0)
    return co.hsv_to_rgb(H, S, V, output=normalized)


def brighter_color(*color, level, mode: str = "hsv", normalized: bool = False):
    '''### Create a brighter color based "color".

    ### Args:
        `colors` (str | tuple | list | int | float):
        *       `str`: If a string is passed, it should be in the form of a hex color "FFFFFF" or "#FFFFFF"
        *       `tuple | list`: If any of these is passed, it shuold be ordered as (R, G, B)
                    where all elements are either in int range(0, 255) or in float range(0, 1)
        *       `int | float`: Integers and floats can only be passed in pairs of 3 consecutive values of the same kind
                        Ex. 128, 84, 31 | Ex2. 0.34, 0.14, 0.78

        `level` (int): Range  0-100. How brighter the new color should be
        `mode` (str): Either "hsl" or "hsv". Method for calculating the new color. Defaults to "hsv".
        `normalized` (bool): Wether the return color shuold have normalized values (in range 0-1). Defaults to False.

    ### Returns:
        tuple[r, g, b]
    '''
    normalized = "normalized" if normalized else "round"
    R, G, B = ih.check_color(color)
    if mode.lower() == "hsl":
        H, S, L = co.rgb_to_hsl(R, G, B)
        L = min(L + level, 100)
        return co.hsl_to_rgb(H, S, L, output=normalized)

    H, S, V = co.rgb_to_hsv(R, G, B)
    V = min(V + level, 100)
    return co.hsv_to_rgb(H, S, V, output=normalized)


def interpolate_hsl(color1, color2, factor=50, output: str = "hex"):
    """### Creates a median color between color1 and color2 based on the factor using HSL

    ### Args:
        `color1, color2` (str | tuple | list):
        *       `str`: If a string is passed, it should be in the form of a hex color "FFFFFF" or "#FFFFFF"
        *       `tuple | list`: If any of these is passed, it shuold be ordered as (R, G, B)
                    where all elements are either in int range(0, 255) or in float range(0, 1)

        `factor` (int | float, optional): Range 0-100. 0 == color1, 100 == color2. Defaults to 50.
        `output` (str, optional): Either "hex", "hexp", "normalized", "round" or "direct"
        *     hex returns a hex string color in the form of AABBCC
        *     hexp returns a hex string color in the form of #AABBCC
        *     normalized returns a tuple(R, G, B) where the values are floats in range(0, 1)
        *     round returns a tuple(R, G, B) where the values are integers in range(0, 255)
        *     direct returns a tuple(R, G, B) where the values are floats in range(0, 255)
        *     In any invalid case the "direct" approach will be used

    ### Returns:
        str | tuple[r, g, b]: Returns a tuple with colors in one of the following formats:
        >>>   "AABBCC" | "#AABBCC" | (170, 187, 204) | (0.66, 0.73, 0.8)
    """
    factor /= 100
    color1 = list(co.rgb_to_hsl(color1, output="normalized"))
    color2 = co.rgb_to_hsl(color2, output="normalized")
    for i in range(3):
        color1[i] += factor * (color2[i] - color1[i])

    return ih.return_rgb(co.hsl_to_rgb(color1), output=output)


def hsl2rgb(h,s,l):
    a = s * min(l, 1 - l)
    def func_n(n):
        k = (n + h / 30) % 12
        return l - a * max(min(k - 3, 9 - k, 1), -1)
    return func_n(0) * 255, func_n(8) * 255, func_n(4) * 255


#!##### HEX WORDS #######
# c0ffee, decaff
# dec0de, 0ff1ce
# decade, facade
# c0ffed, dec1de
# add1c7, effec7
