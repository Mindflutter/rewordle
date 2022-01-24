import pytest

from rewordle.utils import generate_response

test_data = [
    ("автор", "авось", ["green", "green", "gray", "yellow", "gray"]),
    ("гжель", "авось", ["gray", "gray", "gray", "gray", "green"]),
    ("залив", "авось", ["gray", "yellow", "gray", "gray", "yellow"]),
    ("линия", "авось", ["gray", "gray", "gray", "gray", "gray"]),
    ("авось", "авось", ["green", "green", "green", "green", "green"]),
]


@pytest.mark.parametrize("guess_word, secret_word, expected", test_data)
def test_generate_response(guess_word, secret_word, expected):
    result = generate_response(guess_word, secret_word)
    assert result == expected
