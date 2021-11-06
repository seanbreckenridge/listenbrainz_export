# listenbrainz_export

Export your scrobbling history form [ListenBrainz](https://listenbrainz.org/). ListenBrainz is a public/open-source alternative to RateYourMusic

Since the data is public, no API key/Authentication is required.

## Installation

Requires `python3.6+`

To install with pip, run:

    pip install git+https://github.com/seanbreckenridge/listenbrainz_export

---

## Usage

Provide your listenbrainz username -- prints results to STDOUT

```
listenbrainz_export seanbreckenridge > ./data.json
```

Can also only request a few pages:

```
listenbrainz_export seanbreckenridge --pages 3
```

`listenbrainz_export.parse` includes a model of the data and some functions to parse them into python objects, like:

```python
>>> from listenbrainz_export.parse import iter_listens
>>> listens = list(iter_listens("data.json"))
>>> listens[12]
Listen(track_name='The Spine', artist_name='Darren Korb', listened_at=datetime.datetime(2021, 8, 30, 18, 52, 24), inserted_at=datetime.datetime(2021, 8, 31, 1, 53, 57), release_name='Transistor Original Soundtrack', recording_mbid=None, artist_mbids=[], release_mbid=None, tags=[], release_group_mbid=None, work_mbids=[], tracknumber=None, spotify_id=None, listening_from=None, isrc=None, username=None)
```

### Tests

```bash
git clone 'https://github.com/seanbreckenridge/listenbrainz_export'
cd ./listenbrainz_export
pip install '.[testing]'
mypy ./listenbrainz_export
```
