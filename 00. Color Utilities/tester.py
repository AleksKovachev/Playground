# pylint: disable=all

from time import perf_counter
from pprint import pprint

from main import *
import color_utilities.color_utils as cu
import color_utilities.converters as co
import color_utilities.internal_helpers as ih
from color_utilities import xyz
from color_utilities import transfer_functions as tf


# Lightness Test
# Test colors:
COLORS = {#*      B>G>R                B>R>G           R=G=B           G>R>B            R>G>B          10-bit
        "hex":   ("4f7bb8",          "7838d5",       "494949",       "97a25a",        "F5DC91",     "3fd0020d8"),
        "hexp":  ("#4f7bb8",        "#7838d5",      "#494949",      "#97a25a",       "#F5DC91",     "#3fd0020d8"),
        "rgb":  ((79, 123, 184), (120, 56, 213),   (73, 73, 73),  (151, 162, 90), (245, 220, 145), (1021, 2, 216)),
        "normal": ((79/255, 123/255, 184/255), (120/255, 56/255,  213/255), (73/255, 73/255, 73/255),
                    (151/255, 162/255, 90/255), (254/255, 220/255, 145/255), (1021/1023, 2/1023, 216/1023)),
        "hsv":  ((215, 57, 72),   (264, 74, 84),    (0, 0, 29),    (69, 44, 64),    (45, 41, 96),  (347, 100, 100)),
        "hsv_norm":  ((215/360, 57/100, 72/100), (264/360, 74/100, 84/100), (0/360, 0/100, 29/100),
                    (69/360, 44/100, 64/100), (45/360, 41/100, 96/100), (347/360, 100/100, 100/100)),
        "hsv_h-norm":  ((215, 57/100, 72/100), (264, 74/100, 84/100), (0, 0/100, 29/100),
                    (69, 44/100, 64/100), (45, 41/100, 96/100), (347, 100/100, 100/100)),
        "hsl":  ((215, 43, 52),   (264, 65, 53),    (0, 0, 29),    (69, 29, 49),    (45, 83, 76),  (347, 100, 50)),
        "hsl_norm": ((215/360, 43/100, 52/100), (264/360, 65/100, 53/100), (0/360, 0/100, 29/100),
                    (69/360, 29/100, 49/100), (45/360, 83/100, 76/100), (347/360, 100/100, 50/100)),
        "hsl_h-norm": ((215, 43/100, 52/100), (264, 65/100, 53/100), (0, 0/100, 29/100),
                    (69, 29/100, 49/100), (45, 83/100, 76/100), (347, 100/100, 50/100)),
        "hsi":  ((215, 39, 50),   (264, 57, 51),    (0, 0, 29),    (69, 33, 53),    (45, 29, 80),  (347, 100, 40)),
        "hsi_norm":  ((215/360, 39/100, 50/100), (264/360, 57/100, 51/100), (0/360, 0/100, 29/100),
                    (69/360, 33/100, 53/100), (45/360, 29/100, 80/100), (347/360, 100/100, 40/100)),
        "hsi_h-norm":  ((215, 39/100, 50/100), (264, 57/100, 51/100), (0, 0/100, 29/100),
                    (69, 33/100, 53/100), (45, 29/100, 80/100), (347, 100/100, 40/100)),
        "xyz_d65": ((19, 19, 48), (21, 12, 64),     (6, 7, 7),    (28, 33, 15),    (68, 73, 37),        ()),
        "xyz_d50": ((19, 19, 48), (19, 11, 64),     (6, 7, 7),    (29, 33, 11),    (71, 74, 28),        ()),
}

# Color brightness method comarison
def test_color_brightness():

    methods = (
        '1 - HSV Value', '2 - HSI Intensity', '3 - HSL Lightness', '4 - HSP Perceived Brightness / Weighted Euclidean Norm',
        '5 - HSP Perceived Brightness Old', '6 - Euclidean Norm', '7 - Geometric Mean', '8 - Luma, Adobe',
        '9 - Luma, Rec709/sRGB (HDTV)', '10 - Luma, Rec2020 UHDTV, HDR', '11 - Luminance (Y) sRGB', '12 - Perceived Lightness (L*) from L*ab')
    brights = [(methods[i-1], get_color_brightness(COLORS["hex"][1], method=i, output="direct")) for i in range(1, len(methods) + 1)]

    print('\n'*2 + '#'*80 + '\n')
    for n, (i, k) in enumerate(brights):
        print(f"{i}{' ' * ((len(brights[3][0]) - len(brights[n][0])) + 4)}{round(k, 3)} %")
        print(f"{' ' * ((len(brights[3][0])) + 4)}{k/100}")
        print("-"*80)

#* HEX
def hex_tests():
    print(f"hex_to_rgb(pounded): {hex_to_rgb('#822720')}")
    print(f"hex_to_rgb(clear)  : {hex_to_rgb('4f7bb8', normalized=1)}")

    print(f"rgb_to_hex(clear): {rgb_to_hex(120, 56, 213)}")
    print(f"rgb_to_hex(tuple):  {rgb_to_hex((120, 56, 213), pound=0)}")
    print(f"rgb_to_hex(norml): {rgb_to_hex(0.592156862745098, 0.6352941176470588, 0.35294117647058826)}")

#* HSL / HLS
def hsl_tests():
    print(f"gb_to_hsl: {rgb_to_hsl('#822720')}")
    print(f"gb_to_hsl: {rgb_to_hsl(120, 56, 213, output='')}")
    print(f"gb_to_hsl: {rgb_to_hsl('494949', output='normalized')}")
    print(f"gb_to_hsl: {rgb_to_hsl(0.592156862745098, 0.6352941176470588, 0.35294117647058826, output='normalized')}")
    print("-"*70)
    print(f"gb_to_hls: {rgb_to_hls('#822720', output='round')}")
    print(f"gb_to_hls: {rgb_to_hls(120, 56, 213)}")
    print(f"gb_to_hls: {rgb_to_hls('494949', output='normalized')}")
    print(f"gb_to_hls: {rgb_to_hls(0.592156862745098, 0.6352941176470588, 0.35294117647058826, output='normalized')}")

#* HSV/HSB
def hsv_tests():
    print(f"rgb_to_hsv: {rgb_to_hsv('F5DC91')}")
    print(f"rgb_to_hsv: {rgb_to_hsv('#494949')}")
    print(f"rgb_to_hsv: {rgb_to_hsv(0.47058823529411764, 0.2196078431372549,  0.8352941176470589, output='')}")
    print("-"*70)
    print(f"hsv_to_rgb: {hsv_to_rgb(264, 74, 84)}")
    print(f"hsv_to_rgb: {hsv_to_rgb((264/360, 74/100, 84/100))}")
    print(f"hsv_to_rgb: {hsv_to_rgb(45, 41, 96, output='normalized')}")
    print(f"hsv_to_rgb: {hsv_to_rgb(45, 0, 45, output='round')}")
    print("-"*70)
    print(f"hsv_to_hsl: {hsv_to_hsl((264, 74, 84))}")
    print(f"hsv_to_hsl: {hsv_to_hsl(69, 44, 64, output='')}")
    print(f"hsv_to_hsl: {hsv_to_hsl(215, 57, 72, output='normalized')}")
    print("-"*70)
    print(f"hsl_to_hsv: {hsl_to_hsv((215, 43, 52))}")
    print(f"hsl_to_hsv: {hsl_to_hsv(41, 98, 78, output='')}")
    print(f"hsl_to_hsv: {hsl_to_hsv(69, 29, 49, output='normalized')}")

#* CMYK
def cmyk_tests():
    print(f"rgb_to_cmyk: {rgb_to_cmyk('7838d5')}")
    print(f"rgb_to_cmyk: {rgb_to_cmyk((151/255, 162/255,  90/255), normalized=1)}")
    print("-"*70)
    print(f"cmyk_to_rgb: {cmyk_to_rgb(44, 74, 0, 16)}")
    print(f"cmyk_to_rgb: {cmyk_to_rgb(7, 0, 44, 36, normalized=0)}")

#* XYZ
def xyz_():
    print(f"rgb_to_xyz: {rgb_to_xyz('7838d5', illuminant='D50', output='round')}")
    print(f"rgb_to_xyz: {rgb_to_xyz(254/255, 220/255, 145/255, output='direct')}")
    print(f"xyz_to_rgb: {xyz_to_rgb(21, 12, 64)}")
    print(f"xyz_to_rgb: {xyz_to_rgb(71.57919445658126, 74.30465989427253, 37.35442174882148)}")
    print(f"xyz_to_lab: {xyz_to_lab(71.57919445658126, 74.30465989427253, 37.35442174882148, illuminant='D65')}")

# test_color_brightness()
# hex_tests()
# hsl_tests()
# hsv_tests()
# cmyk_tests()
# xyz_()
