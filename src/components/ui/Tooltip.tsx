import { useState, useRef, useEffect } from 'react';

interface Props {
  content: string;
  children: React.ReactNode;
}

export function Tooltip({ content, children }: Props) {
  const [visible, setVisible] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function handleClick(e: MouseEvent) {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        setVisible(false);
      }
    }
    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, []);

  return (
    <div
      ref={ref}
      className="relative inline-flex items-center gap-1 cursor-help group"
      onMouseEnter={() => setVisible(true)}
      onMouseLeave={() => setVisible(false)}
    >
      {children}
      <span className="text-[9px] text-slate-600 border border-slate-700 rounded-full w-3.5 h-3.5 flex items-center justify-center leading-none shrink-0 group-hover:text-slate-400 group-hover:border-slate-500 transition-colors">
        ?
      </span>
      {visible && (
        <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 z-50 w-64 bg-[#1e2330] border border-white/[0.12] rounded-lg p-3 shadow-xl pointer-events-none">
          <p className="text-[11px] text-slate-300 leading-relaxed">{content}</p>
          <div className="absolute top-full left-1/2 -translate-x-1/2 border-4 border-transparent border-t-[#1e2330]" />
        </div>
      )}
    </div>
  );
}
