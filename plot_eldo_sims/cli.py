import click
import matplotlib.pyplot as plt

from matplotlib.ticker import EngFormatter


@click.command()
@click.argument("input", type=click.File("r"))
def cli(input):
    tran_flag = False
    dc_flag = False
    all_traces = {
        "tran": {"V": {"unit": "V", "traces": []}, "I": {"unit": "A", "traces": []}},
        "dc": {"V": {"unit": "V", "traces": []}, "I": {"unit": "A", "traces": []}}
    }

    for line in input.readlines():
        if "TRANSIENT ANALYSIS" in line:
            tran_flag = True
            dc_flag = False
            data_flag = False
            print_legends = {}
            continue

        elif "DC TRANSFER CURVES" in line:
            tran_flag = False
            dc_flag = True
            data_flag = False
            print_legends = {}

        if tran_flag:
            if "Print_Legend" in line:
                legend = line.split()[-1]
                header_name = line.split()[1][:-1]
                print_legends[header_name] = legend

            elif "TIME" in line:
                headers = [print_legends.get(header, header) for header in line.split()]
                trace = {header: [] for header in headers}

                data_flag = True
                counter = 0

            elif data_flag and counter < 2:
                counter += 1

            elif data_flag and counter == 2:
                if "Y" in line:
                    tran_flag = False
                    trace_type = headers[-1][0]
                    all_traces["tran"][trace_type]["traces"].append(trace)
                else:
                    values = line.split()
                    for header, value in zip(headers, values):
                        trace[header].append(float(value))

        elif dc_flag:
            if "Print_Legend" in line:
                legend = line.split()[-1]
                header_name = line.split()[1][:-1]
                print_legends[header_name] = legend

            elif "PARAM" in line:
                headers = [print_legends.get(header, header) for header in line.split()]
                trace = {header: [] for header in headers}

                data_flag = True
                counter = 0

            elif data_flag and counter < 2:
                counter += 1

            elif data_flag and counter == 2:
                if "Y" in line:
                    dc_flag = False
                    trace_type = headers[-1][0]
                    all_traces["dc"][trace_type]["traces"].append(trace)
                else:
                    values = line.split()
                    for header, value in zip(headers, values):
                        trace[header].append(float(value))

    print(all_traces)

    if all_traces["tran"]:
        # transient simulations plot
        for label, plot in all_traces["tran"].items():
            if not plot["traces"]:
                continue

            fig, ax = plt.subplots()
            for trace in plot["traces"]:
                signals = [key for key in trace.keys() if key != "TIME"]

                for signal in signals:
                    ax.plot(trace["TIME"], trace[signal], label=signal[2:-1])

                plt.ylabel(f"{label} ({plot['unit']})")
                plt.xlabel("Time (s)")
                ax.xaxis.set_major_formatter(EngFormatter(unit="s"))
                ax.yaxis.set_major_formatter(EngFormatter(unit=plot["unit"]))
                plt.title("Transient simulation")
                ax.grid(True, which="major")
                ax.grid(True, which="minor", linestyle=":")
                ax.minorticks_on()
                ax.legend()

    if all_traces["dc"]:
        # dc sweep simulations plot
        for label, plot in all_traces["dc"].items():
            if not plot["traces"]:
                continue

            fig, ax = plt.subplots()
            for trace in plot["traces"]:
                signals = [key for key in trace.keys() if key != "PARAM"]

                for signal in signals:
                    ax.plot(trace["PARAM"], trace[signal], label=signal[2:-1])

                plt.ylabel(f"{label} ({plot['unit']})")
                ax.xaxis.set_major_formatter(EngFormatter())
                ax.yaxis.set_major_formatter(EngFormatter(unit=plot["unit"]))
                plt.title("DC sweep simulation")
                ax.grid(True, which="major")
                ax.grid(True, which="minor", linestyle=":")
                ax.minorticks_on()
                ax.legend()

        plt.show()


if __name__ == "__main__":
    cli()
