import contextlib

from rx import Observer
from rx.subjects import Subject

# from .utils.misc import identity

class FakeObservable(object):
    """A fake observable that does nothing

    It provides a :meth:`FakeObservable.subscribe` method
    which does nothing.
    """

    def __init__(self):
        pass
        #self._queue = []

    def subscribe(self, observer):
        pass
        #self._queue.append(observer)


@contextlib.contextmanager
def signals_blocked(qobject):
    """Allows the user to update a QWidget without sending any signals.

    This is essential to avoid cyclic dependency graphs.

    .. code-block:

        line = QLineEdit()
        with signals_blocked(line):
            line.setText("This will not send a Qt Signal.")
        line.setText("This will send a Qt Signal.)
    """
    qobject.blockSignals(True)
    yield
    qobject.blockSignals(False)


class RxObserver(Observer):
    """A controller for a RxWidget.

    This will observe the observables that have been subscribed
    and will use their values to update the associated QWidget.
    Some customizations are possible.

    This is the Rx equivalent of a Qt Slot.
    """

    def __init__(self, qobject, func, transform=lambda x: x):
        super().__init__()
        self.qobject = qobject
        self.func = func
        self.transform = transform

    def on_next(self, value):
        with signals_blocked(self.qobject):
            self.func(self.transform(value))

    def on_completed(self):
        pass

    def on_error(self, e):
        print(e)

class RxObservable(Subject):
    """A stream that will emit the values sent by Qt Signals.

    This is the Rx equivalent of a Qt Signal.
    """

    def __init__(self, signal,
                 transform=lambda x: x,
                 get=None):
        super().__init__()
        self.signal = signal
        self.transform = transform
        if get is None:
            self.signal.connect(self.on_next)
        else:
            self.signal.connect(
                lambda: self.on_next(get()))

    def on_next(self, value):
        super().on_next(self.transform(value))

    def on_completed(self):
        pass

    def on_error(self, e):
        print(e)

class RxPort(Subject):
    """A class for reactive 2-way data binding.
    This class controls associates a QWidget with a reactive value.

    It contains a controller and a stream.
    """

    def __init__(self, controller, stream):
        self.controller = controller
        self.stream = stream


    def on_next(self, value):
        self.controller.on_next(value)

    def on_completed(self):
        self.controller.on_completed()

    def on_error(self, error):
        self.controller.on_error(error)

    def subscribe(self, observer):
        self.stream.subscribe(observer)

class RxPortManager(object):
    """A class that contains several :class:`RxPort`
    """
    pass


def connect_controller(subject, rx_port, right=None, left=None):
    """Bind an Subject to the controller of a rx_port object.

    The reverse binding will be available.
    """
    if right is None:
        subject.subscribe(rx_port.controller)
    else:
        subject.map(right).subscribe(rx_port.controller)
    if left is None:
        subject.input = rx_port.stream
    else:
        subject.input = rx_port.stream.map(left)

def connect(subject, rx_port, right=None, left=None):
    """Bind a Subject to a :class:`RxPort` object.


    """
    if right is None:
        subject.subscribe(rx_port.controller)
    else:
        subject.map(right).subscribe(rx_port.controller)
    if left is None:
        rx_port.stream.subscribe(subject)
    else:
        rx_port.stream.map(left).subscribe(subject)
