import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import { api } from "../api/client";

export default function Dashboard() {
  const { data: recentPres } = useQuery({ queryKey: ["presentations", "recent"], queryFn: () => api.presentations.list({ skip: "0", limit: "10" }) });
  const { data: conferences } = useQuery({ queryKey: ["conferences"], queryFn: () => api.conferences.list(0, 5) });
  const { data: watchlist } = useQuery({ queryKey: ["watchlist"], queryFn: () => api.watchlist.list() });
  const { data: upcomingSessions } = useQuery({ queryKey: ["sessions", "upcoming"], queryFn: () => api.sessions.list() });

  const watchedPresentations = watchlist?.filter((w) => w.target_type === "presentation") || [];
  const watchedSessions = watchlist?.filter((w) => w.target_type === "session") || [];

  return (
    <div className="p-6 space-y-8">
      <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>

      <section>
        <h2 className="text-lg font-semibold text-gray-700 mb-3">Watched Presentations</h2>
        {watchedPresentations.length === 0 ? (
          <p className="text-sm text-gray-400">No watched presentations yet. Use the watch button on a presentation to add it here.</p>
        ) : (
          <table className="w-full text-sm">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-3 py-2 text-left text-gray-600 font-medium">ID</th>
                <th className="px-3 py-2 text-left text-gray-600 font-medium">Type</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {watchedPresentations.map((w) => (
                <tr key={w.id} className="hover:bg-gray-50">
                  <td className="px-3 py-2"><Link to={`/presentations/${w.target_id}`} className="text-blue-600 hover:underline">{w.target_id.slice(0, 8)}...</Link></td>
                  <td className="px-3 py-2"><span className="inline-block px-2 py-0.5 rounded text-xs bg-blue-100 text-blue-700">{w.target_type}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>

      <section>
        <h2 className="text-lg font-semibold text-gray-700 mb-3">Upcoming Watched Sessions</h2>
        {watchedSessions.length === 0 ? (
          <p className="text-sm text-gray-400">No watched sessions yet.</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {watchedSessions.map((w) => (
              <Link key={w.id} to={`/sessions/${w.target_id}`} className="block p-4 bg-white rounded-lg border border-gray-200 hover:border-blue-400 transition-colors">
                <span className="inline-block px-2 py-0.5 rounded text-xs bg-green-100 text-green-700 mb-2">session</span>
                <div className="text-xs text-gray-500">ID: {w.target_id.slice(0, 8)}...</div>
              </Link>
            ))}
          </div>
        )}
      </section>

      <section>
        <h2 className="text-lg font-semibold text-gray-700 mb-3">Recent Conferences</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {conferences?.items?.map((c) => (
            <Link key={c.id} to={`/conferences/${c.id}`} className="block p-4 bg-white rounded-lg border border-gray-200 hover:border-blue-400 transition-colors">
              <div className="font-semibold text-gray-900">{c.acronym} {c.year}</div>
              <div className="text-sm text-gray-600 mt-1">{c.name}</div>
              {c.location && <div className="text-xs text-gray-400 mt-1">{c.location}</div>}
            </Link>
          ))}
        </div>
      </section>

      <section>
        <h2 className="text-lg font-semibold text-gray-700 mb-3">Recent Presentations</h2>
        <table className="w-full text-sm">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-3 py-2 text-left text-gray-600 font-medium">Title</th>
              <th className="px-3 py-2 text-left text-gray-600 font-medium">Type</th>
              <th className="px-3 py-2 text-left text-gray-600 font-medium">Presenter</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {recentPres?.items?.map((p) => (
              <tr key={p.id} className="hover:bg-gray-50">
                <td className="px-3 py-2"><Link to={`/presentations/${p.id}`} className="text-blue-600 hover:underline">{p.title}</Link></td>
                <td className="px-3 py-2 text-gray-600">{p.presentation_type || "-"}</td>
                <td className="px-3 py-2 text-gray-600">{p.presenter_name || "-"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <section>
        <h2 className="text-lg font-semibold text-gray-700 mb-3">AI Insights</h2>
        <div className="p-6 bg-gray-50 rounded-lg border border-gray-200">
          <p className="text-sm text-gray-500">AI-powered conference intelligence is coming soon. This panel will show trend analysis, entity extraction, and insight dashboards.</p>
        </div>
      </section>
    </div>
  );
}