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

function drawPieChart(container, chart) {
  if (chart.data.length === 0) {
    container.className = "placeholder";
    container.textContent = "No results for this selection.";
    return;
  }
  container.className = "pie-chart-layout";
  container.removeAttribute("role");
  container.replaceChildren();
  const total = chart.data.reduce((sum, item) => sum + item.value, 0);
  if (total <= 0) {
    container.textContent = "No results for this selection.";
    return;
  }

  const colors = ["#2563eb", "#0f766e", "#f59e0b", "#9333ea", "#dc2626",
    "#0891b2", "#65a30d", "#db2777", "#64748b", "#ea580c", "#4f46e5", "#059669"];
  const svgNS = "http://www.w3.org/2000/svg";
  const svg = document.createElementNS(svgNS, "svg");
  svg.setAttribute("viewBox", "0 0 220 220");
  svg.setAttribute("class", "pie-chart");
  svg.setAttribute("role", "img");
  svg.setAttribute("aria-label", chart.title + ": " + chart.data.map(item => item.label + " " + item.value).join(", "));
  let angle = -Math.PI / 2;
  chart.data.forEach((item, index) => {
    if (item.value <= 0) return;
    const slice = item.value / total * Math.PI * 2;
    const end = angle + slice;
    const x1 = 110 + 96 * Math.cos(angle);
    const y1 = 110 + 96 * Math.sin(angle);
    const x2 = 110 + 96 * Math.cos(end);
    const y2 = 110 + 96 * Math.sin(end);
    const path = document.createElementNS(svgNS, "path");
    if (item.value === total) {
      path.setAttribute("d", "M 110 14 A 96 96 0 1 1 109.99 14 Z");
    } else {
      path.setAttribute("d", `M 110 110 L ${x1} ${y1} A 96 96 0 ${slice > Math.PI ? 1 : 0} 1 ${x2} ${y2} Z`);
    }
    path.setAttribute("fill", colors[index % colors.length]);
    path.setAttribute("stroke", "#ffffff");
    path.setAttribute("stroke-width", "2");
    const title = document.createElementNS(svgNS, "title");
    title.textContent = `${item.label}: ${item.value} (${(item.value / total * 100).toFixed(1)}%)`;
    path.appendChild(title);
    svg.appendChild(path);
    angle = end;
  });

  const legend = document.createElement("div");
  legend.className = "pie-legend";
  chart.data.forEach((item, index) => {
    const row = document.createElement("div");
    row.className = "pie-legend-row";
    const swatch = document.createElement("span");
    swatch.className = "pie-swatch";
    swatch.style.backgroundColor = colors[index % colors.length];
    swatch.setAttribute("aria-hidden", "true");
    const label = document.createElement("span");
    label.className = "pie-legend-label";
    label.textContent = item.label;
    const value = document.createElement("strong");
    value.className = "pie-legend-value";
    value.textContent = `${item.value} (${(item.value / total * 100).toFixed(1)}%)`;
    row.append(swatch, label, value);
    legend.appendChild(row);
  });
  container.append(svg, legend);
}

function showAnalysis(result, selectionId) {
  if (!analysisSelection || selectionId !== analysisSelection.selectionId
    || analysisSelection.filteredRows.length === 0) return false;
  validateCharts(result);
  analysisRequest++;
  resetCharts("No chart supplied for this selection.");
  result.charts.forEach((chart, index) => {
    chartTitles[index].textContent = chart.title;
    if (index === 0) drawPieChart(chartContainers[index], chart);
    else drawBarChart(chartContainers[index], chart);
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
