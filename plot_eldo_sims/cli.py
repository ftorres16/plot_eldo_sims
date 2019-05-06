import json

import click
import matplotlib.pyplot as plt

from matplotlib.ticker import EngFormatter


SIM_HEADERS = {
    "TRANSIENT ANALYSIS": "tran",
    "DC TRANSFER CURVES": "dc",
    "AC ANALYSIS": "ac",
}


@click.command()
@click.argument("input", type=click.File("r"))
def cli(input):
    """
    Expected JSON format:

    {
        "tran": {"V": {"unit": "V", "plots": []}, "I": {"unit": "A", "plots": []}},
        "dc": {"V": {"unit": "V", "plots": []}, "I": {"unit": "A", "plots": []}},
        "ac": {"Mag": {"unit": "db", "plots": []}, "Phase": {"unit": "°", "plots": []}},
    }
    """
    sim_results = json.load(input)

    tran_results = {
        label: plot_type
        for label, plot_type in sim_results["tran"].items()
        if plot_type["plots"]
    }
    dc_results = {
        label: plot_type
        for label, plot_type in sim_results["dc"].items()
        if plot_type["plots"]
    }
    ac_results = {
        label: plot_type
        for label, plot_type in sim_results["ac"].items()
        if plot_type["plots"]
    }

    for label, plot_type in tran_results.items():
        for plot in plot_type["plots"]:
            fig, ax = plt.subplots()

            time = plot["traces"]["TIME"]
            signals = [
                signal for signal in plot["traces"].items() if signal[0] != "TIME"
            ]

            for signal_name, signal_values in signals:
                ax.plot(time, signal_values, label=signal_name[2:-1])

            plt.ylabel(f"{label} ({plot_type['unit']})")
            plt.xlabel("Time (s)")
            ax.xaxis.set_major_formatter(EngFormatter(unit="s"))
            ax.yaxis.set_major_formatter(EngFormatter(unit=plot_type["unit"]))
            plt.title("Transient simulation")
            ax.grid(True, which="major")
            ax.grid(True, which="minor", linestyle=":")
            ax.minorticks_on()
            ax.legend()

    for label, plot_type in dc_results.items():
        for plot in plot_type["plots"]:
            fig, ax = plt.subplots()

            x_header = [
                header for header in plot["traces"].keys() if "(" not in header
            ][0]
            param = plot["traces"][x_header]
            signals = [
                signal for signal in plot["traces"].items() if signal[0] != x_header
            ]

            for signal_name, signal_values in signals:
                ax.plot(param, signal_values, label=signal_name[2:-1])

            plt.xlabel(f"{x_header}")
            plt.ylabel(f"{label} ({plot_type['unit']})")
            ax.xaxis.set_major_formatter(EngFormatter())
            ax.yaxis.set_major_formatter(EngFormatter(unit=plot_type["unit"]))
            plt.title("DC sweep simulation")
            ax.grid(True, which="major")
            ax.grid(True, which="minor", linestyle=":")
            ax.minorticks_on()
            ax.legend()

    for label, plot_type in ac_results.items():
        for plot in plot_type["plots"]:
            fig, ax = plt.subplots()

            freq = plot["traces"]["HERTZ"]
            signals = [
                signal for signal in plot["traces"].items() if signal[0] != "HERTZ"
            ]

            for signal_name, signal_values in signals:
                label = (
                    signal_name.replace("(", " ")
                    .replace(")", " ")
                    .replace(",", "-")
                    .split()[-1]
                )
                ax.plot(freq, signal_values, label=label)

            plt.ylabel(f"{label} ({plot_type['unit']})")
            plt.xlabel("Freq (Hz)")
            ax.set_xscale("log")
            ax.xaxis.set_major_formatter(EngFormatter())
            plt.title("AC Analysis")
            ax.grid(True, which="major")
            ax.grid(True, which="minor", linestyle=":")
            ax.minorticks_on()
            ax.legend()

    plt.show()


if __name__ == "__main__":
    cli()
