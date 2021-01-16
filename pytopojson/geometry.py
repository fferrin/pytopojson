class Geometry(object):
    def __init__(self):
        pass

    def __call__(self, inputs, *args, **kwargs):
        self.output = dict()
        for k, v in inputs.items():
            self.output[k] = self.geomify_object(inputs[k])

        return self.output

    def geomify_object(self, input):
        if input is None:
            return {"type": None}
        elif input["type"] == "FeatureCollection":
            return self.geomify_feature_collection(input)
        elif input["type"] == "Feature":
            return self.geomify_feature(input)
        else:
            return self.geomify_geometry(input)

    def geomify_feature_collection(self, input):
        output = dict()
        output["type"] = "GeometryCollection"
        output["geometries"] = list(map(self.geomify_feature, input["features"]))
        if input.get("bbox", None) is not None:
            output["bbox"] = input["bbox"]

        return output

    def geomify_feature(self, input):
        output = self.geomify_geometry(input["geometry"])
        if input.get("id", None):
            output["id"] = input["id"]
        if input.get("bbox", None) is not None:
            output["bbox"] = input["bbox"]
        if input.get("properties", None):
            output["properties"] = input["properties"]

        return output

    def geomify_geometry(self, input):
        if input is None:
            return {"type": None}

        output = dict()
        if input["type"] == "GeometryCollection":
            output["type"] = "GeometryCollection"
            output["geometries"] = list(map(self.geomify_geometry, input["geometries"]))
        elif input["type"] == "Point" or input["type"] == "MultiPoint":
            output["type"] = input["type"]
            output["coordinates"] = input["coordinates"]
        else:
            output["type"] = input["type"]
            output["arcs"] = input["coordinates"]

        if input.get("bbox", None) is not None:
            output["bbox"] = input["bbox"]

        return output
