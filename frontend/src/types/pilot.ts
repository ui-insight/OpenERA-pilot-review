/** TypeScript interfaces for the pilot review dashboard. */

export interface PilotRecordSummary {
  record_id: string;
  description: string;
  title: string | null;
  award_count: number;
  proposal_count: number;
  document_count: number;
  duplicate_count: number;
  total_budget: number;
  has_title_gaps: boolean;
  has_award: boolean;
}

export interface PilotDashboard {
  records: PilotRecordSummary[];
  total_awards: number;
  total_proposals: number;
  total_documents: number;
  total_duplicates: number;
  total_budget: number;
}

export interface AwardRead {
  award_id: string;
  award_number: string | null;
  award_title: string | null;
  proposal_id: string | null;
  project_id: string | null;
  sponsor_organization_id: string | null;
  award_status: string | null;
  original_start_date: string | null;
  current_end_date: string | null;
  adjusted_budget: number | null;
  cumulative_funding_amount: number | null;
  needs_veras_title: boolean;
  title_source_type: string | null;
}

export interface ProposalRead {
  proposal_id: string;
  proposal_number: string | null;
  proposal_title: string | null;
  project_id: string | null;
  sponsor_organization_id: string | null;
  proposal_status: string | null;
  start_date: string | null;
  end_date: string | null;
  needs_veras_enrichment: boolean;
  title_source_type: string | null;
}

export interface ProjectRead {
  project_id: string;
  project_title: string | null;
  project_status: string | null;
  start_date: string | null;
  end_date: string | null;
  needs_veras_title: boolean;
}

export interface DocumentRead {
  document_id: string;
  document_type_code: string | null;
  document_type_label: string | null;
  parent_entity_type: string | null;
  parent_entity_id: string | null;
  linked_proposal_id: string | null;
  top_level_bucket: string | null;
  filename: string | null;
  extension: string | null;
  mime_type: string | null;
  file_size_bytes: number | null;
  storage_relative_path: string | null;
  is_content_duplicate: boolean;
  needs_review: string | null;
}

export interface PersonnelRead {
  personnel_id: string;
  full_name: string | null;
  last_name: string | null;
  first_name: string | null;
  person_type: string | null;
  department_organization_id: string | null;
  needs_identity_review: boolean;
}

export interface PilotRecordDetail {
  record_id: string;
  description: string;
  awards: AwardRead[];
  proposals: ProposalRead[];
  projects: ProjectRead[];
  documents: DocumentRead[];
  personnel: PersonnelRead[];
  document_count: number;
  duplicate_count: number;
  category_counts: Record<string, number>;
}

export interface DocumentFilterResult {
  items: DocumentRead[];
  total_count: number;
  page: number;
  page_size: number;
  category_counts: Record<string, number>;
}

export interface AllowedValue {
  allowed_value_id: string;
  group_name: string | null;
  code: string | null;
  label: string | null;
  description: string | null;
}
