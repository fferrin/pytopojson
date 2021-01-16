import math
from collections.abc import Iterable

from pytopojson import (
    bbox,
    commons,
    untransform,
)


class Quantize(object):
    def __init__(self):
        self.bbox = bbox.BBox()
        self.untransform = untransform.Untransform()
        self.t = None

    def __call__(self, topology, transform=None, *args, **kwargs):
        if topology.get("transform", None) is not None:
            raise ValueError("Already quantized.")

        no_transform = transform is None
        no_scale = "scale" not in transform if isinstance(transform, Iterable) else True
        if no_transform or no_scale:
            if transform is None or math.floor(transform) < 2:
                raise ValueError("n must be ≥2.")
            n = math.floor(transform)

            if "bbox" in topology and topology["bbox"] is not None:
                box = topology["bbox"]
            else:
                box = self.bbox(topology)

            x_0, y_0, x_1, y_1 = box
            transform = {
                "scale": [
                    (x_1 - x_0) / (n - 1) if x_0 < x_1 else 1,
                    (y_1 - y_0) / (n - 1) if y_0 < y_1 else 1,
                ],
                "translate": [x_0, y_0],
            }
        else:
            box = topology["bbox"]

        self.t = self.untransform(transform)
        inputs = topology["objects"]
        outputs = dict()

        for k in inputs:
            outputs[k] = self.quantize_geometry(inputs[k])

        return {
            "type": "Topology",
            "bbox": box,
            "transform": transform,
            "objects": outputs,
            "arcs": list(map(lambda x: self.quantize_arc(x), topology["arcs"])),
        }

    def quantize_point(self, point):
        return self.t(point)

    def quantize_geometry(self, input):
        if input["type"] == "GeometryCollection":
            output = {
                "type": "GeometryCollection",
                "geometries": list(
                    map(lambda x: self.quantize_geometry(x), input["geometries"])
                ),
            }
        elif input["type"] == "Point":
            output = {
                "type": "Point",
                "coordinates": self.quantize_point(input["coordinates"]),
            }
        elif input["type"] == "MultiPoint":
            output = {
                "type": "MultiPoint",
                "coordinates": list(
                    map(lambda x: self.quantize_point(x), input["coordinates"])
                ),
            }
        else:
            return input

        if "id" in input:
            output["id"] = input["id"]
        if "bbox" in input:
            output["bbox"] = input["bbox"]
        if "properties" in input:
            output["properties"] = input["properties"]

        return output

    def quantize_arc(self, input):
        i = 1
        j = 1
        n = len(input)
        output = commons.Array(n)  # Pessimistic
        output[0] = self.t(input[0], 0)

        while i < n:
            p = self.t(input[i], i)
            if p[0] or p[1]:
                output[j] = p  # Non-coincident points
                j += 1
            i += 1

        if j == 1:
            output[j] = [0, 0]  # An arc must have at least two points
            j += 1

        output = output[:j]
        return output
