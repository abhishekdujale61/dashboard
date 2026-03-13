import {
  RadarChart,
  Radar,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  Legend,
  Tooltip,
} from 'recharts';
import { ALIGNMENT_MAP } from '../../data';
import { useDashboard } from '../../context/DashboardContext';

const SHORT_LABELS: Record<string, string> = {
  'Talent & Research': 'Talent',
  'Data & Infrastructure': 'Data',
  'Adoption & Commercialization': 'Adoption',
  'Regulation & Governance': 'Regulation',
  'International Collaboration': 'International',
  'Public Trust & Safety': 'Trust',
  'Inclusive AI': 'Inclusion',
  'Sovereignty & Security': 'Sovereignty',
};

export function PillarRadarChart() {
  const { includeExpertReports } = useDashboard();

  const data = ALIGNMENT_MAP.map((entry) => ({
    subject: SHORT_LABELS[entry.pillarLabel] || entry.pillarLabel,
    Public: entry.publicScore,
    Expert: entry.expertScore,
  }));

  return (
    <ResponsiveContainer width="100%" height={340}>
      <RadarChart data={data} margin={{ top: 10, right: 30, bottom: 10, left: 30 }}>
        <PolarGrid stroke="rgba(255,255,255,0.07)" />
        <PolarAngleAxis
          dataKey="subject"
          tick={{ fontSize: 12, fill: '#475569' }}
        />
        <PolarRadiusAxis
          angle={90}
          domain={[0, 10]}
          tick={{ fontSize: 10, fill: '#334155' }}
          tickCount={5}
        />
        <Radar
          name="Public Priority"
          dataKey="Public"
          stroke="#6366f1"
          fill="#6366f1"
          fillOpacity={0.15}
          strokeWidth={2}
        />
        {includeExpertReports && (
          <Radar
            name="Expert Priority"
            dataKey="Expert"
            stroke="#ef4444"
            fill="#ef4444"
            fillOpacity={0.1}
            strokeWidth={2}
            strokeDasharray="4 2"
          />
        )}
        <Tooltip
          formatter={(value) => [`${value}/10`, '']}
          contentStyle={{ background: '#0f1117', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.10)', fontSize: '13px', color: '#f1f5f9' }}
        />
        <Legend
          iconType="line"
          wrapperStyle={{ fontSize: '12px', paddingTop: '12px', color: '#64748b' }}
        />
      </RadarChart>
    </ResponsiveContainer>
  );
}
