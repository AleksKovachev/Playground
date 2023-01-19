## 0.Color Utilities

This is a package I put up for working with colors. It's sole purpose is to be as simple to use as possible which
is why I took the procedural approach with it. Everything inside is over-commented and every function has a detailed
docstring.

### The package is still in development! There are things that are not yet tested or documented.
If you spot any issues, please don't hesitate to contact me.

### Python version: 3.10 or above

##### I'm using VSCode for the development. Along with it, I'm using the extension `better comments` with ID aaron-bond.better-comments
Install it if you want to be able to view all comments color coded and use the settings at the bottom of this file.


## Contents


### main
The main file is underdeveloped. It's just a test file that I keep until I populate the __init__ file.

### tester
As the name suggests, this file has some preconditions for testing the functions. It's also underdeveloped since
it's not important for the final code.


### color_utilities folder


### __init__
The __init__ file is empy for the time being. In the future, it will provide a shortcut to every function in the
package, as well as some combo functions.


### converters
This module consists of functions for converting a color from one form to another.
It consists of the following functions:


#### rgb_to_web_safe
Converts an 8-bit sRGB color to a web safe color.

### convert_to_linear & convert_linear_to
Converts gamma corrected R, G, B values to linear and vice-versa

#### hex_to_rgb & rgb_to_hex
Converts a hexadecimal color representation to R, G, B set of values and vice-versa.

#### rgb_to_hsl & hls_to_rgb
Converts an R, G, B color to its HSL (Hue, Saturation, Lightness) representation and vice-versa.

#### rgb_to_hls
Converts an R, G, B color to its HLS (Hue, Lightness, Saturation) representation.
It's practically the same as the above but in a different order and ~1.75 times faster due to
a different calculation method.

#### rgb_to_hsv & hsv_to_rgb
Converts an R, G, B color to its HSV (Hue, Saturation, Value) representation and vice-versa.

#### hsv_to_hsl & hsl_to_hsv
Converts H, S, V color to H, S, L and vice-versa.

#### rgb_to_hsi & hsi_to_rgb
Converts an R, G, B color to its HSI (Hue, Saturation, Intensity) representation and vice-versa.

#### rgb_to_hsp & hsp_to_rgb
Converts an R, G, B color to its HSP (Hue, Saturation, Perceived brightness) representation and vice-versa
Although HSP isn't an actual standard, one could find it useful. Here, the Hue and the Saturation are
calculated the same way as the ones in HSV (as opposed to the other actual standards where the Saturation is
different despite sharing the name)

#### rgb_to_xyz, rgb_to_xyz_alt & xyz_to_rgb, xyz_to_rgb_alt
Converts an R, G, B color to its XYZ representation and vice-versa.
The `alt` versions calculate the color in a different way and using slightly different inputs.
This one is the hardest one to implement. Many references contradict one-another and there's no really one
single official way to do it, which is why converting an R, G, B color to X, Y, Z using different converters
gives various results (They mostly vary after the 3rd / 4th digit after the decimal point).
More info on that can be found in the `additionals` module

#### xyz_to_lab & lab_to_xyz
Converts an X, Y, Z color to its L*ab representation and vice-versa.

#### xyz_to_yxy & yxy_to_xyz
Converts between X, Y, Z and Y, x, y colors.

#### rgb_to_cmyk & cmyk_to_rgb
Converts an R, G, B color to its CMYK (Cyan, Magenta, Yellow, Key) representation and vice-versa.
This one isn't finished yet. It only does the conversion from and to D65 illuminant which is why
the results are different thatn the ones in Adobe Photoshop which converts from D65 to D50.

#### srgb_to_adobe_rgb & adobe_rgb_to_srgb
Converts a color from sRGB to Adobe RGB color space.
These are still in test mode. They should be working but the documentation isn't finished and the
code isn't refined yet.

#### adobe_rgb_to_xyz
Converts an R, G, B color in Adobe RGB color space to its XYZ representation
This one might be deleted (or at least moved to the `additionals` module) since the `rgb_to_xyz_alt`
function allows input from any supported color space (which includes Adobe RGB)!


###  color_utils
Contains numerous useful functions for working with colors.
It contains the following functions:


#### get_color_brightness
Takes an R, G, B color and returns its brightness based on the chosen calculation method. There are 11 methods.

#### get_median_color
Takes an unlimited number of colors and returns the average color of all.

#### interpolate_color
Takes two colors and returns a color between them based on a factor.

#### get_gradient & get_gradient_alt
Takes two colors and returns the desired amount of equaly spaced colors between them. The alt version does
the same, except that it uses the interpolate_color function to do so, which makes it ~2.25 times slower.

#### half_color
Takes an R, G, B color and returns twice as bright/dark color.
There are 2 alternative calculation methods commented inside. They may be included as a "method" parameter
in the future.

#### get_hue
Takes an R, G, B color and returns its Hue.
This function is used by most of the functions converting to/from representations that include Hue.
This makes the other functions a bit slower but the code a lot cleaner.

#### color_change
Takes an R, G, B color and brightens/darkens it based on a value and mode. 4 modes supported.

#### saturate
Takes an R, G, B color and saturates it based on a value and mode. 2 modes supported.

#### desaturate
Takes an R, G, B color and desaturates it based on a value and mode. 2 modes supported.

#### complementary_color
Takes an R, G, B color and returns its complementary color.

#### monochrome_scheme
Takes an R, G, B color and returns a desired amount of new colors with the same Hue but
varying Saturation and Brightness based on a seed and mode. 2 modes supported.

#### monochrome_scheme_alt
Takes an R, G, B color and returns 4 new colors with the same Hue and varying Saturation and Lightness.
It's very similar to the above one but outputs different results, based on a formula.

#### triadic_scheme
Takes an R, G, B color and returns two new colors forming a triad or a split complementary with the input color.

#### tetradic_scheme
Takes an R, G, B color and returns three new colors froming a tetrad with the input color.

#### convert_bit_depth
Takes an R, G, B color in given bit depth and returns it in the desired bit depth.

#### blend & alpha_blend
These two take 2 colors and blend them into a new one. They are still in test mode and don't have documentation.


### internal_helpers
A collection of internal function that help with values integrity checking, returning correct type of values.
It contains the following functions:


#### check_color
Takes an R, G, B color, checks if it's in valid range, checks its type and the type of its values and
returns the desired type of values.

#### check_hsw
Takes an H, S, W color, where W stands for Wildcard which could be anything in the range 0-100. Checks
the type of the input and all of the values and returns the desired type of values.

#### integers_floats
This internal function's sole purpose is to help `get_median_color()` from the `color_utils` module. All it does
is values distribution to make the code in `get_median_color()` cleaner.

#### check_xyz
Takes X, Y, Z values and checks the type of the input and all of the values. Returns the desired type of values.

#### return_rgb
Takes an R, G, B color, checks it's bit depth and returns its values in the desired type.

#### return_hsw
Takes an H, S, W color, where W stands for Wildcard which could be anything in the range 0-100.
Returns its values in the desired type.


###  xyz
Contains functions and constants for working with X, Y, Z colors. It also contains a lot of
information in the form of comments.
It contains the following functions and constants:

#### color_space_props
A dictionary that contains multiple color spaces and their properties.

#### CIE_E, CIE_K, KODAK_E, BETA, ALPHA
Various constants for calculating values for different color spaces.

#### ILLUMINANTS
A dictionary containing tristimulus values for various illuminants in both observer angles.

#### ADAPTATION_MATRICES
A dictionary with various CATs (Chromatic Adaptation Tables).

#### get_adaptation_matrix
Takes the tristimulus values of the source and target whitepoints and the desired adaptation method and
returns an adaptation matrix to be used with X, Y, Z values.

#### apply_chromatic_adaptation
Takes an X, Y, Z color and uses `get_adaptation_matrix()` to apply chromatic adaptation to it.

#### refine_args
Takes any of (illuminant, observer, color space, adaptation), checks and converts to correct type and form.
Also returns the illuminant of the input color space.

#### working_space_matrix
Creates a matrix for converting between R, G, B and X, Y, Z colors in various color spaces and illuminants.


### additionals
This module contains all kinds of alternatives to the values used throughout the package. Also contains
a lot of information that's not included in the other modules and a few alternative functions.
This module is more like an information table with lots of references.
It contains the following:


#### General reading material and references for anything color-related.

#### Luma values for various color spaces

#### bit_values cheat sheet

#### ILLUMINANTS
Two full sets of alternative values for the illuminants and ILLUMINANT_VARIANTS dictionary containing
5-6 different alternative sets of values for both D65 and D50 illuminants.

#### ILLUMINANT_WHITEPOINTS
Two full sets of different values for the various white point values in both observer angles. These values
are used to calculate the R, G, B primary colors of different color spaces.

#### Tristimulus values and matrices for converting to/from non-illuminant 4200K and 6800K.

#### COLOR_SPACE_MATRICES
A set of pre-caculated matrices for converting between various color spaces. It contains various
additional versions for some matrices in the EXTRA section.

#### color_space_props
This is the same color_space_props that's located in the `xyz` module but it contains some extra color spaces
that couldn't be included in the production code due to missing information. It also contains some extra
properties that are missing from the original because they can be calculated.

#### get_hue
Alternative calculation method for the `get_hue()` function in the `color_utils` module.

#### color_change_old
An old version of the `color_change()` function.

#### darker_color & brighter_color
Before `color_change` came to existance in the `color_utils` module, it was split into these two functions.

#### interpolate_hsl
An alternative color interpolation function to `interpolate_color` in `color_utils` that uses HSL and runs slower.

#### hsl2rgb
An alternative calculation method for converting H, S, L values to R, G, B. Needs speed testing.


### Better comments extension settings:
Paste these in VSCode's settings.json file andter installing the extension and restart so the changes can take effect.

```
"better-comments.tags": [
    {
    "tag": "!",
    "color": "#FF2D00",
    "strikethrough": false,
    "underline": false,
    "backgroundColor": "transparent",
    "bold": false,
    "italic": false
    },
    {
    "tag": "?",
    "color": "#3498DB",
    "strikethrough": false,
    "underline": false,
    "backgroundColor": "transparent",
    "bold": false,
    "italic": false
    },
    {
    "tag": "//",
    "color": "#474747",
    "strikethrough": true,
    "underline": false,
    "backgroundColor": "transparent",
    "bold": false,
    "italic": false
    },
    {
    "tag": "todo",
    "color": "#FF8C00",
    "strikethrough": false,
    "underline": false,
    "backgroundColor": "transparent",
    "bold": false,
    "italic": false
    },
    {
    "tag": "*",
    "color": "#98C379",
    "strikethrough": false,
    "underline": false,
    "backgroundColor": "transparent",
    "bold": false,
    "italic": false
    },
    {
    "tag": "=",
    "color": "#FF6624",
    "strikethrough": false,
    "underline": false,
    "backgroundColor": "transparent",
    "bold": false,
    "italic": false
    },
    {
    "tag": "+",
    "color": "#F8FF24",
    "strikethrough": false,
    "underline": false,
    "backgroundColor": "transparent",
    "bold": false,
    "italic": false
    },
    {
    "tag": "~",
    "color": "#cc39e5",
    "strikethrough": false,
    "underline": false,
    "backgroundColor": "transparent",
    "bold": true,
    "italic": false
    }
]
```
