import json
from typing import Optional

import click

from .export import request_listens


@click.command()
@click.option(
    "--pages", type=int, default=None, help="Request these many pages of your history"
)
@click.argument("LISTENBRAINZ_USERNAME")
def main(pages: Optional[int], listenbrainz_username: str) -> None:
    """
    Downloads all scrobbles for your listenbrainz account
    """
    click.echo(json.dumps(request_listens(username=listenbrainz_username, pages=pages)))


if __name__ == "__main__":
    main(prog_name="listenbrainz_export")
