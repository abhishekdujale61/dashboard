import { useNavigate, useLocation } from 'react-router-dom';
import { PILLARS } from '../../data';
import { useDashboard } from '../../context/DashboardContext';
import { TensionBadge } from '../ui/TensionBadge';

export function Sidebar() {
  const { activePillarId, setActivePillarId } = useDashboard();
  const navigate = useNavigate();
  const location = useLocation();
  const isRecommendations = location.pathname === '/recommendations';

  function handlePillarClick(pillarId: string) {
    if (activePillarId === pillarId) {
      setActivePillarId(null);
    } else {
      setActivePillarId(pillarId);
      if (!isRecommendations) {
        navigate('/recommendations');
      }
    }
  }

  function handleAllClick() {
    setActivePillarId(null);
  }

  return (
    <aside className="w-56 shrink-0 hidden lg:block">
      <div className="sticky top-20">
        <p className="text-[10px] font-semibold uppercase tracking-widest text-slate-600 mb-3 px-2">
          Filter by Pillar
        </p>
        {!isRecommendations && (
          <p className="text-xs text-slate-600 italic mb-2 px-2">
            Click a pillar to filter recommendations
          </p>
        )}
        <div className="space-y-0.5">
          <button
            onClick={handleAllClick}
            className={`w-full text-left px-3 py-2 rounded-lg text-sm transition-colors ${
              activePillarId === null
                ? 'bg-white/[0.08] text-white font-medium'
                : 'text-slate-500 hover:text-white hover:bg-white/[0.05]'
            }`}
          >
            All Pillars
            <span className="ml-1 text-xs opacity-60">
              ({PILLARS.reduce((a, p) => a + p.totalRecommendations, 0)})
            </span>
          </button>
          {PILLARS.map((pillar) => (
            <button
              key={pillar.id}
              onClick={() => handlePillarClick(pillar.id)}
              className={`w-full text-left px-3 py-2 rounded-lg text-sm transition-colors flex items-center gap-2 ${
                activePillarId === pillar.id
                  ? 'text-white font-medium'
                  : 'text-slate-500 hover:text-white hover:bg-white/[0.05]'
              }`}
              style={
                activePillarId === pillar.id
                  ? { backgroundColor: pillar.color + '33' }
                  : {}
              }
            >
              <span
                className="w-2 h-2 rounded-full shrink-0"
                style={{ backgroundColor: pillar.color }}
              />
              <span className="truncate flex-1">{pillar.label}</span>
              <span className="text-xs opacity-60 shrink-0">
                {pillar.totalRecommendations}
              </span>
            </button>
          ))}
        </div>
        <div className="mt-4 px-2">
          <p className="text-[10px] font-semibold uppercase tracking-widest text-slate-600 mb-2">Alignment Legend</p>
          <div className="space-y-1">
            <TensionBadge status="aligned" />
            <TensionBadge status="tension" />
            <TensionBadge status="diverges" />
          </div>
        </div>
      </div>
    </aside>
  );
}
