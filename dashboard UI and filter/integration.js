"use strict";

// Set this after the team agrees the analysis route and request format.
const analysisUrl = "";

if (analysisUrl) {
  window.RedsDashboard.setAnalysisLoader(async selection => {
    const response = await fetch(analysisUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        matchId: selection.matchId,
        filters: selection.filters,
        eventIds: selection.filteredRows.map(event => event.ID)
      })
    });
    if (!response.ok) {
      throw new Error("Analysis request failed with status " + response.status);
    }
    return response.json();
  });
}
