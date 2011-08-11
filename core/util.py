from math import floor
from fractions import Fraction


def prettyprint(unit):
    """
    Convert from decimal to a more friendly recipe-ish way

    like instead of 2.2 cups to 2 + 1/5 cups
    """
    int_part = int(floor(unit))
    if float(unit - int_part) <= 0.1:
        return str(int_part)
    r_part = str(Fraction.from_decimal(unit - int_part).limit_denominator(5))
    if r_part == '1':
        return str(int_part+1)

    if int_part == 0:
        return "%s"% ( r_part)

    return "%s + %s"% (int_part, r_part)


