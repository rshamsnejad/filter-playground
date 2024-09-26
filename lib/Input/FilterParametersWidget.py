from PyQt6.QtWidgets import (
    QGroupBox,
    QGridLayout,
    QLabel,
    QSpinBox,
    QDoubleSpinBox,
    QCheckBox,
    QSpacerItem,
    QSizePolicy
)
from PyQt6.QtCore import QLocale

class FilterParametersWidget(QGroupBox):
    """
    Qt widget for the filter parameter fields
    """

    def __init__(self,
        order: int,
        frequency: int,
        gain: float,
        Q: float,
        passband_ripple: float,
        stopband_attenuation: float,
        transband_width: int,
        *args, **kwargs
    ) -> None:
        """
        Args:
            order (int): The default filter order
            frequency (int): The default filter frequency
            gain (float): The default filter gain
            Q (float): The default filter quality factor
            passband_ripple (float): The default passband ripple
            stopband_attenuation (float): The default stopband attenuation
            transband_width (int): The default transition band width
        """

        super().__init__(*args, **kwargs)

        self.setTitle("Filter parameters")
        self.setLayout(QGridLayout())

        spinbox_width = 60
        locale = QLocale("en_US")

        label_order = QLabel("Filter order:")
        self.field_order = QSpinBox()
        self.field_order.setMinimum(1)
        self.field_order.setMaximum(100)
        self.field_order.setValue(order)
        self.field_order.setFixedWidth(spinbox_width)
        self.field_order.setAccelerated(True)

        self.layout().addWidget(label_order, 0, 0, 1, 1)
        self.layout().addWidget(self.field_order, 0, 1, 1, 1)

        label_frequency = QLabel("Frequency (Hz):")
        self.field_frequency = QSpinBox()
        self.field_frequency.setMinimum(1)
        self.field_frequency.setMaximum(100000)
        self.field_frequency.setValue(frequency)
        self.field_frequency.setFixedWidth(spinbox_width)
        self.field_frequency.setAccelerated(True)

        self.layout().addWidget(label_frequency, 1, 0, 1, 1)
        self.layout().addWidget(self.field_frequency, 1, 1, 1, 1)

        label_gain = QLabel("Gain (dB):")
        self.field_gain = QDoubleSpinBox()
        self.field_gain.setLocale(locale)
        self.field_gain.setMinimum(-100)
        self.field_gain.setMaximum(100)
        self.field_gain.setValue(gain)
        self.field_gain.setFixedWidth(spinbox_width)
        self.field_gain.setAccelerated(True)

        self.layout().addWidget(label_gain, 2, 0, 1, 1)
        self.layout().addWidget(self.field_gain, 2, 1, 1, 1)

        label_Q = QLabel("Q:")
        self.field_Q = QDoubleSpinBox()
        self.field_Q.setLocale(locale)
        self.field_Q.setMinimum(0)
        self.field_Q.setMaximum(100)
        self.field_Q.setValue(Q)
        self.field_Q.setFixedWidth(spinbox_width)
        self.field_Q.setAccelerated(True)

        self.layout().addWidget(label_Q, 3, 0, 1, 1)
        self.layout().addWidget(self.field_Q, 3, 1, 1, 1)

        label_passband_ripple = QLabel("Max. passband ripple (dB):")
        self.field_passband_ripple = QDoubleSpinBox()
        self.field_passband_ripple.setLocale(locale)
        self.field_passband_ripple.setMinimum(0)
        self.field_passband_ripple.setMaximum(100)
        self.field_passband_ripple.setValue(passband_ripple)
        self.field_passband_ripple.setFixedWidth(spinbox_width)
        self.field_passband_ripple.setAccelerated(True)

        self.layout().addWidget(label_passband_ripple, 0, 2, 1, 1)
        self.layout().addWidget(self.field_passband_ripple, 0, 3, 1, 1)

        label_stopband_attenuation = QLabel("Min. stopband attenuation (dB):")
        self.field_stopband_attenuation = QDoubleSpinBox()
        self.field_stopband_attenuation.setLocale(locale)
        self.field_stopband_attenuation.setMinimum(0)
        self.field_stopband_attenuation.setMaximum(100)
        self.field_stopband_attenuation.setValue(stopband_attenuation)
        self.field_stopband_attenuation.setFixedWidth(spinbox_width)
        self.field_stopband_attenuation.setAccelerated(True)

        self.layout().addWidget(label_stopband_attenuation, 1, 2, 1, 1)
        self.layout().addWidget(self.field_stopband_attenuation, 1, 3, 1, 1)

        label_transband_width = QLabel("Transition band width (Hz):")
        self.field_transband_width = QSpinBox()
        self.field_transband_width.setMinimum(1)
        self.field_transband_width.setMaximum(1000)
        self.field_transband_width.setValue(transband_width)
        self.field_transband_width.setFixedWidth(spinbox_width)
        self.field_transband_width.setAccelerated(True)

        self.layout().addWidget(label_transband_width, 2, 2, 1, 1)
        self.layout().addWidget(self.field_transband_width, 2, 3, 1, 1)

        label_flip_phase = QLabel("Flip phase:")
        self.field_flip_phase = QCheckBox()
        self.field_flip_phase.setChecked(False)

        self.layout().addWidget(label_flip_phase, 3, 2, 1, 1)
        self.layout().addWidget(self.field_flip_phase, 3, 3, 1, 1)

        label_delay_samples = QLabel("Delay (samples):")
        self.field_delay_samples = QSpinBox()
        self.field_delay_samples.setMinimum(0)
        self.field_delay_samples.setValue(0)
        self.field_delay_samples.setFixedWidth(spinbox_width)
        self.field_delay_samples.setAccelerated(True)

        self.layout().addWidget(label_delay_samples, 4, 0, 1, 1)
        self.layout().addWidget(self.field_delay_samples, 4, 1, 1, 1)

        label_delay_msec = QLabel("Delay (ms):")
        self.field_delay_msec = QDoubleSpinBox()
        self.field_delay_msec.setLocale(locale)
        self.field_delay_msec.setMinimum(0)
        self.field_delay_msec.setMaximum(2147483647)
        self.field_delay_msec.setDecimals(4)
        self.field_delay_msec.setValue(0)
        self.field_delay_msec.setFixedWidth(spinbox_width)
        self.field_delay_msec.setAccelerated(True)

        self.layout().addWidget(label_delay_msec, 4, 2, 1, 1)
        self.layout().addWidget(self.field_delay_msec, 4, 3, 1, 1)

        self.layout().addItem(
            QSpacerItem(1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding),
            5, 3, 1, 1
        )