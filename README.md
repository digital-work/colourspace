colour
======

colour is a Python package for colour metrics and colour space transforms. Many common colour spaces and colour metrics are available, and more are continuously added. The package consists of six modules:

* colour.data
* colour.space
* colour.metric
* colour.tensor
* colour.statistics
* colour.misc

All the modules are imported when importing the package.

The basic functionality of supposedly general interest is found in the three first modules. Only the really basic functionality is documented here. For more advanced features, please refer to the code, or contact the author.

Representing and Converting Colour Data
---------------------------------------

Basic numeric colour data are represented as numpy arrays of dimensions NxMx...Px3. In other words, colour data can be of any dimension, as long as the last dimension is the colour dimension. In particular, single points in the colour space will be ndarrays of shape (3,), lists of colour data will have dimension (N,3), and colour images will have dimension (M,N,3).

Colour data is scaled such that the natural maximum value is unity for most colour spaces, including XYZ having Y=1 for the whichever white point, and the RGB spaces having (1,1,1) as white points. For colour spaces with explicitly defined scaling like CIELAB and CIELAB (where the white point is defined as L*=100), the original scaling is used.

Colour data, i.e., colour points, lists of colours, colour images etc., are most conveniently represented by objects of the colour.data.Data class. In order to construct such an object, the colour data and the colour space has to be specified. Typically, if `col_xyz` is an ndarray with colour data in XYZ, a colour data object can be constructed as

```python
col_data = colour.data.Data(colour.space.xyz, col_xyz)
```

Then the corresponding ndarray data in other colour spaces can be acquired by the get method:

```python
col_srgb = col_data.get(colour.space.srgb)
col_lab  = col_data.get(colour.space.cielab)
col_xyY  = col_data.get(colour.space.xyY)
```

and so on. The colour conversions are computed only once and buffered within the Data object, so no extra overhead (besides the function call) is caused by sequential calls to the get method with the same colour space as the argument.

There are also built-in colour data sets available. They are all represented by Data objects that can be constructed upon need by functions in the colour.data module. These functions have names starting with `d_`. Most of these data sets are mainly of interest for colour metrics researcher, but some of them will have broader interest, such as the various CIE colour matching functions, and the data of the Munsell patches.

Constructing Colour Spaces
--------------------------

New colour space objects are constructed by starting with an exisiting base colour space, and applying colour space transformations. For example, the fictive colour space `my_rgb` can be defined by a linear transformation from XYZ using the matrix `my_M` followed by a gamma correction with `my_gamma` as follows

```python
my_rgb_linear = colour.space.TransformLinear(colour.space.xyz, my_M)
my_rgb = colour.space.TransformGamma(my_rgb_linear, my_gamma)
```

Any existing colour space can be used as the base for the transformation. Currently, the following common colour space transformations have been defined:

* TransformLinear: A linear transformation defined by a 3x3 matrix (represented as a ndarray of shape (3,3)).
* TransformGamma: A gamma correction applied individually to all channels. If the channel values are negative (should not be the case for RGB type spaces, but occurs, e.g., in IPT), the gamma transform is applied to the absolute value of the channel, and the sign is added in the end.
* TransformPolar: Transform the two last colour coordinates from cartesian to polar. This can be used, e.g., to transform from CIELAB to CIELCH. Keep in mind, though, that this transformation is singular at the origin of the chromatic plane, and that this can confuse some colour metrics. The angle is represented in radians.
* TransformCartesian: The oposite of the above.
* TransformxyY: The projective transform from, e.g., XYZ to xyY, with that order of the coordinates.
* TransformCIELAB: The non-linear transformation from XYZ to CIELAB, including the linear part for small XYZ values. The white point is a parameter, so this transformation can be used also to create CIELAB D50, etc. The base space does not have to be XYZ, so this transform can also be used to create, e.g., the DIN99 colour spaces.
* TransformCIELUV: The non-linear transformation from XYZ to CIELUV, including the linear part for small XYZ values.The white point is a parameter, so this transformation can be used also to create CIELUV D50, etc.
* TransformSRGB: The non-linear gamma-like correction from linear RGB with sRGB primaries to the non-linear sRGB colour space.

In addition, the following more special colour space transforms are available:

* TransformLogCompressL
* TransformLogCompressC
* TransformPoincareDisk
* TransformCIEDE00
* TransformLGJOSA
* TransformLGJE

Adding to this, new colour space transforms can be defined as classes inheriting from the colour.space.Transform base class.
