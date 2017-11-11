from qtpy.QtWidgets import QApplication, QGridLayout, QWidget, QLabel

from reaqt.widgets import RxLabel, RxLineEdit, RxPushButton
from reaqt.common import connect
from reaqt.state import RxMap

class MyWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # The state of the widget is a reactive map (RxMap)
        # containing only a single key.
        # There is nothing special about the `self.state` attribute.
        # You can give it any name you want, and you don't even need to
        # make it an attribute. It could be a normal variable.
        # Making it an attribute allows you to refer to it from outside the
        # `__init__()` method, which is usually desirable
        self.state = RxMap({"name": ""})

        # Define a reactive text box to enter the name
        # The text box is not realtime. The value of the state will only be
        # updated when the box loses focus.
        name_input = RxLineEdit(realtime=False)
        # Define a reactive label widget to display the name
        name_display = RxLabel()

        # Connect the text box to the reactive map.
        # Each time the text box is updated, the map will be updated
        connect(self.state["name"], name_input.rx.text)
        # When the reactive map is changed, we want to change the display text.
        # We susbcribe the self.state["name"] to the controller of the `text` port
        # of the `name_display` widget.
        self.state["name"].subscribe(name_display.rx.text)
        # Note that after connecting the reactive map to the reactive widgets,
        # (using the `connect()` function or the `Observable.subscribe()` method,
        # we manipulate the state directly, and the widgets are automatically updated
        # according to the state changes.

        debug_button = RxPushButton("&Debug")
        # Cause the debug button to print the state to the console
        # using the default RxMap.debug() method.
        # To do this, we subscribe the reactive value to a function.
        # We can also subscribe to an Observer or to a Subject.
        debug_button.rx.clicked.subscribe(lambda x: self.state.debug())

        # Arrange the widgets in a grid layout.
        # This is ordinary Qt programming and has nothing to do with ReaQt.
        # Reactive layouts are possible, but they're not shown here.
        grid = QGridLayout()
        grid.addWidget(QLabel("Input:"), 0, 0)
        grid.addWidget(name_input, 0, 1)
        grid.addWidget(QLabel("Display:"), 1, 0)
        grid.addWidget(name_display, 1, 1)
        grid.addWidget(debug_button, 2, 0, 1, 2)
        # Set the layout
        self.setLayout(grid)


def test_main():
    import sys

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    test_main()

