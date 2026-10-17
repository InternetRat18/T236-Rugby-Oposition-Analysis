# Opposition dashboard

Rui's webpage, filters and UI integration module. The analysis values come from
JiaLin's Python module. The Power BI prototype is a reference for the insights
and visualisations the team wants to show.

## Open the page

Open `index.html` in a browser. To edit, open this folder in VS Code, save a
source change and refresh the page. No installation is needed for the offline
event preview. `Rui_Dashboard_Preview.html` is a standalone snapshot of these
files; source edits do not update that snapshot.

| File | Purpose |
| --- | --- |
| index.html | Page sections, filter controls, charts and event table |
| styles.css | Colours, spacing and smaller-screen layout |
| dashboard.js | Event filtering, summary counts and table pages |
| analysis.js | Display supplied chart values and handle loading states |
| integration.js | Connection to the team's analysis service |
| sample-data.js | Supplied match events, unchanged from the previous handoff |

## Working features

Team, Player, Action and Half filters apply together. Changing Team clears the
Player choice. Reset restores NSW Waratahs and clears the other filters. The
table shows 15 rows per page. Cards count event rows, named players and action
IDs; these are not possession or success-rate calculations.

The chart renderer accepts up to two category bar charts. It uses the titles,
labels, values and units provided by the analysis module. Values are not derived
from the raw events in `analysis.js`. Chart types can be revised when the team
confirms the Power BI reference and actual analysis output.

## Connect the analysis

The connection is not live yet: neither the backend route nor JiaLin's output
format has been provided. The following is a proposed interface for the handoff.

1. Agree the route and JSON format with JiaLin and the backend developer.
2. Set `analysisUrl` in `integration.js`. The example sends a POST with
   `matchId`, `filters` and the selected `eventIds`. Adjust this adapter to the
   agreed backend contract. Do not put credentials in the source files.
3. Return a result in the format below. The example value is the verified
   NSW Waratahs Kick total from the supplied workbook, not a live Python result.
4. Serve the page over HTTP for the backend connection. Using the same origin
   as the backend avoids needing a separate CORS configuration.

```json
{
  "charts": [
    {
      "title": "Kick events",
      "unit": "",
      "data": [{ "label": "NSW Waratahs", "value": 37 }]
    }
  ]
}
```

Each chart needs a non-empty `title` and a `data` array. Each item needs a text
`label` and a numeric `value` of zero or greater. `unit` is an optional suffix,
such as `%`. An empty data array displays an empty state. More than two charts
or invalid values produce an error rather than partial results.

`setAnalysisLoader` registers a function that receives the current selection
and returns the result, or a Promise for it. Registration processes the initial
selection too. Subsequent filter changes reload analysis automatically.

For an existing connection that returns results through a different mechanism:

```javascript
const selection = window.RedsDashboard.getSelection();
// After obtaining the result for this selection:
window.RedsDashboard.setAnalysis(result, selection.selectionId);
```

Keep the captured `selectionId` with its result. Results for an old selection
are ignored. Do not obtain a new ID when an old request finishes.

Other entry points remain available:

```javascript
window.RedsDashboard.getFilters();
window.RedsDashboard.getFilteredRows();
window.RedsDashboard.setData(rawEvents);
window.RedsDashboard.setAnalysisLoader(null); // disconnect the loader
```

The `dashboard:filters-changed` event includes `selectionId`, `matchId`,
`filters` and `filteredRows`. The filters use strings: `teamId`, `actionId`,
`period`, and a `playerId` formatted as `team_id:PLID`. The player value
`unnamed` selects events without a named player. Empty strings mean all.
The example adapter sends event IDs as well, so the backend can use the exact
selection. Python and SQLite are not executed inside the browser.

## Source data and handoff status

All 3,588 event rows and 88 fields from `949231_REDSvWARA_BI.xlsx`, sheet `in`,
are retained. Waratahs has 2,063 rows; Reds has 1,525. `MatchTime` uses MMSS:
`8002` becomes `80:02`. Missing names/results remain missing, and unlabelled
actions keep their IDs. All original fields are available in the filtered rows.

Rui handles webpage layout, filters and displaying the analysis results. JiaLin
handles reusable Python analysis functions and their chart data. Daniel's
processed events can be passed to `setData` as objects with the source column
names. The actual backend connection and its data mapping still need team
integration testing. The Week 11 WIP copy is a separate, unchanged prototype.
