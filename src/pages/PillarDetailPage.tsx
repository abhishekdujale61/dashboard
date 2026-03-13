import { useParams, Link } from 'react-router-dom';
import { PILLARS, RECOMMENDATIONS, EXPERT_REPORTS, ALIGNMENT_MAP } from '../data';
import { TensionBadge } from '../components/ui/TensionBadge';
import { RecommendationCard } from '../components/cards/RecommendationCard';
import { useDashboard } from '../context/DashboardContext';

export function PillarDetailPage() {
  const { pillarId } = useParams<{ pillarId: string }>();
  const { includeExpertReports } = useDashboard();

  const pillar = PILLARS.find((p) => p.slug === pillarId);
  if (!pillar) {
    return (
      <div className="text-center py-16">
        <p className="text-slate-500">Pillar not found.</p>
        <Link to="/" className="text-indigo-400 text-sm hover:underline mt-2 block">← Back to overview</Link>
      </div>
    );
  }

  const recs = RECOMMENDATIONS.filter((r) => {
    if (!includeExpertReports && r.expertOnly) return false;
    return r.pillarId === pillar.id;
  });

  const alignment = ALIGNMENT_MAP.find((a) => a.pillarId === pillar.id);
  const report = EXPERT_REPORTS.find((r) => r.pillarId === pillar.id);

  const urgencyConfig = {
    critical: 'bg-red-500/10 text-red-400 border-red-500/20',
    high: 'bg-amber-500/10 text-amber-400 border-amber-500/20',
    medium: 'bg-slate-500/10 text-slate-400 border-slate-500/20',
  };

  return (
    <div className="space-y-6">
      {/* Back */}
      <Link to="/" className="inline-flex items-center gap-1 text-sm text-slate-500 hover:text-slate-300 transition-colors">
        ← All Pillars
      </Link>

      {/* Hero */}
      <div
        className="rounded-2xl p-6 text-white"
        style={{ background: `linear-gradient(135deg, ${pillar.color}ee, ${pillar.color}99)` }}
      >
        <div className="flex items-start justify-between gap-4">
          <div>
            <p className="text-sm font-medium opacity-75 mb-1">Pillar {pillar.pillarNumber} of 8</p>
            <h1 className="text-2xl font-bold">{pillar.label}</h1>
            <p className="mt-2 text-sm opacity-85 max-w-xl leading-relaxed">{pillar.summary}</p>
          </div>
          <TensionBadge status={pillar.alignmentStatus} size="md" />
        </div>

        {/* Scores */}
        {alignment && (
          <div className="mt-5 flex items-center gap-6">
            <div className="text-center">
              <p className="text-3xl font-bold">{alignment.publicScore}</p>
              <p className="text-xs opacity-75">Public Priority /10</p>
            </div>
            {includeExpertReports && (
              <>
                <div className="text-2xl opacity-50">vs</div>
                <div className="text-center">
                  <p className="text-3xl font-bold">{alignment.expertScore}</p>
                  <p className="text-xs opacity-75">Expert Priority /10</p>
                </div>
                <div className="text-center">
                  <p className={`text-2xl font-bold ${Math.abs(alignment.delta) >= 1.5 ? 'text-red-200' : 'text-white'}`}>
                    {alignment.delta > 0 ? '+' : ''}{alignment.delta.toFixed(1)}
                  </p>
                  <p className="text-xs opacity-75">Gap</p>
                </div>
              </>
            )}
          </div>
        )}
        {alignment?.keyTension && (
          <p className="mt-3 text-sm bg-white/15 rounded-lg px-3 py-2">
            ⚡ {alignment.keyTension}
          </p>
        )}
      </div>

      {/* Expert Report */}
      {includeExpertReports && report && (
        <div className="bg-[#0f1117] rounded-xl border border-white/[0.07] p-5 space-y-5">
          {/* Header */}
          <div className="flex items-start justify-between gap-4">
            <div>
              <p className="text-xs text-slate-500 mb-0.5">Task Force Report · {report.publishedDate}</p>
              <h2 className="text-base font-semibold text-slate-100">{report.reportTitle}</h2>
              <div className="flex flex-wrap gap-1.5 mt-2">
                {report.authors.map((author) => (
                  <span key={author} className="text-xs bg-white/[0.06] text-slate-300 px-2 py-0.5 rounded-full border border-white/[0.08]">
                    {author}
                  </span>
                ))}
              </div>
            </div>
            <span className={`shrink-0 text-xs font-medium px-2.5 py-1 rounded-full border ${urgencyConfig[report.urgencyLevel]}`}>
              {report.urgencyLevel.charAt(0).toUpperCase() + report.urgencyLevel.slice(1)} urgency
            </span>
          </div>

          {/* Key Findings */}
          <div>
            <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Key Findings</p>
            <div className="space-y-2">
              {report.keyFindings.map((finding, i) => (
                <div key={i} className="flex gap-2">
                  <span className="text-indigo-400 mt-0.5 shrink-0 text-xs font-bold">{i + 1}.</span>
                  <p className="text-sm text-slate-300 leading-relaxed">{finding}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Recommendations */}
          {report.recommendations?.length > 0 && (
            <div>
              <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Expert Recommendations</p>
              <div className="space-y-2">
                {report.recommendations.map((rec, i) => (
                  <div key={i} className="flex gap-2 bg-white/[0.03] rounded-lg px-3 py-2">
                    <span className="text-emerald-400 mt-0.5 shrink-0 text-xs font-bold">{i + 1}.</span>
                    <p className="text-sm text-slate-300 leading-relaxed">{rec}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Policy Gap */}
          <div className="bg-red-500/5 border border-red-500/20 rounded-lg p-3">
            <p className="text-xs font-semibold text-red-400 mb-1">Policy Gap Identified</p>
            <p className="text-sm text-red-300 leading-relaxed">{report.policyGap}</p>
          </div>
        </div>
      )}

      {/* Recommendations */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-slate-100">
            Recommendations ({recs.length})
          </h2>
          {!includeExpertReports && (
            <p className="text-xs text-slate-500">
              {RECOMMENDATIONS.filter(r => r.pillarId === pillar.id && r.expertOnly).length} expert-only hidden
            </p>
          )}
        </div>
        {recs.length > 0 ? (
          <div className="grid grid-cols-1 xl:grid-cols-2 gap-4">
            {recs.map((rec) => (
              <RecommendationCard key={rec.id} rec={rec} />
            ))}
          </div>
        ) : (
          <p className="text-slate-500 text-sm">No recommendations visible with current filters.</p>
        )}
      </div>
    </div>
  );
}
