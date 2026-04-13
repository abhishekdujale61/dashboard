import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from 'recharts';
import { DEMOGRAPHICS } from '../../data';

export function GeographyBarChart() {
  const data = DEMOGRAPHICS.geography.slice(0, 8);

  return (
    <ResponsiveContainer width="100%" height={280}>
      <BarChart
        data={data}
        layout="vertical"
        margin={{ top: 5, right: 30, left: 10, bottom: 5 }}
      >
        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" horizontal={false} />
        <XAxis
          type="number"
          tick={{ fontSize: 11, fill: '#475569' }}
          axisLine={false}
          tickLine={false}
          domain={[0, 45]}
          tickFormatter={(v) => `${v}%`}
        />
        <YAxis
          type="category"
          dataKey="province"
          tick={{ fontSize: 11, fill: '#475569' }}
          axisLine={false}
          tickLine={false}
          width={28}
          tickFormatter={(v: string) => v.length > 3 ? v.slice(0, 2) : v}
        />
        <Tooltip
          formatter={(value, _name, props) => [
            `${value}% (${(props.payload as { count?: number }).count?.toLocaleString()} respondents)`,
            (props.payload as { fullName?: string }).fullName ?? '',
          ]}
          contentStyle={{ background: '#0f1117', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.10)', fontSize: '13px', color: '#f1f5f9' }}
          cursor={{ fill: 'rgba(255,255,255,0.03)' }}
        />
        <Bar dataKey="value" radius={[0, 4, 4, 0]}>
          {data.map((_entry, index) => (
            <Cell
              key={index}
              fill={index < 2 ? '#6366f1' : index < 4 ? '#0ea5e9' : '#94a3b8'}
              fillOpacity={0.85}
            />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}
