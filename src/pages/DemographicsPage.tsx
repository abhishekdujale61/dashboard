import { DEMOGRAPHICS } from '../data';
import { SectionHeader } from '../components/ui/SectionHeader';
import { SectorPieChart } from '../components/charts/SectorPieChart';
import { GeographyBarChart } from '../components/charts/GeographyBarChart';
import { RespondentDonut } from '../components/charts/RespondentDonut';

export function DemographicsPage() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-white tracking-tight">Who Responded</h1>
        <p className="text-slate-400 text-sm mt-1">
          Breakdown of the {DEMOGRAPHICS.totalRespondents.toLocaleString()} respondents to Canada's AI Strategy consultation
        </p>
      </div>

      {/* Top stats */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        {DEMOGRAPHICS.respondentTypes.map((type) => (
          <div key={type.label} className="bg-[#0f1117] border border-white/[0.07] rounded-xl p-4 text-center">
            <p className="text-3xl font-bold text-indigo-400">{type.value}%</p>
            <p className="text-sm text-slate-300 font-medium mt-1">{type.label}</p>
            <p className="text-xs text-slate-500 mt-0.5">{type.count?.toLocaleString()} respondents</p>
          </div>
        ))}
        <div className="bg-[#0f1117] border border-white/[0.07] rounded-xl p-4 text-center">
          <p className="text-3xl font-bold text-white">{DEMOGRAPHICS.totalQuestions}</p>
          <p className="text-sm text-slate-300 font-medium mt-1">Survey Questions</p>
          <p className="text-xs text-slate-500 mt-0.5">{DEMOGRAPHICS.totalResponses.toLocaleString()} total responses</p>
        </div>
        <div className="bg-[#0f1117] border border-white/[0.07] rounded-xl p-4 text-center">
          <p className="text-3xl font-bold text-white">8</p>
          <p className="text-sm text-slate-300 font-medium mt-1">Strategy Pillars</p>
          <p className="text-xs text-slate-500 mt-0.5">Covered in consultation</p>
        </div>
      </div>

      {/* Charts row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-[#0f1117] rounded-xl border border-white/[0.07] p-5">
          <SectionHeader
            title="Respondent Type"
            subtitle="Individual citizens vs. organizations"
          />
          <RespondentDonut />
        </div>
        <div className="bg-[#0f1117] rounded-xl border border-white/[0.07] p-5">
          <SectionHeader
            title="Sector Breakdown"
            subtitle="What industries respondents represent"
          />
          <SectorPieChart />
        </div>
      </div>

      {/* Geography */}
      <div className="bg-[#0f1117] rounded-xl border border-white/[0.07] p-5">
        <SectionHeader
          title="Geographic Distribution"
          subtitle="Responses by province/territory — Ontario and BC together account for 60%"
        />
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <GeographyBarChart />
          <div className="grid grid-cols-2 gap-3 content-start">
            {DEMOGRAPHICS.geography.map((entry) => (
              <div
                key={entry.province}
                className="flex items-center justify-between bg-white/[0.04] rounded-lg px-3 py-2"
              >
                <div>
                  <p className="text-sm font-semibold text-slate-200">{entry.province}</p>
                  <p className="text-xs text-slate-500 truncate">{entry.fullName}</p>
                </div>
                <div className="text-right">
                  <p className="text-sm font-bold text-indigo-400">{entry.value}%</p>
                  <p className="text-xs text-slate-500">{entry.count.toLocaleString()}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Age groups + gender */}
      {DEMOGRAPHICS.ageGroups && DEMOGRAPHICS.gender && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-[#0f1117] rounded-xl border border-white/[0.07] p-5">
            <SectionHeader
              title="Age Groups"
              subtitle="Among submitted respondents (3,162 total)"
            />
            <div className="space-y-2">
              {DEMOGRAPHICS.ageGroups.map((age) => (
                <div key={age.label} className="flex items-center gap-3">
                  <span className="text-sm text-slate-400 w-28 shrink-0">{age.label}</span>
                  <div className="flex-1 bg-white/[0.06] rounded-full h-3 overflow-hidden">
                    <div
                      className="h-full bg-indigo-500 rounded-full"
                      style={{ width: `${(age.value / 30) * 100}%`, opacity: 0.75 }}
                    />
                  </div>
                  <span className="text-sm font-semibold text-slate-300 w-12 text-right">{age.value}%</span>
                </div>
              ))}
            </div>
          </div>
          <div className="bg-[#0f1117] rounded-xl border border-white/[0.07] p-5">
            <SectionHeader
              title="Gender Identity"
              subtitle="Among submitted respondents who answered"
            />
            <div className="space-y-2">
              {DEMOGRAPHICS.gender.map((g) => (
                <div key={g.label} className="flex items-center gap-3">
                  <span className="text-sm text-slate-400 w-28 shrink-0">{g.label}</span>
                  <div className="flex-1 bg-white/[0.06] rounded-full h-3 overflow-hidden">
                    <div
                      className="h-full rounded-full"
                      style={{ width: `${(g.value / 50) * 100}%`, backgroundColor: g.color ?? '#6366f1', opacity: 0.75 }}
                    />
                  </div>
                  <span className="text-sm font-semibold text-slate-300 w-12 text-right">{g.value}%</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Pillar response volume */}
      {DEMOGRAPHICS.pillarResponseCounts && (
        <div className="bg-[#0f1117] rounded-xl border border-white/[0.07] p-5">
          <SectionHeader
            title="Response Volume by Pillar"
            subtitle="Total open-text responses per strategy pillar (submitted respondents)"
          />
          <div className="space-y-2">
            {[...DEMOGRAPHICS.pillarResponseCounts].sort((a, b) => b.count - a.count).map((p) => (
              <div key={p.pillarId} className="flex items-center gap-3">
                <span className="text-sm text-slate-400 w-52 shrink-0 truncate">
                  {p.pillarId.replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase())}
                </span>
                <div className="flex-1 bg-white/[0.06] rounded-full h-4 overflow-hidden">
                  <div
                    className="h-full bg-indigo-500 rounded-full"
                    style={{ width: `${(p.count / 24000) * 100}%`, opacity: 0.75 }}
                  />
                </div>
                <span className="text-sm font-semibold text-indigo-400 w-16 text-right">
                  {p.count.toLocaleString()}
                </span>
              </div>
            ))}
          </div>
          <p className="text-xs text-slate-500 mt-3">
            Note: Adoption &amp; Commercialization covers 10 questions (highest volume). Talent &amp; Research covers 4 questions.
          </p>
        </div>
      )}

      {/* Arts sector callout */}
      <div className="bg-indigo-500/5 border border-indigo-500/20 rounded-xl p-4 text-sm text-indigo-400">
        <strong className="text-indigo-300">Real data finding:</strong> The arts, entertainment & recreation sector (13.9% of org respondents)
        is notably overrepresented vs. its share of the Canadian workforce. The government summary did not weight
        responses by sector representativeness — inclusion scores in particular would shift meaningfully under weighted analysis.
        Additionally, only <strong>25% of respondents</strong> mentioned inclusion keywords, vs. 83% who mentioned trust/safety.
      </div>
    </div>
  );
}
