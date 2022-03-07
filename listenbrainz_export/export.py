import logging
from typing import Optional, List, Dict, Any
from datetime import datetime

import requests
import backoff  # type: ignore[import]
import logzero  # type: ignore[import]

BASE_LISTENBRAINZ_URL = "https://api.listenbrainz.org/1/user/{username}/listens"

Json = Any


@backoff.on_exception(
    lambda: backoff.constant(interval=10),
    exception=requests.RequestException,
    max_tries=3,
)
def request_chunk(
    username: str,
    *,
    count: int = 100,
    max_ts: Optional[int] = None,
    logger: Optional[logging.Logger] = None,
) -> List[Json]:
    """
    paginate through listens for a user, by specifying an epoch time
    to receive scrobbles before
    once we receive the first chunk of scrobbles, use the epoch time of the
    last currently known scrobbles, and filter anything that was posted before that
    """
    params: Dict[str, Any] = {}
    if max_ts is not None:
        params["max_ts"] = max_ts
    params["count"] = count
    r = requests.get(BASE_LISTENBRAINZ_URL.format(username=username), params=params)
    if logger:
        logger.debug(f"Requesting {r.url}")
    r.raise_for_status()
    data = r.json()
    listens: List[Json] = data["payload"]["listens"]
    return listens


def request_listens(
    username: str, logger: logging.Logger = logzero.logger, pages: Optional[int] = None
) -> Json:
    max_ts: Optional[int] = None
    all_listens: List[Json] = []
    curpage = 0
    while True:
        new_listens = request_chunk(username, max_ts=max_ts, logger=logger)
        all_listens.extend(new_listens)
        if len(new_listens) == 0:  # exhausted all paginations
            break
        max_ts = int(all_listens[-1]["listened_at"])
        logger.debug(
            f"Have {len(all_listens)}, now searching for listens before {datetime.utcfromtimestamp(max_ts)}..."
        )
        curpage += 1
        if pages is not None and curpage >= pages:
            break
    return all_listens
