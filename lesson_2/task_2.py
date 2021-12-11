"""
Расширить реализацию класса Version, чтобы позволять использовать его для
семантического сравнения.


Doctest example:

>>> Version('1.1.3') < Version('2.2.3')
True

>>> Version('1.3.0') > Version('0.3.0')
True

>>> Version('0.3.0b') < Version('1.2.42')
True

>>> Version('1.3.42') == Version('42.3.1')
False

>>> Version('1.3.42') <= Version('42.3.1')
True

>>> Version('1.3.42') >= Version('42.3.1')
False

>>> Version("1.1.1b") >= Version("1.0.10-alpha.beta")
True
"""


class Version:
    def __init__(self, version: str):
        self.version = version

    @staticmethod
    def version_(version: str) -> tuple:
        return tuple([point.zfill(8) for point in version.split(".")])

    def __eq__(self, other) -> bool:
        return self.version_(self.version) == self.version_(other.version)

    def __ne__(self, other) -> bool:
        return self.version_(self.version) != self.version_(other.version)

    def __gt__(self, other) -> bool:
        return self.version_(self.version) > self.version_(other.version)

    def __ge__(self, other) -> bool:
        return self.version >= other.version

    def __lt__(self, other) -> bool:
        return self.version_(self.version) < self.version_(other.version)

    def __le__(self, other) -> bool:
        return self.version <= other.version


def main():
    to_test = [
        ("1.0.0", "2.0.0"),
        ("1.0.0", "1.42.0"),
        ("1.2.0", "1.2.42"),
        ("1.1.0-alpha", "1.2.0-alpha.1"),
        ("1.0.1b", "1.0.10-alpha.beta"),
        ("1.0.0-rc.1", "1.0.0"),
    ]

    for version_1, version_2 in to_test:
        assert Version(version_1) < Version(version_2), "le failed"
        assert Version(version_2) > Version(version_1), "ge failed"
        assert Version(version_2) != Version(version_1), "neq failed"


if __name__ == "__main__":
    main()