import click
import matplotlib.pyplot as plt

from matplotlib.ticker import EngFormatter

import re


SIM_HEADERS = {
    "TRANSIENT ANALYSIS": "tran",
    "DC TRANSFER CURVES": "dc",
    "AC ANALYSIS": "ac",
}


@click.command()
@click.argument("input", type=click.File("r"))
def cli(input):
    sim_flag = False
    sim_results = {
        "tran": {"V": {"unit": "V", "plots": []}, "I": {"unit": "A", "plots": []}},
        "dc": {"V": {"unit": "V", "plots": []}, "I": {"unit": "A", "plots": []}},
        "ac": {"Mag": {"unit": "db", "plots": []}, "Phase": {"unit": "°", "plots": []}},
    }

    all_lines = input.readlines()

    for index, line in enumerate(all_lines):
        if any(sim_header in line for sim_header in SIM_HEADERS):
            sim_flag = True
            sim_type = [
                sim_type
                for sim_header, sim_type in SIM_HEADERS.items()
                if sim_header in line
            ][0]
            data_flag = False
            print_legends = {}
            continue

        if sim_flag:
            if line.startswith("Print_Legend"):
                # Gather all the print legends
                legend_regex = r"Print_Legend (\d+): (\w+\(\w+(?:\.\w+)?\))"
                header_name, legend = re.findall(legend_regex, line)[0]
                print_legends[header_name] = legend

            elif "X" in line:
                headers = [
                    print_legends.get(header, header)
                    for header in all_lines[index - 1].split()
                ]
                traces = {header: [] for header in headers}
                data_flag = True

            elif data_flag and "Y" not in line:
                values = line.split()
                for header, value in zip(headers, values):
                    traces[header].append(float(value))

            elif data_flag:
                sim_flag = False
                data_flag = False
                if sim_type == "ac":
                    trace_type = headers[-1].split("(")[0][1:]
                    if trace_type == "DB":
                        trace_type = "Mag"
                    elif trace_type == "P":
                        trace_type = "Phase"
                else:
                    trace_type = headers[-1][0]  # tran
                sim_results[sim_type][trace_type]["plots"].append({"traces": traces})

    print(sim_results)

    tran_results = {
        label: plot_type
        for label, plot_type in sim_results["tran"].items()
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

    dc_results = {
        label: plot_type
        for label, plot_type in sim_results["dc"].items()
        if plot_type["plots"]
    }

    for label, plot_type in dc_results.items():
        for plot in plot_type["plots"]:
            fig, ax = plt.subplots()

            x_header = [header for header in plot["traces"].keys() if "(" not in header][0]
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

    ac_results = {
        label: plot_type
        for label, plot_type in sim_results["ac"].items()
        if plot_type["plots"]
    }

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
