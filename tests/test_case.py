"""
ReaQt example: Reactive Match
"""

from qtpy.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout # pylint: disable=E0611

from reaqt.widgets import RxLineEdit, RxCase
from reaqt.state import RxMap
from reaqt.common import connect

class MyWidget(QWidget):
    """ReaQt example: Reactive Match"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.state = RxMap({'text': ''})

        lineEdit = RxLineEdit(realtime=True)
        lineEdit.setMaxLength(1)
        connect(self.state['text'], lineEdit.rx.text)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Recognized characters: A, B, C, D"))
        layout.addWidget(lineEdit)
        layout.addWidget(
            RxCase(self.state['text'],
                branches=[
                    ('', lambda: QLabel("No input.")),
                    ('A', lambda: QLabel("Recognized letter <b>A</b>.")),
                    ('B', lambda: QLabel("Recognized letter <b>B</b>.")),
                    ('C', lambda: QLabel("Recognized letter <b>C</b>.")),
                    ('D', lambda: QLabel("Recognized letter <b>D</b>."))],
                otherwise=lambda: QLabel("Character not recognized.")))
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

