/** API module for pilot review dashboard endpoints. */

import { api } from "./client";
import type {
  AllowedValue,
  DocumentFilterResult,
  PilotDashboard,
  PilotRecordDetail,
} from "../types/pilot";

function toParams(obj: Record<string, unknown>): Record<string, string> {
  const params: Record<string, string> = {};
  for (const [key, value] of Object.entries(obj)) {
    if (value !== undefined && value !== null && value !== "") {
      params[key] = String(value);
    }
  }
  return params;
}

export const pilotApi = {
  getDashboard: () => api.get<PilotDashboard>("/pilot/dashboard"),

  getRecord: (recordId: string) =>
    api.get<PilotRecordDetail>(`/pilot/records/${recordId}`),

  getRecordDocuments: (
    recordId: string,
    filters?: {
      category?: string;
      parent_type?: string;
      is_duplicate?: boolean;
      search?: string;
      page?: number;
      page_size?: number;
    }
  ) =>
    api.get<DocumentFilterResult>(
      `/pilot/records/${recordId}/documents`,
      toParams(filters ?? {})
    ),

  getAllDocuments: (filters?: {
    record_id?: string;
    category?: string;
    parent_type?: string;
    is_duplicate?: boolean;
    search?: string;
    page?: number;
    page_size?: number;
  }) => api.get<DocumentFilterResult>("/pilot/documents", toParams(filters ?? {})),

  getDocumentTypes: () =>
    api.get<AllowedValue[]>("/pilot/allowed-values/document-types"),
};
