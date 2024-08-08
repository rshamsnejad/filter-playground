from locale import locale_alias
from re import LOCALE
from PyQt6.QtWidgets import (
    QGroupBox,
    QGridLayout,
    QLabel,
    QSpinBox,
    QDoubleSpinBox
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
        *args, **kwargs
    ) -> None:
        """
        Args:
            order (int): The default filter order
            frequency (int): The default filter frequency
            gain (float): The default filter gain
            Q (float): The default filter quality factor
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

        label_passband_ripple = QLabel("Max. passband ripple:")
        self.field_passband_ripple = QDoubleSpinBox()
        self.field_passband_ripple.setLocale(locale)
        self.field_passband_ripple.setMinimum(0)
        self.field_passband_ripple.setMaximum(100)
        self.field_passband_ripple.setValue(passband_ripple)
        self.field_passband_ripple.setFixedWidth(spinbox_width)
        self.field_passband_ripple.setAccelerated(True)

        self.layout().addWidget(label_passband_ripple, 4, 0, 1, 1)
        self.layout().addWidget(self.field_passband_ripple, 4, 1, 1, 1)

        label_stopband_attenuation = QLabel("Min. stopband attenuation:")
        self.field_stopband_attenuation = QDoubleSpinBox()
        self.field_stopband_attenuation.setLocale(locale)
        self.field_stopband_attenuation.setMinimum(0)
        self.field_stopband_attenuation.setMaximum(100)
        self.field_stopband_attenuation.setValue(stopband_attenuation)
        self.field_stopband_attenuation.setFixedWidth(spinbox_width)
        self.field_stopband_attenuation.setAccelerated(True)

        self.layout().addWidget(label_stopband_attenuation, 5, 0, 1, 1)
        self.layout().addWidget(self.field_stopband_attenuation, 5, 1, 1, 1)
