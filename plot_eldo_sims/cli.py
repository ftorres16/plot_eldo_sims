import click
import matplotlib.pyplot as plt


@click.command()
@click.argument("input", type=click.File("r"))
def cli(input):
    plot_flag = False
    data_flag = False
    counter = 0

    all_traces = []

    for line in input.readlines():
        if "TRANSIENT ANALYSIS" in line:
            plot_flag = True
            counter = 0
            continue

        if plot_flag and counter < 5:
            counter += 1
            continue

        if plot_flag and counter == 5:
            headers = line.split()
            trace = {header: [] for header in headers}

            plot_flag = False
            data_flag = True
            counter = 0

        if data_flag and counter < 3:
            counter += 1
            continue

        if data_flag and counter == 3:
            if 'Y' in line:
                data_flag = False
                counter = 0
                all_traces.append(trace)
                continue
            else:
                values = line.split()
                for header, value in zip(headers, values):
                    trace[header].append(float(value))

    print(all_traces)

    for trace in all_traces:
        keys = list(trace.keys())
        if 'TIME' in keys:
            signals = [key for key in keys if key != 'TIME']
            for signal in signals:
                plt.plot(trace['TIME'], trace[signal], label=signal)
                plt.xlabel('TIME')
                plt.grid(True)

    plt.legend()
    plt.show()


if __name__ == "__main__":
    cli()
