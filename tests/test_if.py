"""
ReaQt example: Reactive Horizontal Box
"""

from qtpy.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout # pylint: disable=E0611

from reaqt.widgets import RxCheckBox, RxIf
from reaqt.state import RxMap
from reaqt.common import connect

class MyWidget(QWidget):
    """ReaQt example: Reactive Horizontal Box"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.state = RxMap({'condition': True})

        checkBox = RxCheckBox("self.state['condition'])")
        connect(self.state['condition'], checkBox.rx.checked)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Set the value of the condition:"))
        layout.addWidget(checkBox)
        layout.addWidget(
            RxIf(self.state['condition'],
                 then=lambda: QLabel("Condition is now <b>True</b>."),
                 else_=lambda: QLabel("Condition is now <b>False</b>.")))
        self.setLayout(layout)



def test_main():
    """Run the example"""
    import sys

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    test_main()

