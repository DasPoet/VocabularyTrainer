"""Contains only one class: Vocab.
See Vocab for more information."""


class Vocab:

    languages_swapped = False
    current_return = 0

    def __init__(self, *, form1, form2, languages=None):
        """Initialise a Vocab object with a word, its translation (the second form) and its languages.
        Note: the first form must correspond to the language of the first element of languages,
        and the second form must correspond to the language of the second element of languages.
        """

        if isinstance(form1, str) and isinstance(form2, str):
            self._FIRST = self._first = form1  # self._FIRST: the first form, does not change
            self._LAST = self._last = form2  # self._LAST: the second form, does not change
        else:
            raise ValueError(f"Forms must be of type string & string not {type(form1)} & {type(form2)}")

        self._languages = None

        if languages is not None:
            if isinstance(languages, tuple) or isinstance(languages, list):
                self._languages = languages
            else:
                raise ValueError(f"Languages must be of type tuple or list not {type(languages)}")

    def __repr__(self):
        """Return information about an instance of Vocab, containing the first and the second form."""

        return f"Vocab object -> first forms: {self.first_form.strip()} | last forms: {self.last_form.strip()}"

    def __iter__(self):
        """See Vocab.__next__()."""

        return self

    def __next__(self):
        """Make the Vocab object iterable so that it yields its first and second form when iterated over."""

        if self.current_return == 2:
            self.current_return = 0
        elif self.current_return == 0:
            self.current_return = 1
            return self.first_form
        elif self.current_return == 1:
            self.current_return = 2
            return self.last_form
        raise StopIteration

    @property
    def real_first(self):
        """Get the first form the object was initialised with."""

        return self._FIRST

    @property
    def real_last(self):
        """Get the last form the object was initialised with."""

        return self._LAST

    @property
    def first_form(self):
        """Get the first form."""

        return self._first

    @first_form.setter
    def first_form(self, form):
        """Set the first form."""

        self._first = form

    @property
    def last_form(self):
        """Get the last form."""

        return self._last

    @last_form.setter
    def last_form(self, form):
        """Set the last form."""

        self._last = form

    @property
    def languages(self):
        """Get languages."""

        return self._languages

    @languages.setter
    def languages(self, langs):
        """Set languages."""

        self._languages = langs

    def swap_languages(self):
        """Switch the first and second form."""

        self.languages_swapped = not self.languages_swapped
        self.first_form, self.last_form = self.last_form, self.first_form
        self.languages = list(reversed(self.languages))
