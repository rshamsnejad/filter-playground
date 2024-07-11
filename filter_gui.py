from hashlib import file_digest
import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QGridLayout,
    QRadioButton,
    QLineEdit
)
from PyQt6.QtGui import (
    QIcon
)
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure
from scipy import signal
import numpy as np


def remove_phase_discontinuities(phase: list) -> list:
    """
    In a wrapped phase array, replaces the two points before and after
    each wrap with NaN. This is useful to prevent matplotlib from plotting
    vertical lines at the wrap locations

    Args:
        phase (list): phase points list

    Returns:
        list: input list with NaN before and after each wrap
    """

    # Get sign of each point
    # Negative  gives -1
    # Positive  gives 1
    # Zero      gives 0
    signs = np.sign(phase)

    # Split the list in adjacent pairs
    pairs = []
    for i in range(len(signs) - 1):
        pairs.append( (signs[i], signs[i + 1]) )

    # A pair of (-1, 1) indicates a wrap: find out the indexes of such pairs
    pairs_indexes = [index for index, element in enumerate(pairs) if element == (-1, 1) or element == (1, -1)]

    # Replace all points before the wraps with NaN
    phase_nan = phase.copy()
    phase_nan[pairs_indexes] = np.nan

    return phase_nan


class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__order = 4
        self.__cutoff = 165
        self.__type = 'highpass'

        self.setWindowTitle("Filter Playground")
        self.setWindowIcon(QIcon('arkamys.jpg'))

        self.__layout = QGridLayout()
        self.setLayout(self.__layout)

        self.init_type_rb()
        self.init_order_field()
        self.init_cutoff_field()
        self.init_graph()

        self.show()

    def init_type_rb(self):
        rb_highpass = QRadioButton("Highpass", self)
        rb_highpass.toggled.connect(self.handle_type)
        rb_lowpass = QRadioButton("Lowpass", self)
        rb_lowpass.toggled.connect(self.handle_type)

        self.__layout.addWidget(rb_highpass, 0, 0, 1, 1)
        self.__layout.addWidget(rb_lowpass, 1, 0, 1, 1)

    def init_order_field(self):
        field_order = QLineEdit(str(self.__order), self)
        field_order.placeholderText = "Order"
        field_order.maxLength = 3
        field_order.textChanged.connect(self.handle_order)

        self.__layout.addWidget(field_order, 0, 1, 1, 1)

    def init_cutoff_field(self):
        field_cutoff = QLineEdit(str(self.__cutoff), self)
        field_cutoff.placeholderText = "Cutoff"
        field_cutoff.maxLength = 5
        field_cutoff.textChanged.connect(self.handle_cutoff)

        self.__layout.addWidget(field_cutoff, 1, 1, 1, 1)

    def init_graph(self):
        self.__canvas = FigureCanvas(Figure())
        self.__layout.addWidget(self.__canvas, 3, 0, 1, -1)


        plot_freq_range     = [20, 20e3]
        plot_mag_range      = [-40, 10]
        plot_phase_range    = [-200, 200]

        self.__fig = self.__canvas.figure
        self.__axs = self.__fig.subplots(2, 1, sharex=True)

        self.update_title()
        self.compute_filter()

        # Magnitude
        self.__mag, = self.__axs[0].semilogx(self.__filter['frequencies'], self.__filter['magnitude'])
        self.__axs[0].set_xscale('log')
        self.__axs[0].set_xlim(plot_freq_range)
        self.__axs[0].set_ylabel('Gain [dB]')
        self.__axs[0].set_ylim(plot_mag_range)
        self.__axs[0].margins(0, 0.1)
        self.__axs[0].grid(which='both', axis='both')
        self.__axline_mag = self.__axs[0].axvline(self.__cutoff, color='red')

        # Phase
        self.__phase, = self.__axs[1].semilogx(self.__filter['frequencies'], self.__filter['phase'])
        self.__axs[1].set_xlabel('Frequency [Hz]')
        self.__axs[1].set_xscale('log')
        self.__axs[1].set_xlim(plot_freq_range)
        self.__axs[1].set_ylabel('Phase [°]')
        self.__axs[1].set_ylim(plot_phase_range)
        self.__axs[1].margins(0, 0.1)
        self.__axs[1].grid(which='both', axis='both')
        self.__axline_phase = self.__axs[1].axvline(self.__cutoff, color='red')

    def compute_filter(self):
        b, a = signal.butter(self.__order, self.__cutoff, self.__type, True)
        frequencies, magnitude = signal.freqs(b, a, worN=np.logspace(0, 5, 1000))

        mag_db = 20 * np.log10(abs(magnitude))
        phase_deg = np.angle(magnitude, deg=True)
        phase_deg_nan = remove_phase_discontinuities(phase_deg)

        self.__filter = {
            "frequencies": frequencies,
            "magnitude": mag_db,
            "phase": phase_deg_nan
        }

    def handle_type(self):
        rb = self.sender()

        self.__type = rb.text()

        self.update_filter()

    def handle_order(self):
        rb = self.sender()

        self.__order = int(rb.text() or 1)

        self.update_filter()

    def handle_cutoff(self):
        rb = self.sender()

        self.__cutoff = int(rb.text() or 1000)

        self.update_filter()

    def update_title(self):
        self.__fig.suptitle(f"Butterworth {self.__type.lower()} filter, order {self.__order}, $f_0 = {self.__cutoff}$ Hz")

    def update_filter(self):
        self.compute_filter()

        self.update_title()

        self.__mag.set_data(self.__filter['frequencies'], self.__filter['magnitude'])
        self.__phase.set_data(self.__filter['frequencies'], self.__filter['phase'])

        self.__axline_mag.set_xdata([self.__cutoff])
        self.__axline_phase.set_xdata([self.__cutoff])

        self.__mag.figure.canvas.draw()
        self.__phase.figure.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()

    sys.exit(app.exec())