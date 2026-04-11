# Music Recommender Model Card

## Model Name

🎧 THE SOUND-BENDER

## Goal / Task

This recommender tries to suggest songs a user might like.
It looks at genre, mood, and energy.
It gives each song a score and returns the top matches.

Status: ACTIVE 🟢

## 📂 Data Used

The dataset has 20 songs in [data/songs.csv](data/songs.csv).
Each song has genre, mood, energy, tempo, valence, danceability, and acousticness.
The catalog is small, so it does not cover every kind of music taste.
Some genres only have one or two songs.

## ⚙️ Algorithm Summary

The model gives points for a genre 🏷️ match, a mood 🎭 match, and energy 🔥 closeness.
Genre and mood each add 1 point.
Energy closeness is multiplied by 3, so it has the strongest effect.
That means a song with close energy can rank high even if one other label does not match.

## ⚠️ Observed Behavior / Biases

One pattern is energy ⚡ dominance.
High-energy songs often rise to the top, even when the user wanted a calmer feel.
This can make songs like "Gym Hero" show up for many different profiles.

Another bias is small-data 📦 bias.
With only 20 songs, the system repeats the same songs for some users because there are not many options.
That is especially true for underrepresented genres like rock, metal, and jazz.

The model also has an energy-gap 📉 trap.
Users with very low energy or very high energy can get weaker matches than mid-range users.
That happens because the energy score is linear and the catalog does not have many songs at the extremes.

## 🧪 Evaluation Process

I tested 6 profiles.
Three were normal profiles and three were adversarial or conflicting profiles.
The profiles were High-Energy Pop, Chill Lofi, Deep Intense Rock, Conflicting Happy but Low Energy, Sad but High Energy, and Noisy Mismatch.

I checked the top 5 results for each profile.
I also compared the outputs before and after a weight-shift experiment.
That experiment showed that stronger energy weighting changed the ranking more than the genre weight did.
I also compared the catalog genre counts with the recommendation counts to look for repetition and bias.

## Optional Extensions Implemented (Plain Language)

I implemented all 4 optional extension challenges and captured a side-by-side dashboard screenshot-like artifact.

- Dashboard image artifact: [assets/side_by_side_table.png](assets/side_by_side_table.png)

### Challenge 1: Advanced Song Features

I expanded the song data with additional features that were not in the baseline:

- Popularity (0-100)
- Release Year
- Detailed Mood Tag
- Instrumentalness
- Speechiness
- Liveness

In plain terms, this means the recommender now looks beyond just genre/mood/energy and can reward songs that better match a preferred era, detailed vibe, and audio texture profile.

### Challenge 2: Multiple Scoring Modes

I built multiple scoring strategies so the same user can be ranked in different ways:

- Conservative mode: balanced and stable with trend/discovery bonuses
- Discovery mode: leans more toward hidden gems and exploratory matching
- Hybrid mode: blends Conservative and Discovery using alpha

In plain terms, this lets the recommender behave like a "safe" mode, an "explore" mode, or a blend between the two.

### Challenge 3: Diversity and Fairness Logic

I added a Diversity Penalty of -0.5 when an artist is already in the selected top-k list.

In plain terms, this reduces artist repetition so recommendations feel less repetitive and more varied.

### Challenge 4: Visual Summary Table

I built a visual side-by-side terminal summary using Rich, including scores and per-mode reasons.

In plain terms, you can quickly compare why a song ranks differently across Conservative, Discovery, and Hybrid without reading raw logs.

## ✅ Intended Use and ❌ Non-Intended Use

This system is for classroom learning and simple experiments.
It is good for showing how a scoring rule works.
It is also good for explaining why a result ranked first.

It should not be used as a real music app.
It does not know lyrics, context, or personal history.
It should not be treated as a full picture of a user's taste.

## Ideas 💡 for Improvement

- Reduce the energy multiplier so genre and mood matter more.
- Add more songs, especially for underrepresented genres.
- Add diversity logic so the same songs do not keep repeating.

## Personal 💭 Reflection

The biggest thing I learned was that a recommender can look balanced on paper and still behave unevenly in practice.
A small weight choice changed which songs rose to the top, and that made me pay attention to the difference between a score that is mathematically correct and a result that actually feels right.

AI tools, Gemini/Copilot - helped me move faster when I needed to test ideas, compare outputs, and write summaries.
I still had to double-check them when the result depended on exact scores, because a tiny change in the numbers could change the ranking.
That mattered most when I checked why "Gym Hero" kept appearing and when I tested the weight shift.

What surprised me most was how simple rules can still feel like real recommendations.
Even without any learning from users, the system could produce results that seemed sensible for one profile and wrong for another.
If I kept extending this project, I would add more songs, rebalance the weights, and add a diversity rule so the same songs do not keep coming back.
