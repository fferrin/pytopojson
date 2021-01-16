class Stitch(object):
    def __init__(self):
        pass

    def __call__(self, topology, arcs, *args, **kwargs):
        self.stitched_arcs = dict()
        self.fragment_by_start = dict()
        self.fragment_by_end = dict()
        self.fragments = list()
        self.empty_index = -1
        self.topology = topology

        # Stitch empty arcs first, since they may be subsumed by other arcs.
        for i, j in zip(arcs[0::2], arcs[1::2]):
            idx = self._get_idx(i)
            arc = self.topology["arcs"][idx]
            if len(arc) < 3 and not arc[1][0] and not arc[1][1]:
                self.empty_index += 1
                arcs[self.empty_index], arcs[j] = i, arcs[self.empty_index]

        for i in arcs:
            e = self.ends(i)
            start, end = tuple(e[0]), tuple(e[1])

            if start in self.fragment_by_end:
                f = self.fragment_by_end[start]
                self.fragment_by_end.pop(f["end"], None)
                idx = (
                    sorted(list(filter(lambda x: isinstance(x, int), f.keys())))[-1] + 1
                )
                f[idx] = i
                f["end"] = end

                # g = self.fragment_by_start.get(end, None)
                # if g is not None:
                if end in self.fragment_by_start:
                    g = self.fragment_by_start[end]
                    self.fragment_by_start.pop(g["start"], None)
                    fg = f if g == f else f + g
                    fg["start"] = f["start"]
                    fg["end"] = g["end"]
                    self.fragment_by_start[fg["start"]] = fg
                    self.fragment_by_end[fg["end"]] = fg
                else:
                    self.fragment_by_start[f["start"]] = f
                    self.fragment_by_end[f["end"]] = f
            else:
                if end in self.fragment_by_start:
                    f = self.fragment_by_start[end]
                    self.fragment_by_start.pop(f["start"], None)
                    self.unshift(f, i)
                    f["start"] = start
                    g = self.fragment_by_end.get(start, None)
                    if g is not None:
                        self.fragment_by_end.pop(g["end"], None)
                        gf = f if g == f else g + f
                        gf["start"] = g["start"]
                        gf["end"] = f["end"]
                        self.fragment_by_start[gf["start"]] = gf
                        self.fragment_by_end[gf["end"]] = gf
                    else:
                        self.fragment_by_start[f["start"]] = f
                        self.fragment_by_end[f["end"]] = f
                else:
                    f = {0: i, "start": tuple(start), "end": tuple(end)}
                    self.fragment_by_start[f["start"]] = f
                    self.fragment_by_end[f["end"]] = f

        self.flush(self.fragment_by_end, self.fragment_by_start)
        self.flush(self.fragment_by_start, self.fragment_by_end)

        for i in arcs:
            idx = self._get_idx(i)
            if idx not in self.stitched_arcs:
                self.fragments.append([i])

        # Convert dict to list
        fragments = list()
        for f in self.fragments:
            if 1 in f:
                fragments.append([f[0], f[1]])
            else:
                fragments.append([f[0]])

        return fragments

    @staticmethod
    def _get_idx(i):
        return ~i if i < 0 else i

    @staticmethod
    def unshift(d, value):
        sorted_keys = sorted(
            list(filter(lambda x: isinstance(x, int), d.keys())), reverse=True
        )
        for k in sorted_keys:
            d[k + 1] = d[k]
        d[0] = value

    def ends(self, i):
        idx = self._get_idx(i)
        arc = self.topology["arcs"][idx]
        p_0 = arc[0]

        if "transform" in self.topology:
            p_1 = [0, 0]
            for dp in arc:
                p_1[0] += dp[0]
                p_1[1] += dp[1]
        else:
            p_1 = arc[-1]

        return [p_1, p_0] if i < 0 else [p_0, p_1]

    def flush(self, fragment_by_end, fragment_by_start):
        for _, f in fragment_by_end.items():
            fragment_by_start.pop(f["start"], None)
            f.pop("start", None)
            f.pop("end", None)
            for _, i in f.items():
                self.stitched_arcs[self._get_idx(i)] = 1
            self.fragments.append(f)
