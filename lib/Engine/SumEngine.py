from lib.Engine.GraphEngine import GraphEngine
import numpy as np
from scipy.signal import sosfreqz

class SumEngine(GraphEngine):
    """
    Child class to compute the output convolution
    """

    def __init__(self,
        input_engines: list[GraphEngine],
        *args, **kwargs
    ) -> None:
        """
        Args:
            input_engines (list[GraphEngine]):
                List of references to the input cell's engines
        """

        super().__init__(*args, **kwargs)

        self.input_engines = input_engines

    def compute(self) -> None:
        """
        Compute the convolution of all the input cells
        """

        self.sos = list(self.input_engines[0].sos)

        for engine in self.input_engines[1:]:
            self.sos.extend(engine.sos)

        frequencies, magnitude = sosfreqz(self.sos, worN=self.frequency_points, fs=self.fs)

        mag_db = 20 * np.log10(abs(magnitude))
        phase_deg = np.angle(magnitude, deg=True)

        self.filter = {
            "frequencies": frequencies,
            "magnitude": mag_db,
            "phase_deg": phase_deg
        }

        self.remove_phase_discontinuities()
        self.wrap_phase()

        self.generate_zpk()

    def generate_title(self) -> str:
        """
        Create a string to display as graph title.
        """

        return "Cascading of the inputs"

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