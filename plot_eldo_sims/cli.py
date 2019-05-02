import click
import matplotlib.pyplot as plt

from matplotlib.ticker import EngFormatter


@click.command()
@click.argument("input", type=click.File("r"))
def cli(input):
    tran_flag = False
    all_traces = []

    for line in input.readlines():
        if "TRANSIENT ANALYSIS" in line:
            tran_flag = True
            data_flag = False
            print_legends = {}
            continue

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
                    all_traces.append(trace)
                else:
                    values = line.split()
                    for header, value in zip(headers, values):
                        trace[header].append(float(value))

    print(all_traces)

    # transient simulations plot
    tran_traces = [trace for trace in all_traces if "TIME" in trace.keys()]

    v_tran_traces = []
    i_tran_traces = []
    for trace in tran_traces:
        for key in trace.keys():
            if "V(" in key:
                v_tran_traces.append(trace)
                break
            elif "I(" in key:
                i_tran_traces.append(trace)
                break

    tran_plots = [
        {
            "traces": v_tran_traces,
            "label": "V (V)",
            "y_axis_formatter": EngFormatter(unit="V"),
        },
        {
            "traces": i_tran_traces,
            "label": "I (A)",
            "y_axis_formatter": EngFormatter(unit="A"),
        },
    ]
    for plot in tran_plots:
        if not plot["traces"]:
            continue

        fig, ax = plt.subplots()
        for trace in plot["traces"]:
            signals = [key for key in trace.keys() if key != "TIME"]

            for signal in signals:
                ax.plot(trace["TIME"], trace[signal], label=signal[2:-1])

            plt.ylabel(plot["label"])
            plt.xlabel("Time (s)")
            ax.xaxis.set_major_formatter(EngFormatter(unit="s"))
            ax.yaxis.set_major_formatter(plot["y_axis_formatter"])
            plt.title("Transient simulation")
            ax.grid(True, which="major")
            ax.grid(True, which="minor", linestyle=":")
            ax.minorticks_on()
            ax.legend()

    plt.legend()
    plt.show()


if __name__ == "__main__":
    cli()
