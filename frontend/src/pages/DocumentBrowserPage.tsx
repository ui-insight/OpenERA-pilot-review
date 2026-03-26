import { useEffect, useState } from "react";
import { pilotApi } from "../api/pilot";
import DocumentTable from "../components/DocumentTable";
import type { AllowedValue, DocumentFilterResult } from "../types/pilot";

const PILOT_RECORDS = ["AA4673", "AA6006", "OS7090", "SI3394", "V250261"];

export default function DocumentBrowserPage() {
  const [result, setResult] = useState<DocumentFilterResult | null>(null);
  const [docTypes, setDocTypes] = useState<AllowedValue[]>([]);
  const [error, setError] = useState<string | null>(null);

  // Filters
  const [recordId, setRecordId] = useState("");
  const [category, setCategory] = useState("");
  const [parentType, setParentType] = useState("");
  const [isDuplicate, setIsDuplicate] = useState<string>("");
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const pageSize = 25;

  // Load document types on mount
  useEffect(() => {
    pilotApi.getDocumentTypes().then(setDocTypes).catch(() => {});
  }, []);

  // Fetch documents when filters change
  useEffect(() => {
    const filters: Record<string, unknown> = { page, page_size: pageSize };
    if (recordId) filters.record_id = recordId;
    if (category) filters.category = category;
    if (parentType) filters.parent_type = parentType;
    if (isDuplicate === "true") filters.is_duplicate = true;
    if (isDuplicate === "false") filters.is_duplicate = false;
    if (search) filters.search = search;

    pilotApi
      .getAllDocuments(filters as Parameters<typeof pilotApi.getAllDocuments>[0])
      .then(setResult)
      .catch((err) => setError(err.message));
  }, [recordId, category, parentType, isDuplicate, search, page]);

  const totalPages = result ? Math.ceil(result.total_count / pageSize) : 0;

  return (
    <div>
      <h1 className="mb-2 text-2xl font-bold text-gray-900">
        Document Browser
      </h1>
      <p className="mb-6 text-sm text-gray-500">
        Browse and filter all staged documents across pilot records.
      </p>

      {/* Filters */}
      <div className="mb-6 flex flex-wrap items-end gap-3 rounded-lg border border-gray-200 bg-white p-4">
        <div>
          <label className="mb-1 block text-xs font-medium text-gray-500">
            Record
          </label>
          <select
            value={recordId}
            onChange={(e) => { setRecordId(e.target.value); setPage(1); }}
            className="rounded border border-gray-300 px-3 py-1.5 text-sm"
          >
            <option value="">All Records</option>
            {PILOT_RECORDS.map((id) => (
              <option key={id} value={id}>
                {id}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="mb-1 block text-xs font-medium text-gray-500">
            Category
          </label>
          <select
            value={category}
            onChange={(e) => { setCategory(e.target.value); setPage(1); }}
            className="rounded border border-gray-300 px-3 py-1.5 text-sm"
          >
            <option value="">All Categories</option>
            {docTypes.map((dt) => (
              <option key={dt.code} value={dt.label ?? ""}>
                {dt.label}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="mb-1 block text-xs font-medium text-gray-500">
            Parent Type
          </label>
          <select
            value={parentType}
            onChange={(e) => { setParentType(e.target.value); setPage(1); }}
            className="rounded border border-gray-300 px-3 py-1.5 text-sm"
          >
            <option value="">All</option>
            <option value="Award">Award</option>
            <option value="Proposal">Proposal</option>
          </select>
        </div>

        <div>
          <label className="mb-1 block text-xs font-medium text-gray-500">
            Duplicates
          </label>
          <select
            value={isDuplicate}
            onChange={(e) => { setIsDuplicate(e.target.value); setPage(1); }}
            className="rounded border border-gray-300 px-3 py-1.5 text-sm"
          >
            <option value="">All</option>
            <option value="true">Duplicates Only</option>
            <option value="false">Non-Duplicates Only</option>
          </select>
        </div>

        <div className="flex-1">
          <label className="mb-1 block text-xs font-medium text-gray-500">
            Search Filename
          </label>
          <input
            type="text"
            value={search}
            onChange={(e) => { setSearch(e.target.value); setPage(1); }}
            placeholder="Type to search..."
            className="w-full rounded border border-gray-300 px-3 py-1.5 text-sm"
          />
        </div>
      </div>

      {error && (
        <div className="mb-4 rounded border border-red-200 bg-red-50 p-3 text-sm text-red-700">
          {error}
        </div>
      )}

      {result && (
        <>
          {/* Category facet chips */}
          {Object.keys(result.category_counts).length > 0 && (
            <div className="mb-4 flex flex-wrap gap-2">
              {Object.entries(result.category_counts)
                .sort(([, a], [, b]) => b - a)
                .map(([cat, count]) => (
                  <button
                    key={cat}
                    onClick={() => { setCategory(cat); setPage(1); }}
                    className={`rounded-full border px-3 py-1 text-xs transition-colors ${
                      category === cat
                        ? "border-blue-300 bg-blue-50 text-blue-700"
                        : "border-gray-200 bg-white text-gray-600 hover:border-blue-200"
                    }`}
                  >
                    {cat}: {count}
                  </button>
                ))}
            </div>
          )}

          <p className="mb-3 text-sm text-gray-500">
            {result.total_count} documents found
          </p>

          <DocumentTable documents={result.items} showBucket />

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="mt-4 flex items-center justify-between">
              <button
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                disabled={page === 1}
                className="rounded border border-gray-300 px-3 py-1.5 text-sm disabled:opacity-40"
              >
                Previous
              </button>
              <span className="text-sm text-gray-500">
                Page {page} of {totalPages}
              </span>
              <button
                onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                disabled={page === totalPages}
                className="rounded border border-gray-300 px-3 py-1.5 text-sm disabled:opacity-40"
              >
                Next
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
}
