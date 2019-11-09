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

<a name="topology" href="#topology">#</a> pytopojson.<b>topology.Topology()</b>
[<>](https://github.com/fferrin/pytopojson/blob/master/pytopojson/topology.py "Source")

You must create a `Topology` object to compute the topology:

```python
# Import topology
from pytopojson import topology as topo

# Create Topology object
topology = topo.Topology()

# Call it using a GeoJSON (dict) object and a quantization value (optional)
topology = topology(geojson, quantization=quantization)
```

This returns a TopoJSON topology for the specified 
[GeoJSON *objects*](http://geojson.org/geojson-spec.html#geojson-objects). 
The returned topology makes a shallow copy of the input *objects*: 
the identifier, bounding box, properties and coordinates of input objects may 
be shared with the output topology.

If a *quantization* parameter is specified, the input geometry is quantized 
prior to computing the topology, the returned topology is quantized, and its 
arcs are 
[delta-encoded](https://github.com/topojson/topojson-specification/blob/master/README.md#213-arcs). 
Quantization is recommended to improve the quality of the topology if the 
input geometry is messy (*i.e.*, small floating point error means that 
adjacent boundaries do not have identical values); typical values are powers 
of ten, such as 1e4, 1e5 or 1e6. 

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
geo2topo states=us-states.json > us.json
```

The resulting topology has a “states” object which corresponds to the input 
geometry. For convenience, you can omit the object name and specify only the 
output *file* name; the object name will then be the basename of the file, 
with the directory and extension removed. For example, to convert the 
states.json GeoJSON FeatureCollection to a TopologyJSON topology with the 
“states” object in us.json:

```bash
geo2topo states.json > us.json
```

Any properties and identifiers of input 
[feature objects](https://tools.ietf.org/html/rfc7946#section-3.2) are 
propagated to the output. If you want to transform or filter properties, 
try [ndjson-cli](https://github.com/mbostock/ndjson-cli) as demonstrated in 
[Command-Line Cartography](https://medium.com/@mbostock/command-line-cartography-part-1-897aa8f8ca2c).

<a name="geo2topo_help" href="#geo2topo_help">#</a> geo2topo <b>-h</b>
<br><a href="#geo2topo_help">#</a> geo2topo <b>--help</b>

Output usage information.

<a name="geo2topo_version" href="#geo2topo_version">#</a> geo2topo <b>-v</b>
<br><a href="#geo2topo_version">#</a> geo2topo <b>--version</b>

Output the version number.

<a name="geo2topo_out" href="#geo2topo_out">#</a> geo2topo <b>-o</b> <i>file</i>
<br><a href="#geo2topo_out">#</a> geo2topo <b>--out</b> <i>file</i>

Specify the output TopoJSON file name. Defaults to “-” for stdout.

<a name="geo2topo_quantization" href="#geo2topo_quantization">#</a> geo2topo <b>-q</b> <i>count</i>
<br><a href="#geo2topo_quantization">#</a> geo2topo <b>--quantization</b> <i>count</i>

Specify a pre-quantization paramter. 0 disables quantization. See 
<a href="#topology">pytopojson.topology.Topology</a> for a description of 
quantization.