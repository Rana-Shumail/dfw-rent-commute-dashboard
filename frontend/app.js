const hubSelect = document.getElementById("hubSelect");
const weightRange = document.getElementById("weightRange");
const weightDisplay = document.getElementById("weightDisplay");
const resultsList = document.getElementById("resultsList");

async function fetchTradeoffs() {
  const hubId = hubSelect.value;
  const rentWeight = parseFloat(weightRange.value);
  const commuteWeight = (1.0 - rentWeight).toFixed(2);

  // Update label
  const rentPct = Math.round(rentWeight * 100);
  const commutePct = Math.round(commuteWeight * 100);
  weightDisplay.textContent = `${rentPct}% Rent / ${commutePct}% Commute`;

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/api/tradeoff?hub_id=${hubId}&rent_weight=${rentWeight}`
    );

    if (!response.ok) {
      throw new Error(`Server returned HTTP ${response.status}`);
    }

    const payload = await response.json();
    renderRankings(payload.data);
  } catch (error) {
    resultsList.innerHTML = `<p style="color: #ef4444;">Failed to load data: ${error.message}</p>`;
  }
}

function renderRankings(neighborhoods) {
  if (!neighborhoods || neighborhoods.length === 0) {
    resultsList.innerHTML = "<p>No data returned for this hub.</p>";
    return;
  }

  resultsList.innerHTML = neighborhoods
    .map(
      (item, idx) => `
      <div class="item">
        <div class="item-rank">#${idx + 1}</div>
        <div class="item-details">
          <div class="item-title">${item.neighborhood}, ${item.city}</div>
          <div class="item-metrics">
            $${item.rent.toLocaleString()}/mo • ${item.commute_mins} mins (${item.distance_miles} mi)
          </div>
        </div>
        <div class="score-badge">Score: ${item.score}</div>
      </div>
    `
    )
    .join("");
}

// Event Listeners
hubSelect.addEventListener("change", fetchTradeoffs);
weightRange.addEventListener("input", fetchTradeoffs);

// Initial Load
fetchTradeoffs();