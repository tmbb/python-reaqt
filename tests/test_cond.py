"""
ReaQt example: Reactive Match
"""

from qtpy.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout # pylint: disable=E0611

from reaqt.widgets import RxLineEdit, RxCond
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

        is_empty = self.state['text'].map(lambda x: x == '')
        is_A = self.state['text'].map(lambda x: x == 'A')
        is_B = self.state['text'].map(lambda x: x == 'B')
        is_C = self.state['text'].map(lambda x: x == 'C')
        is_D = self.state['text'].map(lambda x: x == 'D')
        is_none_of_the_above = is_empty.zip(is_A, is_B, is_C, is_D,
                                            lambda empty, a, b, c, d: not (empty or a or b or c or d))
        is_none_of_the_above.subscribe(lambda v: print('none_if_the_above:', v))
        is_empty.subscribe(lambda v: print('is_empty:', v))

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Recognized letters: A, B, C, D"))
        layout.addWidget(lineEdit)
        layout.addWidget(
            RxCond(
                branches=[
                    (is_empty, lambda: QLabel("No input.")),
                    (is_A, lambda: QLabel("Recognized letter <b>A</b>.")),
                    (is_B, lambda: QLabel("Recognized letter <b>B</b>.")),
                    (is_C, lambda: QLabel("Recognized letter <b>C</b>.")),
                    (is_D, lambda: QLabel("Recognized letter <b>D</b>.")),
                    (is_none_of_the_above, lambda: QLabel("Character not recognized."))]))
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

