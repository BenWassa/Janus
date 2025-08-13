# Claude Dashboard Files
below is the code for the Claude Dashboard components

```tsx

import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, LineChart, Line, ResponsiveContainer } from 'recharts';
import { Play, Settings, Filter, Download, AlertTriangle, Check, Clock, RefreshCw } from 'lucide-react';

// Type definitions
type Trait = 
  | 'Hubris' | 'Avarice' | 'Deception' | 'Control & Perfectionism'
  | 'Wrath' | 'Fear & Insecurity' | 'Impulsivity' | 'Envy'
  | 'Apathy & Sloth' | 'Pessimism & Cynicism' | 'Moodiness & Indirectness' | 'Rigidity';

type Policy = 'hubris' | 'control_fear' | 'deception_avarice' | 'reckless' | 'balanced' | 'random';

type RunSummary = {
  runId: string;
  policy: Policy;
  seed?: number;
  steps: number;
  normalized: Record<Trait, number>;
  top3: Trait[];
  endingId?: string;
  flags: string[];
  timestamp: string;
};

type Decision = {
  step: number;
  sceneId: string;
  choiceId: string;
  text: string;
  primary: Trait;
  pw: 0 | 0.2 | 0.5 | 0.8;
  secondary?: Trait;
  sw?: number;
};

type RunDetail = RunSummary & {
  timeline: Array<{ step: number; totals: Record<Trait, number> }>;
  decisions: Decision[];
  revealText: string;
};

// Color scheme
const traitColors: Record<Trait, string> = {
  'Hubris': '#FF6B6B',
  'Avarice': '#4ECDC4',
  'Deception': '#45B7D1',
  'Control & Perfectionism': '#96CEB4',
  'Wrath': '#FECA57',
  'Fear & Insecurity': '#FF9FF3',
  'Impulsivity': '#54A0FF',
  'Envy': '#5F27CD',
  'Apathy & Sloth': '#00D2D3',
  'Pessimism & Cynicism': '#FF9F43',
  'Moodiness & Indirectness': '#EE5A6F',
  'Rigidity': '#C44569'
};

// Mock data
const mockRunSummaries: RunSummary[] = [
  {
    runId: 'run-001',
    policy: 'hubris',
    seed: 12345,
    steps: 15,
    normalized: {
      'Hubris': 85, 'Avarice': 32, 'Deception': 45, 'Control & Perfectionism': 67,
      'Wrath': 23, 'Fear & Insecurity': 12, 'Impulsivity': 78, 'Envy': 34,
      'Apathy & Sloth': 15, 'Pessimism & Cynicism': 29, 'Moodiness & Indirectness': 41, 'Rigidity': 56
    },
    top3: ['Hubris', 'Impulsivity', 'Control & Perfectionism'],
    endingId: 'ending_dominance',
    flags: ['High trait concentration'],
    timestamp: '2024-01-15T10:30:00Z'
  },
  {
    runId: 'run-002',
    policy: 'control_fear',
    seed: 67890,
    steps: 18,
    normalized: {
      'Hubris': 15, 'Avarice': 25, 'Deception': 89, 'Control & Perfectionism': 92,
      'Wrath': 8, 'Fear & Insecurity': 87, 'Impulsivity': 12, 'Envy': 45,
      'Apathy & Sloth': 23, 'Pessimism & Cynicism': 67, 'Moodiness & Indirectness': 34, 'Rigidity': 78
    },
    top3: ['Control & Perfectionism', 'Deception', 'Fear & Insecurity'],
    endingId: 'ending_control',
    flags: [],
    timestamp: '2024-01-15T11:15:00Z'
  }
];

// Components
const SliderWithNumber: React.FC<{
  label: string;
  value: number;
  onChange: (value: number) => void;
  min: number;
  max: number;
  step?: number;
}> = ({ label, value, onChange, min, max, step = 1 }) => (
  <div className="space-y-2">
    <div className="flex justify-between items-center">
      <label className="text-sm font-medium text-gray-300">{label}</label>
      <input
        type="number"
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
        className="w-16 px-2 py-1 bg-gray-700 border border-gray-600 rounded text-sm text-white"
        min={min}
        max={max}
        step={step}
      />
    </div>
    <input
      type="range"
      value={value}
      onChange={(e) => onChange(Number(e.target.value))}
      min={min}
      max={max}
      step={step}
      className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer slider"
    />
    <div className="flex justify-between text-xs text-gray-500">
      <span>{min}</span>
      <span>{max}</span>
    </div>
  </div>
);

const ArchetypeSelect: React.FC<{
  selected: Policy[];
  onChange: (selected: Policy[]) => void;
}> = ({ selected, onChange }) => {
  const archetypes: { value: Policy; label: string }[] = [
    { value: 'hubris', label: 'Hubris-Forward' },
    { value: 'control_fear', label: 'Control+Fear' },
    { value: 'deception_avarice', label: 'Deception+Avarice' },
    { value: 'reckless', label: 'Reckless' },
    { value: 'balanced', label: 'Balanced' }
  ];

  const toggleArchetype = (archetype: Policy) => {
    if (selected.includes(archetype)) {
      onChange(selected.filter(a => a !== archetype));
    } else {
      onChange([...selected, archetype]);
    }
  };

  return (
    <div className="space-y-2">
      <label className="text-sm font-medium text-gray-300">Archetypes</label>
      <div className="flex flex-wrap gap-2">
        {archetypes.map(({ value, label }) => (
          <button
            key={value}
            onClick={() => toggleArchetype(value)}
            className={`px-3 py-1 rounded-full text-sm transition-colors ${
              selected.includes(value)
                ? 'bg-blue-600 text-white'
                : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
            }`}
          >
            {label}
          </button>
        ))}
      </div>
    </div>
  );
};

const WeightBadge: React.FC<{ weight: number }> = ({ weight }) => {
  const getStyle = (w: number) => {
    switch (w) {
      case 0: return 'bg-gray-600 text-gray-300';
      case 0.2: return 'bg-yellow-600 text-yellow-100';
      case 0.5: return 'bg-orange-600 text-orange-100';
      case 0.8: return 'bg-red-600 text-red-100';
      default: return 'bg-gray-600 text-gray-300';
    }
  };

  const getLabel = (w: number) => {
    switch (w) {
      case 0: return 'Decoy';
      case 0.2: return '+0.2';
      case 0.5: return '+0.5';
      case 0.8: return '+0.8';
      default: return w.toString();
    }
  };

  return (
    <span className={`px-2 py-1 rounded text-xs font-medium ${getStyle(weight)}`}>
      {getLabel(weight)}
    </span>
  );
};

const TraitChip: React.FC<{ trait: Trait }> = ({ trait }) => (
  <span
    className="px-2 py-1 rounded text-xs font-medium text-white"
    style={{ backgroundColor: traitColors[trait] }}
  >
    {trait}
  </span>
);

const ControlPanel: React.FC<{
  thresholds: { dominance: number; actCap: number; decoyRatio: number };
  onThresholdChange: (key: string, value: number) => void;
  selectedArchetypes: Policy[];
  onArchetypeChange: (archetypes: Policy[]) => void;
  onRun: (type: 'random' | 'archetype' | 'suite') => void;
  isRunning: boolean;
}> = ({ thresholds, onThresholdChange, selectedArchetypes, onArchetypeChange, onRun, isRunning }) => (
  <div className="bg-gray-800 rounded-lg p-6 space-y-6">
    <h2 className="text-lg font-semibold text-white mb-4">Control Panel</h2>
    
    <div className="space-y-4">
      <h3 className="text-sm font-medium text-gray-300 border-b border-gray-700 pb-2">Thresholds & Caps</h3>
      <SliderWithNumber
        label="Dominance Threshold (%)"
        value={thresholds.dominance}
        onChange={(v) => onThresholdChange('dominance', v)}
        min={0}
        max={100}
      />
      <SliderWithNumber
        label="Per-trait Act Cap"
        value={thresholds.actCap}
        onChange={(v) => onThresholdChange('actCap', v)}
        min={1}
        max={50}
      />
      <SliderWithNumber
        label="Decoy Target Ratio (%)"
        value={thresholds.decoyRatio}
        onChange={(v) => onThresholdChange('decoyRatio', v)}
        min={0}
        max={100}
      />
    </div>

    <div className="space-y-4">
      <h3 className="text-sm font-medium text-gray-300 border-b border-gray-700 pb-2">Run Configuration</h3>
      <ArchetypeSelect
        selected={selectedArchetypes}
        onChange={onArchetypeChange}
      />
    </div>

    <div className="space-y-3">
      <h3 className="text-sm font-medium text-gray-300 border-b border-gray-700 pb-2">Execute</h3>
      <div className="grid grid-cols-1 gap-2">
        <button
          onClick={() => onRun('random')}
          disabled={isRunning}
          className="flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed text-white px-4 py-2 rounded transition-colors"
        >
          {isRunning ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4" />}
          Run Random
        </button>
        <button
          onClick={() => onRun('archetype')}
          disabled={isRunning || selectedArchetypes.length === 0}
          className="flex items-center justify-center gap-2 bg-green-600 hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed text-white px-4 py-2 rounded transition-colors"
        >
          {isRunning ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4" />}
          Run Archetype{selectedArchetypes.length > 1 ? 's' : ''}
        </button>
        <button
          onClick={() => onRun('suite')}
          disabled={isRunning}
          className="flex items-center justify-center gap-2 bg-purple-600 hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed text-white px-4 py-2 rounded transition-colors"
        >
          {isRunning ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4" />}
          Run Full Suite
        </button>
      </div>
    </div>
  </div>
);

const GroupedBarChart: React.FC<{ data: RunSummary[] }> = ({ data }) => {
  const chartData = Object.keys(traitColors).map(trait => {
    const traitData = { trait };
    data.forEach(run => {
      traitData[run.policy] = run.normalized[trait as Trait];
    });
    return traitData;
  });

  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
        <XAxis dataKey="trait" stroke="#9CA3AF" angle={-45} textAnchor="end" height={100} />
        <YAxis stroke="#9CA3AF" />
        <Tooltip
          contentStyle={{ backgroundColor: '#1F2937', border: '1px solid #374151', borderRadius: '8px' }}
          labelStyle={{ color: '#E5E7EB' }}
        />
        <Legend />
        {data.map(run => (
          <Bar
            key={run.runId}
            dataKey={run.policy}
            fill={`hsl(${data.indexOf(run) * 60}, 70%, 50%)`}
            name={run.policy.replace('_', '+')}
          />
        ))}
      </BarChart>
    </ResponsiveContainer>
  );
};

const RunsTable: React.FC<{ runs: RunSummary[]; onRunClick: (runId: string) => void }> = ({ runs, onRunClick }) => (
  <div className="bg-gray-800 rounded-lg overflow-hidden">
    <div className="overflow-x-auto">
      <table className="w-full">
        <thead className="bg-gray-700">
          <tr>
            <th className="text-left px-4 py-3 text-sm font-medium text-gray-300">Run ID</th>
            <th className="text-left px-4 py-3 text-sm font-medium text-gray-300">Policy</th>
            <th className="text-left px-4 py-3 text-sm font-medium text-gray-300">Steps</th>
            <th className="text-left px-4 py-3 text-sm font-medium text-gray-300">Top 3 Traits</th>
            <th className="text-left px-4 py-3 text-sm font-medium text-gray-300">Flags</th>
            <th className="text-left px-4 py-3 text-sm font-medium text-gray-300">Timestamp</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-700">
          {runs.map(run => (
            <tr
              key={run.runId}
              onClick={() => onRunClick(run.runId)}
              className="hover:bg-gray-700 cursor-pointer transition-colors"
            >
              <td className="px-4 py-3 text-sm text-blue-400 font-mono">{run.runId}</td>
              <td className="px-4 py-3 text-sm text-gray-300">{run.policy.replace('_', '+')}</td>
              <td className="px-4 py-3 text-sm text-gray-300">{run.steps}</td>
              <td className="px-4 py-3">
                <div className="flex flex-wrap gap-1">
                  {run.top3.map(trait => (
                    <TraitChip key={trait} trait={trait} />
                  ))}
                </div>
              </td>
              <td className="px-4 py-3">
                {run.flags.length > 0 ? (
                  <div className="flex items-center gap-1 text-yellow-400">
                    <AlertTriangle className="w-4 h-4" />
                    <span className="text-sm">{run.flags.length}</span>
                  </div>
                ) : (
                  <Check className="w-4 h-4 text-green-400" />
                )}
              </td>
              <td className="px-4 py-3 text-sm text-gray-400">
                {new Date(run.timestamp).toLocaleString()}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  </div>
);

// Main Dashboard Component
const Dashboard: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'dashboard' | 'runs' | 'traits' | 'settings'>('dashboard');
  const [selectedRun, setSelectedRun] = useState<string | null>(null);
  const [runs, setRuns] = useState<RunSummary[]>(mockRunSummaries);
  const [isRunning, setIsRunning] = useState(false);
  const [chartView, setChartView] = useState<'bars' | 'timeline'>('bars');
  
  const [thresholds, setThresholds] = useState({
    dominance: 70,
    actCap: 15,
    decoyRatio: 25
  });
  
  const [selectedArchetypes, setSelectedArchetypes] = useState<Policy[]>(['hubris']);

  const handleThresholdChange = (key: string, value: number) => {
    setThresholds(prev => ({ ...prev, [key]: value }));
  };

  const handleRun = async (type: 'random' | 'archetype' | 'suite') => {
    setIsRunning(true);
    
    // Simulate run execution
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Generate mock result
    const newRun: RunSummary = {
      runId: `run-${Date.now()}`,
      policy: type === 'random' ? 'random' : selectedArchetypes[0] || 'balanced',
      seed: Math.floor(Math.random() * 100000),
      steps: Math.floor(Math.random() * 10) + 10,
      normalized: Object.keys(traitColors).reduce((acc, trait) => {
        acc[trait as Trait] = Math.floor(Math.random() * 100);
        return acc;
      }, {} as Record<Trait, number>),
      top3: ['Hubris', 'Deception', 'Control & Perfectionism'],
      endingId: `ending_${Math.floor(Math.random() * 5)}`,
      flags: Math.random() > 0.7 ? ['High concentration detected'] : [],
      timestamp: new Date().toISOString()
    };

    setRuns(prev => [newRun, ...prev]);
    setIsRunning(false);
  };

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-1">
              <ControlPanel
                thresholds={thresholds}
                onThresholdChange={handleThresholdChange}
                selectedArchetypes={selectedArchetypes}
                onArchetypeChange={setSelectedArchetypes}
                onRun={handleRun}
                isRunning={isRunning}
              />
            </div>
            <div className="lg:col-span-2 space-y-6">
              <div className="bg-gray-800 rounded-lg p-6">
                <div className="flex justify-between items-center mb-4">
                  <h2 className="text-lg font-semibold text-white">Overview Charts</h2>
                  <div className="flex gap-2">
                    <button
                      onClick={() => setChartView('bars')}
                      className={`px-3 py-1 rounded text-sm transition-colors ${
                        chartView === 'bars' ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300'
                      }`}
                    >
                      Grouped Bars
                    </button>
                    <button
                      onClick={() => setChartView('timeline')}
                      className={`px-3 py-1 rounded text-sm transition-colors ${
                        chartView === 'timeline' ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300'
                      }`}
                    >
                      Timeline
                    </button>
                  </div>
                </div>
                {chartView === 'bars' ? (
                  <GroupedBarChart data={runs} />
                ) : (
                  <div className="h-96 flex items-center justify-center text-gray-400">
                    Timeline view coming soon
                  </div>
                )}
              </div>
            </div>
          </div>
        );

      case 'runs':
        if (selectedRun) {
          const run = runs.find(r => r.runId === selectedRun);
          if (!run) return null;
          
          return (
            <div className="space-y-6">
              <div className="flex items-center gap-4">
                <button
                  onClick={() => setSelectedRun(null)}
                  className="text-blue-400 hover:text-blue-300"
                >
                  ← Back to Runs
                </button>
                <h1 className="text-xl font-semibold text-white">Run Detail: {run.runId}</h1>
              </div>
              
              <div className="bg-gray-800 rounded-lg p-6">
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                  <div>
                    <label className="text-sm text-gray-400">Policy</label>
                    <p className="text-white">{run.policy.replace('_', '+')}</p>
                  </div>
                  <div>
                    <label className="text-sm text-gray-400">Seed</label>
                    <p className="text-white font-mono">{run.seed}</p>
                  </div>
                  <div>
                    <label className="text-sm text-gray-400">Steps</label>
                    <p className="text-white">{run.steps}</p>
                  </div>
                  <div>
                    <label className="text-sm text-gray-400">Timestamp</label>
                    <p className="text-white">{new Date(run.timestamp).toLocaleString()}</p>
                  </div>
                </div>
                
                <div className="mb-6">
                  <h3 className="text-lg font-medium text-white mb-3">Top 3 Traits</h3>
                  <div className="flex flex-wrap gap-2">
                    {run.top3.map(trait => (
                      <TraitChip key={trait} trait={trait} />
                    ))}
                  </div>
                </div>

                <div className="mb-6">
                  <h3 className="text-lg font-medium text-white mb-3">Normalized Scores</h3>
                  <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
                    {Object.entries(run.normalized).map(([trait, score]) => (
                      <div key={trait} className="bg-gray-700 p-3 rounded">
                        <div className="text-sm text-gray-300 mb-1">{trait}</div>
                        <div className="text-lg font-semibold text-white">{score}%</div>
                        <div
                          className="h-2 bg-gray-600 rounded mt-2"
                        >
                          <div
                            className="h-full rounded"
                            style={{
                              width: `${score}%`,
                              backgroundColor: traitColors[trait as Trait]
                            }}
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {run.flags.length > 0 && (
                  <div className="bg-yellow-900/20 border border-yellow-700 rounded-lg p-4">
                    <div className="flex items-center gap-2 mb-2">
                      <AlertTriangle className="w-5 h-5 text-yellow-400" />
                      <h3 className="text-lg font-medium text-yellow-400">Flags</h3>
                    </div>
                    <ul className="space-y-1">
                      {run.flags.map((flag, idx) => (
                        <li key={idx} className="text-yellow-300">{flag}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          );
        }

        return (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <h1 className="text-2xl font-bold text-white">Test Runs</h1>
              <div className="flex gap-3">
                <button className="flex items-center gap-2 bg-gray-700 hover:bg-gray-600 text-gray-300 px-4 py-2 rounded transition-colors">
                  <Filter className="w-4 h-4" />
                  Filter
                </button>
                <button className="flex items-center gap-2 bg-gray-700 hover:bg-gray-600 text-gray-300 px-4 py-2 rounded transition-colors">
                  <Download className="w-4 h-4" />
                  Export
                </button>
              </div>
            </div>
            <RunsTable runs={runs} onRunClick={setSelectedRun} />
          </div>
        );

      case 'traits':
        return (
          <div className="space-y-6">
            <h1 className="text-2xl font-bold text-white">Trait Deep Dives</h1>
            <div className="bg-gray-800 rounded-lg p-6">
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                {Object.entries(traitColors).map(([trait, color]) => (
                  <div key={trait} className="bg-gray-700 p-4 rounded-lg">
                    <div className="flex items-center gap-2 mb-3">
                      <div
                        className="w-4 h-4 rounded-full"
                        style={{ backgroundColor: color }}
                      />
                      <h3 className="font-medium text-white text-sm">{trait}</h3>
                    </div>
                    <p className="text-xs text-gray-400 mb-2">
                      Average across all runs: {Math.floor(Math.random() * 40 + 30)}%
                    </p>
                    <div className="text-xs text-gray-500">
                      Placeholder description for {trait.toLowerCase()} trait analysis.
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        );

      case 'settings':
        return (
          <div className="space-y-6">
            <h1 className="text-2xl font-bold text-white">Settings</h1>
            <div className="bg-gray-800 rounded-lg p-6 space-y-6">
              <div>
                <h2 className="text-lg font-semibold text-white mb-4">Default Thresholds</h2>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <SliderWithNumber
                    label="Dominance Threshold (%)"
                    value={thresholds.dominance}
                    onChange={(v) => handleThresholdChange('dominance', v)}
                    min={0}
                    max={100}
                  />
                  <SliderWithNumber
                    label="Per-trait Act Cap"
                    value={thresholds.actCap}
                    onChange={(v) => handleThresholdChange('actCap', v)}
                    min={1}
                    max={50}
                  />
                  <SliderWithNumber
                    label="Decoy Target Ratio (%)"
                    value={thresholds.decoyRatio}
                    onChange={(v) => handleThresholdChange('decoyRatio', v)}
                    min={0}
                    max={100}
                  />
                </div>
              </div>

              <div>
                <h2 className="text-lg font-semibold text-white mb-4">Data Source</h2>
                <div className="space-y-2">
                  <label className="flex items-center gap-2 text-gray-300">
                    <input type="radio" name="dataSource" value="fixtures" defaultChecked />
                    Mock Fixtures
                  </label>
                  <label className="flex items-center gap-2 text-gray-300">
                    <input type="radio" name="dataSource" value="files" />
                    Local Files
                  </label>
                  <label className="flex items-center gap-2 text-gray-300">
                    <input type="radio" name="dataSource" value="api" />
                    API Endpoint
                  </label>
                </div>
              </div>

              <div>
                <h2 className="text-lg font-semibold text-white mb-4">Theme</h2>
                <div className="space-y-2">
                  <label className="flex items-center gap-2 text-gray-300">
                    <input type="radio" name="theme" value="dark" defaultChecked />
                    Dark Theme
                  </label>
                  <label className="flex items-center gap-2 text-gray-300">
```

