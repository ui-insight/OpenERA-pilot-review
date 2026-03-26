import { useEffect, useState } from "react";
import { pilotApi } from "../api/pilot";
import RecordCard from "../components/RecordCard";
import StatCard from "../components/StatCard";
import type { PilotDashboard } from "../types/pilot";

export default function DashboardPage() {
  const [dashboard, setDashboard] = useState<PilotDashboard | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    pilotApi
      .getDashboard()
      .then(setDashboard)
      .catch((err) => setError(err.message));
  }, []);

  if (error) {
    return (
      <div className="rounded-lg border border-red-200 bg-red-50 p-6 text-red-700">
        <h2 className="font-semibold">Error loading dashboard</h2>
        <p className="mt-1 text-sm">{error}</p>
      </div>
    );
  }

  if (!dashboard) {
    return (
      <div className="flex items-center justify-center py-20">
        <p className="text-gray-500">Loading dashboard...</p>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">
          Pilot Migration Review
        </h1>
        <p className="mt-1 text-sm text-gray-500">
          VERAS/Banner to OpenERA — 5 representative records for OSP review
        </p>
      </div>

      {/* Overall stats */}
      <div className="mb-8 grid grid-cols-2 gap-4 sm:grid-cols-5">
        <StatCard
          label="Total Documents"
          value={dashboard.total_documents}
          accent="blue"
        />
        <StatCard
          label="Total Awards"
          value={dashboard.total_awards}
          accent="green"
        />
        <StatCard
          label="Total Proposals"
          value={dashboard.total_proposals}
          accent="green"
        />
        <StatCard
          label="Duplicates"
          value={dashboard.total_duplicates}
          accent="amber"
        />
        <StatCard
          label="Total Funding"
          value={`$${(dashboard.total_budget / 1_000_000).toFixed(1)}M`}
          accent="blue"
        />
      </div>

      {/* Pilot record cards */}
      <h2 className="mb-4 text-lg font-semibold text-gray-800">
        Pilot Records
      </h2>
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {dashboard.records.map((record) => (
          <RecordCard key={record.record_id} record={record} />
        ))}
      </div>
    </div>
  );
}
