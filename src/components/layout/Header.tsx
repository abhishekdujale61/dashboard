import { NavLink } from 'react-router-dom';
import { Toggle } from '../ui/Toggle';
import { useDashboard } from '../../context/DashboardContext';

const navLinks = [
  { to: '/', label: 'Overview' },
  { to: '/demographics', label: 'Demographics' },
  { to: '/alignment', label: 'Expert vs Public' },
  { to: '/recommendations', label: 'Recommendations' },
];

export function Header() {
  const { includeExpertReports, setIncludeExpertReports } = useDashboard();

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-[#08090f]/95 backdrop-blur-sm border-b border-white/[0.07] h-16">
      <div className="max-w-screen-xl mx-auto h-full px-4 flex items-center justify-between gap-4">
        {/* Logo */}
        <div className="flex items-center gap-3 shrink-0">
          <div className="flex items-center justify-center w-8 h-8 rounded bg-red-600">
            <span className="text-white text-lg leading-none">🍁</span>
          </div>
          <div className="leading-tight">
            <div className="text-sm font-bold text-white">GovAI.fm</div>
            <div className="text-xs text-slate-400 hidden sm:block">Canada AI Task Force Dashboard</div>
          </div>
        </div>

        {/* Nav */}
        <nav className="hidden md:flex items-center gap-1">
          {navLinks.map(({ to, label }) => (
            <NavLink
              key={to}
              to={to}
              end={to === '/'}
              className={({ isActive }) =>
                `px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-white/[0.08] text-white'
                    : 'text-slate-400 hover:text-white hover:bg-white/[0.05]'
                }`
              }
            >
              {label}
            </NavLink>
          ))}
        </nav>

        {/* Expert toggle */}
        <div className="flex items-center gap-2 shrink-0">
          <Toggle
            checked={includeExpertReports}
            onChange={setIncludeExpertReports}
            label="Expert Reports"
          />
        </div>
      </div>
    </header>
  );
}
