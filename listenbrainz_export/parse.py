import json
from datetime import datetime
from typing import Optional, NamedTuple, Any, Dict, List, Iterator

DATE_REGEX = "%a, %d %b %Y %H:%M:%S %Z"


class Listen(NamedTuple):
    track_name: str
    artist_name: str
    # could be null if you're currently listening to something
    listened_at: Optional[datetime]
    inserted_at: Optional[datetime]
    release_name: Optional[str]
    recording_mbid: Optional[str]
    artist_mbids: List[str]
    release_mbid: Optional[str]
    tags: List[str]
    release_group_mbid: Optional[str]
    work_mbids: List[str]
    tracknumber: Optional[int]
    spotify_id: Optional[str]
    listening_from: Optional[str]
    isrc: Optional[str]
    username: Optional[str]

    @classmethod
    def from_blob(cls, blob: Dict[str, Any]) -> "Listen":
        track_metadata = blob["track_metadata"]
        listened_at: Optional[int] = blob.get("listened_at")
        inserted_at: Optional[str] = blob.get("inserted_at")
        additional_info = track_metadata.get("additional_info", {})
        return cls(
            track_name=track_metadata["track_name"],
            artist_name=track_metadata["artist_name"],
            listened_at=datetime.fromtimestamp(listened_at)
            if listened_at is not None
            else None,
            inserted_at=datetime.strptime(inserted_at, DATE_REGEX)
            if inserted_at is not None
            else None,
            release_name=track_metadata.get("release_name"),
            recording_mbid=additional_info.get("recording_mbid"),
            artist_mbids=additional_info.get("artist_mbids", []),
            release_mbid=additional_info.get("release_mbid"),
            tags=additional_info.get("tags", []),
            release_group_mbid=additional_info.get("release_group_mbid"),
            work_mbids=additional_info.get("work_mbids", []),
            tracknumber=additional_info.get("tracknumber"),
            spotify_id=additional_info.get("spotify_id"),
            listening_from=additional_info.get("listening_from"),
            isrc=additional_info.get("isrc"),
            username=blob.get("username"),
        )


def iter_listens(from_file: str) -> Iterator[Listen]:
    with open(from_file, "r") as f:
        data: List[Dict[str, Any]] = json.load(f)
    for blob in data:
        yield Listen.from_blob(blob)
