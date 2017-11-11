import numbers
import base64

from qtpy.QtGui import *
from qtpy.QtWidgets import *

def stretch(value=1):
    return value

def vsplitter(shadow=QFrame.Sunken):
    separator = QFrame()
    separator.setFrameStyle(QFrame.VLine)
    separator.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
    separator.setFrameShadow(shadow)
    return separator


def hsplitter(shadow=QFrame.Sunken):
    separator = QFrame()
    separator.setFrameStyle(QFrame.HLine)
    separator.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
    separator.setFrameShadow(shadow)
    return separator

def makeHStretchable(widget):
    widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

def make_compact(widget):
    widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    widget.setStyleSheet('padding: 0')

def _box(children, boxtype):
    box = boxtype()
    for child in children:
        _addChild(box, child)
    return box

def hbox(*children):
    """Returns a QHBoxLayout with the given children."""
    return _box(children, QHBoxLayout)

def vbox(*children):
    """Returns a QVBoxLayout with the given children."""
    return _box(children, QVBoxLayout)

def hwidget(*children):
    widget = QWidget()
    widget.setLayout(hbox(*children))
    return widget

def vwidget(*children):
    widget = QWidget()
    widget.setLayout(vbox(*children))
    return widget

def hcenter(*children):
    """Returns a horizontally centered QHBoxLayout"""
    args = [1] + list(children) + [1]
    return hbox(*args)

def vcenter(*children):
    """Returns a vertically centered QVBoxLayout"""
    args = [1] + list(children) + [1]
    return vbox(*args)

def _addChild(parent, child):
    if isinstance(child, numbers.Real):
        parent.addStretch(child)
    elif isinstance(child, QLayout):
        parent.addLayout(child)
    elif isinstance(child, QWidget):
        parent.addWidget(child)
    elif isinstance(child, str):
        parent.addWidget(QLabel(child))
    else:
        raise Exception("Unsupported Argument!")

def group_box(text_label, child):
    groupbox = QGroupBox(text_label)
    groupbox.setLayout(child)
    return groupbox

def css_data_url(content):
    return 'data:text/css;charset=utf-8;base64,{0}'.format(
                base64.b64encode(unicode(content)))
