import sys
import os
sys.path.insert(0, os.path.abspath('..'))


def get_next_x_years(year, x):
    """(int, int) -> list of int
    Returns the next x years after and including year in a list
    """
    years = []
    for i in range(year, year + x):
        years.append(i)
    return years


def pass_match(pass1, pass2):
    """(str, str) -> bool
    Returns True iff pass1 == pass2
    """
    return pass1 == pass2
