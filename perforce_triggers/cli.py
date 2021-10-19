import click

from click.decorators import argument

from perforce_triggers import perforce
from perforce_triggers import triggers
from perforce_triggers import config


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


@cli.command(
    name="show-config",
    help="Prints out configurations."
)
@argument(
    "configuration",
    nargs=1,
    type=click.Choice(["auth", "triggers"])
)
@argument(
    "fields",
    nargs=-1
)
def show_config(configuration, fields):
    try:
        config_ = config.get_config()
        for field in fields:
            click.echo(
                f"{configuration}.{field} = {config_[configuration][field]}"
            )
    except KeyError as e:
        click.secho(
            f"Unkonwn configuration '{configuration}' field {e}",
            fg="red")
