import { ALIGNMENT_MAP } from '../data';
import { SectionHeader } from '../components/ui/SectionHeader';
import { AlignmentScatterPlot } from '../components/charts/AlignmentScatterPlot';
import { TensionBadge } from '../components/ui/TensionBadge';

export function AlignmentPage() {
  const sorted = [...ALIGNMENT_MAP].sort((a, b) => Math.abs(b.delta) - Math.abs(a.delta));

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-white tracking-tight">Expert vs. Public Alignment</h1>
        <p className="text-slate-400 text-sm mt-1">
          Where the 28 Task Force experts and 11,300+ public respondents agree — and where they diverge
        </p>
      </div>

      {/* Legend */}
      <div className="flex flex-wrap gap-3">
        <div className="flex items-center gap-2 text-sm text-slate-400">
          <span className="w-3 h-3 rounded-full bg-emerald-500 inline-block" />
          Aligned (Δ &lt; 1.0)
        </div>
        <div className="flex items-center gap-2 text-sm text-slate-400">
          <span className="w-3 h-3 rounded-full bg-amber-500 inline-block" />
          In Tension (Δ 1.0–1.5)
        </div>
        <div className="flex items-center gap-2 text-sm text-slate-400">
          <span className="w-3 h-3 rounded-full bg-red-500 inline-block" />
          Diverges (Δ &gt; 1.5)
        </div>
        <div className="flex items-center gap-2 text-sm text-slate-500 ml-auto">
          <span className="text-xs">--- Diagonal = perfect alignment</span>
        </div>
      </div>

      {/* Scatter chart */}
      <div className="bg-[#0f1117] rounded-xl border border-white/[0.07] p-5">
        <SectionHeader
          title="Priority Score Comparison"
          subtitle="Each point is an AI pillar. Points above the diagonal = experts rate it higher than the public."
        />
        <AlignmentScatterPlot />
      </div>

      {/* Table */}
      <div className="bg-[#0f1117] rounded-xl border border-white/[0.07] overflow-hidden">
        <div className="p-5 border-b border-white/[0.07]">
          <SectionHeader
            title="Alignment Detail"
            subtitle="Sorted by largest gap between expert and public priority scores"
          />
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-xs text-slate-600 uppercase tracking-wider border-b border-white/[0.07]">
                <th className="px-5 py-3 text-left">Pillar</th>
                <th className="px-4 py-3 text-center">Public</th>
                <th className="px-4 py-3 text-center">Expert</th>
                <th className="px-4 py-3 text-center">Gap</th>
                <th className="px-4 py-3 text-center">Status</th>
                <th className="px-4 py-3 text-center hidden sm:table-cell">Responses</th>
                <th className="px-5 py-3 text-left hidden lg:table-cell">Key Tension</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/[0.04]">
              {sorted.map((entry) => (
                <tr key={entry.pillarId} className="hover:bg-white/[0.03] transition-colors">
                  <td className="px-5 py-3 font-medium text-slate-200">{entry.pillarLabel}</td>
                  <td className="px-4 py-3 text-center">
                    <span className="font-bold text-indigo-400">{entry.publicScore}</span>
                    <span className="text-slate-500 text-xs">/10</span>
                  </td>
                  <td className="px-4 py-3 text-center">
                    <span className="font-bold text-slate-300">{entry.expertScore}</span>
                    <span className="text-slate-500 text-xs">/10</span>
                  </td>
                  <td className="px-4 py-3 text-center">
                    <span
                      className={`font-bold text-sm ${
                        Math.abs(entry.delta) >= 1.5
                          ? 'text-red-400'
                          : Math.abs(entry.delta) >= 0.5
                          ? 'text-amber-400'
                          : 'text-emerald-400'
                      }`}
                    >
                      {entry.delta > 0 ? '+' : ''}{entry.delta.toFixed(1)}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-center">
                    <TensionBadge status={entry.status} />
                  </td>
                  <td className="px-4 py-3 text-center text-xs text-slate-500 hidden sm:table-cell">
                    {entry.responseCount?.toLocaleString() ?? '—'}
                  </td>
                  <td className="px-5 py-3 text-xs text-slate-500 max-w-xs hidden lg:table-cell">
                    {entry.keyTension ?? (
                      <span className="text-slate-600 italic">No major tension identified</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="bg-white/[0.03] border border-white/[0.06] rounded-xl p-4 text-sm text-slate-500">
        <strong className="text-slate-400">How to read this:</strong> A positive gap means experts prioritized the pillar higher than the public.
        A negative gap means the public wanted more action than experts recommended. "Diverges" (&gt;1.5 gap) indicates
        a significant awareness or values difference that policy should address explicitly.
      </div>
    </div>
  );
}
