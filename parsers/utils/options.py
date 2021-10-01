import click


def silent_option():
    return click.option("--silent", is_flag=True, help="Silence output")
