import json
from datetime import datetime, timezone
from typing import Optional, NamedTuple, Any, Dict, List, Iterator

DATE_REGEX = "%a, %d %b %Y %H:%M:%S %Z"

Json = Dict[str, Any]

class Listen(NamedTuple):
    track_name: str
    artist_name: str
    # could be null if you're currently listening to something
    listened_at: Optional[datetime]
    inserted_at: Optional[datetime]
    recording_id: Optional[str]
    release_name: Optional[str]
    metadata: Json
    username: Optional[str]

    @classmethod
    def from_blob(cls, blob: Dict[str, Any]) -> "Listen":
        # this works by using 'pop's on the dictionary to slowly
        # decompose them without running into possible errors,
        # and taking any remaining data left over in the typical
        # structure and merging them into the 'metadata' blob,
        # since theres so many possible keys on this object
        #
        # just extracts the most useful stuff and attaches the
        # rest onto metadata
        track_metadata = blob.pop("track_metadata", {})
        listened_at: Optional[int] = blob.pop("listened_at", None)
        inserted_at: Optional[str] = blob.pop("inserted_at", None)
        recording_id: Optional[str] = blob.pop("recording_msid", None)
        username: Optional[str] = blob.pop("user_name", None)
        release_name = track_metadata.pop("release_name", None)
        artist_name: str = track_metadata.pop("artist_name", "<unknown>")
        track_name: str = track_metadata.pop("track_name", "<unknown>")
        # merge all other additional info into the JSON object
        metadata: Json = {}
        additional_info = track_metadata.pop("additional_info", {})
        metadata.update(additional_info)
        metadata.update(track_metadata)
        metadata.update(blob)
        return cls(
            track_name=track_name,
            artist_name=artist_name,
            listened_at=datetime.fromtimestamp(listened_at, tz=timezone.utc)
            if listened_at is not None
            else None,
            inserted_at=datetime.strptime(inserted_at, DATE_REGEX)
            if inserted_at is not None
            else None,
            recording_id=recording_id,
            release_name=release_name,
            metadata=metadata,
            username=username,
        )


def iter_listens(from_file: str) -> Iterator[Listen]:
    with open(from_file, "r") as f:
        data: List[Dict[str, Any]] = json.load(f)
    for blob in data:
        yield Listen.from_blob(blob)
