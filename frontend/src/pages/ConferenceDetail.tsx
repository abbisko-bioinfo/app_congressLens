import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Link, useParams } from "react-router-dom";
import { api } from "../api/client";

type Tab = "overview" | "sessions" | "presentations" | "calendar" | "insights";

export default function ConferenceDetail() {
  const { id } = useParams<{ id: string }>();
  const [activeTab, setActiveTab] = useState<Tab>("overview");

  const { data: conf } = useQuery({ queryKey: ["conference", id], queryFn: () => api.conferences.get(id!) });
  const { data: sessions } = useQuery({ queryKey: ["sessions", id], queryFn: () => api.sessions.list(id!), enabled: !!id });
  const { data: presentations } = useQuery({ queryKey: ["presentations", id], queryFn: () => api.presentations.list({ conference_id: id!, skip: "0", limit: "50" }), enabled: !!id });
  const { data: watchlist } = useQuery({ queryKey: ["watchlist"], queryFn: () => api.watchlist.list() });
  const { data: calendarEvents } = useQuery({ queryKey: ["calendar"], queryFn: () => api.calendar.events() });

  if (!conf) return <div className="p-6 text-gray-500">Loading...</div>;

  const tabs: { key: Tab; label: string }[] = [
    { key: "overview", label: "Overview" },
    { key: "sessions", label: "Sessions" },
    { key: "presentations", label: "Presentations" },
    { key: "calendar", label: "Calendar" },
    { key: "insights", label: "Insights" },
  ];

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">{conf.acronym} {conf.year}</h1>
      <p className="text-gray-600">{conf.name}</p>

      <nav className="flex border-b border-gray-200">
        {tabs.map((tab) => (
          <button
            key={tab.key}
            onClick={() => setActiveTab(tab.key)}
            className={`px-4 py-2 text-sm font-medium ${activeTab === tab.key ? "text-blue-600 border-b-2 border-blue-600" : "text-gray-500 hover:text-gray-700"}`}
          >
            {tab.label}
          </button>
        ))}
      </nav>

      {activeTab === "overview" && (
        <div className="space-y-4">
          {conf.location && <div className="text-sm text-gray-600"><span className="font-medium">Location:</span> {conf.location}</div>}
          {conf.start_date && <div className="text-sm text-gray-600"><span className="font-medium">Dates:</span> {conf.start_date} - {conf.end_date}</div>}
          {conf.timezone && <div className="text-sm text-gray-600"><span className="font-medium">Timezone:</span> {conf.timezone}</div>}
          {conf.website && <a href={conf.website} className="text-sm text-blue-600 hover:underline">Conference Website</a>}
          {conf.description && <p className="text-sm text-gray-600 mt-2">{conf.description}</p>}
          <div className="text-sm text-gray-500">
            {sessions?.items && <span>{sessions.items.length} sessions</span>}
            {presentations?.items && <span className="ml-2">{presentations.items.length} presentations</span>}
          </div>
        </div>
      )}

      {activeTab === "sessions" && (
        <table className="w-full text-sm">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-3 py-2 text-left text-gray-600 font-medium">Title</th>
              <th className="px-3 py-2 text-left text-gray-600 font-medium">Type</th>
              <th className="px-3 py-2 text-left text-gray-600 font-medium">Room</th>
              <th className="px-3 py-2 text-left text-gray-600 font-medium">Time</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {sessions?.items?.map((s) => (
              <tr key={s.id} className="hover:bg-gray-50">
                <td className="px-3 py-2"><Link to={`/sessions/${s.id}`} className="text-blue-600 hover:underline">{s.title}</Link></td>
                <td className="px-3 py-2 text-gray-600">{s.session_type || "-"}</td>
                <td className="px-3 py-2 text-gray-600">{s.room || "-"}</td>
                <td className="px-3 py-2 text-gray-600">{s.start_time || "-"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {activeTab === "presentations" && (
        <table className="w-full text-sm">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-3 py-2 text-left text-gray-600 font-medium">Title</th>
              <th className="px-3 py-2 text-left text-gray-600 font-medium">Number</th>
              <th className="px-3 py-2 text-left text-gray-600 font-medium">Presenter</th>
              <th className="px-3 py-2 text-left text-gray-600 font-medium">Type</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {presentations?.items?.map((p) => (
              <tr key={p.id} className="hover:bg-gray-50">
                <td className="px-3 py-2"><Link to={`/presentations/${p.id}`} className="text-blue-600 hover:underline">{p.title}</Link></td>
                <td className="px-3 py-2 text-gray-600">{p.abstract_number || p.presentation_number || "-"}</td>
                <td className="px-3 py-2 text-gray-600">{p.presenter_name || "-"}</td>
                <td className="px-3 py-2 text-gray-600">{p.presentation_type || "-"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {activeTab === "calendar" && (
        <div className="space-y-4">
          <div className="p-4 bg-gray-50 rounded-lg">
            <h3 className="text-sm font-semibold text-gray-700 mb-2">Conference Dates</h3>
            {conf.start_date && <p className="text-sm text-gray-600">{conf.start_date} - {conf.end_date}</p>}
          </div>
          {calendarEvents?.events?.filter((e) => e.target_type === "conference" && e.target_id === id).length > 0 && (
            <div className="p-4 bg-blue-50 rounded-lg">
              <h3 className="text-sm font-semibold text-blue-700 mb-2">Watched Items for This Conference</h3>
              <p className="text-xs text-blue-600">This conference is on your watchlist.</p>
            </div>
          )}
          <div className="space-y-2">
            {calendarEvents?.events?.filter((e) => e.target_type === "session").map((e) => (
              <Link key={e.watchlist_id} to={`/sessions/${e.target_id}`} className="block p-3 bg-white rounded border border-gray-200 hover:border-green-400">
                <span className="inline-block px-2 py-0.5 rounded text-xs bg-green-100 text-green-700">session</span>
                <span className="text-sm text-gray-700 ml-2">{e.title || e.target_id.slice(0, 8)}</span>
              </Link>
            ))}
          </div>
        </div>
      )}

      {activeTab === "insights" && (
        <div className="p-6 bg-gray-50 rounded-lg border border-gray-200">
          <h2 className="text-lg font-semibold text-gray-700 mb-3">AI Insights</h2>
          <p className="text-sm text-gray-500">AI-powered conference intelligence is coming soon. This tab will show trend analysis, entity extraction, competitive landscape, and conference insight reports.</p>
        </div>
      )}
    </div>
  );
}