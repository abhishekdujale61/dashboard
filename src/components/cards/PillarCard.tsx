import { Link } from 'react-router-dom';
import type { Pillar } from '../../types';
import { TensionBadge } from '../ui/TensionBadge';

interface PillarCardProps {
  pillar: Pillar;
}

export function PillarCard({ pillar }: PillarCardProps) {
  return (
    <Link
      to={`/pillars/${pillar.slug}`}
      className="group block bg-[#0f1117] rounded-xl border border-white/[0.07] hover:border-white/[0.14] hover:bg-[#161720] transition-all overflow-hidden"
    >
      <div className="h-1 w-full" style={{ backgroundColor: pillar.color }} />
      <div className="p-4">
        <div className="flex items-start justify-between gap-2 mb-2">
          <div>
            <p className="text-xs text-slate-600 mb-0.5">Pillar {pillar.pillarNumber}</p>
            <h3 className="text-sm font-semibold text-slate-100 group-hover:text-white transition-colors leading-tight">
              {pillar.label}
            </h3>
          </div>
          <TensionBadge status={pillar.alignmentStatus} />
        </div>
        <p className="text-xs text-slate-500 leading-relaxed line-clamp-2 mb-3">
          {pillar.summary}
        </p>
        <div className="flex items-center justify-between pt-2 border-t border-slate-800">
          <div className="flex items-center gap-3">
            <div className="text-center">
              <p className="text-lg font-bold" style={{ color: pillar.color }}>
                {pillar.publicPriorityScore}
              </p>
              <p className="text-xs text-slate-400">Public</p>
            </div>
            <div className="text-center">
              <p className="text-lg font-bold text-slate-400">
                {pillar.expertPriorityScore}
              </p>
              <p className="text-xs text-slate-400">Expert</p>
            </div>
          </div>
          <span className="text-xs font-medium text-slate-400 bg-white/[0.06] px-2 py-1 rounded-full">
            {pillar.totalRecommendations} recs
          </span>
        </div>
      </div>
    </Link>
  );
}
