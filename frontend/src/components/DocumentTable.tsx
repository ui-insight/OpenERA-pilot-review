import type { DocumentRead } from "../types/pilot";

interface DocumentTableProps {
  documents: DocumentRead[];
  showBucket?: boolean;
}

function formatSize(bytes: number | null): string {
  if (!bytes) return "—";
  if (bytes >= 1_048_576) return `${(bytes / 1_048_576).toFixed(1)} MB`;
  if (bytes >= 1_024) return `${(bytes / 1_024).toFixed(0)} KB`;
  return `${bytes} B`;
}

export default function DocumentTable({
  documents,
  showBucket = false,
}: DocumentTableProps) {
  if (documents.length === 0) {
    return (
      <p className="py-8 text-center text-sm text-gray-500">
        No documents found.
      </p>
    );
  }

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200 text-sm">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-4 py-3 text-left font-medium text-gray-500">
              Filename
            </th>
            <th className="px-4 py-3 text-left font-medium text-gray-500">
              Category
            </th>
            <th className="px-4 py-3 text-left font-medium text-gray-500">
              Linked To
            </th>
            {showBucket && (
              <th className="px-4 py-3 text-left font-medium text-gray-500">
                Record
              </th>
            )}
            <th className="px-4 py-3 text-right font-medium text-gray-500">
              Size
            </th>
            <th className="px-4 py-3 text-center font-medium text-gray-500">
              Flags
            </th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-100">
          {documents.map((doc) => (
            <tr key={doc.document_id} className="hover:bg-gray-50">
              <td className="max-w-xs truncate px-4 py-2 font-mono text-xs text-gray-900">
                {doc.filename}
              </td>
              <td className="px-4 py-2 text-gray-600">
                {doc.document_type_label ?? "—"}
              </td>
              <td className="px-4 py-2 text-gray-600">
                <span className="text-xs text-gray-400">
                  {doc.parent_entity_type}:
                </span>{" "}
                {doc.parent_entity_id}
              </td>
              {showBucket && (
                <td className="px-4 py-2 font-medium text-gray-700">
                  {doc.top_level_bucket}
                </td>
              )}
              <td className="px-4 py-2 text-right text-gray-500">
                {formatSize(doc.file_size_bytes)}
              </td>
              <td className="px-4 py-2 text-center">
                {doc.is_content_duplicate && (
                  <span className="rounded bg-amber-100 px-1.5 py-0.5 text-xs text-amber-700">
                    dup
                  </span>
                )}
                {doc.needs_review && (
                  <span className="ml-1 rounded bg-red-100 px-1.5 py-0.5 text-xs text-red-700">
                    review
                  </span>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
