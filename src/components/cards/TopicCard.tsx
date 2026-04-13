import { Link } from 'react-router-dom';
import type { Topic } from '../../types';
import { TensionBadge } from '../ui/TensionBadge';
import { SentimentBadge } from '../ui/SentimentBadge';

interface Props {
  topic: Topic;
  pillarColor: string;
}

export function TopicCard({ topic, pillarColor }: Props) {
  const totalChunks = topic.publicChunkCount + topic.expertChunkCount;

  return (
    <Link
      to={`/pillars/${topic.pillarId}/topics/${topic.id}`}
      className="group block bg-[#0f1117] rounded-xl border border-white/[0.07] hover:border-white/[0.14] p-4 transition-all hover:-translate-y-0.5"
    >
      {/* Header */}
      <div className="flex items-start justify-between gap-3 mb-3">
        <h3 className="text-sm font-semibold text-slate-100 leading-snug group-hover:text-white transition-colors">
          {topic.label}
        </h3>
        <TensionBadge status={topic.alignmentStatus} />
      </div>

      {/* Score comparison bar */}
      <div className="mb-3 space-y-1.5">
        <div className="flex items-center gap-2">
          <span className="text-[10px] text-slate-500 w-14 shrink-0">Public</span>
          <div className="flex-1 bg-white/[0.06] rounded-full h-1.5 overflow-hidden">
            <div
              className="h-full rounded-full transition-all"
              style={{ width: `${(topic.publicScore / 10) * 100}%`, backgroundColor: pillarColor, opacity: 0.7 }}
            />
          </div>
          <span className="text-xs font-bold text-slate-300 w-8 text-right">{topic.publicScore}</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-[10px] text-slate-500 w-14 shrink-0">Expert</span>
          <div className="flex-1 bg-white/[0.06] rounded-full h-1.5 overflow-hidden">
            <div
              className="h-full rounded-full transition-all"
              style={{ width: `${(topic.expertScore / 10) * 100}%`, backgroundColor: pillarColor, opacity: 0.45 }}
            />
          </div>
          <span className="text-xs font-bold text-slate-400 w-8 text-right">{topic.expertScore}</span>
        </div>
      </div>

      {/* Sentiment + response count */}
      <div className="flex items-center justify-between pt-2.5 border-t border-white/[0.06]">
        <div className="flex items-center gap-1.5">
          <SentimentBadge sentiment={topic.dominantPublicSentiment} />
          {topic.dominantExpertSentiment !== topic.dominantPublicSentiment && (
            <>
              <span className="text-[10px] text-slate-600">vs</span>
              <SentimentBadge sentiment={topic.dominantExpertSentiment} />
            </>
          )}
        </div>
        <span className="text-[10px] text-slate-600">
          {totalChunks.toLocaleString()} voices →
        </span>
      </div>
    </Link>
  );
}
