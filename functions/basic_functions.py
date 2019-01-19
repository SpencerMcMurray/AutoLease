def get_next_x_years(year, x):
    """(int, int) -> list of int
    Returns the next x years after and including year in a list
    """
    years = []
    for i in range(year, year + x):
        years.append(i)
    return years
