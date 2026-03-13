import { useNavigate } from 'react-router-dom';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Cell,
  ResponsiveContainer,
} from 'recharts';
import { PILLARS } from '../../data';

export function PillarBarChart() {
  const navigate = useNavigate();

  const data = PILLARS.map((p) => ({
    name: p.label.split(' & ')[0],
    recs: p.totalRecommendations,
    color: p.color,
    slug: p.slug,
  }));

  return (
    <ResponsiveContainer width="100%" height={220}>
      <BarChart data={data} margin={{ top: 5, right: 10, left: -10, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
        <XAxis
          dataKey="name"
          tick={{ fontSize: 11, fill: '#475569' }}
          axisLine={false}
          tickLine={false}
        />
        <YAxis
          tick={{ fontSize: 11, fill: '#475569' }}
          axisLine={false}
          tickLine={false}
          domain={[0, 20]}
        />
        <Tooltip
          formatter={(value) => [`${value} recommendations`, '']}
          contentStyle={{ background: '#0f1117', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.10)', fontSize: '13px', color: '#f1f5f9' }}
          cursor={{ fill: 'rgba(255,255,255,0.03)' }}
        />
        <Bar
          dataKey="recs"
          radius={[4, 4, 0, 0]}
          cursor="pointer"
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
          onClick={(d: any) => navigate(`/pillars/${d.slug}`)}
        >
          {data.map((entry) => (
            <Cell key={entry.slug} fill={entry.color} fillOpacity={0.85} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}
