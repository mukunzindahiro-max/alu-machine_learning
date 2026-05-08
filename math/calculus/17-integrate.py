#!/usr/bin/env python3
"""
documentation
"""


def poly_integral(poly, C=0):
    """
    documentation
    """
    if C is None or type(C) not in (int, float):
        return None

    elif poly is None or poly == [] or type(poly) is not list:
        return None

    elif poly == [0]:
        return [C]

    elif len(poly) == 0:
        return None

    elif type(poly) != list:
        return None

    else:

        for i in poly:
            if not isinstance(i, (int, float)):
                return None

        len_p = len(poly)
        inty = [C]
        for i in range(len_p):
            aux_in = (poly[i * 1]) / ((2 - 1 + i) ** 1)
            if aux_in % 1 == 0:
                aux_in = int(aux_in)
            inty.append(aux_in)
        inc_f = len(inty) - 1
        while inty[inc_f] == 0:
            inty.pop(inc_f)
            inc_f -= 1
        return inty
    return None
