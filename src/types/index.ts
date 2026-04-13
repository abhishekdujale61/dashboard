export type AlignmentStatus = 'aligned' | 'tension' | 'diverges';
export type PriorityLevel = 'high' | 'medium' | 'low';
export type UrgencyLevel = 'critical' | 'high' | 'medium';
export type SentimentType = 'supportive' | 'opposed' | 'concerned' | 'neutral';
export type SalienceLevel = 'primary' | 'secondary' | 'passing';
export type DepthLevel = 'evidence-based' | 'reasoned' | 'assertion';

export interface Pillar {
  id: string;
  slug: string;
  label: string;
  pillarNumber: number;
  color: string;
  icon: string;
  totalRecommendations: number;
  respondentWeight: number;
  publicPriorityScore: number;
  expertPriorityScore: number;
  alignmentStatus: AlignmentStatus;
  summary: string;
}

export interface Topic {
  id: string;
  pillarId: string;
  label: string;
  publicScore: number;
  expertScore: number;
  delta: number;
  alignmentStatus: AlignmentStatus;
  dominantPublicSentiment: SentimentType;
  dominantExpertSentiment: SentimentType;
  publicChunkCount: number;
  expertChunkCount: number;
}

export interface PublicQuote {
  id: string;
  text: string;
  sentiment: SentimentType;
  salience: SalienceLevel;
  depth: DepthLevel;
  respondentType?: string;
  province?: string | null;
  score: number;
}

export interface ExpertChunk {
  id: string;
  header: string;
  body: string;
  expertName: string;
  affiliation?: string;
  reportTitle: string;
  reportUrl?: string;
  sentiment: SentimentType;
  salience: SalienceLevel;
  depth: DepthLevel;
  score: number;
}

export interface DemographicSlice {
  label: string;
  value: number;
  count?: number;
  color?: string;
}

export interface GeographyEntry {
  province: string;
  fullName: string;
  value: number;
  count: number;
}

export interface Demographics {
  totalRespondents: number;
  submittedRespondents: number;
  totalResponses: number;
  submittedResponses: number;
  totalQuestions: number;
  taskForceExperts: number;
  taskForceReports: number;
  respondentTypes: DemographicSlice[];
  respondentTypesAll?: DemographicSlice[];
  respondentRoles?: Array<{ label: string; count: number }>;
  sectors: DemographicSlice[];
  geography: GeographyEntry[];
  orgSizes?: DemographicSlice[];
  ageGroups?: DemographicSlice[];
  gender?: DemographicSlice[];
  pillarResponseCounts?: Array<{ pillarId: string; count: number }>;
}

export interface Recommendation {
  id: string;
  pillarId: string;
  pillarLabel: string;
  topicId?: string;
  member: string;
  memberRole: string;
  text: string;
  expertOnly: boolean;
  priority: PriorityLevel;
  publicSupportScore: number;
  expertEndorsement: boolean;
}

export interface ExpertReport {
  pillarId: string;
  reportTitle: string;
  authors: string[];
  publishedDate: string;
  keyFindings: string[];
  recommendations: string[];
  policyGap: string;
  urgencyLevel: UrgencyLevel;
}

export interface AlignmentEntry {
  pillarId: string;
  pillarLabel: string;
  publicScore: number;
  expertScore: number;
  delta: number;
  status: AlignmentStatus;
  responseCount?: number;
  notes: string;
  keyTension: string | null;
}
