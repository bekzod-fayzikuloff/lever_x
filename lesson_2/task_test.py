import pytest

from lesson_2.task_2 import Version


versions_eq = [("1.0", "1.0"), ("1.42.1", "1.42.1"), ("0.1", "0.1")]
versions_ne = [("1.0.1", "1.1.1"), ("10", "0.1"), ("6.7", "9.2")]

versions_gt = [("1.1.12", "1.0.1"), ("10.11", "10.1"), ("16.7b", "9.2")]

versions_lt = [("1.0.1", "1.1.1"), ("0.1", "1.1"), ("5.7", "9.2")]


@pytest.mark.parametrize(["first_version", "second_version"], versions_eq)
def test_version_eq(first_version, second_version):
    assert Version(first_version) == Version(second_version)


@pytest.mark.parametrize(["first_version", "second_version"], versions_ne)
def test_version_ne(first_version, second_version):
    assert Version(first_version) != Version(second_version)


@pytest.mark.parametrize(["first_version", "second_version"], versions_gt)
def test_version_gt(first_version, second_version):
    assert Version(first_version) > Version(second_version)


@pytest.mark.parametrize(["first_version", "second_version"], versions_lt)
def test_version_lt(first_version, second_version):
    assert Version(first_version) < Version(second_version)
