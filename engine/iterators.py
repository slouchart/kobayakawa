class GameIterator:
    """
    Iterates through a iterable (passed at initialization)
    Fires some events:
    - iterator reset
    - iterator stops
    - iterator changes
    """

    def __init__(self, iterable):
        """
        :param iterable: any iterable
        """
        self._iterable = iterable
        self._iter = self._iterable.__iter__()
        self.on_reset = None
        self.on_stop = None
        self.on_change = None
        self._last_item = None

    def __iter__(self):
        return self

    def __next__(self):
        try:
            new_item = next(self._iter)
            self._trigger_event('on_change')
            return new_item
        except StopIteration:
            self._trigger_event('on_stop')
            raise

    def reset(self):
        self._iter = self._iterable.__iter__()
        self._last_item = None
        self._trigger_event('on_reset')

    def _trigger_event(self, event):
        if hasattr(self, event) and self.__getattribute__(event) is not None:
            self.__getattribute__(event)()

    def set_event(self, event, target):
        self.__setattr__(event, target)


class GamePlayOrderIterator(GameIterator):
    """
    Iterates through a play order with a starting player
    Optionally fires an event when the iterator is exhausted (all players have played)
    Provides a method to compare two members with respect to their distance from the first player
    """

    def __init__(self, iterable, starting):
        super().__init__(iterable)

        seq = list(iterable)
        start = seq.index(starting)

        self._list = seq[start:] + seq[:start]
        self._iter = self._list.__iter__()
        self._ignore = set()

    def reset(self, starting=None, iterable=None):
        super().reset()  # to fire the event
        if iterable is not None:
            self._list = list(iterable)

        # actual processing
        if starting is not None:
            start = self._list.index(starting)
            self._list = self._list[start:] + self._list[:start]

        self._iter = self._list.__iter__()

    def compare(self, item1, item2):
        assert item1 in self._list
        assert item2 in self._list

        d1 = self._list.index(item1)
        d2 = self._list.index(item2)

        assert (d1 != d2)
        if d1 > d2:
            return item2
        else:
            return item1
