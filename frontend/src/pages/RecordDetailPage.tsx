import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { pilotApi } from "../api/pilot";
import DocumentTable from "../components/DocumentTable";
import type { PilotRecordDetail } from "../types/pilot";

type Tab = "overview" | "documents" | "quality";

function formatDate(d: string | null): string {
  return d ?? "—";
}

function formatCurrency(n: number | null): string {
  if (n == null) return "—";
  return `$${n.toLocaleString(undefined, { minimumFractionDigits: 2 })}`;
}

export default function RecordDetailPage() {
  const { recordId } = useParams<{ recordId: string }>();
  const [detail, setDetail] = useState<PilotRecordDetail | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<Tab>("overview");

  useEffect(() => {
    if (!recordId) return;
    pilotApi
      .getRecord(recordId)
      .then(setDetail)
      .catch((err) => setError(err.message));
  }, [recordId]);

  if (error) {
    return (
      <div className="rounded-lg border border-red-200 bg-red-50 p-6 text-red-700">
        <p>{error}</p>
        <Link to="/" className="mt-2 inline-block text-sm underline">
          Back to dashboard
        </Link>
      </div>
    );
  }

  if (!detail) {
    return (
      <div className="flex items-center justify-center py-20">
        <p className="text-gray-500">Loading...</p>
      </div>
    );
  }

  const tabs: { id: Tab; label: string; count?: number }[] = [
    { id: "overview", label: "Overview" },
    {
      id: "documents",
      label: "Documents",
      count: detail.document_count,
    },
    { id: "quality", label: "Quality" },
  ];

  return (
    <div>
      {/* Header */}
      <div className="mb-6">
        <Link
          to="/"
          className="text-sm text-blue-600 hover:text-blue-800"
        >
          &larr; Dashboard
        </Link>
        <h1 className="mt-2 text-2xl font-bold text-gray-900">
          {detail.record_id}
        </h1>
        <p className="text-sm text-gray-500">{detail.description}</p>
      </div>

      {/* Tabs */}
      <div className="mb-6 flex gap-1 border-b border-gray-200">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-4 py-2 text-sm font-medium transition-colors ${
              activeTab === tab.id
                ? "border-b-2 border-blue-600 text-blue-700"
                : "text-gray-500 hover:text-gray-700"
            }`}
          >
            {tab.label}
            {tab.count != null && (
              <span className="ml-1.5 rounded-full bg-gray-100 px-2 py-0.5 text-xs text-gray-600">
                {tab.count}
              </span>
            )}
          </button>
        ))}
      </div>

      {/* Tab content */}
      {activeTab === "overview" && (
        <div className="space-y-6">
          {/* Awards */}
          {detail.awards.length > 0 && (
            <section>
              <h2 className="mb-3 text-lg font-semibold text-gray-800">
                Awards
              </h2>
              <div className="overflow-x-auto rounded-lg border border-gray-200">
                <table className="min-w-full divide-y divide-gray-200 text-sm">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-4 py-3 text-left font-medium text-gray-500">ID</th>
                      <th className="px-4 py-3 text-left font-medium text-gray-500">Title</th>
                      <th className="px-4 py-3 text-left font-medium text-gray-500">Status</th>
                      <th className="px-4 py-3 text-left font-medium text-gray-500">Dates</th>
                      <th className="px-4 py-3 text-right font-medium text-gray-500">Budget</th>
                      <th className="px-4 py-3 text-right font-medium text-gray-500">Funding</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-100">
                    {detail.awards.map((a) => (
                      <tr key={a.award_id}>
                        <td className="px-4 py-2 font-medium">{a.award_id}</td>
                        <td className="max-w-sm truncate px-4 py-2 text-gray-700">
                          {a.award_title || <span className="italic text-amber-600">Missing</span>}
                        </td>
                        <td className="px-4 py-2">{a.award_status}</td>
                        <td className="px-4 py-2 text-xs text-gray-500">
                          {formatDate(a.original_start_date)} — {formatDate(a.current_end_date)}
                        </td>
                        <td className="px-4 py-2 text-right">{formatCurrency(a.adjusted_budget)}</td>
                        <td className="px-4 py-2 text-right font-medium">{formatCurrency(a.cumulative_funding_amount)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </section>
          )}

          {/* Proposals */}
          {detail.proposals.length > 0 && (
            <section>
              <h2 className="mb-3 text-lg font-semibold text-gray-800">
                Proposals ({detail.proposals.length})
              </h2>
              <div className="overflow-x-auto rounded-lg border border-gray-200">
                <table className="min-w-full divide-y divide-gray-200 text-sm">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-4 py-3 text-left font-medium text-gray-500">ID</th>
                      <th className="px-4 py-3 text-left font-medium text-gray-500">Title</th>
                      <th className="px-4 py-3 text-left font-medium text-gray-500">Status</th>
                      <th className="px-4 py-3 text-left font-medium text-gray-500">Dates</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-100">
                    {detail.proposals.map((p) => (
                      <tr key={p.proposal_id}>
                        <td className="px-4 py-2 font-medium">{p.proposal_id}</td>
                        <td className="max-w-sm truncate px-4 py-2 text-gray-700">
                          {p.proposal_title || <span className="italic text-amber-600">Missing</span>}
                        </td>
                        <td className="px-4 py-2">{p.proposal_status}</td>
                        <td className="px-4 py-2 text-xs text-gray-500">
                          {formatDate(p.start_date)} — {formatDate(p.end_date)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </section>
          )}

          {/* Personnel */}
          {detail.personnel.length > 0 && (
            <section>
              <h2 className="mb-3 text-lg font-semibold text-gray-800">
                Personnel ({detail.personnel.length})
              </h2>
              <div className="overflow-x-auto rounded-lg border border-gray-200">
                <table className="min-w-full divide-y divide-gray-200 text-sm">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-4 py-3 text-left font-medium text-gray-500">Name</th>
                      <th className="px-4 py-3 text-left font-medium text-gray-500">Role</th>
                      <th className="px-4 py-3 text-left font-medium text-gray-500">Department</th>
                      <th className="px-4 py-3 text-center font-medium text-gray-500">Flags</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-100">
                    {detail.personnel.map((p) => (
                      <tr key={p.personnel_id}>
                        <td className="px-4 py-2 font-medium">{p.full_name}</td>
                        <td className="px-4 py-2">{p.person_type}</td>
                        <td className="px-4 py-2 text-gray-500">{p.department_organization_id ?? "—"}</td>
                        <td className="px-4 py-2 text-center">
                          {p.needs_identity_review && (
                            <span className="rounded bg-amber-100 px-1.5 py-0.5 text-xs text-amber-700">
                              needs review
                            </span>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </section>
          )}
        </div>
      )}

      {activeTab === "documents" && (
        <div>
          {/* Category breakdown */}
          {Object.keys(detail.category_counts).length > 0 && (
            <div className="mb-4 flex flex-wrap gap-2">
              {Object.entries(detail.category_counts)
                .sort(([, a], [, b]) => b - a)
                .map(([cat, count]) => (
                  <span
                    key={cat}
                    className="rounded-full border border-gray-200 bg-white px-3 py-1 text-xs text-gray-600"
                  >
                    {cat}: {count}
                  </span>
                ))}
            </div>
          )}
          {detail.duplicate_count > 0 && (
            <p className="mb-4 text-sm text-amber-600">
              {detail.duplicate_count} content duplicates flagged
            </p>
          )}
          <DocumentTable documents={detail.documents} />
        </div>
      )}

      {activeTab === "quality" && (
        <div className="space-y-4">
          <div className="rounded-lg border border-gray-200 bg-white p-5">
            <h3 className="font-semibold text-gray-800">Title Coverage</h3>
            <div className="mt-3 space-y-2 text-sm">
              {detail.awards.map((a) => (
                <div key={a.award_id} className="flex items-center gap-2">
                  <span className={`h-2 w-2 rounded-full ${a.award_title ? "bg-green-500" : "bg-red-400"}`} />
                  <span className="text-gray-600">Award {a.award_id}:</span>
                  <span>{a.award_title ? "Has title" : "Missing title"}</span>
                </div>
              ))}
              {detail.proposals.map((p) => (
                <div key={p.proposal_id} className="flex items-center gap-2">
                  <span className={`h-2 w-2 rounded-full ${p.proposal_title ? "bg-green-500" : "bg-red-400"}`} />
                  <span className="text-gray-600">Proposal {p.proposal_id}:</span>
                  <span>{p.proposal_title ? "Has title" : "Missing title"}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="rounded-lg border border-gray-200 bg-white p-5">
            <h3 className="font-semibold text-gray-800">Document Quality</h3>
            <div className="mt-3 space-y-2 text-sm text-gray-600">
              <p>Total documents: {detail.document_count}</p>
              <p>Content duplicates: {detail.duplicate_count}</p>
              <p>Categories used: {Object.keys(detail.category_counts).length}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
