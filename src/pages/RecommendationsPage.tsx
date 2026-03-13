import { useState } from 'react';
import { useDashboard } from '../context/DashboardContext';
import { PILLARS, RECOMMENDATIONS } from '../data';
import { RecommendationCard } from '../components/cards/RecommendationCard';
import { PillarBadge } from '../components/ui/PillarBadge';

export function RecommendationsPage() {
  const { filteredRecommendations, includeExpertReports, activePillarId, setActivePillarId } = useDashboard();
  const [priorityFilter, setPriorityFilter] = useState<string>('all');
  const [search, setSearch] = useState('');

  const displayed = filteredRecommendations.filter((rec) => {
    if (priorityFilter !== 'all' && rec.priority !== priorityFilter) return false;
    if (search && !rec.text.toLowerCase().includes(search.toLowerCase()) && !rec.member.toLowerCase().includes(search.toLowerCase())) {
      return false;
    }
    return true;
  });

  const totalVisible = filteredRecommendations.length;
  const totalWithoutPillar = RECOMMENDATIONS.filter(r => includeExpertReports || !r.expertOnly).length;
  const hiddenCount = RECOMMENDATIONS.length - totalWithoutPillar;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white tracking-tight">Recommendations</h1>
        <p className="text-slate-400 text-sm mt-1">
          Task Force recommendations mapped to all 8 pillars
        </p>
      </div>

      {/* Filters */}
      <div className="bg-[#0f1117] rounded-xl border border-white/[0.07] p-4 space-y-3">
        <div className="flex flex-wrap gap-2 items-center">
          {/* Pillar chips */}
          <button
            onClick={() => setActivePillarId(null)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              activePillarId === null
                ? 'bg-white text-slate-900 border-transparent'
                : 'border-white/[0.10] text-slate-400 hover:border-white/20 hover:text-white'
            }`}
          >
            All Pillars
          </button>
          {PILLARS.map((p) => (
            <button
              key={p.id}
              onClick={() => setActivePillarId(p.id === activePillarId ? null : p.id)}
              className={`transition-colors ${
                activePillarId === p.id ? 'opacity-100' : 'opacity-60 hover:opacity-100'
              }`}
            >
              <PillarBadge label={p.label} color={p.color} />
            </button>
          ))}
        </div>
        <div className="flex gap-3 flex-wrap">
          {/* Priority filter */}
          <div className="flex items-center gap-1 rounded-lg border border-white/[0.07] overflow-hidden">
            {(['all', 'high', 'medium'] as const).map((p) => (
              <button
                key={p}
                onClick={() => setPriorityFilter(p)}
                className={`px-3 py-1.5 text-xs font-medium transition-colors ${
                  priorityFilter === p
                    ? 'bg-white/[0.1] text-white'
                    : 'text-slate-500 hover:bg-white/[0.05] hover:text-slate-300'
                }`}
              >
                {p === 'all' ? 'All Priority' : p.charAt(0).toUpperCase() + p.slice(1)}
              </button>
            ))}
          </div>
          {/* Search */}
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search recommendations or experts..."
            className="flex-1 min-w-48 px-3 py-1.5 text-sm bg-white/[0.05] border border-white/[0.10] rounded-lg text-white placeholder-slate-600 focus:outline-none focus:border-indigo-500/50 focus:ring-0"
          />
        </div>
      </div>

      {/* Count + toggle status */}
      <div className="flex items-center justify-between text-sm">
        <p className="text-slate-500">
          Showing <strong className="text-slate-200">{displayed.length}</strong> of <strong className="text-slate-200">{totalVisible}</strong>
          {activePillarId && <span className="text-indigo-400 ml-1">(pillar filtered)</span>}
          {!includeExpertReports && hiddenCount > 0 && (
            <span className="text-slate-500 ml-1">· {hiddenCount} expert-only hidden</span>
          )}
        </p>
        {(activePillarId || priorityFilter !== 'all' || search) && (
          <button
            onClick={() => { setActivePillarId(null); setPriorityFilter('all'); setSearch(''); }}
            className="text-xs text-indigo-400 hover:underline"
          >
            Clear all filters
          </button>
        )}
      </div>

      {/* Cards grid */}
      {displayed.length > 0 ? (
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-4">
          {displayed.map((rec) => (
            <RecommendationCard key={rec.id} rec={rec} />
          ))}
        </div>
      ) : (
        <div className="text-center py-16 text-slate-600">
          <p className="text-lg">No recommendations match your filters.</p>
          <button
            onClick={() => { setActivePillarId(null); setPriorityFilter('all'); setSearch(''); }}
            className="mt-3 text-sm text-indigo-400 hover:underline"
          >
            Clear all filters
          </button>
        </div>
      )}
    </div>
  );
}
