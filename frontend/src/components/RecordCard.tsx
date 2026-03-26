import { Link } from "react-router-dom";
import type { PilotRecordSummary } from "../types/pilot";

interface RecordCardProps {
  record: PilotRecordSummary;
}

function formatBudget(amount: number): string {
  if (amount >= 1_000_000) return `$${(amount / 1_000_000).toFixed(1)}M`;
  if (amount >= 1_000) return `$${(amount / 1_000).toFixed(0)}K`;
  return `$${amount.toFixed(0)}`;
}

export default function RecordCard({ record }: RecordCardProps) {
  return (
    <Link
      to={`/records/${record.record_id}`}
      className="block rounded-lg border border-gray-200 bg-white p-5 shadow-sm transition-all hover:border-blue-300 hover:shadow-md"
    >
      <div className="flex items-start justify-between">
        <div>
          <h3 className="text-lg font-semibold text-gray-900">
            {record.record_id}
          </h3>
          <p className="mt-1 text-sm text-gray-500">{record.description}</p>
        </div>
        {!record.has_award && (
          <span className="rounded-full bg-amber-100 px-2 py-0.5 text-xs font-medium text-amber-700">
            Proposal Only
          </span>
        )}
      </div>

      {record.title && (
        <p className="mt-3 text-sm font-medium text-gray-700 line-clamp-2">
          {record.title}
        </p>
      )}

      <div className="mt-4 grid grid-cols-4 gap-3 text-center">
        <div>
          <p className="text-lg font-semibold text-gray-900">
            {record.document_count}
          </p>
          <p className="text-xs text-gray-500">Documents</p>
        </div>
        <div>
          <p className="text-lg font-semibold text-gray-900">
            {record.award_count}
          </p>
          <p className="text-xs text-gray-500">Awards</p>
        </div>
        <div>
          <p className="text-lg font-semibold text-gray-900">
            {record.proposal_count}
          </p>
          <p className="text-xs text-gray-500">Proposals</p>
        </div>
        <div>
          <p className="text-lg font-semibold text-blue-700">
            {formatBudget(record.total_budget)}
          </p>
          <p className="text-xs text-gray-500">Funding</p>
        </div>
      </div>

      {record.duplicate_count > 0 && (
        <div className="mt-3 flex items-center gap-1 text-xs text-amber-600">
          <span>{record.duplicate_count} content duplicates flagged</span>
        </div>
      )}
    </Link>
  );
}
