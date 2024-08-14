## **Color Utilities**

This is a package I put up for working with colors. It's sole purpose is to be as simple to use as possible which
is why I took the procedural approach with it. Everything inside is over-commented and every function has a detailed
docstring.

### The package is still in development! There are things that are not yet tested or documented.
If you spot any issues, please don't hesitate to contact me.

### **Python version: 3.10 or above**

##### I'm using VSCode for the development. Along with it, I'm using the extension `better comments` with ID aaron-bond.better-comments
Install it if you want to be able to view all comments color coded and use the settings at the bottom of this file.


# This markdown file is not up-to-date with the latest version of the library!!!

## ***Contents***


### **tester**
This file contains some unit tests. Not all tests are written yet, it's a work-in-progress.

### ***color_utilities folder***


### **\_\_init__**
The __init__ file provides a shortcut to every function in the package, as well as some combo functions.
The additional functions are not yet complete, but at the moment are:

#### *hsv_to_hsi & hsi_to_hsv*
Converts HSV color to HSI and vice-versa.

#### *hsv_to_hsp & hsp_to_hsv*
Converts HSV color to HSP and vice-versa.

#### *hsl_to_hsi & hsi_to_hsl*
Converts HSL color to HSI and vice-versa.

#### *hsl_to_hsp & hsp_to_hsl*
Converts HSL color to HSP and vice-versa.

#### *hsi_to_hsp & hsp_to_hsi*
Converts HSI color to HSP and vice-versa.

#### *rgb_to_lab & lab_to_rgb*
Converts RGB color to CIE L*ab and vice-versa.


### **color_space**
This module contains data for various color spaces in the form of a dictionary.
It contains the following color spaces:
ACES2065-1 (ACES), ACEScc, ACEScct, ACEScg, ACESproxy, ARRI Wide Gamut 3 (ALEXA Wide Gamut), ARRI Wide Gamut 4,
Adobe RGB (adobe1998), Adobe Wide Gamut, Apple RGB, Best RGB, Beta RGB, Blackmagic Wide Gamut, Bruce RGB, CIE RGB,
Cinema Gamut, Colormatch RGB, DaVinci Wide Gamut, DCDM (in development), DCI-P3, DCI-P3-P, DJI D-Gamut, Display P3,
DON RGB v4, Dragoncolor, Dragoncolor 2, EBU TECH. 3213-E, ECI RGB v2, EKTA Space PS 5, ERIMM, FUJI F-Gamut,
Filmlight E-Gamut, ITU-T H.273 - 22 Unspecified, ITU-T H.273 - Generic Film, M.A.C (MAC), MAX RGB, Nikon N-Gamut,
NTSC 1953, NTSC 1987 (SMPTE-C, ITU-R BT 470-7, ITU-R BO.786, MUSE, HI VISION), P3-D65, PAL (SECAM), ProPhoto (ROMM),
Protune Native, Rec. 601, Rec. 709 (ITU-R BT.709), Rec. 2020 (ITU-R BT.2020), Rec.2100 (in development),
REDCOLOR, REDCOLOR2, REDCOLOR3, REDCOLOR4, Red Wide Gamut RGB, RIMM, Russell RGB, Sony S-Gamut, Sony S-Gamut 3,
Sony S-Gamut 3 Cine, scRGB (in development), SHARP RGB, SMPTE 240M, sRGB, Panasonic V-Gamut, Venice S-Gamut 3,
Venice S-Gamut 3 Cine, XTREME RGB


### **transfer_functions**
Contains transfer functions methods for various color spaces. Encoding/Decoding, EOTF, OETF, CCTF. All functions
convert a color in both directions - to linear and to a given color space. It consists of the following functions:

srgb, rec601, rec2020, romm, eci, rimm, erimm, blackmagic, davinci, dcdm, slog, slog2, slog3, vlog, flog, nlog, djidlog,
filmlightlog, arri_log_c3, arri_log_c4, red_log, red_log_film, log3_g10, log3_g12, acescc, acescct, acesproxy, protune,
smpte240m, gamma_function.

Some of these are used for more than one color space since the calculations are the same. gamma_function is used for
typical camma encoding/decoding using the gamma of a given color space and is being used for multiple colro sapces.


### **converters**
This module consists of functions for converting a color from one form to another.
It consists of the following functions:


#### *rgb_to_web_safe*
Converts an 8-bit sRGB color to a web safe color.

#### *hex_to_rgb & rgb_to_hex*
Converts a hexadecimal color representation to RGB set of values and vice-versa.

#### *rgb_to_hsl & hls_to_rgb*
Converts an RGB color to its HSL (Hue, Saturation, Lightness) representation and vice-versa.

#### *rgb_to_hls*
Converts an RGB color to its HLS (Hue, Lightness, Saturation) representation.
It's practically the same as the above but in a different order and ~1.75 times faster due to
a different calculation method.

#### *rgb_to_hsv & hsv_to_rgb*
Converts an RGB color to its HSV (Hue, Saturation, Value) representation and vice-versa.

#### *hsv_to_hsl & hsl_to_hsv*
Converts HSV color to HSL and vice-versa.

#### *rgb_to_hsi & hsi_to_rgb*
Converts an RGB color to its HSI (Hue, Saturation, Intensity) representation and vice-versa.

#### *rgb_to_hsp & hsp_to_rgb*
Converts an RGB color to its HSP (Hue, Saturation, Perceived brightness) representation and vice-versa
Although HSP isn't an actual standard, one could find it useful. Here, the Hue and the Saturation are
calculated the same way as the ones in HSV (as opposed to the other actual standards where the Saturation is
different despite sharing the name)

#### *rgb_to_xyz, rgb_to_xyz_alt & xyz_to_rgb, xyz_to_rgb_alt*
Converts an RGB color to its XYZ representation and vice-versa.
The `alt` versions calculate the color in a different way and using slightly different inputs.
This one is the hardest one to implement. Many references contradict one-another and there's no really one
single official way to do it, which is why converting an RGB color to XYZ using different converters
gives various results (They mostly vary after the 3rd / 4th digit after the decimal point).
More info on that can be found in the `additionals` module

#### *xyz_to_lab & lab_to_xyz*
Converts an XYZ color to its CIE L*ab representation and vice-versa.

#### *xyz_to_yxy & yxy_to_xyz*
Converts between XYZ and Yxy colors.

#### *rgb_to_cmyk & cmyk_to_rgb*
Converts an RGB color to its CMYK (Cyan, Magenta, Yellow, Key) representation and vice-versa.
This one isn't finished yet. It only does the conversion from and to D65 illuminant which is why
the results are different thatn the ones in Adobe Photoshop which converts from D65 to D50.

#### *srgb_to_adobe_rgb & adobe_rgb_to_srgb*
Converts a color from sRGB to Adobe RGB color space.
These are still in test mode. They should be working but the documentation isn't finished and the
code isn't refined yet.

#### *adobe_rgb_to_xyz*
Converts an RGB color in Adobe RGB color space to its XYZ representation
This one might be deleted (or at least moved to the `additionals` module) since the `rgb_to_xyz_alt`
function allows input from any supported color space (which includes Adobe RGB)!


### **color_utils**
Contains numerous useful functions for working with colors.
It contains the following functions:


#### *get_color_brightness*
Takes an RGB color and returns its brightness based on the chosen calculation method. There are 11 methods.

#### *get_median_color*
Takes an unlimited number of colors and returns the average color of all.

#### *interpolate_color*
Takes two colors and returns a color between them based on a factor.

#### *get_gradient & get_gradient_alt*
Takes two colors and returns the desired amount of equaly spaced colors between them. The alt version does
the same, except that it uses the interpolate_color function to do so, which makes it ~2.25 times slower.

#### *half_color*
Takes an RGB color and returns twice as bright/dark color.
There are 2 alternative calculation methods commented inside. They may be included as a "method" parameter
in the future.

#### *get_hue*
Takes an RGB color and returns its Hue.
This function is used by most of the functions converting to/from representations that include Hue.
This makes the other functions a bit slower but the code a lot cleaner.

#### *color_change*
Takes an RGB color and brightens/darkens it based on a value and mode. 4 modes supported.

#### *saturate*
Takes an RGB color and saturates it based on a value and mode. 2 modes supported.

#### *desaturate*
Takes an RGB color and desaturates it based on a value and mode. 2 modes supported.

#### *complementary_color*
Takes an RGB color and returns its complementary color.

#### *monochrome_scheme*
Takes an RGB color and returns a desired amount of new colors with the same Hue but
varying Saturation and Brightness based on a seed and mode. 2 modes supported.

#### *monochrome_scheme_alt*
Takes an RGB color and returns 4 new colors with the same Hue and varying Saturation and Lightness.
It's very similar to the above one but outputs different results, based on a formula.

#### *triadic_scheme*
Takes an RGB color and returns two new colors forming a triad or a split complementary with the input color.

#### *tetradic_scheme*
Takes an RGB color and returns three new colors froming a tetrad with the input color.

#### *convert_bit_depth*
Takes an RGB color in given bit depth and returns it in the desired bit depth.

#### *blend & alpha_blend*
These two take 2 colors and blend them into a new one. They are still in test mode and don't have documentation.


### **internal_helpers**
A collection of internal function that help with values integrity checking, returning correct type of values.
It contains the following functions:


#### *check_color*
Takes an RGB color, checks if it's in valid range, checks its type and the type of its values and
returns the desired type of values.

#### *check_hsw*
Takes an HSW color, where W stands for Wildcard which could be anything in the range 0-100. Checks
the type of the input and all of the values and returns the desired type of values.

#### *integers_floats*
This internal function's sole purpose is to help `get_median_color()` from the `color_utils` module. All it does
is values distribution to make the code in `get_median_color()` cleaner.

#### *check_xyz*
Takes XYZ values and checks the type of the input and all of the values. Returns the desired type of values.

#### *return_rgb*
Takes an RGB color, checks it's bit depth and returns its values in the desired type.

#### *return_hsw*
Takes an HSW color, where W stands for Wildcard which could be anything in the range 0-100.
Returns its values in the desired type.

#### *return_scale*
Takes a set of 3 color values in a given range. Returns the values in the desired type.


###  **xyz**
Contains functions and constants for working with XYZ colors. It also contains a lot of
information in the form of comments.
It contains the following functions and constants:

#### *CIE_E, CIE_K, KODAK_E*
Various constants for calculating values for different color spaces.

#### *ILLUMINANTS*
A dictionary containing tristimulus values for various illuminants in both observer angles.

#### *ADAPTATION_MATRICES*
A dictionary with various CATs (Chromatic Adaptation Tables).

#### *get_adaptation_matrix*
Takes the tristimulus values of the source and target whitepoints and the desired adaptation method and
returns an adaptation matrix to be used with X, Y, Z values.

#### *apply_chromatic_adaptation*
Takes an X, Y, Z color and uses `get_adaptation_matrix()` to apply chromatic adaptation to it.

#### *refine_args*
Takes any of (illuminant, observer, color space, adaptation), checks and converts to correct type and form.
Also returns the illuminant of the input color space.

#### *working_space_matrix*
Creates a matrix for converting between R, G, B and X, Y, Z colors in various color spaces and illuminants.


### **additionals**
This module contains all kinds of alternatives to the values used throughout the package. Also contains
a lot of information that's not included in the other modules and a few alternative functions.
This module is more like an information table with lots of references.
It contains the following:


#### *General reading material and references for anything color-related.*

#### *Luma values for various color spaces*

#### *bit_values cheat sheet*

#### *ILLUMINANTS*
Two full sets of alternative values for the illuminants and ILLUMINANT_VARIANTS dictionary containing
5-6 different alternative sets of values for both D65 and D50 illuminants.

#### *ILLUMINANT_WHITEPOINTS*
Two full sets of different values for the various white point values in both observer angles. These values
are used to calculate the R, G, B primary colors of different color spaces.

#### *Tristimulus values and matrices for converting to/from non-illuminant 4200K and 6800K.*

#### *COLOR_SPACE_MATRICES*
A set of pre-caculated matrices for converting between various color spaces. It contains various
additional versions for some matrices in the EXTRA section.

#### *color_space_props*
This is an older version of the color_spaces module in the form of a dictionary that contains some extra color spaces
that couldn't be included in the production code due to missing information. It also contains some extra
properties that are missing from the color_spaces module because they can be calculated.

#### *get_hue*
Alternative calculation method for the `get_hue()` function in the `color_utils` module.

#### *color_change_old*
An old version of the `color_change()` function.

#### *darker_color & brighter_color*
Before `color_change` came to existance in the `color_utils` module, it was split into these two functions.

#### *interpolate_hsl*
An alternative color interpolation function to `interpolate_color` in `color_utils` that uses HSL and runs slower.

#### *hsl2rgb*
An alternative calculation method for converting H, S, L values to R, G, B. Needs speed testing.

#### *convert_to_linear & convert_linear_to*
These 2 functions were the ones used before the code was refactored to use the transfer_functions module


### **alexa_transfer_function_helpers**
This module contains data for Alexa Log C curve conversion


### ***Better comments extension settings***:
Paste these in VSCode's settings.json file andter installing the extension and restart so the changes can take effect.
