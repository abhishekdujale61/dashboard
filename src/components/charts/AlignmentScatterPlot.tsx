import {
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ReferenceLine,
  ResponsiveContainer,
  Cell,
} from 'recharts';
import { ALIGNMENT_MAP } from '../../data';
import type { AlignmentStatus } from '../../types';

const statusColor: Record<AlignmentStatus, string> = {
  aligned: '#10b981',
  tension: '#f59e0b',
  diverges: '#ef4444',
};

interface CustomDotProps {
  cx?: number;
  cy?: number;
  payload?: { pillarLabel: string; status: AlignmentStatus };
}

function CustomDot({ cx = 0, cy = 0, payload }: CustomDotProps) {
  const color = payload ? statusColor[payload.status] : '#6366f1';
  return (
    <g>
      <circle cx={cx} cy={cy} r={8} fill={color} fillOpacity={0.85} />
      <text
        x={cx}
        y={cy - 13}
        textAnchor="middle"
        fontSize={10}
        fill="#64748b"
      >
        {payload?.pillarLabel.split(' & ')[0].split(' ')[0]}
      </text>
    </g>
  );
}

interface TooltipPayload {
  payload: {
    pillarLabel: string;
    publicScore: number;
    expertScore: number;
    delta: number;
    status: AlignmentStatus;
    keyTension: string | null;
  };
}

function CustomTooltip({ active, payload }: { active?: boolean; payload?: TooltipPayload[] }) {
  if (!active || !payload?.length) return null;
  const d = payload[0].payload;
  return (
    <div className="bg-[#0f1117] border border-white/[0.10] rounded-lg p-3 shadow-xl text-sm max-w-xs">
      <p className="font-semibold text-slate-100 mb-1">{d.pillarLabel}</p>
      <p className="text-slate-400">Public: <strong className="text-white">{d.publicScore}/10</strong></p>
      <p className="text-slate-400">Expert: <strong className="text-white">{d.expertScore}/10</strong></p>
      <p className={`font-medium mt-1 ${d.delta > 0 ? 'text-amber-400' : d.delta < 0 ? 'text-indigo-400' : 'text-slate-400'}`}>
        Δ {d.delta > 0 ? '+' : ''}{d.delta.toFixed(1)}
      </p>
      {d.keyTension && (
        <p className="mt-2 text-xs text-amber-300 bg-amber-500/10 border border-amber-500/20 rounded p-1.5 leading-relaxed">
          {d.keyTension}
        </p>
      )}
    </div>
  );
}

export function AlignmentScatterPlot() {
  const data = ALIGNMENT_MAP.map((entry) => ({
    ...entry,
    x: entry.publicScore,
    y: entry.expertScore,
  }));

  return (
    <ResponsiveContainer width="100%" height={380}>
      <ScatterChart margin={{ top: 30, right: 30, bottom: 30, left: 10 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
        <XAxis
          type="number"
          dataKey="x"
          name="Public Score"
          domain={[5, 10]}
          tick={{ fontSize: 11, fill: '#475569' }}
          axisLine={false}
          tickLine={false}
          label={{ value: 'Public Priority Score', position: 'insideBottom', offset: -15, fontSize: 12, fill: '#475569' }}
        />
        <YAxis
          type="number"
          dataKey="y"
          name="Expert Score"
          domain={[5, 10]}
          tick={{ fontSize: 11, fill: '#475569' }}
          axisLine={false}
          tickLine={false}
          label={{ value: 'Expert Priority Score', angle: -90, position: 'insideLeft', offset: 20, fontSize: 12, fill: '#475569' }}
        />
        {/* Perfect alignment diagonal */}
        <ReferenceLine
          segment={[{ x: 5, y: 5 }, { x: 10, y: 10 }]}
          stroke="rgba(255,255,255,0.12)"
          strokeDasharray="6 3"
          label={{ value: 'Perfect alignment', position: 'insideTopRight', fontSize: 10, fill: '#475569' }}
        />
        <Tooltip content={<CustomTooltip />} />
        <Scatter data={data} shape={<CustomDot />}>
          {data.map((entry, index) => (
            <Cell key={index} fill={statusColor[entry.status]} />
          ))}
        </Scatter>
      </ScatterChart>
    </ResponsiveContainer>
  );
}
