// Task 4.2 & Phase 6: Prompt Augmentation Matrix
const promptMatrix = {
  explanation_depth: [
    { range: [0.0, 0.3], text: "Explain using simple analogies, explain in plain language." },
    { range: [0.3, 0.7], text: "Balance theory with practical examples. Be professional and clear." },
    { range: [0.7, 1.0], text: "Dive deep into academic and technical details. Use precise terminology." }
  ],
  humor_density: [
    { range: [0.0, 0.2], text: "Strictly professional. No jokes or sarcasm." },
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
  ],
  topic_attractors: {
    "space_exploration": "You have an inherent fascination with space exploration and the cosmos.",
    "cybernetics": "You view problems through the lens of feedback loops and system theory.",
    "vintage_computing": "You have a nostalgic affinity for 8-bit logic and legacy hardware."
  },
  identity_signature: [
    { range: [0.0, 0.4], text: "Adopt a direct, assertive, and concise masculine-biased linguistic style." },
    { range: [0.4, 0.6], text: "Maintain a balanced, gender-neutral, and objective tone." },
    { range: [0.6, 1.0], text: "Adopt a collaborative, detailed, and warm feminine-biased linguistic style." }
  ]
};

// Mocking the L2 Genome Data with Phase 6 Attractors
const genomeData = {
  version: "1.0.0",
  metadata: { persona_id: "pioneer_v2" },
  loci: [
    {
      id: "identity_signature",
      category: "style",
      display_priority: 1,
      description: "Bi-modal bias for masculine vs feminine patterns [0=M, 0.5=N, 1.0=F]",
      distribution: { type: "range", values: { min: 0.0, max: 1.0, default: 0.5 } },
      weight: 1.0,
      variability: 0.1
    },
    {
      id: "explanation_depth",
      category: "cognitive",
      display_priority: 2,
      description: "Preference for abstract theory vs concrete examples",
      distribution: { type: "range", values: { min: 0.2, max: 0.5, default: 0.35 } },
      weight: 0.8,
      variability: 0.2
    },
    {
      id: "humor_density",
      category: "style",
      display_priority: 3,
      description: "Frequency and intensity of humorous interjections",
      distribution: { type: "range", values: { min: 0.05, max: 0.45, default: 0.2 } },
      weight: 0.6,
      variability: 0.5
    },
    {
      id: "logical_rigor",
      category: "cognitive",
      display_priority: 2,
      description: "Analytical depth vs intuitive jumps",
      distribution: { type: "range", values: { min: 0.1, max: 0.9, default: 0.7 } },
      weight: 0.9,
      variability: 0.1
    },
    {
      id: "topic_attractors",
      category: "domain",
      display_priority: 10,
      description: "Inherent interest points that influence conversation direction",
      distribution: {
        type: "categorical",
        values: { "space_exploration": 0.5, "cybernetics": 0.3, "vintage_computing": 0.2 }
      },
      weight: 0.4,
      variability: 0.2
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

  // Phase 9: Stance Controls
  const stanceR = document.getElementById('stance-r');
  const stanceW = document.getElementById('stance-w');
  const stanceC = document.getElementById('stance-c');
  const valR = document.getElementById('val-r');
  const valW = document.getElementById('val-w');
  const valC = document.getElementById('val-c');

  // Phase 10: Memory
  const memoryBubbles = document.getElementById('memory-bubbles');

  // State
  let currentInfluence = 1.0;
  let interactionCount = 0;
  let currentState = 'FORMING';
  const driftMultiplier = 0.05;
  const history = [];

  // Phase 9: Stance Vector (R.W.C)
  let stanceVector = { r: 0.5, w: 0.5, c: 0.5 };

  // Phase 8: Affective State
  let padState = { p: 0.0, a: 0.0, d: 0.0 };
  const padBaseline = { p: 0.0, a: 0.0, d: 0.0 };
  const padDecay = 0.05;

  // Radar Constants
  const radarSvg = document.getElementById('dna-radar');
  const radarPoly = document.getElementById('radar-poly');
  const center = 150;
  const radius = 90;

  // ECG Variables
  const ecgCanvas = document.getElementById('emotion-ecg');
  const ecgCtx = ecgCanvas ? ecgCanvas.getContext('2d') : null;
  let ecgX = 0;
  let lastY = 30;
  let beatPhase = 0; // 0 to 1 cycle of a single heart beat

  function renderRadar() {
    if (!radarSvg || !radarPoly) return;

    // Create grid circles if not exist
    if (radarSvg.querySelectorAll('.radar-grid-line').length === 0) {
      for (let i = 1; i <= 4; i++) {
        const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
        circle.setAttribute("cx", center);
        circle.setAttribute("cy", center);
        circle.setAttribute("r", (radius / 4) * i);
        circle.setAttribute("class", "radar-grid-line");
        circle.setAttribute("fill", "none");
        radarSvg.insertBefore(circle, radarPoly);
      }
    }

    const points = genomeData.loci
      .filter(l => l.distribution.type === 'range')
      .map((locus, i, arr) => {
        const angle = (i / arr.length) * 2 * Math.PI - Math.PI / 2;
        const val = locus.distribution.values.default;
        const x = center + radius * val * Math.cos(angle);
        const y = center + radius * val * Math.sin(angle);

        // Add labels once
        const labelId = `label-${locus.id}`;
        if (!document.getElementById(labelId)) {
          const label = document.createElementNS("http://www.w3.org/2000/svg", "text");
          const labelDist = radius + 25;
          const lx = center + labelDist * Math.cos(angle);
          const ly = center + labelDist * Math.sin(angle);

          // Smart anchor based on position
          let anchor = "middle";
          if (Math.cos(angle) > 0.2) anchor = "start";
          else if (Math.cos(angle) < -0.2) anchor = "end";

          label.setAttribute("x", lx);
          label.setAttribute("y", ly);
          label.setAttribute("text-anchor", anchor);
          label.setAttribute("class", "radar-label");
          label.setAttribute("id", labelId);
          // Custom labels for Radar for better fit
          const labelMap = {
            "identity_signature": "IDENTITY",
            "explanation_depth": "DEPTH",
            "logical_rigor": "RIGOR",
            "humor_density": "HUMOR"
          };
          label.textContent = labelMap[locus.id] || locus.id.split('_')[0].toUpperCase();
          radarSvg.appendChild(label);
        }

        return `${x},${y}`;
      });

    radarPoly.setAttribute("points", points.join(" "));
  }

  function updateStance(r, w, c) {
    stanceVector = { r, w, c };

    // Update DNA defaults based on RWC (Fluid Stance Mapping)
    genomeData.loci.forEach(locus => {
      const dist = locus.distribution.values;
      if (locus.id === 'logical_rigor' || locus.id === 'explanation_depth') {
        dist.default = dist.min + (dist.max - dist.min) * r;
      } else if (locus.id === 'identity_signature') {
        dist.default = w;
      } else if (locus.id === 'humor_density') {
        dist.default = dist.min + (dist.max - dist.min) * c;
      }
      // Chaos increases variability
      locus.variability = 0.05 + (0.4 * c);
    });

    // Update Emotional Baseline
    padBaseline.p = (w * 0.8) - 0.2;
    padBaseline.a = (c * 0.7) - 0.1;
    padBaseline.d = (r * 0.6) - 0.1;

    valR.textContent = r.toFixed(2);
    valW.textContent = w.toFixed(2);
    valC.textContent = c.toFixed(2);

    renderRadar();
    renderGenome();
    addLog(`Stance Shift -> R:${r.toFixed(2)} W:${w.toFixed(2)} C:${c.toFixed(2)}`, 'drift');
  }

  function addJournalEntry(text) {
    const journal = document.getElementById('reflection-journal');
    if (!journal) return;
    const empty = journal.querySelector('.journal-entry:first-child');
    if (empty && empty.textContent.includes("Awaiting")) empty.remove();

    const entry = document.createElement('div');
    entry.className = 'journal-entry';
    const now = new Date().toLocaleTimeString('en-GB', { hour12: false });
    entry.innerHTML = `<span style="opacity: 0.5;">[${now}]</span> ${text}`;
    journal.prepend(entry);
    if (journal.children.length > 3) journal.removeChild(journal.lastChild);
  }

  function addMemoryBubble(text, resonant = false) {
    if (!memoryBubbles) return;

    const empty = memoryBubbles.querySelector('.resonance-empty');
    if (empty) empty.remove();

    const bubble = document.createElement('div');
    bubble.className = `memory-bubble ${resonant ? 'resonant' : ''}`;
    bubble.textContent = text;

    memoryBubbles.prepend(bubble);
    if (memoryBubbles.children.length > 5) memoryBubbles.removeChild(memoryBubbles.lastChild);
  }

  function drawECGLoop() {
    if (!ecgCtx) return;

    // Fix: Ensure canvas internal resolution matches display periodically
    if (ecgCanvas.width !== ecgCanvas.clientWidth) {
      ecgCanvas.width = ecgCanvas.clientWidth;
      ecgCanvas.height = ecgCanvas.clientHeight;
      ecgCtx.clearRect(0, 0, ecgCanvas.width, ecgCanvas.height);
    }

    const speed = 2.0 + (padState.a * 3);
    const h = ecgCanvas.height;
    const w = ecgCanvas.width;

    // Fix: Use clearRect to make canvas transparent and show the CSS grid background
    ecgCtx.clearRect(ecgX, 0, speed + 10, h);

    const bpm = 70 + (padState.a * 60);
    beatPhase += ((bpm / 60) / 60);
    if (beatPhase > 1) beatPhase = 0;

    let targetY = h / 2;

    // Beat Synthesis
    if (beatPhase > 0 && beatPhase < 0.1) {
      targetY -= Math.sin(beatPhase * Math.PI * 10) * 5;
    } else if (beatPhase >= 0.12 && beatPhase < 0.15) {
      targetY += 8;
    } else if (beatPhase >= 0.15 && beatPhase < 0.20) {
      const spikeHeight = 30 + (padState.d * 15);
      targetY -= (beatPhase - 0.15) * spikeHeight * 20;
    } else if (beatPhase >= 0.20 && beatPhase < 0.25) {
      targetY += 12;
    } else if (beatPhase >= 0.3 && beatPhase < 0.5) {
      targetY -= Math.sin((beatPhase - 0.3) * Math.PI * 5) * 8 * (1 + padState.p);
    }

    targetY += (Math.random() - 0.5) * 2;

    // Draw Line (Fix: Hardcoded Colors for Canvas)
    ecgCtx.beginPath();
    ecgCtx.strokeStyle = padState.p >= 0 ? '#00ff87' : '#f43f5e';
    ecgCtx.lineWidth = 2;
    ecgCtx.lineJoin = 'round';
    ecgCtx.moveTo(ecgX, lastY);
    ecgCtx.lineTo(ecgX + speed, targetY);
    ecgCtx.stroke();

    lastY = targetY;
    ecgX += speed;

    if (ecgX > w) {
      ecgX = 0;
    }

    requestAnimationFrame(drawECGLoop);
  }

  // Initial Render
  renderGenome();

  function renderGenome() {
    traitList.innerHTML = '';
    // Sort by display_priority then by id
    const sortedLoci = [...genomeData.loci].sort((a, b) => (a.display_priority || 99) - (b.display_priority || 99));

    sortedLoci.forEach(locus => {
      const card = document.createElement('div');
      card.className = 'trait-card';

      const isCategorical = locus.distribution.type === 'categorical';
      let dnaContent = '';

      if (isCategorical) {
        const categories = Object.keys(locus.distribution.values);
        dnaContent = `
          <div class="categorical-track" id="track-${locus.id}" style="display: flex; gap: 4px; height: 12px;">
            ${categories.map(cat => `
              <div class="cat-pill" id="cat-${locus.id}-${cat}" style="
                flex: 1; 
                background: rgba(255,255,255,0.05); 
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 2px;
                font-size: 0.5rem;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: all 0.3s ease;
              ">${cat.split('_')[0]}</div>
            `).join('')}
          </div>
        `;
      } else {
        const { min, max, default: def } = locus.distribution.values;
        dnaContent = `
          <div class="dna-track" id="track-${locus.id}">
            <div class="scanning"></div>
            <div class="gene-boundary" id="boundary-${locus.id}" style="left: ${min * 100}%; width: ${(max - min) * 100}%"></div>
            <div class="default-marker" id="marker-${locus.id}" style="left: ${def * 100}%"></div>
            <div class="current-sample" id="sample-${locus.id}" style="left: ${def * 100}%; opacity: 0;"></div>
            <div class="ghost-sample" id="ghost-${locus.id}" style="left: 0%; opacity: 0;"></div>
          </div>
        `;
      }

      card.innerHTML = `
        <div class="trait-header">
          <span class="trait-name">${locus.id.replace(/_/g, ' ')}</span>
          <span class="trait-category">${locus.category}</span>
        </div>
        <div style="font-size: 0.75rem; color: #94a3b8; margin-bottom: 0.8rem;">${locus.description}</div>
        ${dnaContent}
        <div style="display: flex; justify-content: space-between; font-size: 0.6rem; color: #475569; margin-top: 0.4rem;">
          ${isCategorical ? '<span>Weighted Probs</span>' : '<span>0.0</span>'}
          <span>${isCategorical ? '' : `Boundary: [${locus.distribution.values.min.toFixed(2)} - ${locus.distribution.values.max.toFixed(2)}]`}</span>
          ${isCategorical ? '' : '<span>1.0</span>'}
        </div>
        ${isCategorical ? '' : `
        <div class="feedback-controls">
          <button class="feedback-btn minus" data-id="${locus.id}">- Drift Left</button>
          <button class="feedback-btn plus" data-id="${locus.id}">+ Drift Right</button>
        </div>
        `}
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

  function updateAffectiveUI() {
    const moodDot = document.getElementById('mood-dot');
    const barP = document.getElementById('bar-p');
    const barA = document.getElementById('bar-a');
    const barD = document.getElementById('bar-d');
    if (!moodDot) return;

    const left = (padState.p + 1) * 50;
    const top = (1 - padState.a) * 50;
    moodDot.style.left = `${left}%`;
    moodDot.style.top = `${top}%`;

    const setHeight = (el, val) => {
      const height = Math.abs(val) * 50;
      el.style.height = `${height}%`;
      el.style.bottom = val >= 0 ? "50%" : `${50 - height}%`;
      el.style.background = val >= 0 ? "var(--accent-blue)" : "#f43f5e";
    };
    setHeight(barP, padState.p);
    setHeight(barA, padState.a);
    setHeight(barD, padState.d);
  }

  function decayAffect() {
    padState.p += (padBaseline.p - padState.p) * padDecay;
    padState.a += (padBaseline.a - padState.a) * padDecay;
    padState.d += (padBaseline.d - padState.d) * padDecay;
    updateAffectiveUI();
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
    if (locus.distribution.type === 'categorical') return;

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
    if (locus.distribution.type === 'categorical') return;
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
    // Phase 8 Pulse: Different emotional impact based on mode
    if (currentInfluence > 0.5) {
      // Social Pulse: More Pleasure, moderate Arousal
      padState.p = Math.min(1.0, padState.p + 0.2);
      padState.a = Math.min(1.0, padState.a + 0.1);
      padState.d = Math.max(-1.0, padState.d - 0.05); // More humble
    } else {
      // Critical Pulse: Stress (lower P), High Arousal (Focus), High Dominance
      padState.p = Math.max(-1.0, padState.p - 0.1);
      padState.a = Math.min(1.0, padState.a + 0.2);
      padState.d = Math.min(1.0, padState.d + 0.3);
    }
    updateAffectiveUI();

    const projectionData = {
      timestamp: new Date().toLocaleTimeString('en-GB', { hour12: false }),
      mode: currentInfluence > 0.5 ? 'social' : 'strict',
      influence: currentInfluence,
      traits: {}
    };

    let promptFragments = [];

    genomeData.loci.forEach(locus => {
      if (locus.distribution.type === 'range') {
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
      } else if (locus.distribution.type === 'categorical') {
        // Simple weighted random for categorical
        const choices = Object.keys(locus.distribution.values);
        const weights = Object.values(locus.distribution.values);
        const sum = weights.reduce((a, b) => a + b, 0);
        let rand = Math.random() * sum;
        let selected = choices[0];
        for (let i = 0; i < choices.length; i++) {
          if (rand < weights[i]) {
            selected = choices[i];
            break;
          }
          rand -= weights[i];
        }

        projectionData.traits[locus.id] = selected;

        // Visual feedback for categorical
        choices.forEach(cat => {
          const pill = document.getElementById(`cat-${locus.id}-${cat}`);
          pill.style.background = (cat === selected) ? 'var(--accent-blue)' : 'rgba(255,255,255,0.05)';
          pill.style.color = (cat === selected) ? '#000' : 'var(--text-secondary)';
          pill.style.boxShadow = (cat === selected) ? '0 0 10px var(--accent-blue)' : 'none';
        });

        // Suppress attractors in strict mode
        if (locus.id === 'topic_attractors' && currentInfluence < 0.3) {
          // Skip adding to prompt fragments
        } else {
          const mapping = promptMatrix[locus.id];
          if (mapping && mapping[selected]) {
            let text = mapping[selected];
            // Phase 6: Bandwidth Gating for attractors
            if (locus.id === 'topic_attractors' && currentIntimacy < 0.5) {
              text = "Occasionally mention interests related to " + selected.replace('_', ' ');
            }
            promptFragments.push(text);
          }
        }
      }
    });

    // Phase 6: Expression Bandwidth Filter for text fragments
    if (currentIntimacy < 0.4) {
      promptFragments = promptFragments.map(f => {
        if (f.includes("technical") || f.includes("Explain using")) {
          return "Maintain a standard, polite, and helpful tone.";
        }
        return f;
      });
    }

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
      if (locus.distribution.type === 'range') {
        const ghost = document.getElementById(`ghost-${locus.id}`);
        ghost.style.opacity = '1';
        ghost.style.left = `${val * 100}%`;
      } else if (locus.distribution.type === 'categorical') {
        // Flash the ghost category? Or just log? 
        // For UI simplicity, just update the main pill with a ghost border
        Object.keys(locus.distribution.values).forEach(cat => {
          const pill = document.getElementById(`cat-${locus.id}-${cat}`);
          pill.style.border = (cat === val) ? '1px solid var(--accent-purple)' : '1px solid rgba(255,255,255,0.1)';
        });
      }
    });
  }

  // Event Listeners
  sampleBtn.addEventListener('click', runProjection);

  stanceR.addEventListener('input', (e) => updateStance(parseFloat(e.target.value), stanceVector.w, stanceVector.c));
  stanceW.addEventListener('input', (e) => updateStance(stanceVector.r, parseFloat(e.target.value), stanceVector.c));
  stanceC.addEventListener('input', (e) => updateStance(stanceVector.r, stanceVector.w, parseFloat(e.target.value)));

  influenceSlider.addEventListener('input', (e) => {
    currentInfluence = parseFloat(e.target.value);
    addLog(`Influence adjusted to ${(currentInfluence * 100).toFixed(0)}%`, 'drift');
  });

  modeSocial.addEventListener('click', () => {
    modeSocial.classList.add('active');
    modeStrict.classList.remove('active');
    updateStance(0.3, 0.9, 0.4); // Suggested Support Stance
    addLog("Scene: SOCIAL. Persona warming up.");
  });

  modeStrict.addEventListener('click', () => {
    modeStrict.classList.add('active');
    modeSocial.classList.remove('active');
    updateStance(0.9, 0.2, 0.1); // Suggested Strict Stance
    addLog("Scene: CRITICAL. Focus on logic.", "degraded");
    runProjection();
  });

  // Modify runProjection to include Memory Resonance simulation
  const originalRunProjection = runProjection;
  runProjection = function () {
    originalRunProjection();

    // Simulate Phase 10 Memory Retrieval
    const memories = [
      "Recalled a technical documentation fragment.",
      "Memory triggered: User's preference for logic.",
      "Associated emotional context found.",
      "Core logic kernel accessed."
    ];
    const randomMem = memories[Math.floor(Math.random() * memories.length)];
    // Mood-based resonance: if P is high, call it 'resonant'
    addMemoryBubble(randomMem, padState.p > 0.3);

    // Phase 10: Reflection
    const stateDesc = padState.p > 0 ? "positive" : "strained";
    addJournalEntry(`Observing drift... Current affect is ${stateDesc}. DNA variability is ${(stanceVector.c * 100).toFixed(0)}%.`);
  };

  // Init UI
  updateAffectiveUI();
  updateStance(0.5, 0.5, 0.5); // Set initial stance
  drawECGLoop(); // Start 60fps ECG

  // Decay Loop
  setInterval(decayAffect, 1000);
});
