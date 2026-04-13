import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { DashboardProvider } from './context/DashboardContext';
import { AppShell } from './components/layout/AppShell';
import { OverviewPage } from './pages/OverviewPage';
import { DemographicsPage } from './pages/DemographicsPage';
import { AlignmentPage } from './pages/AlignmentPage';
import { RecommendationsPage } from './pages/RecommendationsPage';
import { PillarDetailPage } from './pages/PillarDetailPage';
import { TopicDetailPage } from './pages/TopicDetailPage';

export default function App() {
  return (
    <BrowserRouter>
      <DashboardProvider>
        <Routes>
          <Route element={<AppShell />}>
            <Route index element={<OverviewPage />} />
            <Route path="demographics" element={<DemographicsPage />} />
            <Route path="alignment" element={<AlignmentPage />} />
            <Route path="recommendations" element={<RecommendationsPage />} />
            <Route path="pillars/:pillarId" element={<PillarDetailPage />} />
            <Route path="pillars/:pillarId/topics/:topicId" element={<TopicDetailPage />} />
          </Route>
        </Routes>
      </DashboardProvider>
    </BrowserRouter>
  );
}
