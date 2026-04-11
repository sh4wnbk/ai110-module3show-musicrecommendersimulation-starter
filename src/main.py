"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from rich.console import Console
from rich.table import Table

from src.recommender import load_songs, recommend_songs


def _reason_summary(reason_text: str) -> str:
    """Normalize reason text for dashboard cells."""
    cleaned = str(reason_text).strip()
    return cleaned if cleaned else "-"


def _first_reason(reason_text: str) -> str:
    """Return the first reason fragment from a comma-delimited explanation."""
    full = _reason_summary(reason_text)
    return full.split(",")[0].strip()


def _plain_language_summary(profile: dict, dashboard_rows: list) -> str:
    """Build a short, plain-English takeaway for the side-by-side table."""
    if not dashboard_rows:
        return "No recommendations available for this profile."

    top_title = dashboard_rows[0][1]
    top_reason = str(dashboard_rows[0][3]).lower()

    reason_focus = "a general fit"
    if "mood match" in top_reason:
        reason_focus = "mood alignment"
    elif "energy proximity" in top_reason:
        reason_focus = "energy alignment"
    elif "genre match" in top_reason:
        reason_focus = "genre alignment"

    return (
        f"For {profile['name']}, the recommender prioritizes "
        f"{reason_focus}. The top pick is {top_title}."
    )


def main() -> None:
    console = Console()
    songs = load_songs("data/songs.csv")

    # Side-by-side comparison for one profile across all strategy modes.
    comparison_profile = {
        "name": "Intense Jazz Seeker",
        "genre": "jazz",
        "mood": "intense",
        "energy": 0.95,
        "preferred_decade": 2010,
        "preferred_mood_tag": "aggressive",
        "target_instrumentalness": 0.25,
        "target_speechiness": 0.08,
        "target_liveness": 0.22,
    }
    comparison_modes = [
        {"strategy": "conservative", "alpha": 0.5, "key": "cons"},
        {"strategy": "discovery", "alpha": 0.5, "key": "disc"},
        {"strategy": "hybrid", "alpha": 0.7, "key": "hybrid"},
    ]
    dashboard_k = 5

    console.rule("THE SOUND-BENDER: Side-by-Side", style="grey70")
    console.print(
        "[bold]Profile:[/bold] "
        f"{comparison_profile['name']} | "
        f"{comparison_profile['genre']}, {comparison_profile['mood']}, "
        f"energy={comparison_profile['energy']}"
    )

    mode_rankings = {}
    mode_lookup_by_song_id = {}
    for mode_cfg in comparison_modes:
        comparison_input = {
            **comparison_profile,
            "strategy": mode_cfg["strategy"],
            "popularity_weight": 2.0,
            "alpha": mode_cfg["alpha"],
        }
        full_ranking = recommend_songs(comparison_input, songs, k=len(songs))
        mode_rankings[mode_cfg["key"]] = full_ranking
        mode_lookup_by_song_id[mode_cfg["key"]] = {
            song["id"]: (song, score, reasons) for song, score, reasons in full_ranking
        }

    dashboard_rows = []
    for rank, (song, hybrid_score, hybrid_reasons) in enumerate(mode_rankings["hybrid"][:dashboard_k], start=1):
        song_id = song["id"]
        _, conservative_score, conservative_reasons = mode_lookup_by_song_id["cons"][song_id]
        _, discovery_score, discovery_reasons = mode_lookup_by_song_id["disc"][song_id]
        dashboard_rows.append([
            rank,
            f"{song['title']} ({song['artist']})",
            f"{conservative_score:.2f}",
            _first_reason(str(conservative_reasons)),
            f"{discovery_score:.2f}",
            _first_reason(str(discovery_reasons)),
            f"{hybrid_score:.2f}",
            _first_reason(str(hybrid_reasons)),
        ])

    dashboard = Table(
        title="THE SOUND-BENDER: SIDE-BY-SIDE",
        show_header=True,
        header_style="bold magenta",
        box=None,
        pad_edge=False,
        show_lines=False,
    )
    dashboard.add_column("Rank", style="bold", width=4, justify="right")
    dashboard.add_column("Title (Artist)", style="cyan", no_wrap=True)
    dashboard.add_column("Conservative", justify="right", width=12)
    dashboard.add_column("Conservative Why", width=24, overflow="ellipsis", no_wrap=True)
    dashboard.add_column("Discovery", justify="right", width=10)
    dashboard.add_column("Discovery Why", width=24, overflow="ellipsis", no_wrap=True)
    dashboard.add_column("Hybrid", justify="right", style="green", width=8)
    dashboard.add_column("Hybrid Why", width=24, overflow="ellipsis", no_wrap=True)

    for index, row in enumerate(dashboard_rows):
        dashboard.add_row(*[str(item) for item in row])
        if index < len(dashboard_rows) - 1:
            dashboard.add_row(*([""] * len(row)))

    console.print()
    console.print(dashboard)
    console.print()
    console.print()
    console.print(f"[bold magenta]{_plain_language_summary(comparison_profile, dashboard_rows)}[/bold magenta]")
    console.print()
    console.print()

    # Toggle these values to compare strategy behavior.
    # Options: "conservative", "discovery", or "hybrid"
    active_strategy = "hybrid"
    active_popularity_weight = 2.0
    # Only used by hybrid. alpha=1.0 leans conservative, alpha=0.0 leans discovery.
    active_alpha = 0.7

    # Define at least six distinct profiles to test the algorithm's boundaries
    # Phase 4 Evaluation Profiles
    test_profiles = [
        {"name": "High-Energy Pop", "genre": "pop", "mood": "happy", "energy": 0.9},
        {"name": "Chill Lofi", "genre": "lofi", "mood": "chill", "energy": 0.2},
        {"name": "Deep Intense Rock", "genre": "rock", "mood": "intense", "energy": 0.85},
        {"name": "Conflicting Happy but Low Energy", "genre": "pop", "mood": "happy", "energy": 0.2},
        {"name": "Sad but High Energy", "genre": "lofi", "mood": "sad", "energy": 0.9},
        {"name": "Noisy Mismatch", "genre": "jazz", "mood": "intense", "energy": 0.1}
    ]

    for profile in test_profiles:
        print(f"{'='*30}")
        print(f"RUNNING TEST FOR: {profile['name']}")
        print(f"Preferences: {profile['genre']}, {profile['mood']}, Energy: {profile['energy']}")
        print(f"{'='*30}")

        # Inject strategy config so recommendations can switch behavior.
        profile_with_strategy = {
            **profile,
            "strategy": active_strategy,
            "popularity_weight": active_popularity_weight,
            "alpha": active_alpha,
        }
        recommendations = recommend_songs(profile_with_strategy, songs, k=5)

        for rec in recommendations:
            song, score, reasons = rec
            # 1. Header with Emoji and Title
            print(f"⭐ {song['title'].upper()} ({song['artist']})")
            print(f"   Score: {score:.2f}")

            # 2. Handle the reasons (string or list)
            if isinstance(reasons, str):
                reasons_list = [r.strip() for r in reasons.split(",") if r.strip()]
            else:
                reasons_list = reasons

            # 3. Print reasons with a stylistic arrow
            for reason in reasons_list:
                print(f"   ↳ Because: {reason}")

            # 4. Divider and spacing for readability
            print(f"   {'-' * 20}\n")

if __name__ == "__main__":
    main()