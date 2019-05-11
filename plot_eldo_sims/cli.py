import json
import os

import click
import jsonschema
import matplotlib.pyplot as plt

from matplotlib.ticker import EngFormatter


SIM_HEADERS = {
    "TRANSIENT ANALYSIS": "tran",
    "DC TRANSFER CURVES": "dc",
    "AC ANALYSIS": "ac",
}

JSON_SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "jsonschema.json")


@click.command()
@click.argument("input", type=click.File("r"))
@click.option("--force_same_axes/--no_force_same_axes", default=False)
@click.option("--legends/--no_legends", default=True)
def cli(input, force_same_axes, legends):
    """
    Expected JSON format:
        [
            {
                "sim_type": "tran",
                "name": "RC circuit simulation",
                "plots": [
                    [
                        {
                            "name": "time",
                            "unit": "s",
                            "data": [1,2,3,4]
                        },
                        {
                            "name": "N_1",
                            "unit": "V",
                            "data": [1.0,2.0,3.0,4.0]
                        }
                    ]
                ]
            }
        ]
    """
    sim_results = json.load(input)

    with open(JSON_SCHEMA_PATH) as f:
        schema = json.load(f)
    try:
        jsonschema.validate(sim_results, schema)
    except jsonschema.ValidationError:
        click.echo("Could not walidate JSON schema", err=True)
        return

    for sim_result in sim_results:
        sim_type = sim_result["sim_type"]
        if force_same_axes:
            fig, ax = plt.subplots()

        for plot in sim_result["plots"]:
            if not force_same_axes:
                fig, ax = plt.subplots()

            x_var = plot[0]
            for y_var in plot[1:]:
                ax.plot(x_var["data"], y_var["data"], label=y_var["name"])

            if "unit" in x_var:
                plt.xlabel(f"{x_var['name']} ({x_var['unit']})")
                ax.xaxis.set_major_formatter(EngFormatter(unit=x_var["unit"]))
            else:
                plt.xlabel(f"{x_var['name']}")
                ax.xaxis.set_major_formatter(EngFormatter())

            num_y_units = len(
                set([y_var["unit"] for y_var in plot[1:] if "unit" in y_var])
            )
            if num_y_units == 1:
                plt.ylabel(f"{y_var['name']} ({y_var['unit']})")
                ax.yaxis.set_major_formatter(EngFormatter(unit=y_var["unit"]))
            else:
                if num_y_units > 1:
                    click.echo(f"More than one unit for Y axis.", err=True)
                plt.ylabel(f"{y_var['name']}")
                ax.yaxis.set_major_formatter(EngFormatter())

            if sim_type == "ac":
                ax.set_xscale("log")

            plt.title(f"{sim_type} simulation")
            ax.grid(True, which="major")
            ax.grid(True, which="minor", linestyle=":")
            ax.minorticks_on()
            if legends:
                ax.legend()

    plt.show()


if __name__ == "__main__":
    cli()
