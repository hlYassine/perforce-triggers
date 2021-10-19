import click
from click.decorators import argument

from perforce_triggers import perforce
from perforce_triggers import triggers


@click.group()
def cli():
    pass


@cli.command(
    name="list",
    help="List deployed (remote) or configured (local) triggers."
)
@argument(
    "trigger_location",
    type=click.Choice(["remote", "local"])
)
def list_triggers(trigger_location):
    trigger_list = []
    if trigger_location == "remote":
        trigger_list = perforce.get_triggers()
    else:
        for trigger_obj in triggers.get_triggers_from_config():
            trigger_list += trigger_obj.get_p4_trigger_lines()

    click.echo("\n".join(trigger_list))
