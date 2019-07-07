# -*- code: utf-8 -*-
"""
    Text used by GOTO to do UX.
"""
from . import warning, error


class GotoError:
    def __init__(self, name, **kwargs):
        self.name = name
        self.kwargs = kwargs

    @property
    def message(self):
        # Making retrieval fail fast, if not present, stop and show the error.
        # the missing message should then be made
        text = error.messages.get(self.name, None)
        if text is None:
            raise Exception(
                "Missing error message with name: {}".format(self.name))
        return text.format(**self.kwargs)


class GotoWarning:
    def __init__(self, name, **kwargs):
        self.name = name
        self.kwargs = kwargs

    @property
    def message(self):
        # Making retrieval fail fast, if not present, stop and show the error.
        # the missing message should then be made
        text = warning.messages.get(self.name, None)
        if text is None:
            raise Exception(
                "Missing warning message with name: {}".format(self.name))
        return text.format(**self.kwargs)


def print_text(text, **kwargs):
    print(text.format(**kwargs))
