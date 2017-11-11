"""
ReaQt example: Reactive Match
"""

from qtpy.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout # pylint: disable=E0611

from reaqt.widgets import RxLineEdit, RxMatch
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
        layout.addWidget(QLabel("Recognized letters: A, B, C, D"))
        layout.addWidget(lineEdit)
        layout.addWidget(
            RxMatch(self.state['text'],
                branches=[
                    (lambda x: x == '', lambda: QLabel("No input.")),
                    (lambda x: x == 'A', lambda: QLabel("Recognized letter <b>A</b>.")),
                    (lambda x: x == 'B', lambda: QLabel("Recognized letter <b>B</b>.")),
                    (lambda x: x == 'C', lambda: QLabel("Recognized letter <b>C</b>.")),
                    (lambda x: x == 'D', lambda: QLabel("Recognized letter <b>D</b>."))],
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

