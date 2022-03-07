# listenbrainz_export

Export your scrobbling history form [ListenBrainz](https://listenbrainz.org/). ListenBrainz is a public/open-source alternative to RateYourMusic

Since the data is public, no API key/Authentication is required.

## Installation

Requires `python3.7+`

To install with pip, run:

    pip install git+https://github.com/seanbreckenridge/listenbrainz_export

## Usage

Provide your listenbrainz username -- prints results to STDOUT

```
listenbrainz_export seanbreckenridge > ./data.json
```

Can also only request a few pages:

```
listenbrainz_export seanbreckenridge --pages 3
```

[`listenbrainz_export.parse`](./listenbrainz_export/parse.py) includes a model of the data and some functions to parse them into python objects, like:

```python
>>> from listenbrainz_export.parse import iter_listens
>>> listens = list(iter_listens("data.json"))
>>> listens[12]
Listen(track_name='Skate', artist_name='Bruno Mars, Anderson .Paak & Silk Sonic', listened_at=datetime.datetime(2021, 11, 6, 19, 10, 49), inserted_at=datetime.datetime(2021, 11, 7, 2, 12, 31), recording_id='e60b9417-acfe-4796-a048-76208fb4a9ad', release_name='Skate - Single', metadata={'artist_msid': 'df6f6937-5de3-4e3c-bd74-1991ed92abd5', 'recording_msid': 'e60b9417-acfe-4796-a048-76208fb4a9ad', 'release_msid': 'dcf6d703-1e95-4e9c-8218-bb7c3b3bfa0b'}, username='seanbreckenridge')
```

I use this almost exclusively through my [HPI](https://github.com/seanbreckenridge/HPI); that locates my exports on disks and removes any duplicate scrobbles

### Tests

```bash
git clone 'https://github.com/seanbreckenridge/listenbrainz_export'
cd ./listenbrainz_export
pip install '.[testing]'
mypy ./listenbrainz_export
flake8 ./listenbrainz_export
```
