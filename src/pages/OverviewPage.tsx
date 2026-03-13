import { DEMOGRAPHICS, PILLARS } from '../data';
import { SectionHeader } from '../components/ui/SectionHeader';
import { PillarRadarChart } from '../components/charts/PillarRadarChart';
import { PillarBarChart } from '../components/charts/PillarBarChart';
import { RespondentDonut } from '../components/charts/RespondentDonut';
import { PillarCard } from '../components/cards/PillarCard';

function StatBlock({ value, label, sub }: { value: string; label: string; sub?: string }) {
  return (
    <div className="bg-[#0f1117] rounded-xl border border-white/[0.07] p-5 text-center">
      <p className="text-3xl font-bold text-white">{value}</p>
      <p className="text-sm font-medium text-slate-400 mt-1">{label}</p>
      {sub && <p className="text-xs text-slate-500 mt-0.5">{sub}</p>}
    </div>
  );
}

export function OverviewPage() {
  return (
    <div className="space-y-8">
      {/* Hero */}
      <div className="bg-gradient-to-br from-indigo-950/60 to-slate-900/40 border border-indigo-500/20 rounded-2xl p-6 text-white">
        <div className="flex items-start gap-3 mb-4">
          <span className="text-2xl">🍁</span>
          <div>
            <h1 className="text-xl font-bold leading-tight">Canada AI Task Force</h1>
            <p className="text-slate-300 text-sm mt-0.5">National AI Strategy Consultation — Data Dashboard</p>
          </div>
        </div>
        <p className="text-slate-400 text-sm leading-relaxed max-w-2xl">
          The government's official summary was vague with no data weighting. This dashboard surfaces what{' '}
          <strong className="text-white">11,300+ Canadians</strong> actually said — and where the 28 Task Force experts
          agree or diverge from public opinion. Data released under{' '}
          <span className="text-indigo-300">Open Government Licence (Canada)</span>.
        </p>
      </div>

      {/* Key stats */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <StatBlock
          value={DEMOGRAPHICS.totalRespondents.toLocaleString()}
          label="Total Respondents"
          sub={`${DEMOGRAPHICS.submittedRespondents.toLocaleString()} fully submitted`}
        />
        <StatBlock
          value={DEMOGRAPHICS.totalResponses.toLocaleString()}
          label="Open-text Responses"
          sub={`Across ${DEMOGRAPHICS.totalQuestions} questions`}
        />
        <StatBlock
          value={String(DEMOGRAPHICS.taskForceExperts)}
          label="Task Force Experts"
          sub="Across 8 pillars"
        />
        <StatBlock
          value={String(DEMOGRAPHICS.taskForceReports)}
          label="Expert Reports"
          sub="Analyzed & mapped"
        />
      </div>

      {/* Charts row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-[#0f1117] rounded-xl border border-white/[0.07] p-5">
          <SectionHeader
            title="Priority by Pillar"
            subtitle="Public vs Expert priority scores (0–10)"
          />
          <PillarRadarChart />
        </div>
        <div className="bg-[#0f1117] rounded-xl border border-white/[0.07] p-5">
          <SectionHeader
            title="Respondent Type"
            subtitle="Who participated in the consultation"
          />
          <RespondentDonut />
          <div className="mt-6">
            <SectionHeader
              title="Recommendations by Pillar"
              subtitle="Click a bar to explore pillar detail"
            />
            <PillarBarChart />
          </div>
        </div>
      </div>

      {/* Pillars grid */}
      <div>
        <div className="mb-6">
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 mb-2">
            Open Government Data
          </span>
          <h2 className="text-lg font-semibold text-slate-100 tracking-tight">8 AI Strategy Pillars</h2>
          <p className="mt-1 text-sm text-slate-500">All pillars with public & expert alignment scores. Click any pillar to explore recommendations.</p>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
          {PILLARS.map((pillar) => (
            <PillarCard key={pillar.id} pillar={pillar} />
          ))}
        </div>
      </div>

      {/* Real data banner */}
      <div className="bg-emerald-500/5 border border-emerald-500/20 rounded-xl p-4 text-sm text-emerald-400">
        <strong className="text-emerald-300">✓ Real data:</strong> Public priority scores derived by keyword-frequency analysis across{' '}
        <strong className="text-emerald-300">68,702 open-text responses</strong> from the official XLSX (ai-strategy-raw-data-2025-1.xlsx).
        Scores are normalized to a 0–10 scale based on pillar mention rate across submitted responses.
        Expert scores reflect Task Force report emphasis weighting. Source:{' '}
        <span className="font-mono text-xs">open.canada.ca</span> — Open Government Licence (Canada).
      </div>
    </div>
  );
}
