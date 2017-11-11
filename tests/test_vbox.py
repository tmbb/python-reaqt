from qtpy.QtWidgets import QApplication, QGridLayout, QWidget, QLabel, QVBoxLayout

from reaqt.widgets import RxVBox, RxLineEdit, RxPushButton
from reaqt.common import connect
from reaqt.state import RxList

class MyWidget(QWidget):
    """ReaQt example: Reactive Horizontal Box"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class Item(QLabel):

            def __init__(self, index, value):
                super().__init__("Item #{} is '{}'.".format(index, value))

        # State for our Widget: an initially empty reactive list
        self.state = RxList([])

        # Buttons that will serve as the user interface to manipulate the state
        # Each button calls a certain (destructive) list method with certain arguments.
        appendButton = RxPushButton("self.state.append('X')")
        extendButton = RxPushButton("self.state.extend(['Y', 'Y', 'Y'])")
        insert0Button = RxPushButton("self.state.insert(0, 'Z')")
        insert3Button = RxPushButton("self.state.insert(3, 'W')")
        popButton = RxPushButton("self.state.pop()")
        reverseButton = RxPushButton("self.state.reverse()")
        sortButton = RxPushButton("self.state.sort()")
        clearButton = RxPushButton("self.state.clear()")

        # Connect the buttons to events that modify the state.
        # If you want to decouple state manegemen from the UI, it's easy.
        # Just define a monolitic state store and pass parts of it into the Widgets.
        appendButton.rx.clicked.subscribe(lambda _: self.state.append('X'))
        extendButton.rx.clicked.subscribe(lambda _: self.state.extend(['Y', 'Y', 'Y']))
        insert0Button.rx.clicked.subscribe(lambda _: self.state.insert(0, 'Z'))
        insert3Button.rx.clicked.subscribe(lambda _: self.state.insert(3, 'W'))
        popButton.rx.clicked.subscribe(lambda _: self.state.pop())
        reverseButton.rx.clicked.subscribe(lambda _: self.state.reverse())
        sortButton.rx.clicked.subscribe(lambda _: self.state.sort())
        clearButton.rx.clicked.subscribe(lambda _: self.state.clear())

        # Disable some buttons depending on the state.
        # The `.length` of an RxList is an event source which we can subscribe.
        # We disable some buttons based on the length.
        # (we don't want to `.pop` items from an empty list)
        self.state.length.subscribe(lambda n: n == 0 and popButton.setDisabled(True))
        self.state.length.subscribe(lambda n: n != 0 and popButton.setEnabled(True))
        self.state.length.subscribe(lambda n: n < 3 and insert3Button.setDisabled(True))
        self.state.length.subscribe(lambda n: n >= 3 and insert3Button.setEnabled(True))

        # Build the Widget layout
        layout = QVBoxLayout()
        layout.addWidget(QLabel("This list contains items."))
        layout.addWidget(RxVBox(self.state, Item))
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
    import sys

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    widget = MyWidget()
    widget.state.extend(['A', 'B', 'C'])
    widget.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    test_main()

