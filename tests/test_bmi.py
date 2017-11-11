# import rxwrap
from rx import Observable, Observer

from reaqt.widgets import RxWidget, RxLabel, RxPushButton, RxSlider, RxLineEdit
from reaqt.common import connect, connect_controller
from reaqt.state import Nothing, RxMap
from reaqt.utils.layout import vbox, hbox
from reaqt.utils.misc import format_float, scale

from qtpy.QtWidgets import QApplication
from qtpy.QtCore import Qt

def with_units(value, units, precision=2):
    """Prints a floating point value with the specified units and precision"""
    return format_float(value, precision=precision) + " " + units

def weight_from_bmi(bmi, height):
    return bmi * ((height / 100)**2)

def calc_bmi(height, weight):
    return weight / ((height / 100)**2)

class BmiWidget(RxWidget):

    def __init__(self, parent=None):
        super(BmiWidget, self).__init__(parent)

        s_h = RxSlider(Qt.Horizontal,
                       minimum=50, maximum=230)
        s_w = RxSlider(Qt.Horizontal,
                       minimum=0, maximum=250)
        s_b = RxSlider(Qt.Horizontal,
                       minimum=0, maximum=80,               
                       insert=scale(2), extract=scale(0.5))

        l_h = RxLabel(lambda v: "Height: " + with_units(v, 'cm', 0))
        l_w = RxLabel(lambda v: "Weight: " + with_units(v, 'kg', 0))
        l_b = RxLabel(lambda v: "BMI: " + with_units(v, 'kg/m<sup>2</sup>', 1))
        but = RxPushButton("&Debug")

        self.setLayout(vbox(l_h, s_h, l_w, s_w, l_b, s_b, but))

        self.state = RxMap({"h": Nothing,
                            "w": Nothing,
                            "b": Nothing})

        connect(self.state["h"], s_h.rx.value)
        connect_controller(self.state["w"], s_w.rx.value)
        connect_controller(self.state["b"], s_b.rx.value)

        Observable \
            .with_latest_from(self.state["b"].input, self.state["h"],
                              weight_from_bmi) \
            .merge(self.state["w"].input) \
            .subscribe(self.state["w"])

        Observable \
            .combine_latest(self.state["h"], self.state["w"], calc_bmi) \
            .merge(self.state["b"].input) \
            .subscribe(self.state["b"])

        self.state["h"].subscribe(l_h.rx.text.controller)
        self.state["w"].subscribe(l_w.rx.text.controller)
        self.state["b"].subscribe(l_b.rx.text.controller)

        but.rx.clicked.stream.subscribe(lambda x: self.state.debug())


def test_main():
    import sys
    import time

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    widget = BmiWidget()
    widget.state["h"] = 172
    widget.state["w"] = 62
    widget.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    test_main()
