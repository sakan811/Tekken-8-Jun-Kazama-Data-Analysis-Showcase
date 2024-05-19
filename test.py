import re

import pytest


def test_clean_numbers():
    input_str = '+14g~+15g'
    # Extract numbers using regular expressions
    numbers = re.findall(r'-?\d+', input_str)
    # Convert numbers to integers
    numbers = [int(num) for num in numbers]
    assert numbers[0] == 14
    assert numbers[1] == 15
    assert sum(numbers) == 29
    assert sum(numbers) / len(numbers) == 14.5

    input_str = '-6 (high blocked)'
    # Extract numeric values using regular expressions
    numbers = re.findall(r'-?\d+', input_str)
    # Convert numbers to integers
    numbers = [int(num) for num in numbers]
    assert numbers[0] == -6

    input_str = "+21a~+64a (-5~+38)"
    # Extract numeric values using regular expressions
    numbers = re.findall(r'-?\d+', input_str)
    # Convert numbers to integers
    numbers = [int(num) for num in numbers]
    assert numbers[0] == 21
    assert numbers[1] == 64
    assert numbers[2] == -5
    assert numbers[3] == 38
    assert sum(numbers) == 118
    assert sum(numbers) / len(numbers) == 29.5

    input_str = ",i27~28"
    # Extract numeric values using regular expressions
    numbers = re.findall(r'-?\d+', input_str)
    # Convert numbers to integers
    numbers = [int(num) for num in numbers]
    assert sum(numbers) == 55
    assert sum(numbers) / len(numbers) == 27.5

    input_str = "7,9,12,21"
    # Extract numbers using regular expressions
    numbers = re.findall(r'-?\d+', input_str)
    # Convert numbers to integers
    numbers = [int(num) for num in numbers]
    assert sum(numbers) == 49
    assert sum(numbers) / len(numbers) == 12.25

    input_str = "-6~+37g"
    # Extract numbers using regular expressions
    numbers = re.findall(r'-?\d+', input_str)
    # Convert numbers to integers
    numbers = [int(num) for num in numbers]
    assert numbers[0] == -6
    assert numbers[1] == 37
    assert sum(numbers) == 31


if __name__ == '__main__':
    pytest.main([__file__])
