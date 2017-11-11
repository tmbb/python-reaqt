from rx import Observable, Observer
from rx.subjects import Subject, BehaviorSubject
import copy
import enum
import pprint

class Nothing(object):
    """A special value to act as a placeholder in a RxContainer
    who is not supposed to emit anything
    """
    pass

class RxStream(Subject):
    """A reactive stream that remmebers the last accessed value
    
    Unlike BehaviorSubject, this is a cold observable.
    """
        
    def __init__(self, value=Nothing):
        super().__init__()
        self.current_value = value 

    def on_next(self, value):
        super().on_next(value)
        self.current_value = value

    def on_completed(self):
        pass


class RxBehaviorStream(BehaviorSubject):
    """A reactive stream that remmebers the last accessed value
    
    Like BehaviorSubject, this is a hot observable.
    """
        
    def __init__(self, value):
        super().__init__(value)
        self.current_value = value

    def on_next(self, value):
        super().on_next(value)
        self.current_value = value

    def on_completed(self):
        pass


import enum

class RxListEvent(enum.Enum):
    append = 0
    extend = 1
    insert = 2
    remove = 3
    pop = 4
    clear = 5
    # missing:
    # - index
    # - count
    sort = 6
    reverse = 7
    copy = 8
    delitem = 9


class RxContainer(object):
    """A reactive container, to serve as the base of all reactive containers.

    Members must implement the `freeze()` method to make it easier to extract and
    serialize the values.
    """

    def freeze(self):
        raise NotImplemented()

    def debug(self):
        pprint.pprint(self.freeze())



class RxList(RxContainer):
    """A reactive list, which has been instrumented to emit values
    that can be captured by an :class:`RxPort`.
    """
    
    def __init__(self, items):
        self._list = items
        self._stream = Subject()
        self.length = Subject()

    def __len__(self):
        return len(self._list)

    def broadcast_length(self):
        self.length.on_next(len(self._list))

    def append(self, x, propagate=True):
        self._list.append(x)
        self._stream.on_next((RxListEvent.append, x))
        self.length.on_next(len(self._list))

    def pop(self, i=-1):
        if i < 0:
            index = len(self._list) + i
        else:
            index = i
        self._list.pop(index)
        self._stream.on_next((RxListEvent.pop, index))
        self.length.on_next(len(self._list))

    def extend(self, L):
        self._list.extend(L)
        self._stream.on_next((RxListEvent.extend, L))
        self.length.on_next(len(self._list))

    def insert(self, i, x):
        self._list.insert(i, x)
        self._stream.on_next((RxListEvent.insert, (i, (x, self._list[i+1:]))))
        self.length.on_next(len(self._list))

    def clear(self):
        self._list.clear()
        self._stream.on_next((RxListEvent.clear, None))
        self.length.on_next(len(self._list))

    def reverse(self):
        self._list.reverse()
        self._stream.on_next((RxListEvent.reverse, self._list))
        self.length.on_next(len(self._list))

    def sort(self, key=None, reverse=False):
        self._list.sort(key=key, reverse=reverse)
        self._stream.on_next((RxListEvent.sort, self._list))
        self.length.on_next(len(self._list))

    def splice(self, i, j, new):
        raise NotImplemented()

    def __iter__(self):
        return seld._list

    def __getitem__(self, arg):
        return self._list[arg]

    def __delitem__(self, arg):
        del self._list[arg]
        self._stream.on_next((RxListEvent.delitem, arg))
        self.length.on_next(len(self._list))

    def __setitem__(self, key, value):
        raise Exception("Can't set RxList items.")

    def freeze(self):
        return copy.copy(self._list)


class RxMap(RxContainer):
    """A reactive mutable map, which has been instrumented to emit values
    that can be captured by an :class:`RxPort`.
    """

    def __init__(self, d):
        self._streams = dict()
        self.add_items(d)

    def __getitem__(self, key):
        return self._streams[key]

    def __setitem__(self, key, value):
        self._streams[key].on_next(value)

    def add_items(self, d):
        for key, value in d.items():
            if isinstance(value, RxContainer):
                self._streams[key] = value
            else:
                if value is Nothing:
                    self._streams[key] = RxStream(value)
                else:
                    self._streams[key] = RxBehaviorStream(value)

    def freeze(self):
        d = dict()
        for key, value in self._streams.items():
            if isinstance(value, RxContainer):
                d[key] = value.freeze()
            else:
                d[key] = value.current_value

        return d
