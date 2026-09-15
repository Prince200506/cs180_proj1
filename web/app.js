const groups = [
  {
    gridId: "results-grid",
    countId: "results-count",
    prefix: "code/results",
    files: [
      "cathedral.jpg",
      "church.jpg",
      "emir.jpg",
      "harvesters.jpg",
      "icon.jpg",
      "ilemselga.jpg",
      "melons.jpg",
      "monastery.jpg",
      "religous_painting.jpg",
      "self_portrait.jpg",
      "siren.jpg",
      "three_generations.jpg",
      "tobolsk.jpg",
      "wharf.jpg"
    ]
  },
  {
    gridId: "test-results-grid",
    countId: "test-results-count",
    prefix: "code/test_results",
    files: [
      "test1_jpg.jpg",
      "test1_tif.jpg",
      "test2_jpg.jpg",
      "test2_tif.jpg",
      "test3_jpg.jpg",
      "test3_tif.jpg",
      "test4_jpg.jpg",
      "test4_tif.jpg"
    ]
  }
];

function renderGroup(group) {
  const grid = document.getElementById(group.gridId);
  const count = document.getElementById(group.countId);

  if (!grid || !count) return;

  count.textContent = `${group.files.length} images`;

  for (const file of group.files) {
    const url = `${group.prefix}/${encodeURIComponent(file)}`;

    const card = document.createElement("article");
    card.className = "card";

    card.innerHTML = `
      <a href="${url}" target="_blank" rel="noopener noreferrer">
        <img class="thumb" src="${url}" alt="${file}" loading="lazy" />
        <div class="caption">
          <p class="name">${file}</p>
        </div>
      </a>
    `;

    grid.appendChild(card);
  }
}

for (const group of groups) {
  renderGroup(group);
}