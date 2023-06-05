"""Extended version of BeautifulSoup with extra functions. WARNING: Modifies BeautifulSoup globally."""

from __future__ import annotations

from typing import TYPE_CHECKING

from bs4 import BeautifulSoup
from bs4.element import Tag

if TYPE_CHECKING:
    from bs4.element import ResultSet


def extend_class(original_class: object, extended_class: object):
    """Adds all functions from `extended_class` to `original_class` that do not already exist in `original_class`.

    Args:
        original_class (object): The class to be extended.
        extended_class (object): The class that contains the additional functions to be added to `original_class`."""

    # Get a list of all of the functions
    original_functions = dir(original_class)

    # Go through all the function in the extended class
    for function in dir(extended_class):
        # If the function does not exist patch it in
        if function not in original_functions:
            setattr(original_class, function, getattr(extended_class, function))


class StrictBeautifulSoupFaiure(Exception):
    """Exception raised when a strict_* function  fails to find a match."""


# BeatifulSoup functions will return Tag objects
# Changing all of the Tag objects to ExtendedTag objects would be nearly impossible
# As an alternative, patch in extra functions into the Tag class
# This will modify BeautifulSoup globally so it is not an ideal solution but it works well enough
# If BeautifulSoup was typed I would just fork it
# It is not typed so it's easier to just patch in the functions
class ExtendedTag(Tag):
    """Temporary class used to patch in extra functions into the Tag class."""

    def strict_select(self, selector: str) -> ResultSet[Tag]:
        """Modified version of .select that will raise an exception if no matches are found.

        Args:
            selector (str): The CSS selector to search for.

        Returns:
            ResultSet[Tag]: A ResultSet of all Tags that match the selector.

        Raises:
            StrictBeautifulSoupFaiure: If no matches are found for the selector."""

        output = self.select(selector)
        if len(output) != 0:
            return output

        raise StrictBeautifulSoupFaiure(f"No matches found for strict_select({selector})")

    def strict_select_one(self, selector: str) -> Tag:
        """Modified version of .select_one that will raise an exception if the number of matches is not exactly 1.

        Args:
            selector (str): The CSS selector to search for.

        Returns:
            Tag: The first tag that matches the selector.

        Raises:
            StrictBeautifulSoupFaiure: If the number of matches is not exactly 1."""

        output = self.select(selector)
        number_of_matches = len(output)
        if number_of_matches == 1:
            return output[0]

        raise StrictBeautifulSoupFaiure(
            f"Wrong number of matches found for strict_select({selector}), found {number_of_matches}"
        )

    def strict_get(self, key: str) -> str:
        """
        Modified version of .get that will raise an exception no match is found

        Args:
            key (str): The key to search for in the tag's attributes.

        Returns:
            str: The value of the attribute.

        Raises:
            StrictBeautifulSoupFaiure: If no match is found for the key.
        """
        output = self.get(key)
        if isinstance(output, str):
            return output

        raise StrictBeautifulSoupFaiure(f"No matches found for strict_get({key})")


extend_class(Tag, ExtendedTag)


class ExtendedBeautifulSoup(ExtendedTag, BeautifulSoup):  # pylint: disable=W0223
    """Extended version of BeautifulSoup with extra functions.

    A data structure representing a parsed HTML or XML document.

    Most of the methods you'll call on a BeautifulSoup object are inherited from PageElement or Tag.

    Internally, this class defines the basic interface called by the tree builders when converting an HTML/XML document
    into a data structure. The interface abstracts away the differences between parsers. To write a new tree builder,
    you'll need to understand these methods as a whole.

    These methods will be called by the BeautifulSoup constructor:
      * reset()
      * feed(markup)

    The tree builder may call these methods from its feed() implementation:
      * handle_starttag(name, attrs) # See note about return value
      * handle_endtag(name)
      * handle_data(data) # Appends to the current data node
      * endData(containerClass) # Ends the current data node

    No matter how complicated the underlying parser is, you should be able to build a tree using 'start tag' events,
    'end tag' events, 'data' events, and "done with data" events.

    If you encounter an empty-element tag (aka a self-closing tag, like HTML's <br> tag), call handle_starttag and then
    handle_endtag.

    """
