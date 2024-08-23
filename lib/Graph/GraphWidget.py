from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from lib.Engine.GraphEngine import GraphEngine

class GraphWidget(QWidget):
    """
    Base class for displaying a matplotlib graph with toolbar.

    Must be inherited by a child class implementing the
    virtual method(s)
    """

    def __init__(self, *args, **kwargs) -> None:

        super().__init__(*args, **kwargs)

        self.setLayout(QVBoxLayout())

        self.canvas = FigureCanvasQTAgg(Figure())
        self.canvas.setMinimumHeight(250)

        self.figure = self.canvas.figure
        self.figure.set_tight_layout(True)

        self.layout().addWidget(NavigationToolbar(self.canvas))
        self.layout().addWidget(self.canvas)

    def set_engine(self, engine: GraphEngine) -> None:
        """
        Set the computing engine. Has to be done outside of constructor
        otherwise the input widget and the output widget are inter-dependent

        Args:
            engine (GraphEngine): The engine to use to compute the graph
        """

        self.set_engine_specific(engine)

        # self.engine.moveToThread(self.worker_thread)
        # self.worker_thread.started.connect(self.engine.compute)

        # self.compute_and_update()

    def set_engine_specific(self, engine: GraphEngine) -> None:

        raise NotImplementedError

    def update_graph(self) -> None:
        """
        Updates the graph with the data currently stored in the engine.
        Usually called after self.engine.compute()

        Must be implemented by child classes.
        """

        raise NotImplementedError

    def update_title(self) -> None:
        """
        Updates the graph title depending on the filter type
        """

        self.figure.suptitle(self.engine.generate_title())

    def compute_and_update(self) -> None:
        """
        Convenience method to wrap computing the filter
        and updating the graph in one go
        """

        self.engine.compute()
        self.update_graph()
