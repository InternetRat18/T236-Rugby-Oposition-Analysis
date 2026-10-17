"use strict";

const teamSelect = document.getElementById("team");
const playerSelect = document.getElementById("player");
const actionSelect = document.getElementById("action");
const periodSelect = document.getElementById("period");
const pageSize = 15;
let allEvents = [];
let selectedEvents = [];
let currentPage = 0;
let selectionId = 0;

function playerKey(event) {
  if (!event.playerName) return "unnamed";
  const playerId = event.PLID ?? event.playerName;
  return String(event.team_id) + ":" + String(playerId);
}

function actionLabel(event) {
  return event.actionName || "Unlabelled action (" + event.action + ")";
}

function fillSelect(select, events, getValue, getLabel, allLabel) {
  const options = new Map();
  events.forEach(event => options.set(getValue(event), getLabel(event)));
  select.replaceChildren(new Option(allLabel, ""));
  const sorted = [...options].sort((a, b) => a[1].localeCompare(b[1]));
  sorted.forEach(([value, text]) => select.add(new Option(text, value)));
}

function halfLabel(value) {
  if (String(value) === "1") return "First half";
  if (String(value) === "2") return "Second half";
  return "Half " + String(value);
}

function updateHalfOptions(events) {
  const previousValue = periodSelect.value;
  const halves = [...new Set(events
    .map(event => event.period)
    .filter(value => value !== null && value !== undefined && String(value).trim() !== "")
    .map(value => String(value)))].sort((a, b) => Number(a) - Number(b) || a.localeCompare(b));
  periodSelect.replaceChildren(new Option("All halves", ""));
  halves.forEach(value => periodSelect.add(new Option(halfLabel(value), value)));
  periodSelect.value = halves.includes(previousValue) ? previousValue : "";
}

function updatePlayerOptions() {
  const selectedTeam = teamSelect.value;
  const teamEvents = allEvents.filter(event =>
    !selectedTeam || String(event.team_id) === selectedTeam
  );
  fillSelect(
    playerSelect,
    teamEvents,
    playerKey,
    event => event.playerName || "No named player",
    "All players"
  );
}

function getFilters() {
  return {
    teamId: teamSelect.value,
    playerId: playerSelect.value,
    actionId: actionSelect.value,
    period: periodSelect.value
  };
}

function getSelection() {
  return {
    selectionId,
    matchId: allEvents[0]?.FXID ?? null,
    filters: getFilters(),
    filteredRows: selectedEvents.slice()
  };
}

function updateDashboard() {
  const filters = getFilters();
  selectedEvents = allEvents.filter(event => {
    const matchesTeam = !filters.teamId || String(event.team_id) === filters.teamId;
    const matchesPlayer = !filters.playerId || playerKey(event) === filters.playerId;
    const matchesAction = !filters.actionId || String(event.action) === filters.actionId;
    const matchesHalf = !filters.period || String(event.period) === filters.period;
    return matchesTeam && matchesPlayer && matchesAction && matchesHalf;
  });

  const namedPlayers = new Set();
  const actions = new Set();
  for (const event of selectedEvents) {
    if (event.playerName) namedPlayers.add(playerKey(event));
    actions.add(String(event.action));
  }
  const recordCount = selectedEvents.length.toLocaleString("en-AU");
  document.getElementById("eventCount").textContent = recordCount;
  document.getElementById("playerCount").textContent = namedPlayers.size;
  document.getElementById("actionCount").textContent = actions.size;
  document.getElementById("selectionInfo").textContent = recordCount + " matching records";
  currentPage = 0;
  showPage();
  selectionId++;
  const selection = getSelection();
  window.RedsAnalysis.updateSelection(selection);
  window.dispatchEvent(new CustomEvent("dashboard:filters-changed", {
    detail: selection
  }));
}

// MatchTime is MMSS: 8002 becomes 80:02.
function formatClock(value) {
  if (value === null || value === undefined || value === "") return "Not recorded";
  const clock = Number(value);
  if (!Number.isInteger(clock) || clock < 0 || clock % 100 >= 60) return "Not recorded";
  const minutes = Math.floor(clock / 100);
  const seconds = String(clock % 100).padStart(2, "0");
  return minutes + ":" + seconds;
}

function showPage() {
  const tableBody = document.getElementById("eventRows");
  tableBody.replaceChildren();
  const start = currentPage * pageSize;
  const pageEvents = selectedEvents.slice(start, start + pageSize);
  pageEvents.forEach(event => {
    const row = document.createElement("tr");
    const half = event.period === null || event.period === undefined || String(event.period).trim() === ""
      ? "Not recorded"
      : halfLabel(event.period);
    const cells = [
      formatClock(event.MatchTime),
      half,
      event.teamName,
      event.playerName || "Not recorded",
      actionLabel(event),
      event.ActionResultName || "Not recorded"
    ];
    cells.forEach(value => {
      const cell = document.createElement("td");
      cell.textContent = value ?? "Not recorded";
      row.appendChild(cell);
    });
    tableBody.appendChild(row);
  });

  if (selectedEvents.length === 0) {
    const row = tableBody.insertRow();
    const cell = row.insertCell();
    cell.colSpan = 6;
    cell.className = "empty";
    cell.textContent = "No matching events. Change a filter or select Reset filters.";
  }
  const totalPages = Math.ceil(selectedEvents.length / pageSize);
  const pageInfo = document.getElementById("pageInfo");
  if (totalPages === 0) {
    pageInfo.textContent = "0 matching records";
  } else {
    pageInfo.textContent = "Page " + (currentPage + 1) + " of " + totalPages
      + " · " + pageSize + " rows per page";
  }
  document.getElementById("previous").disabled = currentPage === 0;
  document.getElementById("next").disabled = currentPage + 1 >= totalPages;
}

function resetFilters() {
  teamSelect.value = "";
  updatePlayerOptions();
  actionSelect.value = "";
  periodSelect.value = "";
  updateDashboard();
}

function loadData(events) {
  if (!Array.isArray(events)) {
    throw new Error("Provide an array of raw event objects.");
  }
  const invalidEvent = events.some(event =>
    !event || typeof event !== "object" || Array.isArray(event)
  );
  if (invalidEvent) {
    throw new Error("Provide an array of raw event objects.");
  }
  if (new Set(events.map(event => String(event.FXID))).size > 1) {
    throw new Error("This basic dashboard displays one match at a time.");
  }
  allEvents = events.slice();
  fillSelect(
    teamSelect,
    allEvents,
    event => String(event.team_id),
    event => event.teamName || "Unknown team",
    "All teams"
  );
  fillSelect(actionSelect, allEvents, event => String(event.action), actionLabel, "All actions");
  updateHalfOptions(allEvents);
  const first = allEvents[0] || {};
  let matchTitle = allEvents.length ? "Match events" : "No match events found";
  if (first.homeTeamName && first.awayTeamName) {
    matchTitle = first.homeTeamName + " vs " + first.awayTeamName;
  }
  const matchDetails = [
    String(first.datePlayed || "").slice(0, 10),
    first.venueName,
    allEvents.length.toLocaleString("en-AU") + " event records"
  ];
  document.getElementById("matchTitle").textContent = matchTitle;
  document.getElementById("matchDetails").textContent = matchDetails.filter(Boolean).join(" · ");
  resetFilters();
}

teamSelect.addEventListener("change", () => {
  updatePlayerOptions();
  updateDashboard();
});
for (const select of [playerSelect, actionSelect, periodSelect]) {
  select.addEventListener("change", updateDashboard);
}
document.getElementById("reset").addEventListener("click", resetFilters);
document.getElementById("previous").addEventListener("click", () => {
  currentPage--;
  showPage();
});
document.getElementById("next").addEventListener("click", () => {
  currentPage++;
  showPage();
});

window.RedsDashboard = {
  getFilters,
  getSelection,
  getFilteredRows: () => selectedEvents.slice(),
  setData: loadData,
  setAnalysisLoader: window.RedsAnalysis.setLoader,
  setAnalysis: window.RedsAnalysis.showResult
};
(async function initialiseDashboard() {
  try {
    const response = await fetch("/api/events");
    const payload = await response.json().catch(() => ({}));
    if (!response.ok) {
      throw new Error(payload.error || "The database API returned HTTP " + response.status + ".");
    }
    if (!Array.isArray(payload.events)) {
      throw new Error("The database API response does not contain an events array.");
    }
    loadData(payload.events);
  } catch (error) {
    console.error("Could not load SQLite event data:", error);
    document.getElementById("matchTitle").textContent = "Database data unavailable";
    document.getElementById("matchDetails").textContent = error.message;
    document.getElementById("eventCount").textContent = "0";
    document.getElementById("playerCount").textContent = "0";
    document.getElementById("actionCount").textContent = "0";
    document.getElementById("selectionInfo").textContent = "No database records loaded.";
    document.getElementById("analysisStatus").textContent = "Analysis requires records from MainDB.db.";
    const tableBody = document.getElementById("eventRows");
    tableBody.replaceChildren();
    const row = tableBody.insertRow();
    const cell = row.insertCell();
    cell.colSpan = 6;
    cell.className = "empty";
    cell.textContent = "Database records could not be loaded. Ensure database is in the project root and contains the AllData table.";
    document.getElementById("pageInfo").textContent = "0 matching records";
    document.getElementById("previous").disabled = true;
    document.getElementById("next").disabled = true;
  }
})();
