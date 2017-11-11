import datetime

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

from rx.subjects import Subject, BehaviorSubject

from .utils import conversions
from .utils.misc import scale
from .common import FakeObservable, RxPort, RxPortManager, RxObserver, RxObservable
from .state import RxListEvent

from collections import namedtuple

LoopContext = namedtuple('LoopContext', ['value', 'index', 'total'])

class RxPushButton(QPushButton):
    """Reactive QPushButton"""

    def __init__(self, *args, **kwargs):
        super(QPushButton, self).__init__(*args, **kwargs)
        self.rx = RxPortManager()
        # Button signals
        self.rx.clicked  = RxPort(RxObserver(self, self.click()),
                                  RxObservable(self.clicked,  get=lambda: True))
        #self.rx.released = RxPort(RxObserver(self, self.release()), RxObservable(self.released, get=lambda: True))
        #self.rx.pressed  = RxPort(RxObserver(self, self.press()),   RxObservable(self.pressed,  get=lambda: True))

class RxSlider(QSlider):
    """Reactive QSlider"""

    def __init__(self,
                 orientation=Qt.Vertical, parent=None,
                 minimum=None, maximum=None,
                 insert=lambda x: x, extract=lambda x: x):

        super(QSlider, self).__init__(orientation, parent)
        self.rx = RxPortManager()
        # Minumum
        if minimum is not None:
            self.setMinimum(minimum)
        else:
            self.rx.minimum = RxPort(RxObserver(self, self.setMinimum, insert),
                                   FakeObservable())
        # Maximum
        if maximum is not None:
            self.setMaximum(insert(maximum))
        else:
            self.rx.maximum = RxPort(RxObserver(self, self.setMaximum, insert),
                                   FakeObservable())
        # Value
        controller = RxObserver(self, self.setValue, insert)
        stream = RxObservable(self.valueChanged, extract)
        self.rx.value = RxPort(controller, stream)

class RxCheckBox(QCheckBox):
    """Reactive QCheckBox"""

    def __init__(self, text=None, parent=None):
        super(RxCheckBox, self).__init__(parent)
        self.rx = RxPortManager()
        # Checked Value
        controller = RxObserver(self, self.setChecked)
        stream = RxObservable(self.stateChanged)
        self.rx.checked = RxPort(controller, stream)
        # Text
        if text is None:
            self.rx.text = RxPort(RxObserver(self, self.setText),
                                FakeObservable())
        else:
            self.setText(text)

class RxRadioButton(QRadioButton):
    """Reactive QRadioButton"""

    def __init__(self, text=None, parent=None):
        super(RxRadioButton, self).__init__(parent)
        self.rx = RxPortManager()
        # Checked Value
        controller = RxObserver(self, self.setChecked)
        stream = RxObservable(self.toggled)
        self.rx.checked = RxPort(controller, stream)
        # Text
        if text is None:
            self.rx.text = RxPort(RxObserver(self, self.setText),
                                  FakeObservable())
        else:
            self.setText(text)



class RxLabel(QLabel):
    """Reactive QLabel"""

    def __init__(self, insert=str, **kwargs):
        super().__init__(**kwargs)
        self.rx = RxPortManager()
        self.rx.text = RxPort(RxObserver(self, self.setText, insert),
                              FakeObservable())


class RxLineEdit(QLineEdit):
    """Reactive QLineEdit"""

    def __init__(self, realtime=True, **kwargs):
        super().__init__(**kwargs)
        self.rx = RxPortManager()
        controller = RxObserver(self, self.setText)

        if realtime:
            stream = RxObservable(self.textEdited)
        else:
            stream = RxObservable(self.editingFinished,
                                  get=self.text)

        self.rx.text = RxPort(controller, stream)


class RxSpinBox(QSpinBox):
    """Reactive QSpinBox"""

    def __init__(self, **kwargs):
        super(QSpinBox, self).__init__(**kwargs)
        self.rx = RxPortManager()
        controller = RxObserver(self, self.setValue)
        stream = RxObservable(self.valueChanged)

        self.rx.value = RxPort(controller, stream)
        # Minimum
        self.rx.minimum = RxPort(RxObserver(self, self.setMinimum),
                                 FakeObservable())
        # Maximum
        self.rx.maximum = RxPort(RxObserver(self, self.setMaximum),
                                 FakeObservable())

class RxCalendarWidget(QCalendarWidget):
    """Reactive QCalendarWidget"""

    def __init__(self, **kwargs):
        super(QCalendarWidget, self).__init__(**kwargs)
        self.rx = RxPortManager()
        controller = RxObserver(self, self.setSelectedDate, transform=conversions.date_to_QDate)
        stream = RxObservable(self.selectionChanged, transform=conversions.QDate_to_date, get=self.selectedDate)

        self.rx.date = RxPort(controller, stream)
        # Minimum
        controller = RxObserver(self, self.setMinimumDate, transform=conversions.date_to_QDate)
        stream = FakeObservable()
        self.rx.minimum = RxPort(controller, stream)
        # Maximum
        controller = RxObserver(self, self.setMaximumDate, transform=conversions.date_to_QDate)
        stream = FakeObservable()
        self.rx.maximum = RxPort(controller, stream)



class RxDateEdit(QDateEdit):
    """Reactive QDateEdit"""

    def __init__(self, **kwargs):
        super(QDateEdit, self).__init__(**kwargs)
        self.rx = RxPortManager()
        controller = RxObserver(self, self.setDate, transform=conversions.date_to_QDate)
        stream = RxObservable(self.dateChanged, transform=conversions.QDate_to_date)

        self.rx.date = RxPort(controller, stream)

class RxTimeEdit(QTimeEdit):
    """Reactive QTimeEdit"""

    def __init__(self, **kwargs):
        super(QTimeEdit, self).__init__(**kwargs)
        self.rx = RxPortManager()
        controller = RxObserver(self, self.setTime, transform=time_to_QTime)
        stream = RxObservable(self.timeChanged, transform=QTime_to_time)

        self.rx.date = RxPort(controller, stream)


class RxDateTimeEdit(QDateTimeEdit):
    """Reactive QDateTimeEdit"""

    def __init__(self, **kwargs):
        super(QDateTimeEdit, self).__init__(**kwargs)
        self.rx = RxPortManager()
        controller = RxObserver(self, self.setDateTime, transform=conversions.datetime_to_QDateTime)
        stream = RxObservable(self.dateTimeChanged, transform=conversions.QDateTime_to_datetime)

        self.rx.date = RxPort(controller, stream)



class RxWidget(QWidget):
    """Reactive QWidget"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rx = RxPortManager()

class RxConditional(QWidget):
    pass


class RxIf(QWidget):
    """Widget that displays it's contents depending on a condition"""

    def __init__(self, observable, then, else_=None):
        super(QWidget, self).__init__()
        self.rx = RxPortManager()
        self.rx.observable = observable
        self.rx.then_builder = then
        self.rx.else_builder = else_
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)
        self.rx.observable.subscribe(self._conditionChanged)

    def _conditionChanged(self, value):
        if value:
            replace_children_by_widget(self, self.rx.then_builder())
        elif self.rx.else_builder:
            replace_children_by_widget(self, self.rx.else_builder())

def replace_children_by_widget(parent_widget, replacement_widget):
    clear_widget(parent_widget)
    parent_widget.layout().addWidget(replacement_widget)
    parent_widget.adjustSize()

class RxWidgetBranchedWithDefault(QWidget):
    def __init__(self, observable, branches, otherwise=None):
        super(QWidget, self).__init__()
        self.rx = RxPortManager()
        self.rx.observable = observable
        self.rx.branches = branches
        self.rx.otherwise = otherwise
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)
        self.rx.observable.subscribe(self._observableChanged)

    def _observableChanged(self, value):
        raise NotImplementedError

class RxMatch(RxWidgetBranchedWithDefault):

    def _observableChanged(self, value):
        for (predicate, builder) in self.rx.branches:
            if predicate(value):
                replace_children_by_widget(self, builder())
                return

        if self.rx.otherwise:
            replace_children_by_widget(self, self.rx.otherwise())

class RxCase(RxWidgetBranchedWithDefault):

    def _observableChanged(self, value):
        for (comparator, builder) in self.rx.branches:
            if value == comparator:
                replace_children_by_widget(self, builder())
                return

        if self.rx.otherwise:
            replace_children_by_widget(self, self.rx.otherwise())

class RxCond(QWidget):

    def __init__(self, branches):
        super(QWidget, self).__init__()
        self.rx = RxPortManager()
        self.rx.branches = branches
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        for (condition, builder) in self.rx.branches:
            condition.subscribe(lambda x: self._react(x, builder))

    def _react(self, x, builder):
        if x:
            print("Will replace.")
            replace_children_by_widget(self, builder())


class RxTabsWidget(QTabWidget):
    """Reactive QTabs"""

    def __init__(self, tabs=[], *args, **kwargs):
        super(QTabWidget, self).__init__(*args, **kwargs)

        self.rx = RxPortManager()
        controller = RxObserver(self, self.setCurrentIndex)
        stream = RxObservable(self.currentChanged)
        self.rx.current_index = RxPort(controller, stream)

        for tab_args in tabs:
            self.addTab(*tab_args)

class RxSimpleComboBox(QComboBox):

    def __reset_items(self, items):
        self.clear()
        self.rx._data = items
        self.addItems(items)
        if items:
            self.rx.value.stream.on_next(0)

    def set_options_and_value(self, opts, value):
        self.__reset_items(opts)
        self.__set_item_text(index)

    def __index_to_value(self, index):
        return self.rx._data[index]

    def __index_from_value(self, text):
        return self.rx._data.index(text)

    def __set_item_text(self, text):
        index = self.__index_from_value(text)
        self.setCurrentIndex(index)

    def __init__(self):
        super(QWidget, self).__init__()
        self.rx = RxPortManager()
        self.rx._data = []
        # ComboBox items
        controller = RxObserver(self, self.__reset_items)
        stream = FakeObservable()
        self.rx.items = RxPort(controller, stream)
        # ComboBox value
        controller = RxObserver(self, self.__set_item_text)
        stream = RxObservable(self.currentIndexChanged, self.__index_to_value)
        self.rx.value = RxPort(controller, stream)


class RxBox(QWidget):

    def __init__(self, rx_list, item_class, tight=True, layout_class=QVBoxLayout):
        super(QWidget, self).__init__()
        self.rx = RxPortManager()
        self.rx.state = rx_list
        self.rx.controller = RxBoxController(self)
        self.rx.state._stream.subscribe(self.rx.controller)
        self.rx.item_class = item_class
        self.rx.layout_class = layout_class
        layout = self.rx.layout_class()
        if tight:
            layout.setContentsMargins(0,0,0,0)
        for index, item in enumerate(self.rx.state._list):
            layout.addWidget(self.rx.item_class(index, item))
        self.setLayout(layout)


class RxVBox(RxBox):
    """Reactive Vertical Box"""

    def __init__(self, rx_list, item_class, tight=True):
        super().__init__(rx_list, item_class, tight=tight, layout_class=QVBoxLayout)


class RxHBox(RxBox):
    """Reactive Horizontal Box"""

    def __init__(self, rx_list, item_class, tight=True):
        super().__init__(rx_list, item_class, tight=tight, layout_class=QHBoxLayout)

def clear_widget(widget):
    while widget.layout().count() > 0:
        child = widget.layout().takeAt(0).widget()
        child.setParent(None)
        widget.layout().removeWidget(child)

class RxBoxController(Subject):

    def __init__(self, widget):
        super(Subject, self).__init__()
        self.widget = widget

    def on_next(self, event):
        typ, value = event

        if typ == RxListEvent.append:
            widget = self.widget.rx.item_class(len(self.widget.rx.state),
                                               value)
            self.widget.layout().addWidget(widget)

        elif typ == RxListEvent.pop:
            widget = self.widget.layout().takeAt(value).widget()
            widget.setParent(None)
            self.widget.layout().removeWidget(widget)
            self.widget.adjustSize()

        elif typ == RxListEvent.insert:
            i, (x, rest) = value
            self.widget.layout()\
                .insertWidget(i, self.widget.rx.item_class(i, x))

            while self.widget.layout().count() > i+1:
                widget = self.widget.layout().takeAt(i+1).widget()
                widget.setParent(None)
                self.widget.layout().removeWidget(widget)

            # Rerender items after the inserted one because the indices have changed
            for delta, state in enumerate(rest):
                widget = self.widget.rx.item_class(i + 1 + delta,
                                                   state)
                self.widget.layout().addWidget(widget)

        elif typ == RxListEvent.extend:
            initial_length = len(self.widget.rx.state) - len(value)
            for delta, state in enumerate(value):
                widget = self.widget.rx.item_class(initial_length + delta,
                                                   state)
                self.widget.layout().addWidget(widget)

        elif typ == RxListEvent.clear:
            while self.widget.layout().count() > 0:
                widget = self.widget.layout().takeAt(0).widget()
                widget.setParent(None)
                self.widget.layout().removeWidget(widget)
            self.widget.adjustSize()

        elif typ == RxListEvent.reverse or typ == RxListEvent.sort:
            # The whole list must be redrawn, in case the widget
            # value depends on the index in the list
            while self.widget.layout().count() > 0:
                widget = self.widget.layout().takeAt(0).widget()
                widget.setParent(None)
                self.widget.layout().removeWidget(widget)

            for i, state in enumerate(value):
                widget = self.widget.rx.item_class(i, state)
                self.widget.layout().addWidget(widget)

        elif typ == RxListEvent.delitem:
            if isinstance(value, slice):
                widgets = []
                # Collect the widgets
                for i in range(value.start, value.stop, value.step):
                    widget = self.widget.layout().takeAt(i).widget()
                    widgets.append(widget)
                # Delete them
                for widget in widgets:
                    widget.setParent(None)
                    self.widget.layout().removeWidget(widget)
                self.widget.adjustSize()
            else:
                widget = self.widget.layout().takeAt(value).widget()
                widget.setParent(None)
                self.widget.layout().removeWidget(widget)
                self.widget.adjustSize()
