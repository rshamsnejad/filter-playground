from lib.Engine.GraphEngine import GraphEngine
import numpy as np

class SumEngine(GraphEngine):
    """
    Child class to compute the output sum
    """

    def __init__(self, *args, **kwargs) -> None:

        super().__init__(*args, **kwargs)

    def set_input_engines(self,
        input_engines: list[GraphEngine]
    ) -> None:
        """
        Args:
            input_engines (list[GraphEngine]):
                List of references to the input cell's engines
        """

        self.input_engines = input_engines

    def compute_specific(self) -> None:
        """
        Compute the sum of all the input cells
        """

        frequencies = self.input_engines[0].get_frequencies()
        magnitude = np.array(self.input_engines[0].get_magnitude().copy())

        for engine in self.input_engines[1:]:
            magnitude += np.array(engine.get_magnitude())

        mag_lin = np.abs(magnitude)
        mag_db = 20 * np.log10(mag_lin)
        phase_rad = np.angle(magnitude, deg=False)
        phase_deg = np.angle(magnitude, deg=True)

        self.filter = {
            "frequencies": frequencies,
            "magnitude": magnitude,
            "magnitude_lin": mag_lin,
            "magnitude_db": mag_db,
            "phase_rad": phase_rad,
            "phase_deg": phase_deg
        }

    def generate_title(self) -> str:
        """
        Create a string to display as graph title.
        """

        return "Linear sum of the input cascades"

    def add_engine(self, engine: GraphEngine) -> None:
        """
        Add an engine to the internal list
        """

        self.input_engines.append(engine)

    def remove_last_engine(self) -> None:
        """
        Remove the last input engine in the list
        """

        del self.input_engines[-1]

    def generate_zpk(self) -> None:
        """
        Does nothing until I figure out how to do it
        """

        self.z = []
        self.p = []
        self.k = []