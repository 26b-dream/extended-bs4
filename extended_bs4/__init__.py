from __future__ import annotations

from typing import TYPE_CHECKING

from bs4 import BeautifulSoup
from bs4.element import Tag

if TYPE_CHECKING:
    from bs4.element import ResultSet


def extend_class(original_class: object, extended_class: object):
    # Get a list of all of the functions
    original_functions = dir(original_class)

    # Go through all the function in the extended class
    for function in dir(extended_class):
        # If the function does not exist patch it in
        if function not in original_functions:
            setattr(original_class, function, getattr(extended_class, function))


class StrictBeautifulSoupFaiure(Exception):
    """Raised when a strict function fails"""


def strict_select(self: Tag, selector: str) -> ResultSet[Tag]:
    """Same as .select but it will raise an exception if no match is found"""
    output = self.select(selector)
    if len(output) != 0:
        return output

    raise StrictBeautifulSoupFaiure(f"No matches found for strict_select({selector})")


# BeatifulSoup functions will return Tag objects
# Changing all of the Tag objects to ExtendedTag objects would be nearly impossible
# As an alternative, patch in extra functions into the Tag class
# This will modify BeautifulSoup globally so it is not an ideal solution but it works well enough
# If BeautifulSoup was typed I would just fork it
# It is not typed so it's easier to just patch in the functions
class ExtendedTag(Tag):
    def strict_select(self, selector: str) -> ResultSet[Tag]:
        """Same as .select but it will raise an exception if no match is found"""
        output = self.select(selector)
        if len(output) != 0:
            return output

        raise StrictBeautifulSoupFaiure(f"No matches found for strict_select({selector})")

    def strict_select_one(self, selector: str) -> Tag:
        """Same as .select but it will raise an exception the number of matches is not 1"""
        output = self.select(selector)
        number_of_matches = len(output)
        if number_of_matches == 1:
            return output[0]

        raise StrictBeautifulSoupFaiure(
            f"Wrong number of matches found for strict_select({selector}), found {number_of_matches}"
        )

    def strict_get(self, key: str) -> str:
        """Same as .get but it will raise an exception if no match is found"""
        output = self.get(key)
        if isinstance(output, str):
            return output

        raise StrictBeautifulSoupFaiure(f"No matches found for strict_get({key})")


extend_class(Tag, ExtendedTag)


class ExtendedBeautifulSoup(ExtendedTag, BeautifulSoup):
    """Same as BeautifulSoup but with extra functions"""
