from lib.GraphEngine import GraphEngine
import numpy as np

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

        for engine in self.input_engines:
            self.filter['magnitude'] = np.array(self.filter['magnitude']) + np.array(engine.filter['magnitude'])
            self.filter['phase'] = np.array(self.filter['phase']) + np.array(engine.filter['phase'])

        self.wrap_phase()
        self.remove_phase_discontinuities()

    def generate_title(self) -> str:
        return "Sum of the inputs"

    def add_engine(self, engine: GraphEngine) -> None:
        self.input_engines.append(engine)

    def remove_last_engine(self) -> None:
        del self.input_engines[-1]