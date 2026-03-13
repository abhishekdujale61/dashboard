import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { DEMOGRAPHICS } from '../../data';

export function SectorPieChart() {
  const data = DEMOGRAPHICS.sectors;

  return (
    <ResponsiveContainer width="100%" height={280}>
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="45%"
          outerRadius={90}
          dataKey="value"
          nameKey="label"
          label={({ value }) => `${value}%`}
          labelLine={{ stroke: 'rgba(255,255,255,0.2)', strokeWidth: 1 }}
        >
          {data.map((entry, index) => (
            <Cell key={index} fill={entry.color} />
          ))}
        </Pie>
        <Tooltip
          formatter={(value) => [`${value}%`, 'Share']}
          contentStyle={{ background: '#0f1117', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.10)', fontSize: '13px', color: '#f1f5f9' }}
        />
        <Legend
          iconType="circle"
          iconSize={8}
          wrapperStyle={{ fontSize: '12px', color: '#64748b' }}
        />
      </PieChart>
    </ResponsiveContainer>
  );
}
