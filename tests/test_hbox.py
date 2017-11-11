"""
ReaQt example: Reactive Horizontal Box
"""

from qtpy.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout # pylint: disable=E0611

from reaqt.widgets import RxHBox, RxPushButton
from reaqt.state import RxList

class MyWidget(QWidget):
    """ReaQt example: Reactive Horizontal Box"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class Item(QLabel):
            """Item for the Reactive HBox"""

            def __init__(self, index, value):
                super().__init__("Item #{} is '{}' |".format(index, value))

        self.state = RxList([])

        appendButton = RxPushButton("self.state.append('X')")
        extendButton = RxPushButton("self.state.extend(['Y', 'Y', 'Y'])")
        insert0Button = RxPushButton("self.state.insert(0, 'Z')")
        insert3Button = RxPushButton("self.state.insert(3, 'W')")
        popButton = RxPushButton("self.state.pop()")
        reverseButton = RxPushButton("self.state.reverse()")
        sortButton = RxPushButton("self.state.sort()")
        clearButton = RxPushButton("self.state.clear()")

        appendButton.rx.clicked.subscribe(lambda _: self.state.append('X'))
        extendButton.rx.clicked.subscribe(lambda _: self.state.extend(['Y', 'Y', 'Y']))
        insert0Button.rx.clicked.subscribe(lambda _: self.state.insert(0, 'Z'))
        insert3Button.rx.clicked.subscribe(lambda _: self.state.insert(3, 'W'))
        popButton.rx.clicked.subscribe(lambda _: self.state.pop())
        reverseButton.rx.clicked.subscribe(lambda _: self.state.reverse())
        sortButton.rx.clicked.subscribe(lambda _: self.state.sort())
        clearButton.rx.clicked.subscribe(lambda _: self.state.clear())

        self.state.length.subscribe(lambda n: n == 0 and popButton.setDisabled(True))
        self.state.length.subscribe(lambda n: n != 0 and popButton.setEnabled(True))
        self.state.length.subscribe(lambda n: n < 3 and insert3Button.setDisabled(True))
        self.state.length.subscribe(lambda n: n >= 3 and insert3Button.setEnabled(True))

        layout = QVBoxLayout()
        layout.addWidget(QLabel("This list contains items."))
        layout.addWidget(RxHBox(self.state, Item))
        layout.addStretch(1)
        layout.addWidget(appendButton)
        layout.addWidget(extendButton)
        layout.addWidget(insert0Button)
        layout.addWidget(insert3Button)
        layout.addWidget(popButton)
        layout.addWidget(reverseButton)
        layout.addWidget(sortButton)
        layout.addWidget(clearButton)

        self.setLayout(layout)



def test_main():
    """Run the example"""
    import sys

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    widget = MyWidget()
    widget.state.extend(['A', 'B', 'C'])
    widget.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    test_main()

