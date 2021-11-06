import click


def silent_option():
    return click.option("-q", "--silent", is_flag=True, help="Silence output")
