import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from 'recharts';
import { DEMOGRAPHICS } from '../../data';

export function RespondentDonut() {
  const data = DEMOGRAPHICS.respondentTypes;
  const COLORS = ['#6366f1', '#cbd5e1'];

  return (
    <div className="relative">
      <ResponsiveContainer width="100%" height={200}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={55}
            outerRadius={80}
            dataKey="value"
            startAngle={90}
            endAngle={-270}
          >
            {data.map((_, index) => (
              <Cell key={index} fill={COLORS[index]} />
            ))}
          </Pie>
          <Tooltip
            formatter={(value, _name, props) => [
              `${value}% (${(props.payload as { count?: number }).count?.toLocaleString()})`,
              (props.payload as { label?: string }).label ?? '',
            ]}
            contentStyle={{ background: '#0f1117', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.10)', fontSize: '13px', color: '#f1f5f9' }}
          />
        </PieChart>
      </ResponsiveContainer>
      {/* Center label */}
      <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
        <span className="text-2xl font-bold text-white">
          {(DEMOGRAPHICS.totalRespondents / 1000).toFixed(1)}K
        </span>
        <span className="text-xs text-slate-500">respondents</span>
      </div>
      {/* Legend */}
      <div className="flex justify-center gap-4 mt-1">
        {data.map((item, i) => (
          <div key={i} className="flex items-center gap-1.5">
            <span
              className="w-2.5 h-2.5 rounded-full"
              style={{ backgroundColor: COLORS[i] }}
            />
            <span className="text-xs text-slate-400">
              {item.label} <strong className="text-slate-200">{item.value}%</strong>
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
