import { createContext, useContext, useState, useMemo, type ReactNode } from 'react';
import { RECOMMENDATIONS } from '../data';
import type { Recommendation } from '../types';

interface DashboardContextType {
  activePillarId: string | null;
  setActivePillarId: (id: string | null) => void;
  filteredRecommendations: Recommendation[];
}

const DashboardContext = createContext<DashboardContextType | null>(null);

export function DashboardProvider({ children }: { children: ReactNode }) {
  const [activePillarId, setActivePillarId] = useState<string | null>(null);

  const filteredRecommendations = useMemo(() => {
    if (!activePillarId) return RECOMMENDATIONS;
    return RECOMMENDATIONS.filter((rec) => rec.pillarId === activePillarId);
  }, [activePillarId]);

  return (
    <DashboardContext.Provider
      value={{ activePillarId, setActivePillarId, filteredRecommendations }}
    >
      {children}
    </DashboardContext.Provider>
  );
}

export function useDashboard() {
  const ctx = useContext(DashboardContext);
  if (!ctx) throw new Error('useDashboard must be used inside DashboardProvider');
  return ctx;
}
