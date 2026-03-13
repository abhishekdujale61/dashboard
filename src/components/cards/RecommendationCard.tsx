import type { Recommendation } from '../../types';
import { PillarBadge } from '../ui/PillarBadge';
import { PILLARS } from '../../data';

interface RecommendationCardProps {
  rec: Recommendation;
}

const priorityConfig = {
  high: { label: 'High Priority', classes: 'bg-red-500/10 text-red-400 border border-red-500/20' },
  medium: { label: 'Medium', classes: 'bg-amber-500/10 text-amber-400 border border-amber-500/20' },
  low: { label: 'Low', classes: 'bg-slate-500/10 text-slate-400 border border-slate-500/20' },
};

export function RecommendationCard({ rec }: RecommendationCardProps) {
  const pillar = PILLARS.find((p) => p.id === rec.pillarId);
  const pillarColor = pillar?.color ?? '#6366f1';
  const priority = priorityConfig[rec.priority];

  return (
    <div className="bg-[#0f1117] rounded-xl border border-white/[0.07] hover:border-white/[0.12] p-4 transition-all">
      <div className="flex items-start justify-between gap-2 mb-3">
        <div>
          <p className="text-sm font-semibold text-slate-100">{rec.member}</p>
          <p className="text-xs text-slate-500">{rec.memberRole}</p>
        </div>
        {rec.expertOnly && (
          <span className="shrink-0 inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
            🔬 Expert only
          </span>
        )}
      </div>

      <p className="text-sm text-slate-300 leading-relaxed mb-3">{rec.text}</p>

      <div className="flex flex-wrap items-center gap-2 pt-2 border-t border-white/[0.06]">
        <PillarBadge label={rec.pillarLabel} color={pillarColor} />
        <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${priority.classes}`}>
          {priority.label}
        </span>
        <div className="ml-auto flex items-center gap-1">
          <span className="text-xs text-slate-400">Public support:</span>
          <span className="text-xs font-bold text-slate-200">{rec.publicSupportScore}/10</span>
        </div>
      </div>

      {/* Support bar */}
      <div className="mt-2 h-1.5 bg-white/[0.06] rounded-full overflow-hidden">
        <div
          className="h-full rounded-full transition-all"
          style={{
            width: `${(rec.publicSupportScore / 10) * 100}%`,
            backgroundColor: pillarColor,
            opacity: 0.7,
          }}
        />
      </div>
    </div>
  );
}
