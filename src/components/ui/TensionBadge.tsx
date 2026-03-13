import type { AlignmentStatus } from '../../types';

interface TensionBadgeProps {
  status: AlignmentStatus;
  size?: 'sm' | 'md';
}

const config: Record<AlignmentStatus, { label: string; classes: string }> = {
  aligned: { label: 'Aligned', classes: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' },
  tension: { label: 'In Tension', classes: 'bg-amber-500/10 text-amber-400 border-amber-500/20' },
  diverges: { label: 'Diverges', classes: 'bg-red-500/10 text-red-400 border-red-500/20' },
};

export function TensionBadge({ status, size = 'sm' }: TensionBadgeProps) {
  const { label, classes } = config[status];
  return (
    <span
      className={`inline-flex items-center rounded-full border font-medium ${classes} ${
        size === 'sm' ? 'px-2 py-0.5 text-xs' : 'px-3 py-1 text-sm'
      }`}
    >
      <span className="mr-1">{status === 'aligned' ? '✓' : status === 'tension' ? '⚡' : '↗'}</span>
      {label}
    </span>
  );
}
