from lib.GraphEngine import GraphEngine
import numpy as np
from scipy.signal import freqz

class SumEngine(GraphEngine):
    def __init__(self,
        input_engines: list[GraphEngine],
        *args, **kwargs
    ) -> None:

        super().__init__(*args, **kwargs)

        self.input_engines = input_engines

    def compute(self) -> None:
        self.filter = {
            'frequencies': self.input_engines[0].filter['frequencies'],
            'magnitude': np.zeros(len(self.input_engines[0].filter['frequencies'])),
            'phase': np.zeros(len(self.input_engines[0].filter['frequencies']))
        }

        self.b = self.input_engines[0].b
        self.a = self.input_engines[0].a

        for engine in self.input_engines[1:]:
            self.b = np.convolve(self.b, engine.b)
            self.a = np.convolve(self.a, engine.a)

        frequencies, magnitude = freqz(self.b, self.a, worN=self.frequency_points, fs=self.fs)

        mag_db = 20 * np.log10(abs(magnitude))
        phase_deg = np.angle(magnitude, deg=True)

        self.filter = {
            "frequencies": frequencies,
            "magnitude": mag_db,
            "phase": phase_deg
        }

        self.wrap_phase()
        self.remove_phase_discontinuities()

    def generate_title(self) -> str:
        return "Sum of the inputs"

    def add_engine(self, engine: GraphEngine) -> None:
        self.input_engines.append(engine)

    def remove_last_engine(self) -> None:
        del self.input_engines[-1]