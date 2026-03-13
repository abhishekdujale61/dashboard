import pillarsRaw from './pillars.json';
import demographicsRaw from './demographics.json';
import recommendationsRaw from './recommendations.json';
import expertReportsRaw from './expertReports.json';
import alignmentMapRaw from './alignmentMap.json';
import type { Pillar, Demographics, Recommendation, ExpertReport, AlignmentEntry } from '../types';

export const PILLARS = pillarsRaw as Pillar[];
export const DEMOGRAPHICS = demographicsRaw as Demographics;
export const RECOMMENDATIONS = recommendationsRaw as Recommendation[];
export const EXPERT_REPORTS = expertReportsRaw as ExpertReport[];
export const ALIGNMENT_MAP = alignmentMapRaw as AlignmentEntry[];
