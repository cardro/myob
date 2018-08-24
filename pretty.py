"""Contains utility functions for progress and pretty printing.
"""

import colorama
from colorama import Fore as FG, Back as BG, Style as ST

colorama.init()


# -----------------------------------------------------------------------------
# Pretty
# -----------------------------------------------------------------------------

class Pretty(object):
    """Pretty printer with custom formatting.

    Pretty is a pretty printing class that allows output to be cusomtized
    for each object type, custom horizonal tab and line feed strings, and
    indenting. Custom formatters are already specified for :class:`dict`,
    :class:`list`, and :class:`tuple` objects, giving a generic line feed
    scaffold, and a default formatter for :class:`object` is included.
    """

    def __init__(self, htchar='  ', lfchar='\n', indent=0, limit=0):
        """Return an instance of Pretty.

        Args:
            htchar (str): horizontal tab string
            lfchar (str): line feed string
            indent (int): number of htchar to prepend to output (entirety)
        """
        self.htchar = htchar
        self.lfchar = lfchar
        self.indent = indent
        self.limit = limit
        self.types = [
            (dict, self.dict_formatter),
            (list, self.list_formatter),
            (tuple, self.tuple_formatter),
            (object, self.object_formatter)
        ]

    def __call__(self, value, **kwargs):
        """Allows class instance to be invoked as a function for formatting.

        Args:
            value (object): object to be formatted
            **kwargs: named arguments to be assigned as attributes

        Returns:
            str: pretty formatted string ready to be printed
        """
        for k, v in kwargs.items():
            setattr(self, k, v)
        return self.get_formatter(value)(value, self.indent)

    def add_formatter(self, obj, formatter):
        """Adds a custom formatter for an arbitrary object type.

        Args:
            obj (type): object type
            formatter (function): custom formatter function with signature
                formatter(value, indent)
        """
        self.types.insert(0, (obj, formatter))

    def get_formatter(self, obj):
        """Retrieves the custom formatter for the object type (or default).
        """
        for type_, formatter in self.types:
            if isinstance(obj, type_):
                return formatter

    def object_formatter(self, value, indent):
        """Default object formatter.
        """
        string = repr(value)
        if self.limit > 0 and len(string) > self.limit:
            string = (
                string[0:50] +
                FG.RED + ' ... [truncated] ... ' + ST.RESET_ALL +
                s[-50:]
            )
        return string

    def dict_formatter(self, value, indent):
        """Dictionary formatter.
        """
        items = []
        for key in sorted(value.keys()):
            items.append(
                self.lfchar + self.htchar * (indent + 1) +
                FG.GREEN + repr(key) + ST.RESET_ALL + ': ' +
                self.get_formatter(value[key])(value[key], indent + 1)
            )
        return '{%s}' % (','.join(items) + self.lfchar + self.htchar * indent)

    def list_formatter(self, value, indent):
        """List formatter.
        """
        items = [
            self.lfchar + self.htchar * (indent + 1) +
            self.get_formatter(item)(item, indent + 1)
            for item in value
        ]
        return '[%s]' % (','.join(items) + self.lfchar + self.htchar * indent)

    def tuple_formatter(self, value, indent):
        """Tuple formatter.
        """
        items = [
            self.lfchar + self.htchar * (indent + 1) +
            self.get_formatter(item)(item, indent + 1)
            for item in value
        ]
        return '(%s)' % (','.join(items) + self.lfchar + self.htchar * indent)

pretty = Pretty()
