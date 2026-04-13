import { useParams, Link } from 'react-router-dom';
import { PILLARS, TOPICS, ALIGNMENT_MAP } from '../data';
import { TensionBadge } from '../components/ui/TensionBadge';
import { TopicCard } from '../components/cards/TopicCard';

export function PillarDetailPage() {
  const { pillarId } = useParams<{ pillarId: string }>();

  // Support both slug and id (fixes slug 404)
  const pillar = PILLARS.find((p) => p.slug === pillarId || p.id === pillarId);

  if (!pillar) {
    return (
      <div className="text-center py-16">
        <p className="text-slate-500 mb-2">Pillar &ldquo;{pillarId}&rdquo; not found.</p>
        <Link to="/" className="text-indigo-400 text-sm hover:underline">← Back to overview</Link>
      </div>
    );
  }

  const topics = TOPICS.filter((t) => t.pillarId === pillar.id);
  const alignment = ALIGNMENT_MAP.find((a) => a.pillarId === pillar.id);

  return (
    <div className="space-y-6">
      {/* Back */}
      <Link
        to="/"
        className="inline-flex items-center gap-1 text-sm text-slate-500 hover:text-slate-300 transition-colors"
      >
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
          <div className="mt-5 flex items-center gap-6 flex-wrap">
            <div className="text-center">
              <p className="text-3xl font-bold">{alignment.publicScore}</p>
              <p className="text-xs opacity-75">Public Priority /10</p>
            </div>
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
          </div>
        )}

        {alignment?.keyTension && (
          <p className="mt-3 text-sm bg-white/15 rounded-lg px-3 py-2">
            ⚡ {alignment.keyTension}
          </p>
        )}
      </div>

      {/* Topics */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-lg font-semibold text-slate-100">Topics within this pillar</h2>
            <p className="text-xs text-slate-500 mt-0.5">
              Click any topic to explore public voices and expert analysis side by side
            </p>
          </div>
          <span className="text-xs text-slate-600 border border-white/[0.07] rounded px-2 py-1">
            {topics.length} topic{topics.length !== 1 ? 's' : ''}
          </span>
        </div>

        {topics.length === 0 ? (
          <div className="bg-[#0f1117] border border-white/[0.07] rounded-xl p-8 text-center">
            <p className="text-slate-500 text-sm">
              Topics not yet generated. Run the pipeline to populate topics.
            </p>
            <code className="text-xs text-slate-600 mt-2 block">bash pipeline/run_pipeline.sh</code>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4">
            {topics.map((topic) => (
              <TopicCard key={topic.id} topic={topic} pillarColor={pillar.color} />
            ))}
          </div>
        )}
      </div>

      {/* Alignment notes */}
      {alignment?.notes && (
        <div className="bg-white/[0.03] border border-white/[0.06] rounded-xl p-4 text-sm text-slate-500">
          <strong className="text-slate-400">Data note: </strong>{alignment.notes}
        </div>
      )}
    </div>
  );
}
