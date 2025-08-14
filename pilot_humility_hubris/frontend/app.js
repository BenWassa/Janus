import { scenes, TRAIT_KEYS, SIGILS, TRAIT_COLORS, ARCHETYPES } from "./data.js";

 
  // Trait state: multi-trait object from Hamartia Engine
  const traits = Object.fromEntries(TRAIT_KEYS.map(t=>[t,0]));
  const journal = []; // poetic echo lines
  const path = [];    // record of choices
  let sceneIndex = 0;

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
  const traitBar = document.getElementById('traitBar');
  const sigilRepo = document.getElementById('sigils');
  const tarotSpread = document.getElementById('tarotSpread');
  const modeSelect = document.getElementById('mode');
  const restart = document.getElementById('restart');
  const saveBtn = document.getElementById('save');
  const loadBtn = document.getElementById('load');
  const portrait = document.getElementById('portrait');
  const journalEl = document.getElementById('journal');
  const reading = document.getElementById('reading');
  const downloadBtn = document.getElementById('download');
  const againBtn = document.getElementById('again');

  // Entry
  playBtn.addEventListener('click', startGame);
  restart.addEventListener('click', resetAll);
  againBtn.addEventListener('click', resetAll);
  downloadBtn.addEventListener('click', downloadRitual);
  saveBtn.addEventListener('click', saveState);
  loadBtn.addEventListener('click', loadState);

  // Keyboard shortcuts (1/2)
  document.addEventListener('keydown', (e)=>{
    if (game.style.display !== 'none' && (e.key === '1' || e.key === '2')) {
      const idx = e.key === '1' ? 0 : 1;
      const opts = scenes[sceneIndex].options;
      if (opts[idx]) handleChoice(opts[idx], {x: window.innerWidth/2, y: window.innerHeight/2});
    }
  });

  function startGame(){
    start.style.display = 'none';
    reflection.style.display = 'none';
    game.style.display = '';
    TRAIT_KEYS.forEach(k=> traits[k] = 0);
    sigilRepo.innerHTML = '';
    tarotSpread.innerHTML = '';
    sceneIndex = 0; journal.length = 0; path.length = 0;
    renderScene();
    updateAtmosphere();
  }

  function resetAll(){
    start.style.display = '';
    game.style.display = 'none';
    reflection.style.display = 'none';
  }

  function saveState(){
    const state = { traits, journal, path, sceneIndex };
    localStorage.setItem('janusState', JSON.stringify(state));
  }

  function loadState(){
    const raw = localStorage.getItem('janusState');
    if(!raw) return;
    const state = JSON.parse(raw);
    Object.assign(traits, state.traits || {});
    journal.length = 0; (state.journal || []).forEach(j=> journal.push(j));
    path.length = 0; (state.path || []).forEach(p=> path.push(p));
    sceneIndex = state.sceneIndex || 0;

    sigilRepo.innerHTML = '';
    tarotSpread.innerHTML = '';
    for(let i=0;i<sceneIndex && i<path.length;i++){
      const step = path[i];
      for(const [k,v] of Object.entries(step.delta || {})){
        if(Math.abs(v) >= 0.4) showSigil(k);
      }
      addTarotCard();
    }

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
  }

  function renderScene(){
    const s = scenes[sceneIndex];
    sceneId.textContent = s.act;
    sceneTitle.textContent = s.title;
    sceneSubtitle.textContent = s.subtitle;
    sceneText.textContent = s.text;

    decision.innerHTML = '';
    sceneCard.classList.add('dissolve');
    setTimeout(()=> sceneCard.classList.remove('dissolve'), 720);

    const mode = modeSelect.value;
    if (mode === 'orbit') renderOrbit(s.options);
    else if (mode === 'lens') renderLens(s.options);
    else renderWhisper(s.options);
  }

  // -----------------------------
  // Orbit Selector
  // -----------------------------
  function renderOrbit(options){
    const wrap = document.createElement('div');
    wrap.className = 'orbit';
    const cx = 210, cy = 210, r = 150; // center, radius
    const baseAngle = Math.random() * Math.PI * 2 * 0.25; // small randomization
    options.forEach((opt, i)=>{
      const angle = baseAngle + (i * (Math.PI * 2 / options.length));
      const x = cx + r * Math.cos(angle) - 80;
      const y = cy + r * Math.sin(angle) - 22;
      const node = document.createElement('div');
      node.className = 'glyph';
      node.textContent = opt.label;
      node.style.left = x + 'px';
      node.style.top = y + 'px';
      node.style.animationDelay = (i * 80) + 'ms';
      node.addEventListener('click', (ev)=>{
        node.classList.add('selected');
        handleChoice(opt, {x: ev.clientX, y: ev.clientY});
      });
      wrap.appendChild(node);
    });
    decision.appendChild(wrap);
  }

  // -----------------------------
  // Cognitive Lens
  // -----------------------------
  function renderLens(options){
    const wrap = document.createElement('div');
    wrap.className = 'lens-wrap';
    options.forEach((opt, i)=>{
      const card = document.createElement('div');
      card.className = 'lens-card';
      card.innerHTML = `<div>${opt.label}</div><div class="hint">Focus the lens, then click</div>`;
      card.style.animationDelay = (i * 80) + 'ms';
      card.addEventListener('mousemove', (e)=>{
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left, y = e.clientY - rect.top;
        card.style.setProperty('--mx', x + 'px');
        card.style.setProperty('--my', y + 'px');
      });
      card.addEventListener('mouseenter', ()=> card.classList.add('focus'));
      card.addEventListener('mouseleave', ()=> card.classList.remove('focus'));
      card.addEventListener('click', (ev)=> handleChoice(opt, {x: ev.clientX, y: ev.clientY}));
      wrap.appendChild(card);
    });
    decision.appendChild(wrap);
  }

  // -----------------------------
  // Whisper Panel
  // -----------------------------
  function renderWhisper(options){
    let idx = 0;
    const wrap = document.createElement('div');
    wrap.className = 'whisper-wrap';
    const text = document.createElement('div');
    text.className = 'whisper-text';
    const actions = document.createElement('div');
    actions.className = 'whisper-actions';
    const accept = document.createElement('button');
    accept.textContent = 'Accept';
    const reject = document.createElement('button');
    reject.textContent = 'Reject';
    actions.appendChild(accept); actions.appendChild(reject);
    wrap.appendChild(text);
    wrap.appendChild(actions);
    decision.appendChild(wrap);
    function show(){ text.textContent = options[idx].label; }
    accept.addEventListener('click', (ev)=> handleChoice(options[idx], {x: ev.clientX, y: ev.clientY}));
    reject.addEventListener('click', ()=>{ idx = (idx+1)%options.length; show(); });
    show();
  }

  // -----------------------------
  // Choice handling
  // -----------------------------
  function handleChoice(opt, point){
    // Echo ripple feedback
    echoRipple(point.x, point.y);

    // Update traits & record
    for(const [k,v] of Object.entries(opt.delta || {})){
      traits[k] = clamp((traits[k]||0) + v, -1, 1);
      if(Math.abs(v) >= 0.4) showSigil(k);
    }
    const sceneId = scenes[sceneIndex].id;
    path.push({ scene: sceneId, choice: opt.id, delta: opt.delta });
    console.log('[Telemetry]', { scene: sceneId, choice: opt.id, delta: opt.delta || {}, traits: { ...traits } });
    journal.push(`• ${opt.whisper}`);
    addTarotCard();

    updateAtmosphere();

    // Next scene or reflection
    sceneIndex++;
    if (sceneIndex < scenes.length) {
      renderScene();
    } else {
      showReflection();
    }
  }

  function updateAtmosphere(){
    const entries = Object.entries(traits).sort((a,b)=>Math.abs(b[1]) - Math.abs(a[1]));
    const top = entries.slice(0,3);
    let total = 0, hue = 200, sat = 18, light = 8; // defaults
    if(top.length){
      hue = sat = light = 0;
      top.forEach(([k,v])=>{
        const weight = Math.abs(v);
        const [h,s,l] = TRAIT_COLORS[k];
        hue += h*weight; sat += s*weight; light += l*weight; total += weight;
      });
      hue /= total; sat /= total; light /= total;
    }
    document.documentElement.style.setProperty('--bg-hue', hue.toFixed(0));
    document.documentElement.style.setProperty('--bg-sat', sat.toFixed(0)+'%');
    document.documentElement.style.setProperty('--bg-light', light.toFixed(0)+'%');

    const accentHue = (hue + 20) % 360;
    document.documentElement.style.setProperty('--accent', `${accentHue}, 75%, 62%`);

    const hubris = traits.Hubris || 0;
    traitBar.style.width = ((0.5 + hubris/2) * 100) + '%';
  }

  function showReflection(){
    game.style.display = 'none';
    reflection.style.display = '';
    // Portrait & reading
    renderPortraitAndReading();
    // Journal
    journalEl.textContent = journal.join('\n\n');
  }

  function determineArchetype(){
    const keys = Object.entries(traits)
      .sort((a,b)=>Math.abs(b[1]) - Math.abs(a[1]))
      .slice(0,2)
      .map(([k])=>k)
      .sort()
      .join(',');
    return ARCHETYPES[keys] || { name: 'The Unshaped', lines: ['Your pattern resists simple names.'] };
  }

  function renderPortraitAndReading(){
    portrait.innerHTML = '';
    const svgNS = 'http://www.w3.org/2000/svg';
    const svg = document.createElementNS(svgNS, 'svg');
    svg.setAttribute('viewBox','0 0 300 300');

    // Background aura gradient
    const defs = document.createElementNS(svgNS, 'defs');
    const grad = document.createElementNS(svgNS, 'radialGradient');
    grad.id = 'aura';
    grad.innerHTML = `
      <stop offset="0%" stop-color="hsla(${getComputedStyle(document.documentElement).getPropertyValue('--bg-hue')},70%,60%,0.55)"/>
      <stop offset="100%" stop-color="rgba(0,0,0,0)"/>
    `;
    defs.appendChild(grad);
    svg.appendChild(defs);

    const aura = document.createElementNS(svgNS, 'circle');
    aura.setAttribute('cx','150'); aura.setAttribute('cy','110'); aura.setAttribute('r','100');
    aura.setAttribute('fill','url(#aura)');
    svg.appendChild(aura);

    // Determine dominant traits for silhouette/adornments
    const sorted = Object.entries(traits).sort((a,b)=>Math.abs(b[1]) - Math.abs(a[1]));
    const topTraits = sorted.slice(0,2).map(([k])=>k);
    const topTraitsAll = sorted.slice(0,3).map(([k])=>k);

    // Abstract silhouette with trait distortion
    const head = document.createElementNS(svgNS, 'circle');
    head.setAttribute('cx','150'); head.setAttribute('cy','100'); head.setAttribute('r','32');
    head.setAttribute('fill','rgba(255,255,255,0.25)'); head.setAttribute('stroke','rgba(255,255,255,0.3)');
    let bodyPath = 'M110,180 Q150,150 190,180 L190,240 Q150,260 110,240 Z';
    if(topTraits[0] === 'Rigidity') bodyPath = 'M110,180 L150,150 190,180 190,240 110,240 Z';
    else if(topTraits[0] === 'Impulsivity') bodyPath = 'M110,180 Q150,140 190,180 Q150,260 110,240 Z';
    const body = document.createElementNS(svgNS, 'path');
    body.setAttribute('d', bodyPath);
    body.setAttribute('fill','rgba(255,255,255,0.12)');
    body.setAttribute('stroke','rgba(255,255,255,0.25)');
    svg.appendChild(head); svg.appendChild(body);

    // Adornments for dominant traits
    if(topTraits.includes('Impulsivity')){
      const swirl = document.createElementNS(svgNS,'path');
      swirl.setAttribute('d','M60,220 Q150,170 240,220');
      swirl.setAttribute('stroke','rgba(255,255,255,0.25)');
      swirl.setAttribute('stroke-width','3');
      swirl.setAttribute('fill','none');
      svg.appendChild(swirl);
    }
    if(topTraits.includes('Rigidity')){
      const bars = document.createElementNS(svgNS,'path');
      bars.setAttribute('d','M120,180 L120,240 M180,180 L180,240');
      bars.setAttribute('stroke','rgba(255,255,255,0.25)');
      bars.setAttribute('fill','none');
      svg.appendChild(bars);
    }

    portrait.appendChild(svg);

    // Archetype reading
    const arche = determineArchetype();
    const title = `Mythic Persona: ${arche.name}`;
    const narrative = `${arche.lines.join(' ')} Dominant traits: ${topTraitsAll.join(' & ')}.`;
    reading.innerHTML = `<div class="badge">Cosmic Constellation Narrative</div><h2 class="title" style="margin-top:8px;">${title}</h2><div class="scene-text"><p>${narrative}</p></div>`;
  }

  function downloadRitual(){
    const text = `HERO\'S CHRONICLE (Prototype)\n\n` + journal.join('\n\n');
    const blob = new Blob([text], {type:'text/plain'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a'); a.href = url; a.download = 'janus_ritual.txt'; a.click();
    URL.revokeObjectURL(url);
  }

  function clamp(v, a, b){ return Math.max(a, Math.min(b, v)); }

  function showSigil(trait){
    let node = sigilRepo.querySelector(`[data-trait="${trait}"]`);
    if(!node){
      node = document.createElement('div');
      node.className = 'sigil';
      node.dataset.trait = trait;
      node.innerHTML = SIGILS[trait] || '';
      sigilRepo.appendChild(node);
    }
    node.classList.add('active');
    setTimeout(()=> node.classList.remove('active'), 800);
  }

  function addTarotCard(){
    const card = document.createElement('div');
    card.className = 'tarot-card';
    tarotSpread.appendChild(card);
    requestAnimationFrame(()=> card.classList.add('reveal'));
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
  // Constellation bloom (ambient)
  // -----------------------------
  const canvas = document.getElementById('constellation');
  const ctx = canvas.getContext('2d');
  let stars = [];
  function initStars(){
    const w = canvas.width = canvas.clientWidth;
    const h = canvas.height = canvas.clientHeight;
    stars = Array.from({length: 80}, ()=>({
      x: Math.random()*w,
      y: Math.random()*h,
      r: Math.random()*1.7 + 0.3,
      b: Math.random()*0.4 + 0.2,
      vx: (Math.random()-0.5)*0.05,
      vy: (Math.random()-0.5)*0.05,
    }));
  }
  window.addEventListener('resize', initStars);
  initStars();
  function tick(){
    const w = canvas.width = canvas.clientWidth;
    const h = canvas.height = canvas.clientHeight;
    ctx.clearRect(0,0,w,h);

    const hue = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--bg-hue')) || 0;

    // cluster centers move subtly with hubris trait (–1..1) → shift focus left/right
    const hubris = traits.Hubris || 0;
    const cx = w*(0.35 + 0.3*((hubris+1)/2));
    const cy = h*0.55;

    for (const s of stars){
      s.x = (s.x + s.vx + w) % w;
      s.y = (s.y + s.vy + h) % h;
      s.b = clamp(s.b + (Math.random()-0.5)*0.01, 0.2, 0.6);
      const dx = s.x - cx, dy = s.y - cy; const d = Math.sqrt(dx*dx + dy*dy) + 1;
      const glow = 1 / (d*0.04); // nearer to cluster is brighter
      const alpha = clamp(s.b + glow*0.9, 0, 1);
      ctx.beginPath(); ctx.arc(s.x, s.y, s.r, 0, Math.PI*2);
      ctx.fillStyle = `hsla(${hue},50%,80%,${alpha})`;
      ctx.fill();
    }

    for(let i=0;i<stars.length;i++){
      for(let j=i+1;j<stars.length;j++){
        const a = stars[i], b = stars[j];
        const dx = a.x-b.x, dy = a.y-b.y; const d = Math.sqrt(dx*dx+dy*dy);
        if(d < 50){
          const alpha = 0.1 * (1 - d/50);
          ctx.strokeStyle = `hsla(${hue},60%,70%,${alpha})`;
          ctx.lineWidth = 0.5;
          ctx.beginPath(); ctx.moveTo(a.x,a.y); ctx.lineTo(b.x,b.y); ctx.stroke();
        }
      }
    }
    requestAnimationFrame(tick);
  }
  tick();
