import logging
import random
import subprocess
from pathlib import Path

import pytest
from faker import Faker

fake = Faker()

temp_root = Path("/tmp/nnlogging")
assert str(temp_root).startswith("/tmp/")
temp_root.mkdir(parents=True, exist_ok=True)
success = subprocess.run(["aim", "init", "--repo", str(temp_root), "--skip-if-exists"])
assert success


@pytest.fixture
def root_path():
    return temp_root


@pytest.fixture
def folder_path_gen():
    def gen():
        d = temp_root / fake.file_name(extension="")
        d.mkdir(parents=True, exist_ok=True)
        return d

    return gen


@pytest.fixture
def file_path_gen():
    def gen():
        f = temp_root / fake.file_name()
        f.touch(exist_ok=True)
        return f

    return gen


@pytest.fixture
def dataclass_name_gen():
    def gen():
        return fake.language_name()

    return gen


@pytest.fixture
def dataclass_key_gen():
    def gen():
        return fake.state_abbr()

    return gen


@pytest.fixture
def dataclass_value_gen():
    def gen():
        return fake.text(max_nb_chars=10)

    return gen


@pytest.fixture
def shell_name_gen():
    def gen():
        return fake.user_name()

    return gen


@pytest.fixture
def logger_name_gen():
    def gen():
        return fake.company()

    return gen


@pytest.fixture
def run_metadata_label_gen():
    def gen():
        return fake.company()

    return gen


@pytest.fixture
def run_metadata_float_gen():
    def gen():
        return fake.pyfloat(min_value=0, max_value=100)

    return gen


@pytest.fixture
def run_metadata_str_gen():
    def gen():
        return fake.text(max_nb_chars=40)

    return gen


@pytest.fixture
def experiment_name_gen():
    def gen():
        return fake.bs()

    return gen


@pytest.fixture
def branch_name_gen():
    def gen():
        return fake.city()

    return gen


@pytest.fixture
def task_name_gen():
    def gen():
        return fake.domain_word()

    return gen


@pytest.fixture
def task_desc_gen():
    def gen():
        return fake.hostname()

    return gen


@pytest.fixture
def message_gen():
    def gen():
        return fake.text(max_nb_chars=40)

    return gen


@pytest.fixture
def log_level_int_gen():
    levels = tuple(i for i in range(logging.DEBUG, logging.CRITICAL + 1) if i % 10 != 0)

    def gen():
        return random.choice(levels)

    return gen


@pytest.fixture
def log_level_str_gen():
    levels = (
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    )

    def gen():
        return random.choice(levels)

    return gen


@pytest.fixture
def task_total_int_gen():
    def gen():
        return fake.pyfloat(min_value=10, max_value=20)

    return gen


@pytest.fixture
def task_done_gen():
    def gen():
        return fake.pyfloat(min_value=0, max_value=10)

    return gen


@pytest.fixture
def task_advance_gen():
    def gen():
        return fake.pyfloat(min_value=1, max_value=2)

    return gen
