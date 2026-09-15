const finalResults = {
  signalAligner: [
    "cathedral.jpg",
    "monastery.jpg",
    "tobolsk.jpg"
  ],
  pyramid: [
    "church.jpg",
    "emir.jpg",
    "harvesters.jpg",
    "icon.jpg",
    "ilemselga.jpg",
    "melons.jpg",
    "religous_painting.jpg",
    "self_portrait.jpg",
    "siren.jpg",
    "three_generations.jpg",
    "wharf.jpg"
  ]
};

const testResults = [
  {
    sample: "test2",
    variants: [
      { label: "Signal aligner", file: "test2_jpg.jpg" },
      { label: "Pyramid", file: "test2_tif.jpg" }
    ]
  },
  {
    sample: "test3",
    variants: [
      { label: "Signal aligner", file: "test3_jpg.jpg" },
      { label: "Pyramid", file: "test3_tif.jpg" }
    ]
  },
  {
    sample: "test4",
    variants: [
      { label: "Signal aligner", file: "test4_jpg.jpg" },
      { label: "Pyramid", file: "test4_tif.jpg" }
    ]
  }
];

function createCard(prefix, file, label, wide = false) {
  const url = `${prefix}/${encodeURIComponent(file)}`;
  const card = document.createElement("article");
  card.className = wide ? "card card--wide" : "card";

  card.innerHTML = `
    <a href="${url}" target="_blank" rel="noopener noreferrer">
      <div class="badge">${label}</div>
      <img class="thumb" src="${url}" alt="${file}" loading="lazy" />
      <div class="caption">
        <p class="name">${file}</p>
      </div>
    </a>
  `;

  return card;
}

function renderFinalResults() {
  const section = document.getElementById("results-grid");
  const count = document.getElementById("results-count");

  if (!section || !count) return;

  const total = finalResults.signalAligner.length + finalResults.pyramid.length;
  count.textContent = `${total} images`;

  const signalBlock = document.createElement("div");
  signalBlock.className = "subsection";
  signalBlock.innerHTML = `<h3>Signal aligner</h3>`;

  const signalStack = document.createElement("div");
  signalStack.className = "stack";

  for (const file of finalResults.signalAligner) {
    signalStack.appendChild(createCard("code/results", file, "Signal aligner", true));
  }

  signalBlock.appendChild(signalStack);
  section.appendChild(signalBlock);

  const pyramidBlock = document.createElement("div");
  pyramidBlock.className = "subsection";
  pyramidBlock.innerHTML = `<h3>Pyramid</h3>`;

  const pyramidGrid = document.createElement("div");
  pyramidGrid.className = "grid";

  for (const file of finalResults.pyramid) {
    pyramidGrid.appendChild(createCard("code/results", file, "Pyramid"));
  }

  pyramidBlock.appendChild(pyramidGrid);
  section.appendChild(pyramidBlock);
}

function renderTestResults() {
  const section = document.getElementById("test-results-grid");
  const count = document.getElementById("test-results-count");

  if (!section || !count) return;

  count.textContent = `${testResults.length} rows`;

  const rows = document.createElement("div");
  rows.className = "rows";

  for (const item of testResults) {
    const row = document.createElement("div");
    row.className = "result-row";

    const title = document.createElement("div");
    title.className = "row-title";
    title.textContent = item.sample;
    row.appendChild(title);

    const pair = document.createElement("div");
    pair.className = "pair-grid";

    for (const variant of item.variants) {
      pair.appendChild(createCard("code/test_results", variant.file, variant.label));
    }

    row.appendChild(pair);
    rows.appendChild(row);
  }

  section.appendChild(rows);
}

renderFinalResults();
renderTestResults();