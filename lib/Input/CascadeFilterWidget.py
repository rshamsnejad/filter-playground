from lib.Engine.CascadeEngine import CascadeEngine
from lib.Input.InputFilterWidget import InputFilterWidget
from lib.Graph.ThreeTabWidget import ThreeTabWidget

class CascadeFilterWidget(ThreeTabWidget):
    """
    Qt widget for displaying the cascade of several input filters.
    """

    def __init__(self,
        input_filter_widgets: list[InputFilterWidget],
        engine: CascadeEngine,
        *args, **kwargs
    ) -> None:
        """
        Args:
            input_filter_widgets (list[InputFilterWidget]):
                The list of all the filter widgets to display in numbered tabs.
            engine (CascadeEngine):
                The engine to use for computation.
        """

        super().__init__(*args, **kwargs)

        self.input_filters = input_filter_widgets
        self.engine = engine
        self.cascade_toolbar = self.first_tab_widget

        self.engine.set_input_engines([filter.engine for filter in self.input_filters])

        self.bode_graph.set_engine(self.engine)
        self.polezero_graph.set_engine(self.engine)

        self.cascade_toolbar.field_gain.valueChanged.connect(self.handle_gain)
        self.cascade_toolbar.field_flip_phase.stateChanged.connect(self.handle_flip_phase)
