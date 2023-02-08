"""This is a collection of useful functions for working with colors"""
from color_utilities import internal_helpers
from color_utilities import color_utils
from color_utilities import converters
# TODOs:
# Add HCL<->RGB - Hue, Chroma, Luminance
# Add IHLS<->RGB - Improved HLS


# TODOs:
# Include all illuminants from additionals.py in the code.
# Make xyz_to_rgb and rgb_to_xyz functions work with any color depth
# When reading strings (especially color_space_props), in refine_rgb()
    # make it delete epty space chars inside strings as well
# Make the CMYK calculations more accurate by going through XYZ values
# Make indirect conversions. Ex. hsl_to_hsi = hsl_to_rgb() + rgb_to_hsi(), etc.

#* Converters
# HEX
hex_to_rgb = converters.hex_to_rgb
rgb_to_hex = converters.rgb_to_hex

# HSL/HLS
rgb_to_hsl = converters.rgb_to_hsl
rgb_to_hls = converters.rgb_to_hls
hls_to_rgb = converters.hls_to_rgb
hsl_to_rgb = converters.hsl_to_rgb

# HSV/HSB
rgb_to_hsv = converters.rgb_to_hsv
hsv_to_rgb = converters.hsv_to_rgb
hsv_to_hsl = converters.hsv_to_hsl
hsl_to_hsv = converters.hsl_to_hsv

# CMYK
rgb_to_cmyk = converters.rgb_to_cmyk
cmyk_to_rgb = converters.cmyk_to_rgb

# XYZ
rgb_to_xyz = converters.rgb_to_xyz
xyz_to_rgb = converters.xyz_to_rgb
xyz_to_lab = converters.xyz_to_lab

#* Internal helper functions
check_color     = internal_helpers.check_color
check_hsw       = internal_helpers.check_hsw
integers_floats = internal_helpers.integers_floats

#* Useful utility functions
get_color_brightness = color_utils.get_color_brightness
color_change         = color_utils.color_change
get_median_color     = color_utils.get_median_color
lighten_darken_color = color_utils.half_color
get_hue              = color_utils.get_hue
