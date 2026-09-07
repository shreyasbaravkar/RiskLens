async function loadData() {
  const response = await fetch("data/risk_scores.json");
  const countries = await response.json();
  return countries;
}

// Small helper: format numbers cleanly, show "—" for missing data instead of "null"
function fmt(value) {
  return value === null || value === undefined ? "—" : value.toFixed(1);
}

function renderOverviewCards(countries) {
  const container = document.getElementById("overview-cards");

  // Only count countries where we actually have a valid score
  const scored = countries.filter(c => c.risk_score !== null && c.risk_score !== undefined);

  const highRisk = scored.filter(c => c.risk_level === "High Risk").length;
  const avgScore = (scored.reduce((sum, c) => sum + c.risk_score, 0) / scored.length).toFixed(1);
  const riskiest = scored[0]; // already sorted riskiest-first from Python

  container.innerHTML = `
    <div class="card">
      <span class="card-label">Countries Tracked</span>
      <span class="card-value">${countries.length}</span>
    </div>
    <div class="card">
      <span class="card-label">High Risk Countries</span>
      <span class="card-value">${highRisk}</span>
    </div>
    <div class="card">
      <span class="card-label">Average Risk Score</span>
      <span class="card-value">${avgScore}</span>
    </div>
    <div class="card">
      <span class="card-label">Highest Risk</span>
      <span class="card-value">${riskiest.country}</span>
    </div>
  `;
}

function renderScorecardTable(countries) {
  const table = document.getElementById("scorecard-table");

  let html = `
    <tr>
      <th>Country</th>
      <th>GDP Growth</th>
      <th>Inflation</th>
      <th>Debt/GDP</th>
      <th>Unemployment</th>
      <th>Risk Score</th>
      <th>Risk Level</th>
    </tr>
  `;

  countries.forEach(c => {
    html += `
      <tr class="risk-${c.risk_level.replace(" ", "-").toLowerCase()}">
        <td>${c.country}</td>
        <td>${fmt(c.gdp_growth)}</td>
        <td>${fmt(c.inflation)}</td>
        <td>${fmt(c.debt_to_gdp)}</td>
        <td>${fmt(c.unemployment)}</td>
        <td>${c.risk_score ?? "—"}</td>
        <td>${c.risk_level}</td>
      </tr>
    `;
  });

  table.innerHTML = html;
}

function renderChart(countries) {
  const scored = countries.filter(c => c.risk_score !== null && c.risk_score !== undefined);

  const ctx = document.getElementById("riskChart");

  new Chart(ctx, {
    type: "bar",
    data: {
      labels: scored.map(c => c.country),
      datasets: [{
        label: "Risk Score",
        data: scored.map(c => c.risk_score),
        backgroundColor: scored.map(c => {
          if (c.risk_level === "High Risk") return "#dc2626";
          if (c.risk_level === "Moderate Risk") return "#ca8a04";
          return "#16a34a";
        })
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false }
      },
      scales: {
        y: { beginAtZero: true, max: 100, ticks: { color: "#555" } },
        x: { ticks: { color: "#555" } }
      }
    }
  });
}

function renderHighRiskCards(countries) {
  const scored = countries.filter(c => c.risk_score !== null && c.risk_score !== undefined);
  const top3 = scored.slice(0, 3);
  const container = document.getElementById("high-risk-cards");

  container.innerHTML = top3.map(c => `
    <div class="card spotlight-card">
      <span class="card-label">${c.country}</span>
      <span class="card-value">${c.risk_score}</span>
      <span class="card-detail">Inflation: ${fmt(c.inflation)}% · Debt/GDP: ${fmt(c.debt_to_gdp)}%</span>
    </div>
  `).join("");
}

function renderLowRiskCards(countries) {
  const scored = countries.filter(c => c.risk_score !== null && c.risk_score !== undefined);
  const bottom3 = scored.slice(-3).reverse();
  const container = document.getElementById("low-risk-cards");

  container.innerHTML = bottom3.map(c => `
    <div class="card spotlight-card safe">
      <span class="card-label">${c.country}</span>
      <span class="card-value">${c.risk_score}</span>
      <span class="card-detail">GDP Growth: ${fmt(c.gdp_growth)}% · Unemployment: ${fmt(c.unemployment)}%</span>
    </div>
  `).join("");
}

function renderTakeaways(countries) {
  const scored = countries.filter(c => c.risk_score !== null && c.risk_score !== undefined);
  const riskiest = scored[0];
  const safest = scored[scored.length - 1];
  const missing = countries.length - scored.length;

  const takeaways = [
    `${riskiest.country} carries the highest composite risk score (${riskiest.risk_score}), driven largely by inflation and debt levels.`,
    `${safest.country} is the most stable economy tracked, with a risk score of ${safest.risk_score}.`,
    `${missing} of ${countries.length} tracked countries have incomplete debt data and are excluded from scoring until updated figures are published.`
  ];

  document.getElementById("takeaways-list").innerHTML =
    takeaways.map(t => `<li>${t}</li>`).join("");
}

async function init() {
  const countries = await loadData();
  renderOverviewCards(countries);
  renderScorecardTable(countries);
  renderChart(countries);
  renderHighRiskCards(countries);
  renderLowRiskCards(countries);
  renderTakeaways(countries);
}

init();