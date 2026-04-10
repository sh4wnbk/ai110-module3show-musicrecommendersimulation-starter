"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for rec in recommendations:
        song, score, reasons = rec
        print(f"Title: {song['title']}")
        print(f"Artist: {song['artist']}")
        print(f"Score: {score:.2f}")

        if isinstance(reasons, str):
            reasons_list = [reason.strip() for reason in reasons.split(",") if reason.strip()]
        else:
            reasons_list = reasons

        for reason in reasons_list:
            print(f"Because: {reason}")
        print()


if __name__ == "__main__":
    main()
