
from hash.hash import HashMap, HashSet
from hash.point import equal as equal_point
from hash.point import hash as hash_point


# Computes the bounding box of the specified hash of GeoJSON objects.
class Join(object):
    """
    Given an extracted (pre-)topology, identifies all of the junctions. These are
    the points at which arcs (lines or rings) will need to be cut so that each
    arc is represented uniquely.

    A junction is a point where at least one arc deviates from another arc going
    through the same point. For example, consider the point B. If there is a arc
    through ABC and another arc through CBA, then B is not a junction because in
    both cases the adjacent point pairs are {A,C}. However, if there is an
    additional arc ABD, then {A,D} != {A,C}, and thus B becomes a junction.

    For a closed ring ABCA, the first point A's adjacent points are the second
    and last point {B,C}. For a line, the first and last point are always
    considered junctions, even if the line is closed; this ensures that a closed
    line is never rotated.
    """

    def __init__(self):
        pass

    def __call__(self, topology, *args, **kwargs):
        self.coordinates = topology['coordinates']
        self.lines = topology['lines']
        self.rings = topology['rings']
        self.indexes = self.index()
        self.visited_by_index = [None] * len(self.coordinates)
        self.left_by_index = [None] * len(self.coordinates)
        self.right_by_index = [None] * len(self.coordinates)
        self.junction_by_index = [0] * len(self.coordinates)
        self.junction_count = 0

        for i in range(len(self.coordinates)):
            self.visited_by_index[i] = self.left_by_index[i] = self.right_by_index[i] = -1

        for i in range(len(self.lines)):
            line = self.lines[i]
            line_start = line[0]
            line_end = line[1]

            current_index = self.indexes[line_start]
            line_start += 1
            next_index = self.indexes[line_start]
            self.junction_count += 1
            self.junction_by_index[current_index] = 1
            line_start += 1

            while line_start <= line_end:
                previous_index = current_index
                current_index = next_index
                next_index = self.indexes[line_start]
                self.sequence(i, previous_index, current_index, next_index)
                line_start += 1

        self.visited_by_index = self.left_by_index = self.right_by_index = None, None, None
        self.junction_by_point = HashSet(self.junction_count * 1.4, hash_point, equal_point)

        len_junction_by_index = len(self.junction_by_index)
        for i in range(len(self.coordinates)):
            j = self.indexes[i]
            if j < len_junction_by_index and self.junction_by_index[j]:
                self.junction_by_point.add(self.coordinates[j])

        return self.junction_by_point

    def sequence(self, i, previous_index, current_index, next_index):
        # ignore self-intersection
        if self.visited_by_index[current_index] == i:
            return

        self.visited_by_index[current_index] = i
        left_index = self.left_by_index[current_index]

        if 0 <= left_index:
            right_index = self.right_by_index[current_index]
            if (left_index != previous_index or right_index != next_index) \
                    and (left_index != next_index or right_index != previous_index):
                self.junction_count += 1
                self.junction_by_index[current_index] = 1

        else:
            self.left_by_index[current_index] = previous_index
            self.right_by_index[current_index] = next_index

    def index(self):
        index_by_point = HashMap(len(self.coordinates) * 1.4, self.hash_index, self.equal_index, list, -1, list)
        indexes = [0] * len(self.coordinates)

        i = 0
        while i < len(self.coordinates):
            indexes[i] = index_by_point.maybe_set(i, i)
            i += 1

        # for i in range(len(self.coordinates)):
        #     indexes[i] = index_by_point.maybe_set(i, i)

        return indexes

    def hash_index(self, i):
        return hash_point(self.coordinates[i])

    def equal_index(self, i, j):
        return equal_point(self.coordinates[i], self.coordinates[j])

