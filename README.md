# plot_eldo_sims
Plot eldo simulations output file with python.

## Installation

- Git clone this repository
- `pip install -e <path to this repository>`

## Usage

Run your Eldo simulation as usual (`eldo <your spice netlist>`) and save the `.chi` output file.

Please note that for this program to be able to plot anything, you will need to print at least one signal in your netlist with the `.print` command.

If you want more than one signal to be printed on the same pair of axes, you have to include them in the same `.print` command, i.e. `.print V(N_1) V(N_2)` will use the same set of axes, whereas `.print V(N_1)` followed by `.print V(N_2)` on the following line will use two separate windows.

Run `plot_eldo_sims <path to your .chi file>` and wait for the plots to show.

### Supported analyses
- tran
- dc
- ac
