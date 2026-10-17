"use strict";

const analysisUrl = "/api/analysis";

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
    let message = "Analysis request failed with status " + response.status;
    try {
      const error = await response.json();
      if (error.error) message = error.error;
    } catch (_) {}
    throw new Error(message);
  }
  return response.json();
});
