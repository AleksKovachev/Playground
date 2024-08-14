"""A tester module for all functions"""
import math
import unittest

from collections.abc import Sequence

from .constants import *
from color_utilities import *


def logg(*args, level=0):
    """Logging based on level of priority"""
    if level <= LOG_LEVEL:
        print(*args)


brights = [(BRIGHTNESS_VALUES[i-1][0], get_color_brightness(COLORS['purple']['hex'], method=i, output=Out2.DIRECT))
            for i in range(1, len(BRIGHTNESS_VALUES) + 1)]

logg('\n'*2 + '#'*80 + '\n', level=2)
for n, (i, k) in enumerate(brights):
    logg(f"{i}{' ' * ((len(brights[3][0]) - len(brights[n][0])) + 4)}{round(k, 3)} %", level=2)
    logg(f"{' ' * ((len(brights[3][0])) + 4)}{k/100}", level=2)
    logg("-"*80, level=2)
    assert round(k, 3) == BRIGHTNESS_VALUES[n][1]
    assert k / 100 == BRIGHTNESS_VALUES[n][2]


def convert_hsl_hls(hsl: Sequence) -> tuple:
    """Coverts HSL to HLS by swapping the 2 values (SL)"""
    return hsl[0], hsl[2], hsl[1]


def to_direct(color: Sequence, is_rgb: bool = False, depth: int = 8):
    """Converts normalized color to direct output type"""
    if is_rgb:
        return tuple(i * (2**depth - 1) for i in color)
    return color[0] * 360, color[1] * 100, color[2] * 100

class TestRGBConverters(unittest.TestCase):
    """A tester class for all functions

    ## N/B: HSL/HSV/HSI/HSP to RGB conversions don't always give the exact RGB color that was \
    the result of the opposite conversion. This is because RGB has more colors than all \
    of these representations. For that reason, math.isclose() is being used where needed \
    to account for expected disparity."""

    def test_rgb_to_web_safe(self):
        """Test RGB->Web Safe"""
        self.assertEqual(rgb_to_web_safe(COLORS['blue']['hex']), (102, 102, 204))
        self.assertEqual(rgb_to_web_safe(COLORS['purple']['hexp'], output=Out1.HEX), "6633cc")
        self.assertEqual(rgb_to_web_safe(COLORS['gray']['hex'], output=Out1.HEXP), "#333333")
        self.assertEqual(rgb_to_web_safe(COLORS['yellow']['rgb'], output=Out1.NORMALIZED), (0.6, 0.6, 0.4))
        self.assertEqual(rgb_to_web_safe(COLORS['tan']['normal'], output=Out1.ROUND), (255, 204, 153))
        self.assertEqual(rgb_to_web_safe(*COLORS['amber']['rgb'], output=Out1.DIRECT), (0, 51, 204))

    def test_hex_to_rgb_and_back(self):
        """Test RGB<->HEX conversion"""
        for color, vals in COLORS.items():
            depth = 10 if color == "red" else 8

            # HEX -> RGB
            self.assertEqual(hex_to_rgb(vals['hex'], depth=depth), list(vals['rgb']))
            self.assertEqual(hex_to_rgb(vals['hex'], depth=depth), list(vals['rgb']))

            # RGB -> HEX
            self.assertEqual(rgb_to_hex(vals['rgb'], depth=depth), vals['hexp'])
            self.assertEqual(rgb_to_hex(*vals['rgb'], depth=depth, pound=True), vals['hexp'])
            self.assertEqual(rgb_to_hex(vals['hex'], depth=depth, pound=False), vals['hex'])
            self.assertEqual(rgb_to_hex(vals['normal'], depth=depth, pound=False), vals['hex'])

    def test_rgb_to_hsl_hls_and_back(self):
        """Test RGB->HSL/HLS conversion"""
        for color, vals in COLORS.items():
            depth = 10 if color == "red" else 8

            # RGB-> HSL
            self.assertEqual(rgb_to_hsl(vals['hex'], depth=depth), vals['hsl'])

            result = zip(rgb_to_hsl(vals['rgb'], depth=depth, output=Out2.HALF_NORMALIZED), vals['hsl_h-norm'])
            self.assertTrue(all(math.isclose(i, j, abs_tol=0.005) for i, j in result))

            result = zip(rgb_to_hsl(*vals['rgb'], depth=depth, output=Out2.NORMALIZED), vals['hsl_norm'])
            self.assertTrue(all(math.isclose(i, j, abs_tol=0.005) for i, j in result))

            result = zip(rgb_to_hsl(*vals['normal'], depth=depth, output=Out2.DIRECT), to_direct(vals['hsl_norm']))
            self.assertTrue(all(math.isclose(i, j, abs_tol=0.5) for i, j in result))

            # RGB -> HLS
            self.assertEqual(rgb_to_hls(vals['hexp'], depth=depth), convert_hsl_hls(vals['hsl']))

            expected = convert_hsl_hls(vals['hsl_h-norm'])
            result = zip(rgb_to_hls(vals['rgb'], depth=depth, output=Out2.HALF_NORMALIZED), expected)
            self.assertTrue(all(math.isclose(i, j, abs_tol=0.005) for i, j in result))

            expected = convert_hsl_hls(vals['hsl_norm'])
            result = zip(rgb_to_hls(*vals['rgb'], depth=depth, output=Out2.NORMALIZED), expected)
            self.assertTrue(all(math.isclose(i, j, abs_tol=0.005) for i, j in result))

            result = zip(rgb_to_hls(*vals['normal'], depth=depth, output=Out2.DIRECT), 
                         convert_hsl_hls(to_direct((vals['hsl_norm']))))
            self.assertTrue(all(math.isclose(i, j, abs_tol=0.5) for i, j in result))

            # HSL -> RGB
            expected = vals.get('rgb_expected', vals['rgb'])
            result = zip(hsl_to_rgb(vals['hsl'], depth=depth), expected)
            self.assertTrue(all(math.isclose(i, j, abs_tol=2) for i, j in result))

            self.assertEqual(hsl_to_rgb(*vals['hsl'], depth=depth, output=Out1.HEX), vals['hex_expected'])
            self.assertEqual(hsl_to_rgb(*vals['hsl_norm'], depth=depth, output=Out1.HEXP), f"#{vals['hex_expected']}")

            result = zip(hsl_to_rgb(vals['hsl_h-norm'], depth=depth, output=Out1.NORMALIZED), vals['normal'])
            self.assertTrue(all(math.isclose(i, j, abs_tol=0.008) for i, j in result))

            result = zip(hsl_to_rgb(vals['hsl_norm'], depth=depth, output=Out1.DIRECT), expected)
            self.assertTrue(all(math.isclose(i, j, abs_tol=2.5) for i, j in result))

            # HLS -> RGB
            hls = convert_hsl_hls(vals['hsl'])
            result = zip(hls_to_rgb(hls, depth=depth), expected)
            self.assertTrue(all(math.isclose(i, j, abs_tol=2) for i, j in result))

            self.assertEqual(hls_to_rgb(hls, depth=depth, output=Out1.HEX), vals['hex_expected'])
            hls = convert_hsl_hls(vals['hsl_norm'])
            self.assertEqual(hls_to_rgb(hls, depth=depth, output=Out1.HEXP), f"#{vals['hex_expected']}")

            result = zip(hls_to_rgb(hls, depth=depth, output=Out1.DIRECT), expected)
            self.assertTrue(all(math.isclose(i, j, abs_tol=2.5) for i, j in result))

            hls = convert_hsl_hls(vals['hsl_h-norm'])
            result = zip(hls_to_rgb(hls, depth=depth, output=Out1.NORMALIZED), vals['normal'])
            self.assertTrue(all(math.isclose(i, j, abs_tol=0.008) for i, j in result))

    def test_rgb_to_hsv_and_back(self):
        """Test RGB<->HSV/HSB conversion"""
        for color, vals in COLORS.items():
            depth = 10 if color == "red" else 8

            # RGB -> HSV
            self.assertEqual(rgb_to_hsv(vals['hex'], depth=depth), vals['hsv'])

            result = zip(rgb_to_hsv(vals['hexp'], depth=depth, output=Out2.NORMALIZED), vals['hsv_norm'])
            self.assertTrue(all(math.isclose(i, j, abs_tol=0.005) for i, j in result))

            result = zip(rgb_to_hsv(vals['rgb'], depth=depth, output=Out2.HALF_NORMALIZED), vals['hsv_h-norm'])
            self.assertTrue(all(math.isclose(i, j, abs_tol=0.005) for i, j in result))

            result = zip(rgb_to_hsv(*vals['normal'], depth=depth, output=Out2.DIRECT), vals['hsv'])
            self.assertTrue(all(math.isclose(i, j, abs_tol=0.5) for i, j in result))

            # HSV -> RGB
            expected = vals.get('rgb_expected', vals['rgb'])
            result = zip(hsv_to_rgb(*vals['hsv'], depth=depth), expected)
            self.assertTrue(all(math.isclose(i, j, abs_tol=1) for i, j in result))

            result = zip(hsv_to_rgb(vals['hsv_norm'], depth=depth, output=Out1.NORMALIZED), vals['normal'])
            self.assertTrue(all(math.isclose(i, j, abs_tol=0.006) for i, j in result))

            result = zip(hsv_to_rgb(vals['hsv_h-norm'], depth=depth, output=Out1.DIRECT), expected)
            self.assertTrue(all(math.isclose(i, j, abs_tol=1.5) for i, j in result))

            result = hex_to_rgb(hsv_to_rgb(vals['hsv_norm'], depth=depth, output=Out1.HEX), depth=depth)
            expected = vals.get('rgb_expected', hex_to_rgb(vals['hex'], depth=depth))
            self.assertTrue(all(math.isclose(i, j, abs_tol=1) for i, j in zip(result, expected)))

    def test_hsv_to_hsl_and_back(self):
        """Test HSV<->HSL conversion"""
        for color, vals in COLORS.items():
            if color == "red":
                continue

            # HSV -> HSL
            result = zip(hsv_to_hsl(vals['hsv']), vals['hsl'])
            self.assertTrue(all(math.isclose(i, j, abs_tol=1) for i, j in result))

            result = zip(hsv_to_hsl(*vals['hsv'], output=Out2.HALF_NORMALIZED), vals['hsl_h-norm'])
            self.assertTrue(all(math.isclose(i, j, abs_tol=0.011) for i, j in result))

            result = zip(hsv_to_hsl(vals['hsv_norm'], output=Out2.NORMALIZED), vals['hsl_norm'])
            self.assertTrue(all(math.isclose(i, j, abs_tol=0.011) for i, j in result))

            result = zip(hsv_to_hsl(vals['hsv_h-norm'], output=Out2.DIRECT), to_direct(vals['hsl_norm']))
            self.assertTrue(all(math.isclose(i, j, abs_tol=1.1) for i, j in result))

            # HSL -> HSV
            result = zip(hsl_to_hsv(vals['hsl']), vals['hsv'])
            self.assertTrue(all(math.isclose(i, j, abs_tol=1) for i, j in result))

            result = zip(hsl_to_hsv(vals['hsl'], output=Out2.HALF_NORMALIZED), vals['hsv_h-norm'])
            self.assertTrue(all(math.isclose(i, j, abs_tol=0.01) for i, j in result))

            result = zip(hsl_to_hsv(*vals['hsl'], output=Out2.NORMALIZED), vals['hsv_norm'])
            self.assertTrue(all(math.isclose(i, j, abs_tol=0.01 ) for i, j in result))

            result = list(zip(hsl_to_hsv(vals['hsl_h-norm'], output=Out2.DIRECT), to_direct(vals['hsv_norm'])))
            self.assertTrue(all(math.isclose(i, j, abs_tol=1.1) for i, j in result))

    def test_rgb_to_hsi_and_back(self):
        """Test RGB<->HSI conversion"""
        for color, vals in COLORS.items():
            depth = 10 if color == "red" else 8

            # RGB -> HSI
            self.assertEqual(rgb_to_hsi(vals['hexp'], depth=depth), vals['hsi'])

            result = zip(rgb_to_hsi(vals['hexp'], depth=depth, output=Out2.HALF_NORMALIZED), vals['hsi_h-norm'])
            self.assertTrue(all(math.isclose(i, j, abs_tol=0.005) for i, j in result))

            result = zip(rgb_to_hsi(vals['hexp'], depth=depth, output=Out2.NORMALIZED), vals['hsi_norm'])
            self.assertTrue(all(math.isclose(i, j, abs_tol=0.005) for i, j in result))

            result = zip(rgb_to_hsi(vals['hexp'], depth=depth, output=Out2.DIRECT), to_direct(vals['hsi_norm']))
            self.assertTrue(all(math.isclose(i, j, abs_tol=0.5) for i, j in result))

            # HSI -> RGB
            tol = 2 if color != "red" else 12.1
            result = zip(hsi_to_rgb(vals['hsi'], depth=depth), vals['rgb'])
            self.assertTrue(all(math.isclose(i, j, abs_tol=tol) for i, j in result))

            result = zip(hsi_to_rgb(vals['hsi_norm'], depth=depth, output=Out1.NORMALIZED), vals['normal'])
            self.assertTrue(all(math.isclose(i, j, abs_tol=0.05) for i, j in result))

            expected = to_direct(vals['normal'], True, depth)
            result = zip(hsi_to_rgb(*vals['hsi_norm'], depth=depth, output=Out1.DIRECT), expected)
            self.assertTrue(all(math.isclose(i, j, abs_tol=tol) for i, j in result))

            expected = hex_to_rgb(vals['hex'], depth=depth)
            result = hex_to_rgb(hsi_to_rgb(vals['hsi_h-norm'], depth=depth, output=Out1.HEX), depth=depth)
            self.assertTrue(all(math.isclose(i, j, abs_tol=tol) for i, j in zip(result, expected)))

    def test_rgb_to_hsp_and_back(self):
        """Test RGB<->HSP conversion"""





#!!!!!!!!!!!!!!!!!!! Change "check_..." to "validate..." function names. Check how to use Pydantic for the checks



#* Test RGB<->CMYK conversion
res = rgb_to_cmyk('7838d5')
assert res == [44, 74, 0, 16]

res = rgb_to_cmyk((151/255, 162/255,  90/255), normalized=1)
assert res == (0.06790123456790118, 0.0, 0.4444444444444443, 0.3647058823529412)

res = cmyk_to_rgb(44, 74, 0, 16)
assert res == (120, 56, 214)

res = cmyk_to_rgb(7, 0, 44, 36, output=Out1.NORMALIZED)
assert res == (0.5952, 0.64, 0.35840000000000005)

res = cmyk_to_rgb(17, 31, 68, 12, output=Out1.HEX)
assert res == "ba9b48"

res = cmyk_to_rgb(32, 5, 52, 46, output=Out1.HEXP)
assert res == "#5e8342"

res = cmyk_to_rgb(0, 10, 20, 30, output=Out1.DIRECT)
assert res == (178.5, 160.65, 142.79999999999998) and round(res[2], 1) == 142.8


#* Test RGB<->XYZ conversion
res = rgb_to_xyz('7838d5', illuminant='D50')
assert res == (3.1680645805553973, 2.420809770725088, 4.8338859165344035)

res = rgb_to_xyz(254/255, 220/255, 145/255, output=Out3.DIRECT)
assert res == (6.36174649426334, 6.73263522127117, 5.128048928549748)

res = xyz_to_rgb(21, 12, 64)
assert res == (255, 255, 255)

res = xyz_to_rgb(71.57919445658126, 74.30465989427253, 37.35442174882148)
assert res == (255, 255, 255)

res = xyz_to_lab(71.57919445658126, 74.30465989427253, 37.35442174882148, xyz_illuminant='D65')
assert res == (89.06627604445214, 2.031819905858656, 41.13931492256056)

for i in ("hex", "hexp", "rgb", "normal"):
    res = cu.desaturate(COLORS['yellow'][i])
    assert res == "9aa364"


#* Test HSV<->HSI conversion
res = hsv_to_hsi(COLORS['blue']['hsv'])
assert res == (215, 38, 50)

res = hsv_to_hsi(*COLORS['blue']['hsv'], output=Out2.DIRECT)
assert res == (214.99999999999994, 38.49821215733016, 50.34)

res = hsv_to_hsi(COLORS['blue']['hsv_norm'], output=Out2.NORMALIZED)
assert res == (0.5972222222222221, 0.3849821215733016, 0.5034000000000001)

res = hsv_to_hsi(*COLORS['blue']['hsv_h-norm'], output=Out2.HALF_NORMALIZED)
assert res == (215, 0.3849821215733016, 0.5034000000000001)

res = hsi_to_hsv(COLORS['yellow']['hsi'])
assert res == (69, 44, 64)

res = hsi_to_hsv(*COLORS['yellow']['hsi'], output=Out2.DIRECT)
assert res == (69.0, 44.40457501681992, 63.87216216216216)

res = hsi_to_hsv(*COLORS['yellow']['hsi_norm'], output=Out2.NORMALIZED)
assert res == (0.19166666666666668, 0.4440457501681992, 0.6387216216216216)

res = hsi_to_hsv(*COLORS['yellow']['hsi_h-norm'], output=Out2.HALF_NORMALIZED)
assert res == (69, 0.4440457501681992, 0.6387216216216216)


# print(xyz.working_space_matrix("ADOBE RGB", "D65")[1])
# print(xyz.get_adaptation_matrix(xyz.ILLUMINANTS["2"]["D50"], xyz.ILLUMINANTS["2"]["D65"], "bradford"))
# print(cu.get_color_brightness(234, 139, 79))

# print(co.yxy_to_xyz(1, 0.3127, 0.329))


# import colour
# color = (116/255, 8/255, 10/255)
# color = (116, 8, 10)

# qz = colour.RGB_to_IHLS(color)
# az = rgb_to_ihls(color, output="normalized")
# print(f"{qz = }")
# print(f"{az = }")

# qz = colour.IHLS_to_RGB(qz)
# az = ihls_to_rgb(az, output="direct")

# print("--------------------------------")
# print(f"{qz = }")
# print(f"{az = }")
# WEIGHTS = {
#     "ITU-R BT.601": (0.299, 0.114),
#     "ITU-R BT.709": (0.2126, 0.0722),
#     "ITU-R BT.2020": (0.2627, 0.0593),
#     "ITU BT.470-6": (0.2220, 0.0713),
#     "SMPTE-240M": (0.2122, 0.0865)}

# print(RGB_to_YCbCr(
#     color,
#     K=WEIGHTS["ITU-R BT.709"],
#     in_depth = 10,
#     in_legal = 0,

#     out_depth = 8,
#     out_legal = 0,
#     clamp = False,
#     output="round"))

# print("================================")
# color = (116/255, 8/255, 10/255)
# print(colour.models.rgb.ycbcr.RGB_to_YCbCr(
#     color,
#     K=WEIGHTS["ITU-R BT.709"],
#     in_bits = 10,
#     in_legal = 0,
#     in_int = False,

#     out_bits = 8,
#     out_legal = 0,
#     out_int = True,
#     clamp_int = False))
# a = check_color("#4E8653", normalized=True)


# import numpy as np

# R, G, B = (0/255, 2/255, 140/255)

# print(rgb_to_xyz(255, 0, 129))

# print(xyz_to_rgb(45, 23, 23))
# print(yxy_to_xyz((1.00000, 0.95047, 1.08883)))
# print(xyz_to_yxy(0.64, 0.33, 0.03))


if __name__ == "__main__":
    unittest.main()
