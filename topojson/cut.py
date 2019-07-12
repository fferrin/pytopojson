
from topojson.join import Join


class Cut(object):
    """
    Given an extracted (pre-)topology, cuts (or rotates) arcs so that all shared
    point sequences are identified. The topology can then be subsequently deduped
    to remove exact duplicate arcs.
    """

    def __init__(self):
        self.join = Join()

    def __call__(self, topology, *args, **kwargs):
        self.junctions = self.join(topology)
        self.coordinates = topology['coordinates']
        self.lines = topology['lines']
        self.rings = topology['rings']

        for l in self.lines:
            line = l
            line_mid = line[0] + 1
            line_end = line[1]

            while line_mid < line_end:
                if self.junctions.has(self.coordinates[line_mid]):
                    next = {
                        0: line_mid,
                        1: line[1]
                    }

                    line[1] = line_mid
                    line = line['next'] = next

                line_mid += 1

        for r in self.rings:
            ring = r
            ring_start = ring[0]
            ring_mid = ring_start + 1
            ring_end = ring[1]
            ring_fixed = self.junctions.has(self.coordinates[ring_mid])

            while ring_mid < ring_end:
                if self.junctions.has(self.coordinates[ring_mid]):
                    if ring_fixed:
                        next = {
                            0: ring_mid,
                            1: ring[1]
                        }

                        ring[1] = ring_mid
                        ring = ring['next'] = next
                    # For the first junction, we can rotate rather than cut.
                    else:
                        self.rotate_array(self.coordinates, ring_start, ring_end, ring_end - ring_mid)
                        self.coordinates[ring_end] = self.coordinates[ring_start]
                        ring_fixed = True
                        ring_mid = ring_start

                ring_mid += 1

        return topology

    def rotate_array(self, array, start, end, offset):
        self.reverse(array, start, end)
        self.reverse(array, start, start + offset)
        self.reverse(array, start + offset, end)

    def reverse(self, array, start, end):
        mid = start + ((end - start) >> 1)
        end -= 1

        while start < mid:
            t = array[start]
            array[start] = array[end]
            array[end] = t

            start += 1
            end -= 1

