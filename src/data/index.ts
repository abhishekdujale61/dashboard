import pillarsRaw from './pillars.json';
import demographicsRaw from './demographics.json';
import recommendationsRaw from './recommendations.json';
import expertReportsRaw from './expertReports.json';
import alignmentMapRaw from './alignmentMap.json';
import topicsRaw from './topics.json';
import quotesRaw from './quotes.json';
import expertChunksRaw from './expert_chunks.json';
import type {
  Pillar, Demographics, Recommendation, ExpertReport, AlignmentEntry,
  Topic, PublicQuote, ExpertChunk,
} from '../types';

export const PILLARS        = pillarsRaw        as Pillar[];
export const DEMOGRAPHICS   = demographicsRaw   as Demographics;
export const RECOMMENDATIONS = recommendationsRaw as Recommendation[];
export const EXPERT_REPORTS = expertReportsRaw  as ExpertReport[];
export const ALIGNMENT_MAP  = alignmentMapRaw   as AlignmentEntry[];
export const TOPICS         = topicsRaw         as Topic[];
export const QUOTES         = quotesRaw         as Record<string, PublicQuote[]>;
export const EXPERT_CHUNKS  = expertChunksRaw   as Record<string, ExpertChunk[]>;
