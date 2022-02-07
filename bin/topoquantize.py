import argparse
import json
import os
import sys

from pytopojson import quantize


__version__ = "0.0.2"


def read(input_):
    if isinstance(input_, str):
        with open(input_, "r") as src:
            return json.load(src)
    else:
        return json.load(sys.stdin)


def quantize_topology(topology, quantization):
    quantize_ = quantize.Quantize()
    return quantize_(topology, quantization)


def write(output, topology):
    if isinstance(output, str):
        with open(output, "w") as dst:
            json.dump(topology, dst, separators=(",", ":"))
            dst.write("\n")
    else:
        json.dump(topology, sys.stdout, separators=(",", ":"))
        sys.stdout.write("\n")


def _valid_quantization_parameter(arg):
    try:
        f = float(arg)
    except ValueError:
        raise argparse.ArgumentTypeError("Must be a floating point number")
    if f <= 2.0:
        raise argparse.ArgumentTypeError(f"Invalid quantization parameter {arg}")
    return f


def main():
    # Create OptionParser object and set options
    parser = argparse.ArgumentParser(description="Quantizes TopoJSON.")

    parser.add_argument(
        "-i",
        "--in",
        dest="input",
        default="-",
        help='input topology file name; defaults to "-" for stdin',
    )
    parser.add_argument(
        "-o",
        "--out",
        dest="output",
        default="-",
        help='output topology file name; defaults to "-" for stdout',
    )
    parser.add_argument(
        "-q",
        "--quantization",
        dest="quantization",
        type=_valid_quantization_parameter,
        required=True,
        help="quantization value",
    )
    parser.add_argument(
        "-V", "--version", action="version", version=f"%(prog)s v{__version__}"
    )

    # Parse and store the command-line arguments in dictionary
    opts = parser.parse_args()
    kwargs = vars(opts)

    # Read input file
    input_ = kwargs["input"] if kwargs["input"] != "-" else sys.stdin
    output = kwargs["output"] if kwargs["output"] != "-" else sys.stdout

    topology = read(input_)
    quantized = quantize_topology(topology, kwargs["quantization"])
    write(output, quantized)


if __name__ == "__main__":
    main()