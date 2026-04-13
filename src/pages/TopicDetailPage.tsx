import { useParams, Link } from 'react-router-dom';
import { PILLARS, TOPICS, QUOTES, EXPERT_CHUNKS } from '../data';
import { TensionBadge } from '../components/ui/TensionBadge';
import { SentimentBadge } from '../components/ui/SentimentBadge';
import { PublicQuotePanel } from '../components/viewer/PublicQuotePanel';
import { ExpertChunkPanel } from '../components/viewer/ExpertChunkPanel';

export function TopicDetailPage() {
  const { pillarId, topicId } = useParams<{ pillarId: string; topicId: string }>();

  const pillar = PILLARS.find((p) => p.slug === pillarId || p.id === pillarId);
  const topic  = TOPICS.find((t) => t.id === topicId && t.pillarId === (pillar?.id ?? ''));

  if (!pillar || !topic) {
    return (
      <div className="text-center py-16">
        <p className="text-slate-500 mb-2">Topic not found.</p>
        <Link to={`/pillars/${pillarId}`} className="text-indigo-400 text-sm hover:underline">
          ← Back to {pillar?.label ?? 'pillar'}
        </Link>
      </div>
    );
  }

  const quotes        = QUOTES[topic.id]        ?? [];
  const expertChunks  = EXPERT_CHUNKS[topic.id] ?? [];

  return (
    <div className="space-y-6">
      {/* Breadcrumb */}
      <nav className="flex items-center gap-2 text-sm text-slate-500">
        <Link to="/" className="hover:text-slate-300 transition-colors">Overview</Link>
        <span>›</span>
        <Link to={`/pillars/${pillar.slug}`} className="hover:text-slate-300 transition-colors">
          {pillar.label}
        </Link>
        <span>›</span>
        <span className="text-slate-300">{topic.label}</span>
      </nav>

      {/* Topic hero */}
      <div className="bg-[#0f1117] rounded-2xl border border-white/[0.07] p-6">
        <div className="flex items-start justify-between gap-4 mb-4">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <span
                className="w-2 h-2 rounded-full"
                style={{ backgroundColor: pillar.color }}
              />
              <span className="text-xs text-slate-500">{pillar.label}</span>
            </div>
            <h1 className="text-xl font-bold text-white leading-tight">{topic.label}</h1>
          </div>
          <TensionBadge status={topic.alignmentStatus} size="md" />
        </div>

        {/* Score comparison */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-2">
          <div className="bg-white/[0.04] rounded-lg p-3 text-center">
            <p className="text-2xl font-bold text-white">{topic.publicScore}</p>
            <p className="text-[10px] text-slate-500 mt-0.5">Public score /10</p>
          </div>
          <div className="bg-white/[0.04] rounded-lg p-3 text-center">
            <p className="text-2xl font-bold text-slate-300">{topic.expertScore}</p>
            <p className="text-[10px] text-slate-500 mt-0.5">Expert score /10</p>
          </div>
          <div className="bg-white/[0.04] rounded-lg p-3 text-center">
            <p className={`text-2xl font-bold ${
              Math.abs(topic.delta) >= 1.5 ? 'text-red-400' : Math.abs(topic.delta) >= 0.5 ? 'text-amber-400' : 'text-emerald-400'
            }`}>
              {topic.delta > 0 ? '+' : ''}{topic.delta.toFixed(1)}
            </p>
            <p className="text-[10px] text-slate-500 mt-0.5">Gap (expert − public)</p>
          </div>
          <div className="bg-white/[0.04] rounded-lg p-3 text-center">
            <p className="text-2xl font-bold text-white">
              {(topic.publicChunkCount + topic.expertChunkCount).toLocaleString()}
            </p>
            <p className="text-[10px] text-slate-500 mt-0.5">Total voices</p>
          </div>
        </div>

        {/* Sentiment row */}
        <div className="flex flex-wrap items-center gap-3 mt-4 pt-4 border-t border-white/[0.06]">
          <div className="flex items-center gap-2">
            <span className="text-xs text-slate-500">Public sentiment:</span>
            <SentimentBadge sentiment={topic.dominantPublicSentiment} size="md" />
          </div>
          <div className="flex items-center gap-2">
            <span className="text-xs text-slate-500">Expert sentiment:</span>
            <SentimentBadge sentiment={topic.dominantExpertSentiment} size="md" />
          </div>
          {topic.dominantPublicSentiment !== topic.dominantExpertSentiment && (
            <span className="text-xs text-amber-400 bg-amber-500/5 border border-amber-500/15 px-2 py-0.5 rounded">
              Sentiment divergence
            </span>
          )}
        </div>
      </div>

      {/* Comment viewer — two panels */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Public panel */}
        <div className="bg-[#0f1117] rounded-xl border border-white/[0.07] p-5">
          <PublicQuotePanel quotes={quotes} totalCount={topic.publicChunkCount} />
        </div>

        {/* Expert panel */}
        <div className="bg-[#0f1117] rounded-xl border border-white/[0.07] p-5">
          <ExpertChunkPanel chunks={expertChunks} />
        </div>
      </div>

      {/* Back link */}
      <Link
        to={`/pillars/${pillar.slug}`}
        className="inline-flex items-center gap-1 text-sm text-slate-500 hover:text-slate-300 transition-colors"
      >
        ← Back to {pillar.label}
      </Link>
    </div>
  );
}
