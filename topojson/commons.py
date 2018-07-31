
def set_in_list(l, i, v):
    try:
        l[i] = v
    except IndexError:
        l.extend([None] * (i - (len(l) - 1)))
        l[i] = v
