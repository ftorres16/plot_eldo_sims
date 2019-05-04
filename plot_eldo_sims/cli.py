import click
import matplotlib.pyplot as plt

from matplotlib.ticker import EngFormatter


@click.command()
@click.argument("input", type=click.File("r"))
def cli(input):
    tran_flag = False
    dc_flag = False
    ac_flag = False
    sim_results = {
        "tran": {"V": {"unit": "V", "plots": []}, "I": {"unit": "A", "plots": []}},
        "dc": {"V": {"unit": "V", "plots": []}, "I": {"unit": "A", "plots": []}},
        "ac": {"Mag": {"unit": "db", "plots": []}, "Phase": {"unit": "°", "plots": []}},
    }

    for line in input.readlines():
        if "TRANSIENT ANALYSIS" in line:
            tran_flag = True
            dc_flag = False
            ac_flag = False
            data_flag = False
            print_legends = {}
            continue

        elif "DC TRANSFER CURVES" in line:
            tran_flag = False
            dc_flag = True
            ac_flag = False
            data_flag = False
            print_legends = {}

        elif "AC ANALYSIS" in line:
            tran_flag = False
            dc_flag = False
            ac_flag = True
            data_flag = False
            print_legends = {}

        if tran_flag:
            if "Print_Legend" in line:
                legend = line.split()[-1]
                header_name = line.split()[1][:-1]
                print_legends[header_name] = legend

            elif "TIME" in line:
                headers = [print_legends.get(header, header) for header in line.split()]
                traces = {header: [] for header in headers}

                data_flag = True
                counter = 0

            elif data_flag and counter < 2:
                counter += 1

            elif data_flag and counter == 2:
                if "Y" in line:
                    tran_flag = False
                    trace_type = headers[-1][0]
                    sim_results["tran"][trace_type]["plots"].append({"traces": traces})
                else:
                    values = line.split()
                    for header, value in zip(headers, values):
                        traces[header].append(float(value))

        elif dc_flag:
            if "Print_Legend" in line:
                legend = line.split()[-1]
                header_name = line.split()[1][:-1]
                print_legends[header_name] = legend

            elif "PARAM" in line:
                headers = [print_legends.get(header, header) for header in line.split()]
                traces = {header: [] for header in headers}

                data_flag = True
                counter = 0

            elif data_flag and counter < 2:
                counter += 1

            elif data_flag and counter == 2:
                if "Y" in line:
                    dc_flag = False
                    trace_type = headers[-1][0]
                    sim_results["dc"][trace_type]["plots"].append({"traces": traces})
                else:
                    values = line.split()
                    for header, value in zip(headers, values):
                        traces[header].append(float(value))

        elif ac_flag:
            if "Print_Legend" in line:
                legend = line.split()[-1]
                header_name = line.split()[1][:-1]
                print_legends[header_name] = legend

            elif "HERTZ" in line:
                headers = [print_legends.get(header, header) for header in line.split()]
                traces = {header: [] for header in headers}

                data_flag = True
                counter = 0

            elif data_flag and counter < 2:
                counter += 1

            elif data_flag and counter == 2:
                if "Y" in line:
                    ac_flag = False
                    trace_type = headers[-1].split("(")[0][1:]
                    if trace_type == "DB":
                        trace_type = "Mag"
                    elif trace_type == "P":
                        trace_type = "Phase"

                    sim_results["ac"][trace_type]["plots"].append({"traces": traces})
                else:
                    values = line.split()
                    for header, value in zip(headers, values):
                        traces[header].append(float(value))

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

            param = plot["traces"]["PARAM"]
            signals = [signal for signal in plot["traces"].items() if signal[0] != "PARAM"]

            for signal_name, signal_values in signals:
                ax.plot(param, signal_values, label=signal_name[2:-1])

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
