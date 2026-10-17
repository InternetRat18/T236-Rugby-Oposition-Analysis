from collections import Counter

def _value(row, key, default=None):
    value = row.get(key, default)
    return value

def _match_rows(rows, filters=None):
    filters = filters or {}
    result = []
    for row in rows:
        if filters.get("teamId") and str(row.get("team_id", "")) != str(filters["teamId"]):
            continue
        if filters.get("playerId"):
            player_id = filters["playerId"]
            key = "unnamed" if not row.get("playerName") else f'{row.get("team_id")}:{row.get("PLID") or row.get("playerName")}'
            if key != player_id:
                continue
        if filters.get("actionId") and str(row.get("action", "")) != str(filters["actionId"]):
            continue
        if filters.get("period") and str(row.get("period", "")) != str(filters["period"]):
            continue
        result.append(row)
    return result

def _timeline(rows):
    labels = ["0–10 min", "10–20 min", "20–30 min", "30–40 min",
              "40–50 min", "50–60 min", "60–70 min", "70–80 min"]
    counts = Counter({label: 0 for label in labels})
    for row in rows:
        try:
            clock = int(row.get("MatchTime"))
            if clock < 0 or clock % 100 >= 60:
                continue
            seconds = (clock // 100) * 60 + clock % 100
            if 0 <= seconds <= 4800:
                index = min(seconds // 600, 7)
                counts[labels[index]] += 1
        except (TypeError, ValueError):
            continue
    return [{"label": label, "value": counts[label]} for label in labels]

def get_dashboard_analysis(rows, filters=None):
    filtered = _match_rows(rows, filters)
    filters = filters or {}
    action_id = str(filters.get("actionId", "") or "")
    action_names = [str(r.get("actionName", "")).strip() for r in filtered if r.get("actionName")]
    action_name = action_names[0] if action_names else "Selected events"

    outcomes = Counter(
        str(r.get("ActionResultName")).strip()
        for r in filtered
        if r.get("ActionResultName") and str(r.get("ActionResultName")).strip()
    )
    result_chart = {
        "title": f"{action_name} results" if action_name != "Selected events" else "Action results",
        "unit": "",
        "data": [{"label": label, "value": count} for label, count in outcomes.most_common(12)],
    }

    is_tackle = action_id == "2" or any(name.lower() == "tackle" for name in action_names)
    if is_tackle:
        players = Counter(
            str(r.get("playerName")).strip()
            for r in filtered
            if r.get("playerName") and str(r.get("playerName")).strip()
        )
        secondary_chart = {
            "title": "Top players by event count",
            "unit": "",
            "data": [{"label": label, "value": count} for label, count in players.most_common(10)],
        }
    else:
        secondary_chart = {
            "title": f"{action_name} activity over match time",
            "unit": "",
            "data": _timeline(filtered),
        }

    return {"charts": [result_chart, secondary_chart]}
