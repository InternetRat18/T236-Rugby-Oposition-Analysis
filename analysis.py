import sqlite3
import matplotlib.pyplot as plt


# SQLite database
DATABASE = "MainDB.db"

# Team to analyse
TEAM_NAME = "NSW Waratahs"



EVENT_ACTIONS = {
    "Carry": 1,
    "Tackle": 2,
    "Pass": 3,
    "Kick": 4,
    "Ruck": 23
}


def get_event_data(action_id):
    """
    Retrieve event data for NSW Waratahs
    from the SQLite database.
    """

    connection = sqlite3.connect(DATABASE)

    table_name = f"ActionSubtable-{action_id}"

    query = f'''
        SELECT *
        FROM "{table_name}"
        WHERE teamName = ?
    '''

    cursor = connection.cursor()

    cursor.execute(query, (TEAM_NAME,))

    rows = cursor.fetchall()

    connection.close()

    return rows


def get_event_timeline(rows):
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

    for row in rows:

        if not row:
            continue

        
        match_time = row[8]

        try:
            match_time = int(match_time)
        except (ValueError, TypeError):
            continue

        # MatchTime uses MMSS format
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


def get_tackle_outcomes(rows):
    """
    Count different tackle outcomes.

    ActionResultName is column 19.
    """

    outcomes = {}

    for row in rows:

        if not row:
            continue

        outcome = row[19].strip()

        if outcome == "":
            continue

        outcomes[outcome] = outcomes.get(outcome, 0) + 1

    return outcomes


def get_player_event_counts(rows):
    """
    Count how many times each player
    appears in an event dataset.

    playerName is column 3.
    """

    player_counts = {}

    for row in rows:

        if not row:
            continue

        player_name = row[3].strip()

        if player_name == "":
            continue

        player_counts[player_name] = (
            player_counts.get(player_name, 0) + 1
        )

    return player_counts


def create_tackle_outcomes_chart(outcomes):

    plt.figure(figsize=(10, 6))

    bars = plt.bar(
        outcomes.keys(),
        outcomes.values()
    )

    plt.title(
        f"{TEAM_NAME} Tackle Outcomes"
    )

    plt.xlabel("Tackle Outcome")

    plt.ylabel("Number of Tackles")

    plt.xticks(rotation=35)

    for bar, value in zip(
        bars,
        outcomes.values()
    ):

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


def create_top_player_chart(player_counts):

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

    player_names = [
        player for player, count in top_players
    ]

    player_values = [
        count for player, count in top_players
    ]

    plt.figure(figsize=(10, 6))

    bars = plt.bar(
        player_names,
        player_values
    )

    plt.title(
        f"{TEAM_NAME} Top Tackle Players"
    )

    plt.xlabel("Player")

    plt.ylabel("Number of Tackles")

    plt.xticks(
        rotation=35,
        ha="right"
    )

    for bar, value in zip(
        bars,
        player_values
    ):

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


def create_timeline_chart(event_name, timeline):

    plt.figure(figsize=(10, 6))

    bars = plt.bar(
        timeline.keys(),
        timeline.values()
    )

    plt.title(
        f"{TEAM_NAME} {event_name} Activity Over Match Time"
    )

    plt.xlabel("Match Time")

    plt.ylabel(
        f"Number of {event_name} Events"
    )

    plt.xticks(rotation=30)

    for bar, value in zip(
        bars,
        timeline.values()
    ):

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




print("\nLoading data from SQLite...")
print("-------------------------")

tackle_rows = get_event_data(
    EVENT_ACTIONS["Tackle"]
)

print(
    f"Tackle events for {TEAM_NAME}: "
    f"{len(tackle_rows)}"
)




tackle_outcomes = get_tackle_outcomes(
    tackle_rows
)

print("\nTackle Outcomes")
print("-------------------------")

for outcome, count in tackle_outcomes.items():
    print(f"{outcome}: {count}")

create_tackle_outcomes_chart(
    tackle_outcomes
)




player_counts = get_player_event_counts(
    tackle_rows
)

create_top_player_chart(
    player_counts
)




print("\nAvailable events:")
print("1 - Carry")
print("2 - Tackle")
print("3 - Pass")
print("4 - Kick")
print("5 - Ruck")

choice = input(
    "Select an event (1-5): "
)


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

    action_id = EVENT_ACTIONS[
        event_name
    ]

    rows = get_event_data(
        action_id
    )

    timeline = get_event_timeline(
        rows
    )

    print()
    print(event_name + " Timeline")
    print("-------------------------")

    for period, count in timeline.items():

        print(
            f"{period}: {count}"
        )

    create_timeline_chart(
        event_name,
        timeline
    )