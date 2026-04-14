import { Link } from 'react-router-dom';
import type { Topic } from '../../types';
import { SentimentBadge } from '../ui/SentimentBadge';

interface Props {
  topic: Topic;
  pillarColor: string;
}

export function TopicCard({ topic, pillarColor }: Props) {
  const total = topic.publicChunkCount + topic.expertChunkCount;
  const publicPct = total > 0 ? (topic.publicChunkCount / total) * 100 : 50;

  return (
    <Link
      to={`/pillars/${topic.pillarId}/topics/${topic.id}`}
      className="group block bg-[#0f1117] rounded-xl border border-white/[0.07] hover:border-white/[0.14] p-4 transition-all hover:-translate-y-0.5"
    >
      {/* Header */}
      <div className="mb-3">
        <h3 className="text-sm font-semibold text-slate-100 leading-snug group-hover:text-white transition-colors">
          {topic.label}
        </h3>
      </div>

      {/* Response count comparison */}
      <div className="mb-3 space-y-1.5">
        <div className="flex items-center gap-2">
          <span className="text-[10px] text-slate-500 w-14 shrink-0">Public</span>
          <div className="flex-1 bg-white/[0.06] rounded-full h-1.5 overflow-hidden">
            <div
              className="h-full rounded-full transition-all"
              style={{ width: `${publicPct}%`, backgroundColor: pillarColor, opacity: 0.7 }}
            />
          </div>
          <span className="text-[10px] text-slate-400 w-10 text-right">{topic.publicChunkCount.toLocaleString()}</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-[10px] text-slate-500 w-14 shrink-0">Expert</span>
          <div className="flex-1 bg-white/[0.06] rounded-full h-1.5 overflow-hidden">
            <div
              className="h-full rounded-full transition-all"
              style={{ width: `${100 - publicPct}%`, backgroundColor: pillarColor, opacity: 0.35 }}
            />
          </div>
          <span className="text-[10px] text-slate-500 w-10 text-right">{topic.expertChunkCount.toLocaleString()}</span>
        </div>
      </div>

      {/* Sentiment + total */}
      <div className="flex items-center justify-between pt-2.5 border-t border-white/[0.06]">
        <SentimentBadge sentiment={topic.dominantPublicSentiment} />
        <span className="text-[10px] text-slate-600">
          {total.toLocaleString()} responses →
        </span>
      </div>
    </Link>
  );
}
