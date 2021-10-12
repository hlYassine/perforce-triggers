import click
from click.decorators import option

from perforce_triggers import perforce


@click.group()
def cli():
    pass


@click.command()
@option("--listing", "-l", is_flag=True, help="List perforce server triggers.")
def triggers(listing):
    if listing:
        trigger_list = perforce.get_triggers()
        click.echo("\n".join(trigger_list))


cli.add_command(triggers)
