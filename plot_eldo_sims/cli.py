import click


@click.command()
@click.argument("input", type=click.File("r"))
def cli(input):
    pass


if __name__ == "__main__":
    cli()
