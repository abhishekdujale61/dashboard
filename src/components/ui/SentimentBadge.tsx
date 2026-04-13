import type { SentimentType } from '../../types';

const config: Record<SentimentType, { label: string; classes: string; dot: string }> = {
  supportive: { label: 'Supportive', classes: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20', dot: 'bg-emerald-500' },
  concerned:  { label: 'Concerned',  classes: 'bg-amber-500/10  text-amber-400  border-amber-500/20',  dot: 'bg-amber-500'  },
  opposed:    { label: 'Opposed',    classes: 'bg-red-500/10    text-red-400    border-red-500/20',    dot: 'bg-red-500'    },
  neutral:    { label: 'Neutral',    classes: 'bg-slate-500/10  text-slate-400  border-slate-500/20',  dot: 'bg-slate-500'  },
};

interface Props {
  sentiment: SentimentType;
  size?: 'sm' | 'md';
}

export function SentimentBadge({ sentiment, size = 'sm' }: Props) {
  const { label, classes, dot } = config[sentiment] ?? config.neutral;
  const textSize = size === 'md' ? 'text-xs' : 'text-[10px]';
  return (
    <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full border font-medium ${textSize} ${classes}`}>
      <span className={`w-1.5 h-1.5 rounded-full shrink-0 ${dot}`} />
      {label}
    </span>
  );
}
