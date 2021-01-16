import numbers


__all__ = "in_delta"


def in_delta_dict(actual, expected, delta):
    for e in expected:
        if e not in actual or not in_delta(actual[e], expected[e], delta):
            return False
    for a in actual:
        if a not in expected:
            return False

    return True


def in_delta_array(actual, expected, delta):
    if len(actual) != len(expected):
        return False

    return all(
        map(
            lambda actual_i, expected_i: in_delta(actual_i, expected_i, delta),
            actual,
            expected,
        )
    )


def in_delta_number(actual, expected, delta):
    return (actual >= expected - delta) and (actual <= expected + delta)


def in_delta(actual, expected, delta=1e-6):
    if isinstance(expected, list):
        return isinstance(actual, list) and in_delta_array(actual, expected, delta)
    elif isinstance(expected, numbers.Number):
        return isinstance(actual, numbers.Number) and in_delta_number(
            actual, expected, delta
        )
    elif isinstance(expected, dict):
        return isinstance(actual, dict) and in_delta_dict(actual, expected, delta)
    else:
        return actual == expected
