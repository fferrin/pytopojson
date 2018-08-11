
import struct


def to_bin(value):
    if type(value) == str:
        b = ''.join(map(bin, bytearray(value))).replace('0b', '')[:64]
        return b if len(b) == 64 else b.zfill(64)
    else:
        return float_to_bin(value)


def float_to_bin(value):
    """ Convert float to 64-bit binary string. """
    [d] = struct.unpack(">Q", struct.pack(">d", value))
    return '{:064b}'.format(d)


def int_to_bin(value):
    return '{:064b}'.format(value)
    # """ Convert float to 64-bit binary string. """
    # [d] = struct.unpack(">Q", struct.pack(">d", value))
    # return '{:064b}'.format(d)


def string_to_bin(value):
    return '{:064b}'.format(value)
    # """ Convert float to 64-bit binary string. """
    # [d] = struct.unpack(">Q", struct.pack(">d", value))
    # return '{:064b}'.format(d)


def to_bin(value):
    if type(value) == str:
        return string_to_bin(value)
    elif type(value) == float:
        return float_to_bin(value)
    elif type(value) == int:
        return int_to_bin(value)


def bin_to_uint(value):
    return int(value, 2)


def hash(point):
    point = list(point.items()[0]) if type(point) == dict else point
    bins = [to_bin(point[0]), to_bin(point[1])]
    uints = [bin_to_uint(bins[0][:32]), bin_to_uint(bins[0][32:]),
             bin_to_uint(bins[1][:32]), bin_to_uint(bins[1][32:])]
    h = uints[0] ^ uints[1]
    h = h << 5 ^ h >> 7 ^ uints[2] ^ uints[3]
    return h & 0x7fffffff


def equal(p_1, p_2):
    return p_1[0] == p_2[0] and p_1[0] == p_2[0]
