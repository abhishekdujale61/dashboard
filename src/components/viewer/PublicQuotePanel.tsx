import { useState, useMemo } from 'react';
import type { PublicQuote, SentimentType } from '../../types';
import { SentimentBadge } from '../ui/SentimentBadge';

interface Props {
  quotes: PublicQuote[];
  totalCount: number;
}

const PROVINCES = ['All', 'AB', 'BC', 'MB', 'NB', 'NL', 'NS', 'NT', 'NU', 'ON', 'PE', 'QC', 'SK', 'YT'];
const SENTIMENTS: Array<'all' | SentimentType> = ['all', 'supportive', 'concerned', 'opposed', 'neutral'];

const depthLabel: Record<string, string> = {
  'evidence-based': 'Evidence-based',
  'reasoned': 'Reasoned',
  'assertion': 'Opinion',
};

export function PublicQuotePanel({ quotes, totalCount }: Props) {
  const [province, setProvince] = useState('All');
  const [sentiment, setSentiment] = useState<'all' | SentimentType>('all');
  const [respondentType, setRespondentType] = useState('All');

  const respondentTypes = useMemo(() => {
    const types = new Set(quotes.map((q) => q.respondentType ?? 'Individual'));
    return ['All', ...Array.from(types)];
  }, [quotes]);

  const filtered = useMemo(() =>
    quotes.filter((q) => {
      if (province !== 'All' && q.province !== province) return false;
      if (sentiment !== 'all' && q.sentiment !== sentiment) return false;
      if (respondentType !== 'All' && (q.respondentType ?? 'Individual') !== respondentType) return false;
      return true;
    }),
    [quotes, province, sentiment, respondentType],
  );

  return (
    <div className="flex flex-col gap-4">
      {/* Header */}
      <div>
        <h3 className="text-sm font-semibold text-slate-200">Public Voices</h3>
        <p className="text-xs text-slate-500 mt-0.5">
          Showing representative voices from {totalCount.toLocaleString()} respondents
        </p>
        <p className="text-[10px] text-slate-600 mt-1 leading-relaxed">
          Quotes selected by salience and depth — representative examples, not individual attributions.
        </p>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-2">
        {/* Sentiment */}
        <div className="flex gap-1 flex-wrap">
          {SENTIMENTS.map((s) => (
            <button
              key={s}
              onClick={() => setSentiment(s)}
              className={`px-2 py-0.5 rounded-full text-[10px] font-medium border transition-colors ${
                sentiment === s
                  ? 'bg-white/[0.10] text-white border-white/20'
                  : 'text-slate-500 border-white/[0.07] hover:text-slate-300'
              }`}
            >
              {s === 'all' ? 'All sentiments' : s.charAt(0).toUpperCase() + s.slice(1)}
            </button>
          ))}
        </div>

        {/* Province */}
        <select
          value={province}
          onChange={(e) => setProvince(e.target.value)}
          className="text-[10px] bg-white/[0.05] border border-white/[0.08] text-slate-400 rounded-md px-2 py-0.5 focus:outline-none"
        >
          {PROVINCES.map((p) => (
            <option key={p} value={p}>{p === 'All' ? 'All provinces' : p}</option>
          ))}
        </select>

        {/* Respondent type */}
        <select
          value={respondentType}
          onChange={(e) => setRespondentType(e.target.value)}
          className="text-[10px] bg-white/[0.05] border border-white/[0.08] text-slate-400 rounded-md px-2 py-0.5 focus:outline-none"
        >
          {respondentTypes.map((t) => (
            <option key={t} value={t}>{t === 'All' ? 'All respondent types' : t}</option>
          ))}
        </select>
      </div>

      {/* Quote count */}
      {filtered.length > 0 && (
        <p className="text-[10px] text-slate-600">
          {filtered.length} of {quotes.length} quote{quotes.length !== 1 ? 's' : ''} shown
        </p>
      )}

      {/* Quotes */}
      {filtered.length === 0 ? (
        <p className="text-sm text-slate-600 italic">No quotes match these filters.</p>
      ) : (
        <div className="space-y-3">
          {filtered.map((quote) => (
            <div
              key={quote.id}
              className="bg-white/[0.03] border border-white/[0.06] rounded-lg p-3 space-y-2"
            >
              <p className="text-sm text-slate-300 leading-relaxed">
                &ldquo;{quote.text}&rdquo;
              </p>
              <div className="flex flex-wrap items-center gap-2 pt-1 border-t border-white/[0.05]">
                <SentimentBadge sentiment={quote.sentiment} />
                <span className="text-[10px] text-slate-600 bg-white/[0.04] px-1.5 py-0.5 rounded">
                  {depthLabel[quote.depth] ?? quote.depth}
                </span>
                {quote.province && (
                  <span className="text-[10px] text-slate-600">{quote.province}</span>
                )}
                <span className="text-[10px] text-slate-600">{quote.respondentType ?? 'Individual'}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
