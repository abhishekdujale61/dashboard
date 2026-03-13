import { createContext, useContext, useState, useMemo, type ReactNode } from 'react';
import { RECOMMENDATIONS } from '../data';
import type { Recommendation } from '../types';

interface DashboardContextType {
  includeExpertReports: boolean;
  setIncludeExpertReports: (v: boolean) => void;
  activePillarId: string | null;
  setActivePillarId: (id: string | null) => void;
  filteredRecommendations: Recommendation[];
}

const DashboardContext = createContext<DashboardContextType | null>(null);

export function DashboardProvider({ children }: { children: ReactNode }) {
  const [includeExpertReports, setIncludeExpertReports] = useState(true);
  const [activePillarId, setActivePillarId] = useState<string | null>(null);

  const filteredRecommendations = useMemo(() => {
    return RECOMMENDATIONS.filter((rec) => {
      if (!includeExpertReports && rec.expertOnly) return false;
      if (activePillarId && rec.pillarId !== activePillarId) return false;
      return true;
    });
  }, [includeExpertReports, activePillarId]);

  return (
    <DashboardContext.Provider
      value={{
        includeExpertReports,
        setIncludeExpertReports,
        activePillarId,
        setActivePillarId,
        filteredRecommendations,
      }}
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
