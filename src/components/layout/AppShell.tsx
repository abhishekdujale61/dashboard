import { Outlet } from 'react-router-dom';
import { Header } from './Header';
import { Sidebar } from './Sidebar';

export function AppShell() {
  return (
    <div className="min-h-screen bg-[#08090f]">
      <Header />
      <div className="max-w-screen-xl mx-auto px-4 pt-20 pb-12">
        <div className="flex gap-8">
          <Sidebar />
          <main className="flex-1 min-w-0">
            <Outlet />
          </main>
        </div>
      </div>
    </div>
  );
}
