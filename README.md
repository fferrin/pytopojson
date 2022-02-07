# pyTopoJSON 
[![](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/download/releases/3.4.0/) 
[![Build Status](https://travis-ci.com/fferrin/pytopojson.svg?branch=master)](https://travis-ci.com/fferrin/pytopojson)
[![codecov](https://codecov.io/gh/fferrin/pytopojson/branch/master/graph/badge.svg)](https://codecov.io/gh/fferrin/pytopojson)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
[![Known Vulnerabilities](https://snyk.io/test/github/fferrin/pytopojson/badge.svg?targetFile=requirements.txt)](https://snyk.io/test/github/fferrin/pytopojson)

**pyTopoJSON** is based on the work of 
[Mike Bostock](https://github.com/topojson/topojson-server) and it provides 
tools for converting GeoJSON to [TopoJSON](https://github.com/topojson). 
See [How to Infer Topology](https://bost.ocks.org/mike/topology/) for details 
on how the topology is constructed. See also 
[us-atlas](https://github.com/topojson/us-atlas) and 
[world-atlas](https://github.com/topojson/world-atlas) for pre-built TopoJSON.


## Installation

#### Dependencies

**pytopojson** requires:

- NumPy (>= 1.15.0)

#### User installation

If you already have a working installation of NumPy,
the easiest way to install **pytopojson** is using ``pip``:

    pip install pytopojson

## API Reference

<a name="topology" href="#topology">#</a> pytopojson.topology.<b>Topology()</b>
[<>](https://github.com/fferrin/pytopojson/blob/master/pytopojson/topology.py "Source")

You must create a `Topology` object to compute the topology:

```python
# Import topology
from pytopojson import topology

# Create Topology object
topology_ = topology.Topology()

# Call it using a GeoJSON (dict) object, a name for the object and a quantization value (optional)
topojson = topology_({"object_name": geojson}, quantization=quantization)
```

This returns a TopoJSON topology for the specified 
[GeoJSON *objects*](http://geojson.org/geojson-spec.html#geojson-objects). 
The returned topology makes a shallow copy of the input `objects`: 
the identifier, bounding box, properties and coordinates of input objects may 
be shared with the output topology.

If a `quantization` parameter is specified, the input geometry is quantized 
prior to computing the topology, the returned topology is quantized, and its 
arcs are 
[delta-encoded](https://github.com/topojson/topojson-specification/blob/master/README.md#213-arcs). 
Quantization is recommended to improve the quality of the topology if the 
input geometry is messy (*i.e.*, small floating point error means that 
adjacent boundaries do not have identical values); typical values are powers 
of ten, such as 1e4, 1e5 or 1e6. 

<a name="feature" href="#feature">#</a> 
pytopojson.feature.<b>Feature</b>(<i>topology</i>, <i>object</i>) 
[<>](https://github.com/fferrin/pytopojson/blob/master/pytopojson/feature.py "Source")

Returns the GeoJSON Feature or FeatureCollection for the specified *object* in 
the given `topology`. If the specified object is a string, it is treated as 
`topology*['objects'][object]`. Then, if the object is a GeometryCollection, 
a FeatureCollection is returned, and each geometry in the collection is 
mapped to a Feature. Otherwise, a Feature is returned. The returned feature is 
a shallow copy of the source `object`: they may share identifiers, bounding 
boxes, properties and coordinates.

Some examples:

* A point is mapped to a feature with a geometry object of type "Point".
* Likewise for line strings, polygons, and other simple geometries.
* A null geometry object (of type null in TopoJSON) is mapped to a feature 
with a null geometry object.
* A geometry collection of points is mapped to a feature collection of 
features, each with a point geometry.
* A geometry collection of geometry collections is mapped to a feature 
collection of features, each with a geometry collection.

See [test_feature.py](https://github.com/fferrin/pytopojson/blob/master/tests/test_feature.py) 
for more examples.

<a name="merge" href="#merge">#</a> 
pytopojson.merge.<b>Merge</b>(<i>topology</i>, <i>objects</i>) 
[<>](https://github.com/fferrin/pytopojson/blob/master/pytopojson/merge.py "Source")

Returns the GeoJSON MultiPolygon geometry object representing the union for 
the specified array of Polygon and MultiPolygon `objects` in the given 
`topology`. Interior borders shared by adjacent polygons are removed. 
See [Merging States](https://bl.ocks.org/mbostock/5416405) for an example. 
The returned geometry is a shallow copy of the source `object`: they may share 
coordinates.

<a name="mergeArcs" href="#mergeArcs">#</a> 
pytopojson.merge.<b>MergeArcs</b>(<i>topology</i>, <i>objects</i>) 
[<>](https://github.com/fferrin/pytopojson/blob/master/pytopojson/merge.py "Source")

Equivalent to [topojson.merge.Merge()](#merge), but returns TopoJSON rather 
than GeoJSON. The returned geometry is a shallow copy of the source `object`: 
they may share coordinates.

<a name="mesh" href="#mesh">#</a> 
pytopojson.mesh.<b>Mesh</b>(<i>topology</i>[, <i>object</i>[, <i>filter</i>]])
[<>](https://github.com/fferrin/pytopojson/blob/master/pytopojson/mesh.py "Source")

Returns the GeoJSON MultiLineString geometry object representing the mesh for 
the specified `object` in the given `topology`. This is useful for rendering 
strokes in complicated objects efficiently, as edges that are shared by 
multiple features are only stroked once. If `object` is not specified, a mesh 
of the entire topology is returned. The returned geometry is a shallow copy of 
the source `object`: they may share coordinates.

An optional `filter` function may be specified to prune arcs from the returned 
mesh using the topology. The filter function is called once for each candidate 
arc and takes two arguments, `a` and `b`, two geometry objects that share that 
arc. Each arc is only included in the resulting mesh if the filter function 
returns `True`. For typical map topologies the geometries `a` and `b` are 
adjacent polygons and the candidate arc is their boundary. If an arc is only 
used by a single geometry then `a` and `b` are identical. This property is 
useful for separating interior and exterior boundaries; an easy way to produce 
a mesh of interior boundaries is:

```python
# Import topology
from pytopojson import mesh

# Create Mesh object and filter
mesh_ = mesh.Mesh()
custom_filter = lambda x, y: x != y

interiors = mesh_(topology, object_, custom_filter)
```

See this [county choropleth](https://bl.ocks.org/mbostock/4060606) for example. 
Note: the `a` and `b` objects are TopoJSON objects (pulled directly from the 
topology), and not automatically converted to GeoJSON features as by 
[topojson.feature.Feature()](#feature).

<a name="meshArcs" href="#meshArcs">#</a> 
pytopojson.mesh.<b>MeshArcs</b>(<i>topology</i>[, <i>object</i>[, <i>filter</i>]])
[<>](https://github.com/fferrin/pytopojson/blob/master/pytopojson/mesh.py "Source")

Equivalent to [topojson.mesh.Mesh()](#mesh), but returns TopoJSON rather than 
GeoJSON. The returned geometry is a shallow copy of the source `object`: they 
may share coordinates.

<a name="neighbors" href="#neighbors">#</a> 
pytopojson.neighbors.<b>Neighbors</b>(<i>objects</i>)
[<>](https://github.com/fferrin/pytopojson/blob/master/pytopojson/neighbors.py "Source")

Returns an array representing the set of neighboring objects for each object 
in the specified `objects` array. The returned array has the same number of 
elements as the input array; each element `i` in the returned array is the 
array of indexes for neighbors of object `i` in the input array. For example, 
if the specified objects array contains the features `foo` and `bar`, and 
these features are neighbors, the returned array will be `[[1], [0]]`, 
indicating that `foo` is a neighbor of `bar` and vice versa. Each array of 
neighbor indexes for each object is guaranteed to be sorted in ascending order.

For a practical example, see the 
[world map](https://bl.ocks.org/mbostock/4180634) with topological coloring.

### Transforms

<a name="bbox" href="#bbox">#</a> 
pytopojson.bbox.<b>BBox</b>(<i>topology</i>)
[<>](https://github.com/fferrin/pytopojson/blob/master/pytopojson/bbox.py "Source")

Returns the computed 
[bounding box](https://github.com/topojson/topojson-specification#3-bounding-boxes) 
of the specified `topology` [*x*₀, *y*₀, *x*₁, *y*₁] where *x*₀ is the minimum 
*x*-value, *y*₀ is the minimum *y*-value, *x*₁ is the maximum *x*-value, and 
*y*₁ is the maximum *y*-value. If the `topology` has no points and no arcs, 
the returned bounding box is [∞, ∞, -∞, -∞]. (This method ignores the existing
 `topology`.bbox, if any.)

<a name="quantize" href="#quantize">#</a> 
pytopojson.quantize.<b>Quantize</b>(<i>topology</i>, <i>transform</i>)
[<>](https://github.com/fferrin/pytopojson/blob/master/pytopojson/quantize.py "Source")

Returns a shallow copy of the specified `topology` with 
[quantized and delta-encoded](https://github.com/topojson/topojson-specification#213-arcs) 
arcs according to the specified 
[`transform` object](https://github.com/topojson/topojson-specification/blob/master/README.md#212-transforms). 
If the `topology` is already quantized, an error is thrown. See also 
[topoquantize](#topoquantize).

If a quantization number `n` is specified instead of a `transform` object, the 
corresponding transform object is first computed using the bounding box of the 
topology. In this case, the quantization number `n` must be a positive integer 
greater than one which determines the maximum number of expressible values per 
dimension in the resulting quantized coordinates; typically, a power of ten is 
chosen such as 1e4, 1e5 or 1e6. If the `topology` does not already have a 
`topology`.bbox, one is computed using [topojson.bbox.BBox](#bbox).

<a name="transform" href="#transform">#</a> 
pytopojson.transform.<b>Transform</b>(<i>transform</i>)
[<>](https://github.com/fferrin/pytopojson/blob/master/pytopojson/transform.py "Source")

If the specified 
[`transform` object](https://github.com/topojson/topojson-specification/blob/master/README.md#212-transforms) 
is non-null, returns a [point `transform` function](#_transform) to remove 
delta-encoding and apply the transform. If the `transform` is null, returns 
the identity function.

<a name="untransform" href="#untransform">#</a> 
pytopojson.untransform.<b>Untransform</b>(<i>transform</i>)
[<>](https://github.com/fferrin/pytopojson/blob/master/pytopojson/untransform.py "Source")

If the specified 
[`transform` object](https://github.com/topojson/topojson-specification/blob/master/README.md#212-transforms) 
is non-null, returns a [point `transform` function](#_transform) to apply 
quantized delta-encoding and remove the transform. If the `transform` is null, 
returns the identity function. See also [topojson.quantize.Quantize()](#quantize).

## Command-Line Reference

Some command-line tools are also provided:

### geo2topo

<a name="geo2topo" href="#geo2topo">#</a> <b>geo2topo</b> [<i>options…</i>] 
[<i>name</i>=]<i>file</i>… 
[<>](https://github.com/fferrin/pytopojson/blob/master/bin/geo2topo.py "Source")

Converts one or more GeoJSON objects to an output topology. For example, to 
convert a GeoJSON FeatureCollection in the input file us-states.json to a 
TopologyJSON topology in the output file us.json:

```bash
python geo2topo.py states=us-states.json > us.json
```

The resulting topology has a “states” object which corresponds to the input 
geometry. For convenience, you can omit the object name and specify only the 
output `file` name; the object name will then be the basename of the file, 
with the directory and extension removed. For example, to convert the 
states.json GeoJSON FeatureCollection to a TopologyJSON topology with the 
“states” object in us.json:

```bash
python geo2topo.py states.json > us.json
```

Any properties and identifiers of input 
[feature objects](https://tools.ietf.org/html/rfc7946#section-3.2) are 
propagated to the output. If you want to transform or filter properties, 
try [ndjson-cli](https://github.com/mbostock/ndjson-cli) as demonstrated in 
[Command-Line Cartography](https://medium.com/@mbostock/command-line-cartography-part-1-897aa8f8ca2c).

<a name="geo2topo_help" href="#geo2topo_help">#</a> geo2topo <b>-h</b>
<br><a href="#geo2topo_help">#</a> geo2topo <b>--help</b>

Output usage information.

<a name="geo2topo_version" href="#geo2topo_version">#</a> geo2topo <b>-V</b>
<br><a href="#geo2topo_version">#</a> geo2topo <b>--version</b>

Output the version number.

<a name="geo2topo_out" href="#geo2topo_out">#</a> geo2topo <b>-o</b> <i>file</i>
<br><a href="#geo2topo_out">#</a> geo2topo <b>--out</b> <i>file</i>

Specify the output TopoJSON file name. Defaults to “-” for stdout.

<a name="geo2topo_quantization" href="#geo2topo_quantization">#</a> geo2topo <b>-q</b> <i>count</i>
<br><a href="#geo2topo_quantization">#</a> geo2topo <b>--quantization</b> <i>count</i>

Specify a pre-quantization parameter. 0 disables quantization. See 
<a href="#topology">pytopojson.topology.Topology</a> for a description of 
quantization.


### topo2geo

<a name="topo2geo" href="#topo2geo">#</a> <b>topo2geo</b> [<i>options…</i>] 
[<i>name</i>=]<i>file</i>… 
[<>](https://github.com/fferrin/pytopojson/blob/master/bin/topo2geo.py "Source")

Converts one or more TopoJSON objects from an input topology to one or more 
GeoJSON features. For example, to convert the "states" TopoJSON 
`GeometryCollection` object in `us.json` to a GeoJSON feature collection in 
`us-states.json`:

```bash
python topo2geo.py states=us-states.json < us.json
```

For convenience, you can omit the object name and specify only the file *name*; 
the object name will be the basename of the file, with the directory and 
extension removed. For example, to convert the "states" TopoJSON 
`GeometryCollection` object in `us.json` to a GeoJSON feature collection in 
`states.json`:

```bash
python topo2geo.py states.json < us.json
```

See also [geo2topo](https://github.com/fferrin/pytopojson/blob/master/README.md#geo2topo).

To list the available object names, use [--list](#topo2geo_list).

<a name="topo2geo_help" href="#topo2geo_help">#</a> topo2geo <b>-h</b>
<br><a href="#topo2geo_help">#</a> topo2geo <b>--help</b>

Output usage information.

<a name="topo2geo_version" href="#topo2geo_version">#</a> topo2geo <b>-V</b>
<br><a href="#topo2geo_version">#</a> topo2geo <b>--version</b>

Output the version number.

<a name="topo2geo_in" href="#topo2geo_in">#</a> topo2geo <b>-i</b> <i>file</i>
<br><a href="#topo2geo_in">#</a> topo2geo <b>--in</b> <i>file</i>

Specify the input TopoJSON file name. Defaults to "-" for stdin.

<a name="topo2geo_list" href="#topo2geo_list">#</a> topo2geo <b>-l</b>
<br><a href="#topo2geo_list">#</a> topo2geo <b>--list</b>

List the names of the objects in the input topology, and then exit. For 
example, this:

```bash
python topo2geo.py -l < us.json
```

Will output this:

```
counties
states
nation
```

### topoquantize

<a name="topoquantize" href="#topoquantize">#</a> <b>topoquantize</b>
[<i>options…</i>] -q <q> [<i>input</i>] 
[<>](https://github.com/fferrin/pytopojson/blob/master/bin/topoquantize.py "Source")

Quantizes the coordinates of the input TopoJSON topology and 
[delta-encodes](https://github.com/topojson/topojson-specification#213-arcs) 
the topology’s arcs. The quantization parameter `q` must be a positive integer 
greater than one, and determines the maximum expressible number of unique 
values per dimension in the resulting quantized coordinates; typically, a power 
of ten is chosen such as 1e4, 1e5 or 1e6. If the `topology` does not already 
have a [bbox](#bbox), one is computed and assigned. If the `topology` is 
already quantized, an error is thrown. See also 
[pytopojson.quantize.Quantize](#quantize).

<a name="topoquantize_help" href="#topoquantize_help">#</a> topoquantize <b>-h</b>
<br><a href="#topoquantize_help">#</a> topoquantize <b>--help</b>

Output usage information.

<a name="topoquantize_version" href="#topoquantize_version">#</a> 
topoquantize <b>-V</b>
<br><a href="#topoquantize_version">#</a> topoquantize <b>--version</b>

Output the version number.

<a name="topoquantize_in" href="#topoquantize_in">#</a> 
topoquantize <b>-i</b> <i>input</i>
<br><a href="#topoquantize_in">#</a> topoquantize <b>--in</b> <i>input</i>

Specify the input TopoJSON. Defaults to "-" for stdin.

<a name="topoquantize_out" href="#topoquantize_out">#</a> 
topoquantize <b>-o</b> <i>output</i>
<br><a href="#topoquantize_out">#</a> topoquantize <b>--out</b> <i>output</i>

Specify the output TopoJSON file name. Defaults to "-" for stdout.