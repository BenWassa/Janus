// app.js

import { scenes, TRAIT_KEYS, SIGILS, TRAIT_COLORS, ARCHETYPES, CARD_GLYPHS } from "./data.js"; // Import CARD_GLYPHS

// Trait state: multi-trait object from Hamartia Engine
const traits = Object.fromEntries(TRAIT_KEYS.map(t=>[t,0]));
const journal = []; // poetic echo lines
const path = [];    // record of choices
let sceneIndex = 0;
let choicesLocked = false; // Flag to prevent multiple choices
let quickMode = false;
const CHOICE_PAUSE = 1500; // ms delay before advancing

// DOM refs
const start = document.getElementById('start');
const playBtn = document.getElementById('play');
const game = document.getElementById('game');
const reflection = document.getElementById('reflection');
const sceneCard = document.getElementById('sceneCard');
const sceneId = document.getElementById('sceneId');
const sceneTitle = document.getElementById('sceneTitle');
const sceneSubtitle = document.getElementById('sceneSubtitle');
const sceneText = document.getElementById('sceneText');
const decision = document.getElementById('decision');
const consequence = document.getElementById('consequence');
const traitBar = document.getElementById('traitBar');
const sigilRepo = document.getElementById('sigils');
const tarotSpread = document.getElementById('tarotSpread');
// const modeSelect = document.getElementById('mode'); // REMOVED: No longer needed
const restart = document.getElementById('restart');
const saveBtn = document.getElementById('save');
const loadBtn = document.getElementById('load');
const portrait = document.getElementById('portrait');
const journalEl = document.getElementById('journal');
const reading = document.getElementById('reading');
const quickToggle = document.getElementById('quick');
const ambienceToggle = document.getElementById('ambience');
const constellationCanvas = document.getElementById('constellation');
if (quickToggle) quickMode = quickToggle.checked;

const downloadBtn = document.getElementById('download');
const againBtn = document.getElementById('again');

// Quick runtime integrity check for required/optional DOM hooks
function integrityCheck(){
  const required = ['start','play','game','sceneCard','decision'];
  const optional = ['reflection','traitBar','sigils','tarotSpread','portrait','journal','reading','restart','save','load','download','again','constellation','quick','ambience','consequence'];
  const missingRequired = required.filter(id => !document.getElementById(id));
  const missingOptional = optional.filter(id => !document.getElementById(id));
  if(missingRequired.length) console.warn('[IntegrityCheck] Missing required DOM ids:', missingRequired.join(', '));
  if(missingOptional.length) console.info('[IntegrityCheck] Missing optional DOM ids (UI will degrade gracefully):', missingOptional.join(', '));
  return { missingRequired, missingOptional };
}
integrityCheck();

// Entry - attach listeners only if elements exist to avoid runtime errors in trimmed DOMs
if (playBtn) playBtn.addEventListener('click', startGame);
if (restart) restart.addEventListener('click', resetAll);
if (againBtn) againBtn.addEventListener('click', resetAll);
if (downloadBtn) downloadBtn.addEventListener('click', downloadRitual);
if (saveBtn) saveBtn.addEventListener('click', saveState);
if (loadBtn) loadBtn.addEventListener('click', loadState);
if (quickToggle) quickToggle.addEventListener('change', () => { quickMode = quickToggle.checked; });
if (ambienceToggle && constellationCanvas) {
  ambienceToggle.addEventListener('change', () => {
    constellationCanvas.style.display = ambienceToggle.checked ? 'block' : 'none';
  });
  constellationCanvas.style.display = 'none';
}

// Keyboard shortcuts (1/2) - Now for the new simple choice buttons
document.addEventListener('keydown', (e)=>{
  if (game.style.display !== 'none' && !choicesLocked && (e.key === '1' || e.key === '2')) {
    const opts = scenes[sceneIndex].options;
    const idx = e.key === '1' ? 0 : 1;
    const choiceButton = decision.children[idx]; // Get the actual button
    if (opts[idx] && choiceButton) {
        choiceButton.classList.add('selected'); // Add visual feedback for keyboard selection
        handleChoice(opts[idx], {x: choiceButton.getBoundingClientRect().left + choiceButton.offsetWidth/2, y: choiceButton.getBoundingClientRect().top + choiceButton.offsetHeight/2});
    }
  }
});

function startGame(){
  start.style.display = 'none';
  reflection.style.display = 'none';
  game.style.display = '';
  TRAIT_KEYS.forEach(k=> traits[k] = 0); // Reset all traits
  sigilRepo.innerHTML = ''; // Clear sigils
  tarotSpread.innerHTML = ''; // Clear tarot cards
  sceneIndex = 0;
  journal.length = 0;
  path.length = 0;
  choicesLocked = false; // Ensure choices are unlocked for new game
  renderScene();
  updateAtmosphere();
}

function resetAll(){
  // Clear localStorage on full reset for clean slate
  localStorage.removeItem('janusState');
  start.style.display = '';
  game.style.display = 'none';
  reflection.style.display = 'none';
}

function saveState(){
  try {
    const state = { traits, journal, path, sceneIndex };
    localStorage.setItem('janusState', JSON.stringify(state));
    console.log('[Save State] Game state saved successfully.');
  } catch (error) {
    console.error('[Save State] Failed to save state:', error);
    alert('Failed to save game state. Your browser might be in private mode or storage is full.');
  }
}

function loadState(){
  try {
    const raw = localStorage.getItem('janusState');
    if(!raw) {
      console.log('[Load State] No saved state found.');
      alert('No saved game found!');
      return;
    }
    const state = JSON.parse(raw);
    
    // Reset current state to avoid cumulative issues
    TRAIT_KEYS.forEach(k=> traits[k] = 0);
    journal.length = 0;
    path.length = 0;
    sigilRepo.innerHTML = '';
    tarotSpread.innerHTML = '';

    Object.assign(traits, state.traits || {});
    (state.journal || []).forEach(j=> journal.push(j));
    (state.path || []).forEach(p=> path.push(p));
    sceneIndex = state.sceneIndex || 0;

    // Reconstruct UI elements based on loaded path and traits
    // Tarot cards (add glyph based on scene ID from path)
    for(let i=0;i<path.length;i++){
      const sceneIdForCard = path[i].scene;
      addTarotCard(sceneIdForCard, true); // 'true' for immediate reveal on load
    }

    // Sigils (re-evaluate all relevant deltas from path)
    const encounteredTraits = new Set();
    path.forEach(step => {
        for(const [k,v] of Object.entries(step.delta || {})){
            if(Math.abs(v) >= 0.4 && !encounteredTraits.has(k)) { 
                showSigil(k);
                encounteredTraits.add(k); 
            }
        }
    });

    start.style.display = 'none';
    reflection.style.display = 'none';
    game.style.display = '';
    
    if(sceneIndex < scenes.length){
      renderScene();
    } else {
      showReflection();
    }
    updateAtmosphere();
    journalEl.textContent = journal.join('\n\n'); 
    console.log('[Load State] Game state loaded successfully.');
  } catch (error) {
    console.error('[Load State] Failed to load state:', error);
    alert('Failed to load game state. The saved data might be corrupted.');
  }
}


function renderScene(){
  choicesLocked = false; // Unlock choices for the new scene
  const s = scenes[sceneIndex];
  sceneId.textContent = s.act;
  sceneTitle.textContent = s.title;
  sceneSubtitle.textContent = s.subtitle;
  sceneText.textContent = s.text;

  decision.innerHTML = ''; // Clear previous choices
  if (consequence){
    consequence.textContent = '';
    consequence.style.display = 'none';
  }
  decision.style.display = 'flex';
  sceneCard.classList.add('dissolve');
  void sceneCard.offsetWidth; // Trigger reflow for animation
  setTimeout(()=> sceneCard.classList.remove('dissolve'), 1000); // Match CSS dissolve duration

  renderSimpleChoices(s.options); // Call the new simple choice renderer
}

// -----------------------------
// New: Simple Choice Renderer (Dream-Walk style)
// -----------------------------
function renderSimpleChoices(options){
  options.forEach((opt, i)=>{
    const button = document.createElement('button');
    button.className = 'choice-button';
    button.textContent = `${i + 1}. ${opt.label}`; // Add numbering
    button.addEventListener('click', (ev)=>{
      if (choicesLocked) return;
      button.classList.add('selected'); // Visual feedback for click
      handleChoice(opt, {x: ev.clientX, y: ev.clientY});
    });
    decision.appendChild(button);
  });
}

// -----------------------------
// Choice handling
// -----------------------------
function handleChoice(opt, point){
  if (choicesLocked) return;
  choicesLocked = true; // Lock choices immediately

  // Echo ripple feedback
  echoRipple(point.x, point.y);

  // Update traits & record
  const currentDeltas = opt.delta || {};
  for(const [k,v] of Object.entries(currentDeltas)){
    traits[k] = clamp((traits[k]||0) + v, -1, 1); // Ensure clamping for each trait
    if(Math.abs(v) >= 0.4) showSigil(k); // Show sigil for significant trait changes
  }
  const currentSceneId = scenes[sceneIndex].id;
  path.push({ scene: currentSceneId, choice: opt.id, delta: currentDeltas });
  console.log('[Telemetry]', { scene: currentSceneId, choice: opt.id, delta: currentDeltas, traits: { ...traits } });
  journal.push(`• ${opt.whisper}`);
  addTarotCard(currentSceneId); // Pass scene ID to tarot card

  updateAtmosphere();

  if (consequence){
    consequence.textContent = opt.whisper;
    consequence.style.display = 'block';
  }
  decision.style.display = 'none';

  const delay = quickMode ? 0 : CHOICE_PAUSE;
  setTimeout(() => {
    sceneIndex++;
    if (sceneIndex < scenes.length) {
      renderScene();
    } else {
      showReflection();
    }
  }, delay);
}

function updateAtmosphere(){
  // Compute a local blended hue from dominant traits but do NOT mutate global CSS vars
  const entries = Object.entries(traits).sort((a,b)=>Math.abs(b[1]) - Math.abs(a[1]));
  const top = entries.filter(([k,v]) => Math.abs(v) > 0.1).slice(0,3); // Only consider traits with some value
  let totalWeight = 0, hueSum = 0;
  if(top.length){
    top.forEach(([k,v])=>{
      const weight = Math.abs(v);
      const [h] = TRAIT_COLORS[k];
      hueSum += h * weight;
      totalWeight += weight;
    });
  }
  const blendedHue = totalWeight ? Math.round(hueSum / totalWeight) : 215; // fallback to indigo-blue base

  // Local accent (used only for small UI elements like trait bar and portrait accents)
  const accentHue = (blendedHue + 20) % 360;

  // Update small UI elements only (guard existence)
  const hubris = traits.Hubris || 0;
  if (traitBar) {
    traitBar.style.width = ((0.5 + hubris/2) * 100) + '%';
    traitBar.style.background = `linear-gradient(90deg, hsla(${accentHue},70%,55%,0.9), hsla(${(accentHue+30)%360},80%,50%,0.9))`;
  }
}

function showReflection(){
  game.style.display = 'none';
  reflection.style.display = '';
  // Portrait & reading
  renderPortraitAndReading();
  // Journal
  journalEl.textContent = journal.join('\n\n');
}

// Function to determine the archetype
function determineArchetype(){
  const sortedTraits = Object.entries(traits)
    .sort(([,v1], [,v2]) => Math.abs(v2) - Math.abs(v1)); // Sort by magnitude, descending

  // Try to find archetypes based on 2 or 3 most dominant traits
  for (let i = 0; i < Math.min(sortedTraits.length, 3); i++) {
    for (let j = i + 1; j < Math.min(sortedTraits.length, 3); j++) {
      const trait1 = sortedTraits[i][0];
      const trait2 = sortedTraits[j][0];
      const key = [trait1, trait2].sort().join(','); // Standardize key
      if (ARCHETYPES[key]) {
        console.log(`[Archetype] Found pair: ${key}`);
        return ARCHETYPES[key];
      }
      // Consider three-trait combinations for more specific archetypes (e.g., if you add 'Apathy,Cynicism,Fear')
      if (i === 0 && j === 1 && sortedTraits.length >= 3) {
          const trait3 = sortedTraits[2][0];
          const threeKey = [trait1, trait2, trait3].sort().join(',');
          if (ARCHETYPES[threeKey]) {
              console.log(`[Archetype] Found triplet: ${threeKey}`);
              return ARCHETYPES[threeKey];
          }
      }
    }
  }

  // Fallback to single most dominant trait if no pair/triplet found
  if (sortedTraits.length > 0 && Math.abs(sortedTraits[0][1]) > 0.1) {
    const singleTraitKey = sortedTraits[0][0];
    if (ARCHETYPES[singleTraitKey]) {
      console.log(`[Archetype] Found dominant single trait: ${singleTraitKey}`);
      return ARCHETYPES[singleTraitKey];
    }
  }

  // Default fallback if no significant traits or archetypes match
  console.log('[Archetype] No specific archetype found, using default.');
  return {
    name: 'The Seeker of Unwritten Paths',
    lines: [
      'Your journey weaves a unique pattern, less defined by stark forces and more by subtle currents.',
      'The whispers echo not a clear destination, but the boundless potential of the unchosen road.'
    ]
  };
}

function renderPortraitAndReading(){
  if (!portrait) return;
  portrait.innerHTML = '';
  const arche = determineArchetype();
  const card = document.createElement('div');
  card.className = 'archetype-card';
  const title = document.createElement('h2');
  title.textContent = arche.name;
  card.appendChild(title);
  arche.lines.slice(0,2).forEach(l=>{
    const p = document.createElement('p');
    p.textContent = l;
    card.appendChild(p);
  });
  portrait.appendChild(card);
  if (reading){
    const lines = arche.lines.map(l=>`<div>• ${l}</div>`).join('');
    reading.innerHTML = `<div class="badge">Cosmic Constellation Narrative</div><h2 class="title" style="margin-top:8px;">Mythic Persona: ${arche.name}</h2><div class="scene-text">${lines}</div>`;
  }
}

function downloadRitual(){
  const text = `HERO\'S CHRONICLE (Prototype)\n\n` + journal.join('\n\n');
  const blob = new Blob([text], {type:'text/plain'});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a'); a.href = url; a.download = 'janus_ritual.txt'; a.click();
  URL.revokeObjectURL(url);
}

function clamp(v, a, b){ return Math.max(a, Math.min(b, v)); }

function showSigil(traitKey){
  let node = sigilRepo.querySelector(`[data-trait="${traitKey}"]`);
  if(!node){
    node = document.createElement('div');
    node.className = 'sigil';
    node.dataset.trait = traitKey;
    node.innerHTML = SIGILS[traitKey] || '';
    node.style.color = `hsl(${TRAIT_COLORS[traitKey][0]},${TRAIT_COLORS[traitKey][1]}%,${TRAIT_COLORS[traitKey][2]}%)`; // Color sigil by trait
    sigilRepo.appendChild(node);
  }
  node.classList.add('active');
  node.style.opacity = '1'; 
  node.style.transform = 'scale(1.3)'; 
  setTimeout(()=> {
      node.classList.remove('active');
      node.style.transform = 'scale(1)';
      node.style.opacity = '0.4'; 
  }, 800);
}

const svgNS = 'http://www.w3.org/2000/svg';

function addTarotCard(sceneIdForCard, isLoad = false){
  const card = document.createElement('div');
  card.className = 'tarot-card';
  
  // Add an inner SVG glyph based on the scene ID or a general progression pattern
  const glyphSvg = document.createElementNS(svgNS, 'svg');
  glyphSvg.setAttribute('viewBox', '0 0 20 20');
  glyphSvg.innerHTML = CARD_GLYPHS[sceneIdForCard] || CARD_GLYPHS['default']; // Use a default if sceneId doesn't have a specific glyph
  card.appendChild(glyphSvg);

  tarotSpread.appendChild(card);
  if (isLoad) {
    card.classList.add('reveal');
  } else {
    requestAnimationFrame(()=> card.classList.add('reveal'));
  }
  // Scroll to the latest card
  tarotSpread.scroll({ left: tarotSpread.scrollWidth, behavior: 'smooth' });
}

function echoRipple(x, y){
  ['','faint'].forEach((cls, i)=>{
    const r = document.createElement('span');
    r.className = 'ripple' + (cls ? ' ' + cls : '');
    r.style.left = (x - 5) + 'px';
    r.style.top = (y - 5) + 'px';
    if(i) r.style.animationDelay = '120ms';
    document.body.appendChild(r);
    r.addEventListener('animationend', ()=> r.remove());
  });
}

// -----------------------------
// Constellation bloom (ambient) — optional decorative canvas
// If the canvas is removed from the DOM this entire block will skip safely.
// -----------------------------
{
  const canvas = constellationCanvas;
  if (!canvas || !canvas.getContext) {
    console.info('[Constellation] canvas not found or unsupported; skipping constellation rendering.');
  } else {
    const ctx = canvas.getContext('2d');
    let stars = [];
    function initStars(){
      const w = canvas.width = canvas.clientWidth;
      const h = canvas.height = canvas.clientHeight;
      stars = Array.from({length: 80}, ()=>({
        x: Math.random()*w,
        y: Math.random()*h,
        r: Math.random()*1.7 + 0.3,
        b: Math.random()*0.4 + 0.2, // base brightness
        vx: (Math.random()-0.5)*0.08, // Increased velocity
        vy: (Math.random()-0.5)*0.08, // Increased velocity
      }));
    }
    window.addEventListener('resize', initStars);
    initStars();
    function tick(){
      const w = canvas.width = canvas.clientWidth;
      const h = canvas.height = canvas.clientHeight;
      ctx.clearRect(0,0,w,h);

  // compute a local hue for constellation based on traits (non-invasive)
  const entries = Object.entries(traits).sort((a,b)=>Math.abs(b[1]) - Math.abs(a[1]));
  const top = entries.filter(([k,v]) => Math.abs(v) > 0.1).slice(0,3);
  let thSum = 0, tw = 0;
  if(top.length){ top.forEach(([k,v])=>{ const w = Math.abs(v); thSum += TRAIT_COLORS[k][0] * w; tw += w; }); }
  const currentHue = tw ? Math.round(thSum / tw) : 215;

      // cluster centers move subtly with hubris trait (–1..1) → shift focus left/right
      const hubris = traits.Hubris || 0; // Keeping hubris for this specific effect
      const cx = w*(0.35 + 0.3*((hubris+1)/2));
      const cy = h*0.55;

      for (const s of stars){
        s.x = (s.x + s.vx + w) % w;
        s.y = (s.y + s.vy + h) % h;
        s.b = clamp(s.b + (Math.random()-0.5)*0.01, 0.2, 0.6); // Subtle brightness flicker
        const dx = s.x - cx, dy = s.y - cy; const d = Math.sqrt(dx*dx + dy*dy) + 1;
        const glow = 1 / (d*0.04); // nearer to cluster is brighter
        const alpha = clamp(s.b + glow*0.9, 0, 1);
        
        ctx.beginPath(); ctx.arc(s.x, s.y, s.r, 0, Math.PI*2);
        ctx.fillStyle = `hsla(${currentHue},50%,80%,${alpha})`; // Use dynamic hue
        ctx.fill();
      }

      // Draw connections between nearby stars
      for(let i=0;i<stars.length;i++){
        for(let j=i+1;j<stars.length;j++){
          const a = stars[i], b = stars[j];
          const dx = a.x-b.x, dy = a.y-b.y; const d = Math.sqrt(dx*dx+dy*dy);
          if(d < 60){ // Increased connection distance
            const alpha = 0.15 * (1 - d/60); // Stronger opacity for connections
            ctx.strokeStyle = `hsla(${currentHue},60%,70%,${alpha})`;
            ctx.lineWidth = 0.7; // Thicker lines
            ctx.beginPath(); ctx.moveTo(a.x,a.y); ctx.lineTo(b.x,b.y); ctx.stroke();
          }
        }
      }
      requestAnimationFrame(tick);
    }
    tick();
  }
}