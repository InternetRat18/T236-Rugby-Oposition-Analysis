import csv
import matplotlib.pyplot as plt


EVENT_FILES = {
    "Carry": "ExtractedData/1-Carry.csv",
    "Tackle": "ExtractedData/2-Tackle.csv",
    "Pass": "ExtractedData/3-Pass.csv",
    "Kick": "ExtractedData/4-Kick.csv",
    "Ruck": "ExtractedData/23-Ruck.csv"
}




def get_event_timeline(file_path):
    """
    Count events in 10-minute intervals.
    MatchTime is stored in MMSS format.
    """

    time_bins = {
        "0–10 min": 0,
        "10–20 min": 0,
        "20–30 min": 0,
        "30–40 min": 0,
        "40–50 min": 0,
        "50–60 min": 0,
        "60–70 min": 0,
        "70–80 min": 0
    }

    with open(file_path, "r", encoding="utf-8") as file:

        reader = csv.reader(file)

        for row in reader:

            if not row:
                continue

            
            match_time = row[8]

            try:
                match_time = int(match_time)
            except ValueError:
                continue

            
            minutes = match_time // 100
            seconds = match_time % 100

            total_seconds = minutes * 60 + seconds

            if total_seconds < 600:
                time_bins["0–10 min"] += 1

            elif total_seconds < 1200:
                time_bins["10–20 min"] += 1

            elif total_seconds < 1800:
                time_bins["20–30 min"] += 1

            elif total_seconds < 2400:
                time_bins["30–40 min"] += 1

            elif total_seconds < 3000:
                time_bins["40–50 min"] += 1

            elif total_seconds < 3600:
                time_bins["50–60 min"] += 1

            elif total_seconds < 4200:
                time_bins["60–70 min"] += 1

            elif total_seconds <= 4800:
                time_bins["70–80 min"] += 1

    return time_bins




def get_tackle_outcomes(file_path):
    """
    Count different tackle outcomes using
    ActionResultName from the partner dataset.
    """

    outcomes = {}

    with open(file_path, "r", encoding="utf-8") as file:

        reader = csv.reader(file)

        for row in reader:

            if not row:
                continue

            
            outcome = row[19].strip()

            if outcome == "":
                continue

            outcomes[outcome] = outcomes.get(outcome, 0) + 1

    return outcomes





def get_player_event_counts(file_path):
    """
    Count how many times each player appears
    in an event dataset.

    playerName = column 4 (index 3)
    """

    player_counts = {}

    with open(file_path, "r", encoding="utf-8") as file:

        reader = csv.reader(file)

        for row in reader:

            if not row:
                continue

            
            player_name = row[3].strip()

            if player_name == "":
                continue

            player_counts[player_name] = (
                player_counts.get(player_name, 0) + 1
            )

    return player_counts




tackle_file = EVENT_FILES["Tackle"]

tackle_outcomes = get_tackle_outcomes(tackle_file)

print("\nTackle Outcomes")
print("-------------------------")

for outcome, count in tackle_outcomes.items():
    print(f"{outcome}: {count}")




plt.figure(figsize=(10, 6))

bars = plt.bar(
    tackle_outcomes.keys(),
    tackle_outcomes.values()
)

plt.title("NSW Waratahs Tackle Outcomes")
plt.xlabel("Tackle Outcome")
plt.ylabel("Number of Tackles")

plt.xticks(rotation=35)

for bar, value in zip(bars, tackle_outcomes.values()):

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        value + 1,
        str(value),
        ha="center",
        va="bottom"
    )

plt.tight_layout()

plt.savefig(
    "tackle_outcomes.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()





player_counts = get_player_event_counts(tackle_file)


sorted_players = sorted(
    player_counts.items(),
    key=lambda item: item[1],
    reverse=True
)


top_players = sorted_players[:10]

print("\nTop Tackle Players")
print("-------------------------")

for player, count in top_players:
    print(f"{player}: {count}")






player_names = [player for player, count in top_players]
player_values = [count for player, count in top_players]

plt.figure(figsize=(10, 6))

bars = plt.bar(
    player_names,
    player_values
)

plt.title("NSW Waratahs Top Tackle Players")

plt.xlabel("Player")

plt.ylabel("Number of Tackles")

plt.xticks(
    rotation=35,
    ha="right"
)

for bar, value in zip(bars, player_values):

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        value + 0.5,
        str(value),
        ha="center",
        va="bottom"
    )

plt.tight_layout()

plt.savefig(
    "top_tackle_players.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()





print("\nAvailable events:")
print("1 - Carry")
print("2 - Tackle")
print("3 - Pass")
print("4 - Kick")
print("5 - Ruck")

choice = input("Select an event (1-5): ")


event_choices = {
    "1": "Carry",
    "2": "Tackle",
    "3": "Pass",
    "4": "Kick",
    "5": "Ruck"
}



if choice not in event_choices:

    print("Invalid choice.")

else:

    event_name = event_choices[choice]

    file_path = EVENT_FILES[event_name]

    timeline = get_event_timeline(file_path)

    print()
    print(event_name + " Timeline")
    print("-------------------------")

    for period, count in timeline.items():

        print(f"{period}: {count}")


    plt.figure(figsize=(10, 6))

    bars = plt.bar(
        timeline.keys(),
        timeline.values()
    )

    plt.title(
        f"NSW Waratahs {event_name} Activity Over Match Time"
    )

    plt.xlabel("Match Time")

    plt.ylabel(
        f"Number of {event_name} Events"
    )

    plt.xticks(rotation=30)

    for bar, value in zip(bars, timeline.values()):

        plt.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.5,
            str(value),
            ha="center",
            va="bottom"
        )

    plt.tight_layout()


    filename = event_name.lower() + "_timeline.png"

    plt.savefig(
        filename,
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()