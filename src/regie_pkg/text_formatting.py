"""Module for formatting text output."""

def bold(str_val: str) -> str:
    """
    Return a string with bold formatting applied.

    Args:
    str_val (str): The string to apply bold formatting to.

    Returns:
    str: The input string with bold formatting applied.
    """
    return f"\033[1m{str_val}\033[0m"

def underline(str_val: str) -> str:
    """
    Return a string with underline formatting applied.

    Args:
    str_val (str): The string to apply underline formatting to.

    Returns:
    str: The input string with underline formatting applied.
    """
    return f"\033[4m{str_val}"

def insert_newline(num_of_lines: int=1) -> None:
    """
    Insert one or more newlines in the output.

    Args:
    num_of_lines (int, optional): The number of newlines to insert. Defaults to 1.

    Returns:
    None
    """
    for _ in range(num_of_lines):
        print()
    return