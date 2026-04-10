from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    @staticmethod
    def score_song(user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        """Return score and reason strings for how the song matches the user profile."""
        score = 0.0
        reasons: List[str] = []

        if song.genre == user.favorite_genre:
            score += 2.0
            reasons.append("genre match (+2.0)")

        if song.mood == user.favorite_mood:
            score += 1.0
            reasons.append("mood match (+1.0)")

        energy_proximity = max(0.0, 1.0 - abs(song.energy - user.target_energy))
        score += energy_proximity
        reasons.append(f"energy proximity (+{energy_proximity:.2f})")

        return score, reasons

    @staticmethod
    def _score_song(user: UserProfile, song: Song) -> float:
        """Project scoring rule: +2 genre, +1 mood, +0-1 energy proximity."""
        score, _ = Recommender.score_song(user, song)
        return score

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored: List[Tuple[Song, float]] = []

        for song in self.songs:
            score, _ = self.score_song(user, song)
            scored.append((song, score))

        ranked = sorted(scored, key=lambda item: item[1], reverse=True)
        return [song for song, _ in ranked[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        _, reasons = self.score_song(user, song)
        return ", ".join(reasons)

def load_songs(file_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs: List[Dict] = []
    with open(file_path, "r", encoding="utf-8") as file_handle:
        reader = csv.DictReader(file_handle)
        for row in reader:
            songs.append(
                {
                    "id": int(row["id"]),
                    "title": row["title"],
                    "artist": row["artist"],
                    "genre": row["genre"],
                    "mood": row["mood"],
                    "energy": float(row["energy"]),
                    "tempo_bpm": int(row["tempo_bpm"]),
                    "valence": float(row["valence"]),
                    "danceability": float(row["danceability"]),
                    "acousticness": float(row["acousticness"]),
                }
            )
    return songs

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored: List[Tuple[Dict, float, str]] = []

    for song in songs:
        score = 0.0
        reasons: List[str] = []

        if song["genre"] == user_prefs["genre"]:
            score += 2.0
            reasons.append("genre match (+2.0)")

        if song["mood"] == user_prefs["mood"]:
            score += 1.0
            reasons.append("mood match (+1.0)")

        energy_proximity = max(0.0, 1.0 - abs(song["energy"] - user_prefs["energy"]))
        score += energy_proximity
        reasons.append(f"energy proximity (+{energy_proximity:.2f})")

        scored.append((song, score, ", ".join(reasons)))

    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]
