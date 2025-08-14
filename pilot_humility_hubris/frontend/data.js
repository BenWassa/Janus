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
        { id:'hum', label: 'Hum a fragment of song and listen for an answer.', delta:{ Hubris:-0.35, Moodiness:+0.2 }, whisper: 'You invited the room to speak first.' },
        { id:'silence', label: 'Close the parlor door and keep the silence.', delta:{ Hubris:+0.35, Control:+0.2 }, whisper: 'You prized control over reply.' }
      ]
    },
    {
      id: 'riddle_pond', act: 'Act II · Chambers', title: 'Riddle Pond',
      subtitle: 'A hidden pond whispers a riddle only you can hear.',
      text: 'Every answer is a door; most are locked from the other side.',
      options: [
        { id:'clever', label: 'Answer with a clever twist that feels like a lie.', delta:{ Hubris:+0.5, Deception:+0.3 }, whisper: 'You shaped truth into a better weapon.' },
        { id:'stones', label: 'Skip stones until the question dissolves.', delta:{ Hubris:-0.5, Apathy:+0.3 }, whisper: 'You refused the duel of tongues.' }
      ]
    },
    {
      id: 'threshold', act: 'Act III · Crossroads', title: 'Quiet Threshold',
      subtitle: 'Two doors lean toward you like choices already chosen.',
      text: 'One is licked by flame. One is draped in shadow. Both are unlocked.',
      options: [
        { id:'flame', label: 'Step through the flame‑licked archway.', delta:{ Hubris:+0.6, Wrath:+0.3 }, whisper: 'You walked where light demands tribute.' },
        { id:'shadow', label: 'Pass by the shadow‑draped gate.', delta:{ Hubris:-0.6, Fear:+0.3 }, whisper: 'You chose the softness that hides its edge.' }
      ]
    },
    {
      id: 'garden_masks', act: 'Act III · Crossroads', title: 'Garden of Masks',
      subtitle: 'Masks bloom like flowers, waiting for a face.',
      text: 'Each petal hides a gaze.',
      options: [
        { id:'don', label:'Don an ivory mask and speak with borrowed courage.', delta:{ Hubris:+0.5, Deception:+0.5 }, whisper:'You wore a face that was not yours.' },
        { id:'shatter', label:'Shatter a mask and scatter its petals.', delta:{ Wrath:+0.8, Hubris:+0.2 }, whisper:'You left fragments to warn the garden.' },
        { id:'walk_on', label:'Walk past without touching a single bloom.', delta:{}, whisper:'Not every temptation roots in you.' }
      ]
    },
    {
      id: 'clockwork_market', act: 'Act IV · Bazaar', title: 'Clockwork Market',
      subtitle: 'Vendors trade seconds and regrets.',
      text: 'Time ticks from every stall.',
      options: [
        { id:'buy_time', label:'Purchase a minute with an embarrassing memory.', delta:{ Avarice:+0.5, Fear:+0.2 }, whisper:'You paid the past to stretch the future.' },
        { id:'steal_gear', label:'Pocket a tiny gear when no one looks.', delta:{ Deception:+0.5, Avarice:+0.2 }, whisper:'You took motion without paying the toll.' },
        { id:'leave_watch', label:'Leave your watch as a gift and walk on.', delta:{ Hubris:-0.5, Apathy:+0.2 }, whisper:'You released your claim on the hour.' }
      ]
    },
    {
      id: 'abandoned_stage', act: 'Act V · Echoes', title: 'Abandoned Stage',
      subtitle: 'Curtains stir though no wind moves.',
      text: 'An audience of dust waits in silence.',
      options: [
        { id:'perform', label:'Perform a monologue to the unseen crowd.', delta:{ Hubris:+0.8, Impulsivity:+0.2 }, whisper:'You demanded eyes even when none were offered.' },
        { id:'sweep', label:'Sweep the boards until they gleam.', delta:{ Rigidity:+0.5, Control:+0.2 }, whisper:'You gave order to a forgotten hall.' },
        { id:'close', label:'Close the curtains and depart in quiet.', delta:{}, whisper:'Some stories end without applause.' }
      ]
    }
  ];
export const TRAIT_KEYS = ['Hubris','Avarice','Deception','Wrath','Impulsivity','Rigidity','Moodiness','Control','Fear','Apathy','Envy','Cynicism'];
export const SIGILS = {
    Hubris:'<svg viewBox="0 0 20 20"><path d="M10 2 L14 14 L6 14 Z" fill="currentColor"/></svg>',
    Avarice:'<svg viewBox="0 0 20 20"><circle cx="10" cy="10" r="6" fill="none"/></svg>',
    Deception:'<svg viewBox="0 0 20 20"><rect x="4" y="4" width="12" height="12" fill="none"/><path d="M4 4 L16 16" fill="none"/></svg>',
    Wrath:'<svg viewBox="0 0 20 20"><path d="M10 2 L12 10 L10 18 L8 10 Z" fill="currentColor"/></svg>',
    Impulsivity:'<svg viewBox="0 0 20 20"><circle cx="10" cy="10" r="3" fill="currentColor"/><path d="M10 0 V6" fill="none"/><path d="M10 14 V20" fill="none"/></svg>',
    Rigidity:'<svg viewBox="0 0 20 20"><path d="M4 4 H16 V16 H4 Z" fill="none"/></svg>',
    Moodiness:'<svg viewBox="0 0 20 20"><path d="M2 10 Q10 2 18 10 Q10 18 2 10Z" fill="none"/></svg>',
    Control:'<svg viewBox="0 0 20 20"><circle cx="10" cy="10" r="8" fill="none"/><circle cx="10" cy="10" r="3" fill="currentColor"/></svg>',
    Fear:'<svg viewBox="0 0 20 20"><circle cx="10" cy="10" r="8" fill="none"/><circle cx="10" cy="13" r="2" fill="currentColor"/></svg>',
    Apathy:'<svg viewBox="0 0 20 20"><path d="M4 10 H16" fill="none"/></svg>',
    Envy:'<svg viewBox="0 0 20 20"><path d="M10 4 L14 10 L10 16 L6 10 Z" fill="none"/></svg>',
    Cynicism:'<svg viewBox="0 0 20 20"><path d="M3 7 H17 L13 13 H7 Z" fill="none"/></svg>'
  };
export const TRAIT_COLORS = {
    Hubris:[35,80,50],
    Avarice:[50,85,45],
    Deception:[330,60,50],
    Wrath:[0,75,45],
    Impulsivity:[25,90,50],
    Rigidity:[200,30,45],
    Moodiness:[260,35,40],
    Control:[180,35,45],
    Fear:[210,35,35],
    Apathy:[150,20,60],
    Envy:[120,70,40],
    Cynicism:[210,20,50]
  };
export const ARCHETYPES = {
    'Apathy,Cynicism': {
      name: 'The Wanderer',
      lines: [
        'Distance grants safety and perspective.',
        'Beware the comfort of perpetual detachment.'
      ]
    },
    'Hubris,Rigidity': {
      name: 'The Sentinel',
      lines: [
        'You hold the line between order and ambition.',
        'Structure serves you, until you serve it.'
      ]
    },
    'Deception,Impulsivity': {
      name: 'The Trickster',
      lines: [
        'Your steps spark and vanish in equal measure.',
        'Freedom is your ally; consistency your trial.'
      ]
    }
  };
