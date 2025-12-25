import pytest
from faker import Faker

fake = Faker()


@pytest.fixture
def random_text():
    def gen(maxc):
        return fake.pystr(min_chars=1, max_chars=maxc)

    return gen


@pytest.fixture
def random_int():
    def gen(maxi):
        return fake.pyint(min_value=1, max_value=maxi)

    return gen
