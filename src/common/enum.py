# -*- coding: utf-8 -*-

ENUM_ATTRIBUTE_PREFIX = tuple("ABCDEFGHIJKLMNOPQRSTUVWXYZ")


class Enum:
    """
    Base class for application enums. Eventually may have helper methods on here for iterating values etc. or providing
    labels
    """

    # Dictionary of enum value to label
    _labels = None

    @classmethod
    def get_label(cls, value):
        return value if cls._labels is None else cls._labels.get(value, value)

    @classmethod
    def values(cls):
        """
        Returns a list of all the possible values of this Enum, ordered alphabetically
        :return:
        """
        return [
            getattr(cls, a) for a in dir(cls) if a.startswith(ENUM_ATTRIBUTE_PREFIX)
        ]

    @classmethod
    def items(cls):
        """
        Returns a list of tuples of (value, label) of all the enums, ordered alphabetically
        :return:
        """
        return [
            (value, cls.get_label(value=value)) for value in cls.values()
        ]
