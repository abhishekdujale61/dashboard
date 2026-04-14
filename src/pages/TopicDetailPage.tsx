import { useParams, Link } from 'react-router-dom';
import { PILLARS, TOPICS, QUOTES, EXPERT_CHUNKS } from '../data';
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
        <div className="mb-4">
          <div className="flex items-center gap-2 mb-2">
            <span
              className="w-2 h-2 rounded-full"
              style={{ backgroundColor: pillar.color }}
            />
            <span className="text-xs text-slate-500">{pillar.label}</span>
          </div>
          <h1 className="text-xl font-bold text-white leading-tight">{topic.label}</h1>
        </div>

        {/* Response count comparison */}
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-4 mt-2">
          <div className="bg-white/[0.04] rounded-lg p-3 text-center">
            <p className="text-2xl font-bold text-white">{topic.publicChunkCount.toLocaleString()}</p>
            <p className="text-[10px] text-slate-500 mt-0.5">Public responses</p>
          </div>
          <div className="bg-white/[0.04] rounded-lg p-3 text-center">
            <p className="text-2xl font-bold text-slate-300">{topic.expertChunkCount.toLocaleString()}</p>
            <p className="text-[10px] text-slate-500 mt-0.5">Expert references</p>
          </div>
          <div className="bg-white/[0.04] rounded-lg p-3 text-center">
            <p className="text-2xl font-bold text-white">
              {(topic.publicChunkCount + topic.expertChunkCount).toLocaleString()}
            </p>
            <p className="text-[10px] text-slate-500 mt-0.5">Total responses</p>
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
