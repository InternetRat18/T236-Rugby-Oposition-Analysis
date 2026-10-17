"use strict";

const analysisStatus = document.getElementById("analysisStatus");
const refreshButton = document.getElementById("refreshAnalysis");
const chartContainers = [
  document.getElementById("actionChart"),
  document.getElementById("fieldChart")
];
const chartTitles = [
  document.getElementById("actionChartTitle"),
  document.getElementById("fieldChartTitle")
];
let analysisLoader = null;
let analysisSelection = null;
let analysisRequest = 0;

function resetCharts(message) {
  chartTitles[0].textContent = "Action breakdown";
  chartTitles[1].textContent = "Additional analysis";
  chartContainers.forEach(container => {
    container.className = "placeholder";
    container.removeAttribute("role");
    container.textContent = message;
  });
}

function validateCharts(result) {
  if (!result || !Array.isArray(result.charts) || result.charts.length > 2) {
    throw new Error("Provide a charts array with up to two charts.");
  }
  for (const chart of result.charts) {
    if (!chart || typeof chart.title !== "string" || !chart.title.trim()
      || !Array.isArray(chart.data)) {
      throw new Error("Each chart needs a title and a data array.");
    }
    if (chart.unit !== undefined && typeof chart.unit !== "string") {
      throw new Error("Chart units must be text.");
    }
    for (const item of chart.data) {
      if (!item || typeof item.label !== "string" || !item.label.trim()
        || !Number.isFinite(item.value) || item.value < 0) {
        throw new Error("Chart items need a label and a non-negative numeric value.");
      }
    }
  }
}

// Values are supplied by the analysis module. Only the bar width is calculated here.
function drawBarChart(container, chart) {
  if (chart.data.length === 0) {
    container.textContent = "No results for this selection.";
    return;
  }
  container.className = "bar-chart";
  container.setAttribute("role", "list");
  container.replaceChildren();
  let maximum = 1;
  chart.data.forEach(item => maximum = Math.max(maximum, item.value));

  chart.data.forEach(item => {
    const row = document.createElement("div");
    row.className = "chart-row";
    row.setAttribute("role", "listitem");
    const label = document.createElement("span");
    label.className = "chart-label";
    label.textContent = item.label;
    const track = document.createElement("div");
    track.className = "bar-track";
    track.setAttribute("aria-hidden", "true");
    const bar = document.createElement("div");
    bar.className = "bar";
    bar.style.width = (item.value / maximum * 100) + "%";
    track.appendChild(bar);
    const value = document.createElement("span");
    value.className = "chart-value";
    value.textContent = String(item.value) + (chart.unit || "");
    row.append(label, track, value);
    container.appendChild(row);
  });
}

function showAnalysis(result, selectionId) {
  if (!analysisSelection || selectionId !== analysisSelection.selectionId
    || analysisSelection.filteredRows.length === 0) return false;
  validateCharts(result);
  analysisRequest++;
  resetCharts("No chart supplied for this selection.");
  result.charts.forEach((chart, index) => {
    chartTitles[index].textContent = chart.title;
    drawBarChart(chartContainers[index], chart);
  });
  analysisStatus.textContent = result.charts.length
    ? "Analysis updated for the current selection."
    : "No analysis results for this selection.";
  return true;
}

async function refreshAnalysis() {
  const request = ++analysisRequest;
  const selection = analysisSelection;
  resetCharts("No analysis results for this selection.");
  refreshButton.disabled = !analysisLoader || !selection || !selection.filteredRows.length;
  if (!selection || !selection.filteredRows.length) {
    analysisStatus.textContent = "No matching events to analyse.";
    return false;
  }
  if (!analysisLoader) {
    analysisStatus.textContent = "Analysis is not available yet.";
    return false;
  }
  resetCharts("Loading analysis...");
  analysisStatus.textContent = "Loading analysis...";
  try {
    const result = await analysisLoader(selection);
    // Ignore a response if the user has changed filters or refreshed again.
    if (request !== analysisRequest) return false;
    return showAnalysis(result, selection.selectionId);
  } catch (error) {
    if (request !== analysisRequest) return false;
    resetCharts("Analysis could not be loaded.");
    analysisStatus.textContent = "Analysis could not be loaded. Try Refresh analysis.";
    console.error("Analysis loading failed:", error);
    return false;
  }
}

function setAnalysisLoader(loader) {
  if (loader !== null && typeof loader !== "function") {
    throw new Error("Provide an analysis loader function, or null to disconnect it.");
  }
  analysisLoader = loader;
  return refreshAnalysis();
}

function updateAnalysisSelection(selection) {
  analysisSelection = selection;
  return refreshAnalysis();
}

refreshButton.addEventListener("click", refreshAnalysis);
window.RedsAnalysis = {
  updateSelection: updateAnalysisSelection,
  setLoader: setAnalysisLoader,
  showResult: showAnalysis
};
