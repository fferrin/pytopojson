
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

        for i in range(len(self.lines)):
            line = self.lines[i]
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

            self.lines[i] = line

        for i in range(len(self.rings)):
            ring = self.rings[i]
            ring_start = ring[0]
            ring_mid = ring_start
            ring_end = ring[1]
            ring_fixed = self.junctions.has(self.coordinates[ring_mid])

            ring_mid += 1
            while ring_mid < ring_end:
                if self.junctions.has(self.coordinates[ring_mid]):
                    if ring_fixed:
                        next = {
                            0: ring_mid,
                            1: ring[1]
                        }

                        ring[1] = ring_mid
                        ring = next.copy()
                        ring['next'] = next
                    # For the first junction, we can rotate rather than cut.
                    else:
                        self.rotate_array(self.coordinates, ring_start, ring_end, ring_end - ring_mid)
                        self.coordinates[ring_end] = self.coordinates[ring_start]
                        ring_fixed = True
                        ring_mid = ring_start

                ring_mid += 1

            self.rings[i] = ring

        topology['lines'] = self.lines
        topology['rings'] = self.rings

        # Needed to convert rings in topology to dict
        rings_tmp = list()
        for coords in topology['rings']:
            rings_tmp.append(dict(list(zip([0, 1], coords))))
        topology['rings'] = rings_tmp

        # Needed to convert arcs in topology to dict
        for k, v in topology['objects'].items():
            arcs = v.get('arcs', None)
            if arcs is not None:
                if isinstance(arcs[0], list):
                    arcs = arcs if isinstance(arcs[0], list) else [arcs]
                    arcs_tmp = list()
                    for arc in arcs:
                        arcs_tmp.append(dict(list(zip([0, 1], arc))))
                    topology['objects'][k]['arcs'] = arcs_tmp
                else:
                    topology['objects'][k]['arcs'] = dict(list(zip([0, 1], arcs)))

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

