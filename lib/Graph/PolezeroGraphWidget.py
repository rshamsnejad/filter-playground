from lib.Graph.GraphWidget import GraphWidget
from lib.Engine.GraphEngine import GraphEngine

import matplotlib.patches as patch
from numpy import real, imag

class PolezeroGraphWidget(GraphWidget):
    """
    Base class for displaying a matplotlib graph with toolbar.

    Must be inherited by a child class implementing the
    virtual method(s)
    """

    def __init__(self, *args, **kwargs) -> None:

        super().__init__(*args, **kwargs)

        self.axs = self.figure.gca()

        self.init_graph()

    def set_engine(self, engine: GraphEngine) -> None:
        """
        Set the computing engine. Has to be done outside of constructor
        otherwise the input widget and the output widget are inter-dependent

        Args:
            engine (GraphEngine): The engine to use to compute the graph
        """

        self.engine = engine
        self.compute_and_update()

    def init_graph(self,
    ) -> None:
        """
        Prepares an empty graph to host filter data later on.
        """

        self.axs.grid(which='both', axis='both')
        self.axs.set_xlim(-1.5, 1.5)
        self.axs.set_xlabel("Real part")
        self.axs.set_ylim(-1.5, 1.5)
        self.axs.set_ylabel("Imaginary part")
        self.axs.add_patch(patch.Circle([0,0], radius=1, fill=False, linestyle='--'))
        
        self.scatter_zero = self.axs.plot([], [], '.b')
        self.scatter_pole = self.axs.plot([], [], 'xr')

    def update_graph(self) -> None:
        """
        Updates the graph with the data currently stored in the object.
        Usually called after self.engine.compute()
        """

        self.update_title()

        self.scatter_zero[0].set_data(real(self.engine.z), imag(self.engine.z))
        self.scatter_pole[0].set_data(real(self.engine.p), imag(self.engine.p))

        self.canvas.draw()
