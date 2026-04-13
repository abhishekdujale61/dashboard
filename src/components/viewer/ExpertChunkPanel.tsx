import type { ExpertChunk } from '../../types';
import { SentimentBadge } from '../ui/SentimentBadge';

interface Props {
  chunks: ExpertChunk[];
}

const depthConfig: Record<string, { label: string; classes: string }> = {
  'evidence-based': { label: 'Evidence-based', classes: 'bg-indigo-500/10 text-indigo-400 border-indigo-500/20' },
  'reasoned':       { label: 'Reasoned',        classes: 'bg-sky-500/10    text-sky-400    border-sky-500/20'    },
  'assertion':      { label: 'Opinion',          classes: 'bg-slate-500/10  text-slate-400  border-slate-500/20'  },
};

export function ExpertChunkPanel({ chunks }: Props) {
  if (chunks.length === 0) {
    return (
      <div className="flex flex-col gap-4">
        <div>
          <h3 className="text-sm font-semibold text-slate-200">Expert Analysis</h3>
          <p className="text-xs text-slate-500 mt-0.5">Task Force report excerpts</p>
        </div>
        <p className="text-sm text-slate-600 italic">
          No expert report sections mapped to this topic yet. Run the pipeline to populate expert chunks.
        </p>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-4">
      {/* Header */}
      <div>
        <h3 className="text-sm font-semibold text-slate-200">Expert Analysis</h3>
        <p className="text-xs text-slate-500 mt-0.5">
          {chunks.length} section{chunks.length !== 1 ? 's' : ''} from Task Force reports
        </p>
      </div>

      {/* Chunks */}
      <div className="space-y-3">
        {chunks.map((chunk) => {
          const depth = depthConfig[chunk.depth] ?? depthConfig['assertion'];
          return (
            <div
              key={chunk.id}
              className="bg-white/[0.03] border border-white/[0.06] rounded-lg p-4 space-y-2.5"
            >
              {/* Chunk header */}
              {chunk.header && (
                <p className="text-xs font-semibold text-slate-300 uppercase tracking-wide">
                  {chunk.header}
                </p>
              )}

              {/* Body */}
              <p className="text-sm text-slate-300 leading-relaxed">{chunk.body}</p>

              {/* Meta */}
              <div className="flex flex-wrap items-center gap-2 pt-2 border-t border-white/[0.05]">
                <SentimentBadge sentiment={chunk.sentiment} />
                <span className={`text-[10px] font-medium px-2 py-0.5 rounded-full border ${depth.classes}`}>
                  {depth.label}
                </span>
                <div className="ml-auto text-right">
                  <p className="text-xs font-semibold text-slate-300">{chunk.expertName}</p>
                  {chunk.affiliation && (
                    <p className="text-[10px] text-slate-600">{chunk.affiliation}</p>
                  )}
                  {chunk.reportUrl ? (
                    <a
                      href={chunk.reportUrl}
                      target="_blank"
                      rel="noreferrer"
                      className="text-[10px] text-indigo-400 hover:text-indigo-300 italic transition-colors"
                    >
                      {chunk.reportTitle} ↗
                    </a>
                  ) : (
                    <p className="text-[10px] text-slate-600 italic">{chunk.reportTitle}</p>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
