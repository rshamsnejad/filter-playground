from lib.Engine.GraphEngine import GraphEngine
import numpy as np
from scipy.signal import sosfreqz

class CascadeEngine(GraphEngine):
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

    def compute_specific(self) -> None:
        """
        Compute the convolution of all the input cells
        """

        self.sos = list(self.input_engines[0].sos)

        for engine in self.input_engines[1:]:
            self.sos.extend(engine.sos)

        frequencies, magnitude = sosfreqz(self.sos, worN=self.frequency_points, fs=self.fs)

        mag_db = 20 * np.log10(abs(magnitude))
        phase_rad = np.angle(magnitude, deg=False)
        phase_deg = np.angle(magnitude, deg=True)

        self.filter = {
            "frequencies": frequencies,
            "magnitude": magnitude,
            "magnitude_db": mag_db,
            "phase_rad": phase_rad,
            "phase_deg": phase_deg
        }

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