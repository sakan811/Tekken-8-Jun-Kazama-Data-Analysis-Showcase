import re

import pandas as pd
from loguru import logger


def clean_data(data: dict[str, list]) -> pd.DataFrame:
    """
    Clean the scraped data.
    :param data: Dictionary of scraped data.
    :return: Pandas dataframe with cleaned data.
    """
    logger.info('Cleaning data...')

    data = pd.DataFrame(data)

    data["Damage"] = data["Damage"].apply(clean_numbers)
    data["Start Up Frame"] = data["Start Up Frame"].apply(clean_numbers)
    data["Block Frame"] = data["Block Frame"].apply(clean_numbers)
    data["Hit Frame"] = data["Hit Frame"].apply(clean_numbers)
    data["Counter Hit Frame"] = data["Counter Hit Frame"].apply(clean_numbers)

    return data


def clean_numbers(input_str: str) -> float:
    """
    Clean number data.
    :param input_str: Input data as String.
    :return: Float
    """
    # Extract numbers using regular expressions
    numbers: list = re.findall(r'-?\d+', input_str)

    # Convert numbers to integers
    numbers = [int(num) for num in numbers]

    # Calculate average
    if len(numbers) > 0:
        return sum(numbers) / len(numbers)
    else:
        return 0


def clean_first_start_up_column(input_str: str) -> float:
    """
    Clean First Start Up Frame column.
    :param input_str: Input data as String.
    :return: Float
    """
    # Extract the first number using regular expressions
    match = re.search(r'-?\d+', input_str)

    if match:
        return int(match.group(0))
    else:
        return 0


if __name__ == '__main__':
    pass
