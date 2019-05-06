# plot_eldo_sims
Plot eldo simulations output file with python.

This tool allows for a fast and easy to check wave viewer when the standard options are not available, and is thought to be used together with [chi_to_json](https://github.com/ftorres16/chi_to_json), although it could be used with any other tool that outputs the same JSON format.

## Installation

- Git clone this repository
- `pip install -e <path to this repository>`

## Usage

Have your SPICE simulation output parsed into a valid json file (see [Related repos](#Related-repos)).

Run `plot_eldo_sims <path to your .json file>` and wait for the plots to show.

## Supported analyses
- tran
- dc
- ac

## Related repos

If you find this repo useful, there's a good chance you may want to check some of my other related work as well.

- [tannner_to_eldo](https://github.com/ftorres16/tanner_to_eldo) can transform Tanner generated SPICE netlists into ELDO compatible ones.
- [chi_to_json](https://github.com/ftorres16/chi_to_json) extracts the simulation data form an ELDO `chi` output file and writes it into an easier to handle JSON format.
