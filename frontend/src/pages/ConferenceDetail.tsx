import { useQuery } from "@tanstack/react-query";
import { Link, useParams } from "react-router-dom";
import { api } from "../api/client";

export default function ConferenceDetail() {
  const { id } = useParams<{ id: string }>();
  const { data: conf } = useQuery({ queryKey: ["conference", id], queryFn: () => api.conferences.get(id!) });
  const { data: sessions } = useQuery({ queryKey: ["sessions", id], queryFn: () => api.sessions.list(id!), enabled: !!id });
  const { data: presentations } = useQuery({ queryKey: ["presentations", id], queryFn: () => api.presentations.list({ conference_id: id!, skip: "0", limit: "50" }), enabled: !!id });

  if (!conf) return <div className="p-6 text-gray-500">Loading...</div>;

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">{conf.acronym} {conf.year}</h1>
        <p className="text-gray-600 mt-1">{conf.name}</p>
        {conf.location && <p className="text-sm text-gray-400">{conf.location}</p>}
      </div>

      <section>
        <h2 className="text-lg font-semibold text-gray-700 mb-3">Sessions</h2>
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
      </section>

      <section>
        <h2 className="text-lg font-semibold text-gray-700 mb-3">Presentations</h2>
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
      </section>
    </div>
  );
}