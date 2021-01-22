import argparse
import json
import os
import sys

from pytopojson import feature


__version__ = "0.0.2"


def read(input_):
    if isinstance(input_, str):
        with open(input_, "r") as src:
            data = json.load(src)
    else:
        data = json.load(input_)

    return data


def write_list(topology_):
    for name in topology_["objects"]:
        print(name)


def read_newline_delimited_object():
    pass


def write(topology_, objects):
    feat = feature.Feature()
    for specifier in objects:
        i = specifier.find("=")
        if 0 <= i:
            name, file_ = specifier.split("=")
        else:
            file_ = specifier
            filename = os.path.basename(file_)
            name, _ = os.path.splitext(filename)

        if name not in topology_["objects"]:
            print(f"\n  error: object {name} not found\n")
            return

        write_feature(file_, feat(topology, name))


def write_feature(output, feat):
    if output == "-":
        json.dump(feat, sys.stdout, separators=(",", ":"))
        sys.stdout.write("\n")
    else:
        with open(output, "w") as dst:
            json.dump(feat, dst, separators=(",", ":"))
            dst.write("\n")


def main():
    # Create OptionParser object and set options
    parser = argparse.ArgumentParser(
        description="Converts TopoJSON objects to GeoJSON features."
    )

    parser.add_argument(
        "-i",
        "--in",
        dest="file",
        help='input topology file name; defaults to "-" for stdin',
        default="-",
    )
    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        default=False,
        help="list the object names on the input topology",
    )
    parser.add_argument(
        "objects",
        metavar="[geometry_type=]file",
        type=str,
        nargs="+",
        help="output with GeoJSON data for given geometry in input",
    )
    # parser.add_argument('-n', '--newline-delimited',
    #                     help='output newline-delimited JSON')
    parser.add_argument(
        "-V", "--version", action="version", version=f"%(prog)s v{__version__}"
    )

    # Parse and store the command-line arguments in dictionary
    opts = parser.parse_args()
    kwargs = vars(opts)

    # Read input file
    input_ = kwargs["file"] if kwargs["file"] != "-" else sys.stdin
    topology = read(input_)

    if kwargs["list"]:
        write_list(topology)
    else:
        write(topology, kwargs["objects"])


if __name__ == "__main__":
    main()
