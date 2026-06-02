import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import { api } from "../api/client";

export default function Dashboard() {
  const { data: recentPres } = useQuery({ queryKey: ["presentations", "recent"], queryFn: () => api.presentations.list({ skip: "0", limit: "10" }) });
  const { data: conferences } = useQuery({ queryKey: ["conferences"], queryFn: () => api.conferences.list(0, 5) });

  return (
    <div className="p-6 space-y-8">
      <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>

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
    </div>
  );
}