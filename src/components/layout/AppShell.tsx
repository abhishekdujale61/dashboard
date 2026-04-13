import { Outlet } from 'react-router-dom';
import { Header } from './Header';
import { Sidebar } from './Sidebar';

export function AppShell() {
  return (
    <div className="min-h-screen bg-[#08090f] flex flex-col">
      <Header />
      <div className="flex-1 max-w-screen-xl mx-auto w-full px-4 pt-20 pb-12">
        <div className="flex gap-8">
          <Sidebar />
          <main className="flex-1 min-w-0">
            <Outlet />
          </main>
        </div>
      </div>

      {/* Footer */}
      <footer className="border-t border-white/[0.06] py-4 px-4">
        <div className="max-w-screen-xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-2 text-xs text-slate-600">
          <span>
            Data: <a href="https://open.canada.ca" className="hover:text-slate-400 transition-colors" target="_blank" rel="noreferrer">open.canada.ca</a>
            {' '}· Open Government Licence (Canada)
          </span>
          <span>
            Civil society submissions — 65 submissions from 160+ organizations.{' '}
            <a
              href="https://www.peoplesaiconsultation.ca/submissions/"
              className="text-indigo-500 hover:text-indigo-400 transition-colors"
              target="_blank"
              rel="noreferrer"
            >
              Read them here (PCAI) ↗
            </a>
          </span>
        </div>
      </footer>
    </div>
  );
}
