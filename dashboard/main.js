// Task 4.2: Prompt Augmentation Matrix
const promptMatrix = {
  explanation_depth: [
    { range: [0.0, 0.3], text: "Explain using simple metaphors (ELI5)." },
    { range: [0.3, 0.7], text: "Balance theory with practical examples." },
    { range: [0.7, 1.0], text: "Use deep technical and academic terminology." }
  ],
  humor_density: [
    { range: [0.0, 0.2], text: "Strictly professional. No humor." },
    { range: [0.2, 0.5], text: "Occasional dry wit and lightheartedness." },
    { range: [0.5, 1.0], text: "Playful, ironic, and frequent use of puns." }
  ],
  logical_rigor: [
    { range: [0.0, 0.5], text: "Focus on intuitive patterns and snapshots." },
    { range: [0.5, 1.0], text: "Show hyper-logical step-by-step reasoning." }
  ],
  assertiveness: [
    { range: [0.0, 0.5], text: "Be humble and concede when challenged." },
    { range: [0.5, 1.0], text: "Firmly defend logic and assert boundaries." }
  ]
};

// Mocking the L2 Genome Data
const genomeData = {
  version: "1.0.0",
  metadata: { persona_id: "pioneer_v2" },
  loci: [
    {
      id: "explanation_depth",
      category: "cognitive",
      description: "Preference for abstract theory vs concrete examples",
      distribution: { type: "range", values: { min: 0.2, max: 0.5, default: 0.35 } },
      weight: 0.8,
      variability: 0.2
    },
    {
      id: "humor_density",
      category: "style",
      description: "Frequency and intensity of humorous interjections",
      distribution: { type: "range", values: { min: 0.05, max: 0.45, default: 0.2 } },
      weight: 0.6,
      variability: 0.5
    },
    {
      id: "logical_rigor",
      category: "cognitive",
      description: "Analytical depth vs intuitive jumps",
      distribution: { type: "range", values: { min: 0.4, max: 0.9, default: 0.7 } },
      weight: 0.9,
      variability: 0.1
    },
    {
      id: "assertiveness",
      category: "value",
      description: "Willingness to defend or concede a position",
      distribution: { type: "range", values: { min: 0.3, max: 0.8, default: 0.5 } },
      weight: 0.7,
      variability: 0.4
    }
  ]
};

document.addEventListener('DOMContentLoaded', () => {
  const traitList = document.getElementById('trait-list');
  const influenceSlider = document.getElementById('influence-slider');
  const sampleBtn = document.getElementById('sample-btn');
  const eventLog = document.getElementById('event-log');
  const modeSocial = document.getElementById('mode-social');
  const modeStrict = document.getElementById('mode-strict');
  const intCountSpan = document.getElementById('int-count');
  const historyContainer = document.getElementById('history-container');
  const promptOutput = document.getElementById('prompt-output');

  // State
  let currentInfluence = 1.0;
  let interactionCount = 0;
  let currentState = 'FORMING';
  const driftMultiplier = 0.05;
  const history = [];

  // Initial Render
  renderGenome();

  function renderGenome() {
    traitList.innerHTML = '';
    genomeData.loci.forEach(locus => {
      const card = document.createElement('div');
      card.className = 'trait-card';

      const { min, max, default: def } = locus.distribution.values;

      card.innerHTML = `
        <div class="trait-header">
          <span class="trait-name">${locus.id.replace(/_/g, ' ')}</span>
          <span class="trait-category">${locus.category}</span>
        </div>
        <div style="font-size: 0.75rem; color: #94a3b8; margin-bottom: 0.8rem;">${locus.description}</div>
        <div class="dna-track" id="track-${locus.id}">
          <div class="scanning"></div>
          <div class="gene-boundary" id="boundary-${locus.id}" style="left: ${min * 100}%; width: ${(max - min) * 100}%"></div>
          <div class="default-marker" id="marker-${locus.id}" style="left: ${def * 100}%"></div>
          <div class="current-sample" id="sample-${locus.id}" style="left: ${def * 100}%; opacity: 0;"></div>
          <div class="ghost-sample" id="ghost-${locus.id}" style="left: 0%; opacity: 0;"></div>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 0.6rem; color: #475569; margin-top: 0.4rem;">
          <span>0.0</span>
          <span>Boundary: [${min.toFixed(2)} - ${max.toFixed(2)}]</span>
          <span>1.0</span>
        </div>
        <div class="feedback-controls">
          <button class="feedback-btn minus" data-id="${locus.id}">- Drift Left</button>
          <button class="feedback-btn plus" data-id="${locus.id}">+ Drift Right</button>
        </div>
      `;
      traitList.appendChild(card);
    });

    document.querySelectorAll('.feedback-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const id = e.target.getAttribute('data-id');
        const direction = e.target.classList.contains('plus') ? 1 : -1;
        applyDrift(id, direction);
      });
    });
  }

  function addLog(message, type = '') {
    const entry = document.createElement('div');
    entry.className = `log-entry ${type}`;
    const now = new Date().toLocaleTimeString('en-GB', { hour12: false });
    entry.innerHTML = `<span style="color: #475569">[${now}]</span> ${message}`;
    eventLog.prepend(entry);
    if (eventLog.children.length > 20) eventLog.removeChild(eventLog.lastChild);
  }

  function applyDrift(traitId, direction) {
    if (currentState === 'LOCKED') return;
    const locus = genomeData.loci.find(l => l.id === traitId);
    const variability = locus.variability;
    const delta = direction * variability * driftMultiplier;
    const dist = locus.distribution.values;
    dist.default = Math.max(dist.min, Math.min(dist.max, dist.default + delta));
    updateTraitUI(traitId);
    addLog(`Drifting '${traitId}': New Default -> ${dist.default.toFixed(3)}`, 'drift');
    recordInteraction(0.2);
  }

  function updateTraitUI(traitId) {
    const locus = genomeData.loci.find(l => l.id === traitId);
    const { default: def } = locus.distribution.values;
    const marker = document.getElementById(`marker-${traitId}`);
    marker.style.left = `${def * 100}%`;
  }

  function recordInteraction(weight = 1) {
    interactionCount += weight;
    intCountSpan.innerText = Math.floor(interactionCount);
    const oldState = currentState;
    if (currentState === 'FORMING' && interactionCount >= 5) currentState = 'STABILIZING';
    else if (currentState === 'STABILIZING' && interactionCount >= 15) currentState = 'STABLE';
    else if (currentState === 'STABLE' && interactionCount >= 30) {
      currentState = 'LOCKED';
      document.body.classList.add('is-locked');
      addLog("🚫 PERSONA LOCKED.", "degraded");
    }
    if (oldState !== currentState) updateFSMUI(oldState, currentState);
  }

  function updateFSMUI(oldS, newS) {
    addLog(`🔄 STATE TRANSITION: ${oldS} -> ${newS}`);
    document.querySelectorAll('.status-step').forEach(step => {
      step.classList.remove('active');
      if (step.id === `step-${newS.toLowerCase()}`) step.classList.add('active');
    });
  }

  // L3 Projection
  function runProjection() {
    const projectionData = {
      timestamp: new Date().toLocaleTimeString('en-GB', { hour12: false }),
      mode: currentInfluence > 0.5 ? 'social' : 'strict',
      influence: currentInfluence,
      traits: {}
    };

    let promptFragments = [];

    genomeData.loci.forEach(locus => {
      const { min, max, default: def } = locus.distribution.values;
      const rng = Math.random();
      const stochasticVal = min + rng * (max - min);
      const finalVal = def + (stochasticVal - def) * currentInfluence;

      projectionData.traits[locus.id] = finalVal;

      const sampleEl = document.getElementById(`sample-${locus.id}`);
      sampleEl.style.opacity = '1';
      sampleEl.style.left = `${finalVal * 100}%`;

      // Prompt Augmentation logic
      const matrix = promptMatrix[locus.id];
      if (matrix) {
        const match = matrix.find(m => finalVal >= m.range[0] && finalVal <= m.range[1]);
        if (match) promptFragments.push(match.text);
      }
    });

    // Update Prompt Output
    promptOutput.innerHTML = promptFragments.map(f => `• ${f}`).join('<br>');
    promptOutput.style.animation = "pulse 0.5s ease";
    setTimeout(() => promptOutput.style.animation = "", 500);

    saveToHistory(projectionData);
    recordInteraction(1);
    addLog(`L3 Sampling (${projectionData.mode}. Strength: ${currentInfluence.toFixed(2)})...`);
  }

  function saveToHistory(record) {
    history.unshift(record);
    if (history.length > 10) history.pop();
    renderHistory();
  }

  function renderHistory() {
    if (history.length === 0) return;
    historyContainer.innerHTML = '';
    history.forEach((record, index) => {
      const item = document.createElement('div');
      item.className = 'history-item';
      item.onclick = () => replayHistory(index);
      item.innerHTML = `
        <div class="history-header">
          <span>${record.timestamp}</span>
          <span class="history-mode-tag ${record.mode}">${record.mode.toUpperCase()}</span>
        </div>
        <div class="history-summary">Proj #${history.length - index}</div>
      `;
      historyContainer.appendChild(item);
    });
  }

  function replayHistory(index) {
    const record = history[index];
    document.querySelectorAll('.history-item').forEach((it, idx) => it.classList.toggle('active', idx === index));
    addLog(`Replaying history...`);
    genomeData.loci.forEach(locus => {
      const val = record.traits[locus.id];
      const ghost = document.getElementById(`ghost-${locus.id}`);
      ghost.style.opacity = '1';
      ghost.style.left = `${val * 100}%`;
    });
  }

  // Event Listeners
  sampleBtn.addEventListener('click', runProjection);

  influenceSlider.addEventListener('input', (e) => {
    currentInfluence = parseFloat(e.target.value);
  });

  modeSocial.addEventListener('click', () => {
    modeSocial.classList.add('active');
    modeStrict.classList.remove('active');
    influenceSlider.value = 1.0;
    currentInfluence = 1.0;
    addLog("Scene: SOCIAL.");
  });

  modeStrict.addEventListener('click', () => {
    modeStrict.classList.add('active');
    modeSocial.classList.remove('active');
    influenceSlider.value = 0.1;
    currentInfluence = 0.1;
    addLog("Scene: CRITICAL. DEGRADED.", "degraded");
    runProjection();
  });
});
