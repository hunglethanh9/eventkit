from collections import deque

from .op import Op
from ..util import NO_VALUE

import numpy as np


class Array(Op):
    __slots__ = ('_count', '_q')

    def __init__(self, count, source=None):
        Op.__init__(self, source)
        self._count = count
        self._q = deque()

    def on_source(self, *args):
        self._q.append(
            args[0] if len(args) == 1 else args if args else NO_VALUE)
        if self._count and len(self._q) > self._count:
            self._q.popleft()
        self.emit(np.asarray(self._q))

    def min(self) -> "ArrayMin":
        """
        Minimum value.
        """
        return ArrayMin(self)

    def max(self) -> "ArrayMax":
        """
        Maximum value.
        """
        return ArrayMax(self)

    def sum(self) -> "ArraySum":
        """
        Summation.
        """
        return ArraySum(self)

    def mean(self) -> "ArrayMean":
        """
        Mean value.
        """
        return ArrayMean(self)

    def std(self) -> "ArrayStd":
        """
        Sample standard deviation.
        """
        return ArrayStd(self)

    def any(self) -> "ArrayAny":
        """
        Test if any array value is true.
        """
        return ArrayAny(self)

    def all(self) -> "ArrayAll":
        """
        Test if all array values are true.
        """
        return ArrayAll(self)


class ArrayMin(Op):
    __slots__ = ()

    def on_source(self, arg):
        self.emit(arg.min())


class ArrayMax(Op):
    __slots__ = ()

    def on_source(self, arg):
        self.emit(arg.max())


class ArraySum(Op):
    __slots__ = ()

    def on_source(self, arg):
        self.emit(arg.sum())


class ArrayMean(Op):
    __slots__ = ()

    def on_source(self, arg):
        self.emit(arg.mean())


class ArrayStd(Op):
    __slots__ = ()

    def on_source(self, arg):
        self.emit(arg.std(ddof=1) if len(arg) > 1 else np.nan)


class ArrayAny(Op):
    __slots__ = ()

    def on_source(self, arg):
        self.emit(arg.any())


class ArrayAll(Op):
    __slots__ = ()

    def on_source(self, arg):
        self.emit(arg.all())
