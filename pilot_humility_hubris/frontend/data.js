// data.js

// -----------------------------
// Narrative data
// -----------------------------
export const scenes = [
    {
      id: 'mirror_pool', act: 'Act I · Mirrors', title: 'Mirror Pool',
      subtitle: 'A still pool mirrors the sky; your reflection waits for a ripple.',
      text: 'The surface holds your outline with too much patience.',
      options: [
        { id:'disturb', label: 'Disturb the surface and watch your face fracture.', delta:{ Hubris:+0.6, Impulsivity:+0.2 }, whisper: 'You broke the stillness first.' },
        { id:'wait', label: 'Stand motionless until the water calms itself.', delta:{ Hubris:-0.6, Rigidity:+0.2 }, whisper: 'You let the world settle before you moved.' }
      ]
    },
    {
      id: 'twin_scholar', act: 'Act I · Mirrors', title: 'Twin Scholar',
      subtitle: 'Someone identical to you presents a thesis claiming your life’s work.',
      text: 'Their footnotes are perfect. Their voice is yours.',
      options: [
        { id:'dissect', label: 'Publicly dissect their argument until they falter.', delta:{ Hubris:+0.5, Wrath:+0.2 }, whisper: 'You answered threat with edge.' },
        { id:'applaud', label: 'Applaud politely and leave the hall.', delta:{ Hubris:-0.4, Apathy:+0.2 }, whisper: 'You passed through without contest.' }
      ]
    },
    {
      id: 'echo_parlor', act: 'Act II · Chambers', title: 'Echo Parlor',
      subtitle: 'Empty frames reflect only echoes.',
      text: 'A room that remembers sound better than faces.',
      options: [
        { id:'hum', label: 'Hum a fragment of song and listen for an answer.', delta:{ Moodiness:+0.35, Cynicism:-0.2 }, whisper: 'You invited the room to speak first.' },
        { id:'silence', label: 'Close the parlor door and keep the silence.', delta:{ Control:+0.35, Apathy:+0.2 }, whisper: 'You prized control over reply.' }
      ]
    },
    {
      id: 'riddle_pond', act: 'Act II · Chambers', title: 'Riddle Pond',
      subtitle: 'A hidden pond whispers a riddle only you can hear.',
      text: 'Every answer is a door; most are locked from the other side.',
      options: [
        { id:'clever', label: 'Answer with a clever twist that feels like a lie.', delta:{ Deception:+0.5, Hubris:+0.3 }, whisper: 'You shaped truth into a better weapon.' },
        { id:'stones', label: 'Skip stones until the question dissolves.', delta:{ Apathy:+0.3, Impulsivity:+0.2 }, whisper: 'You refused the duel of tongues.' }
      ]
    },
    {
      id: 'threshold', act: 'Act III · Crossroads', title: 'Quiet Threshold',
      subtitle: 'Two doors lean toward you like choices already chosen.',
      text: 'One is licked by flame. One is draped in shadow. Both are unlocked.',
      options: [
        { id:'flame', label: 'Step through the flame‑licked archway.', delta:{ Wrath:+0.6, Impulsivity:+0.3 }, whisper: 'You walked where light demands tribute.' },
        { id:'shadow', label: 'Pass by the shadow‑draped gate.', delta:{ Fear:+0.6, Rigidity:+0.3 }, whisper: 'You chose the softness that hides its edge.' }
      ]
    },
    {
      id: 'garden_masks', act: 'Act III · Crossroads', title: 'Garden of Masks',
      subtitle: 'Masks bloom like flowers, waiting for a face.',
      text: 'Each petal hides a gaze.',
      options: [
        { id:'don', label:'Don an ivory mask and speak with borrowed courage.', delta:{ Deception:+0.5, Hubris:+0.5 }, whisper:'You wore a face that was not yours.' },
        { id:'shatter', label:'Shatter a mask and scatter its petals.', delta:{ Wrath:+0.8, Impulsivity:+0.2 }, whisper:'You left fragments to warn the garden.' },
        { id:'walk_on', label:'Walk past without touching a single bloom.', delta:{ Apathy:+0.4, Cynicism:+0.1 }, whisper:'Not every temptation roots in you.' } // Decoy for multiple traits
      ]
    },
    {
      id: 'clockwork_market', act: 'Act IV · Bazaar', title: 'Clockwork Market',
      subtitle: 'Vendors trade seconds and regrets.',
      text: 'Time ticks from every stall.',
      options: [
        { id:'buy_time', label:'Purchase a minute with an embarrassing memory.', delta:{ Avarice:+0.5, Fear:+0.2 }, whisper:'You paid the past to stretch the future.' },
        { id:'steal_gear', label:'Pocket a tiny gear when no one looks.', delta:{ Deception:+0.5, Avarice:+0.2 }, whisper:'You took motion without paying the toll.' },
        { id:'leave_watch', label:'Leave your watch as a gift and walk on.', delta:{ Apathy:+0.5, Moodiness:-0.2 }, whisper:'You released your claim on the hour.' }
      ]
    },
    {
      id: 'abandoned_stage', act: 'Act V · Echoes', title: 'Abandoned Stage',
      subtitle: 'Curtains stir though no wind moves.',
      text: 'An audience of dust waits in silence.',
      options: [
        { id:'perform', label:'Perform a monologue to the unseen crowd.', delta:{ Hubris:+0.8, Impulsivity:+0.2 }, whisper:'You demanded eyes even when none were offered.' },
        { id:'sweep', label:'Sweep the boards until they gleam.', delta:{ Rigidity:+0.5, Control:+0.2 }, whisper:'You gave order to a forgotten hall.' },
        { id:'close', label:'Close the curtains and depart in quiet.', delta:{ Cynicism:+0.4, Apathy:+0.1 }, whisper:'Some stories end without applause.' } // Decoy for multiple traits
      ]
    }
];

export const TRAIT_KEYS = [
    'Hubris', 'Avarice', 'Deception', 'Control', 'Wrath', 'Fear',
    'Impulsivity', 'Envy', 'Apathy', 'Cynicism', 'Moodiness', 'Rigidity'
];

export const SIGILS = {
    Hubris:'<svg viewBox="0 0 20 20"><path d="M10 2 L14 14 L6 14 Z" fill="currentColor"/></svg>', // Triangle pointing up (ambition, pride)
    Avarice:'<svg viewBox="0 0 20 20"><circle cx="10" cy="10" r="6" fill="currentColor"/><path d="M7 10 L13 10 M10 7 L10 13" stroke="white" stroke-width="1.5"/></svg>', // Coin with cross (possessiveness)
    Deception:'<svg viewBox="0 0 20 20"><path d="M4 10 Q10 2 16 10 Q10 18 4 10 Z" fill="none" stroke="currentColor" stroke-width="1.5"/><circle cx="8" cy="10" r="1.5" fill="currentColor"/><circle cx="12" cy="10" r="1.5" fill="currentColor"/></svg>', // Mask/Eyes
    Control:'<svg viewBox="0 0 20 20"><path d="M10 2 V18 M2 10 H18" stroke="currentColor" stroke-width="1.5"/><circle cx="10" cy="10" r="3" fill="currentColor"/></svg>', // Crossroads/Target
    Wrath:'<svg viewBox="0 0 20 20"><path d="M10 2 L12 10 L10 18 L8 10 Z M10 18 V20" fill="currentColor" stroke="currentColor" stroke-width="0.5"/></svg>', // Flame/Bolt
    Fear:'<svg viewBox="0 0 20 20"><path d="M10 4 L14 16 H6 Z" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M10 10 L10 13" stroke="currentColor" stroke-width="1.5"/></svg>', // Trembling figure/inverted triangle
    Impulsivity:'<svg viewBox="0 0 20 20"><circle cx="10" cy="10" r="3" fill="currentColor"/><path d="M10 0 V6 M10 14 V20 M0 10 H6 M14 10 H20" stroke="currentColor" stroke-width="1.5"/></svg>', // Burst/Explosion
    Envy:'<svg viewBox="0 0 20 20"><path d="M10 2 L10 18 M10 10 L18 10 M10 10 L2 10" stroke="currentColor" stroke-width="1.5"/></svg>', // Reaching hand/incomplete circle
    Apathy:'<svg viewBox="0 0 20 20"><path d="M5 10 H15" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>', // Flat line
    Cynicism:'<svg viewBox="0 0 20 20"><path d="M3 10 C3 6 7 4 10 4 C13 4 17 6 17 10 C17 14 13 16 10 16 C7 16 3 14 3 10 Z" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>', // Closed eye/oval
    Moodiness:'<svg viewBox="0 0 20 20"><path d="M2 10 Q10 2 18 10 Q10 18 2 10Z" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M6 12 Q10 10 14 12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>', // Shifting wave/face
    Rigidity:'<svg viewBox="0 0 20 20"><rect x="4" y="4" width="12" height="12" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>' // Solid square
};

export const TRAIT_COLORS = {
    Hubris:[35,80,50],       // Amber/Gold
    Avarice:[50,85,45],      // Greenish-gold
    Deception:[330,60,50],   // Deep Rose/Purple
    Control:[180,35,45],     // Teal/Cyan
    Wrath:[0,75,45],         // Deep Red
    Fear:[210,35,35],        // Dark Blue/Grey-blue
    Impulsivity:[25,90,50],  // Bright Orange
    Envy:[120,70,40],        // Dark Green
    Apathy:[240,10,60],      // Muted Blue-grey
    Cynicism:[210,20,50],    // Cool Grey-blue
    Moodiness:[260,35,40],   // Violet
    Rigidity:[200,30,45]     // Slate Blue
};

// Archetypes are sorted alphabetically by trait keys for consistent lookup
export const ARCHETYPES = {
    'Apathy,Cynicism': {
      name: 'The Detached Observer',
      lines: [
        'Distance grants safety and perspective, allowing you to witness without entanglement.',
        'Beware the comfort of perpetual detachment, lest the world\'s vibrant hues fade to grey.'
      ]
    },
    'Hubris,Rigidity': {
      name: 'The Unyielding Architect',
      lines: [
        'You build on a foundation of certainty, shaping the world with unwavering will.',
        'Structure serves you, until you serve it, and your ambition calcifies into dogma.'
      ]
    },
    'Deception,Impulsivity': {
      name: 'The Shifting Mask',
      lines: [
        'Your steps spark and vanish in equal measure, leaving trails of unpredictable light.',
        'Freedom is your ally; consistency your trial. Embrace authenticity lest you lose your true face.'
      ]
    },
    'Wrath,Impulsivity': {
      name: 'The Unbridled Storm',
      lines: [
        'You move with the force of a sudden tempest, clearing paths with fervent energy.',
        'Your power is undeniable, but it risks consuming all in its path, including yourself.'
      ]
    },
    'Fear,Control': {
      name: 'The Cautious Warden',
      lines: [
        'You build walls against the unknown, guarding what is precious with meticulous foresight.',
        'Security is a fragile comfort; remember that even the strongest walls can imprison as well as protect.'
      ]
    },
    'Avarice,Envy': {
      name: 'The Hungry Eye',
      lines: [
        'Your gaze is drawn to what is beyond your grasp, seeing potential where others see only lack.',
        'Desire fuels your journey, but endless craving can leave you forever wanting, never truly fulfilled.'
      ]
    },
    'Moodiness,Cynicism': {
      name: 'The Melancholy Seer',
      lines: [
        'You perceive the world\'s flaws with a sensitive and often somber clarity.',
        'Wisdom can be born of sorrow, but ensure your insights do not lead to an isolating despair.'
      ]
    },
    'Hubris': { // Single dominant trait archetype
      name: 'The Ascendant Will',
      lines: [
        'You walk with a radiant certainty, your path illuminated by your own conviction.',
        'Remember that true strength lies not just in height, but in the breadth of understanding.'
      ]
    },
    'Apathy': {
      name: 'The Unmoved Current',
      lines: [
        'You drift through the currents of existence, untouched by the passions that stir others.',
        'While peace can be found in detachment, beware the silence that comes from never truly engaging.'
      ]
    },
    'Fear': {
      name: 'The Shadowed Path',
      lines: [
        'You navigate the labyrinth with a careful step, always aware of the unseen dangers.',
        'Prudence is a guide, but remember that some growth lies beyond the edge of your comfort.'
      ]
    },
    // Add more archetypes for various single traits and other combinations as needed for v2 depth
};