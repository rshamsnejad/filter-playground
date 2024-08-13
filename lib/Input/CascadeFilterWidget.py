from lib.Engine.CascadeEngine import CascadeEngine
from lib.Input.InputFilterWidget import InputFilterWidget
from lib.Graph.ThreeTabWidget import ThreeTabWidget

class CascadeFilterWidget(ThreeTabWidget):
    """
    Qt widget for the input filters
    """

    def __init__(self,
        input_filters: InputFilterWidget,
        engine: CascadeEngine,
        *args, **kwargs
    ) -> None:

        super().__init__(*args, **kwargs)

        self.input_filters = input_filters
        self.engine = engine
        self.cascade_toolbar = self.first_tab_widget

        self.engine.set_input_engines([filter.engine for filter in self.input_filters])

        self.bode_graph.set_engine(self.engine)
        self.polezero_graph.set_engine(self.engine)

        self.cascade_toolbar.field_gain.valueChanged.connect(self.handle_gain)
        self.cascade_toolbar.field_flip_phase.stateChanged.connect(self.handle_flip_phase)
