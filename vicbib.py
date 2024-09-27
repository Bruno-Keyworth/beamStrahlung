from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt


class BasePlotter:
    """
    Provides basic plotting functionalities
    """

    def set_save_path(self):
        self.save_path = Path.home() / "promotion/code/beamStrahlung/plots/"

    def set_params(self) -> None:
        """
        sets basic plot settings
        """
        self.params = {
            "xtick.direction": "in",
            "ytick.direction": "in",
            "xtick.top": True,
            "ytick.right": True,
            "legend.fontsize": self.labelsize,  # "x-large",
            "axes.labelsize": self.labelsize,  # "x-large",
            "axes.titlesize": self.labelsize,  # "x-large",
            "xtick.labelsize": self.labelsize,  # "x-large",
            "ytick.labelsize": self.labelsize,  # "x-large",
            "figure.autolayout": True,
        }  #'figure.figsize': (15, 5),
        mpl.rcParams.update(self.params)
        # mpl.style.use("seaborn-colorblind")

    def __init__(self, save=False, fig_name=None) -> None:
        self.save = save
        self.dpi = 251
        self.fig_name = fig_name
        self.labelsize = 16
        self.set_params()
        self.set_save_path()

    @staticmethod
    def plot():
        fig, ax = (
            plt.subplots()
        )  # layout="constrained" figsize=(5, 6), ,constrained_layout=False
        ax.grid(linestyle=(0, (5, 10)), linewidth=0.5)
        return fig, ax

    def finish(self) -> None:
        """
        sets tight_layout and saves fig or shows
        """
        # plt.tight_layout()
        # plt.tight_layout()
        if self.save:
            plt.savefig(
                Path(self.save_path) / self.fig_name, dpi=self.dpi
            )  # , format="pdf"
        else:
            plt.show()


class BaseLogPlotter(BasePlotter):
    @staticmethod
    def doubleLogPlot():
        fig, ax = BasePlotter.plot()
        ax.set_xscale("log")
        ax.set_yscale("log")
        return fig, ax

    @staticmethod
    def xLogPlot():
        fig, ax = BasePlotter.plot()
        ax.set_xscale("log")
        return fig, ax

    @staticmethod
    def yLogPlot():
        fig, ax = BasePlotter.plot()
        ax.set_yscale("log")
        return fig, ax


def main():
    raise Exception("vicbib is not designed to be executed as __main__")


if __name__ == "__main__":
    main()
