interface SectionHeaderProps {
  title: string;
  subtitle?: string;
  badge?: string;
}

export function SectionHeader({ title, subtitle, badge }: SectionHeaderProps) {
  return (
    <div className="mb-6">
      {badge && (
        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 mb-2">
          {badge}
        </span>
      )}
      <h2 className="text-lg font-semibold text-slate-100 tracking-tight">{title}</h2>
      {subtitle && <p className="mt-1 text-sm text-slate-500">{subtitle}</p>}
    </div>
  );
}
