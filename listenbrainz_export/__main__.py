import json

import click

from .export import request_all_listens


@click.command()
@click.argument("LISTENBRAINZ_USERNAME")
def main(listenbrainz_username: str) -> None:
    """
    Downloads all scrobbles for your listenbrainz account
    """
    click.echo(json.dumps(request_all_listens(listenbrainz_username)))


if __name__ == "__main__":
    main(prog_name="listenbrainz_export")
