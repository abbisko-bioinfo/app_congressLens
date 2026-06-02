import { useQuery } from "@tanstack/react-query";
import { Link, useParams } from "react-router-dom";
import { api } from "../api/client";

export default function SessionDetail() {
  const { id } = useParams<{ id: string }>();
  const { data: session } = useQuery({ queryKey: ["session", id], queryFn: () => api.sessions.get(id!) });
  const { data: presentations } = useQuery({ queryKey: ["presentations", "session", id], queryFn: () => api.presentations.list({ session_id: id!, skip: "0", limit: "100" }), enabled: !!id });

  if (!session) return <div className="p-6 text-gray-500">Loading...</div>;

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">{session.title}</h1>
        <div className="mt-2 text-sm text-gray-600 space-x-4">
          {session.session_type && <span>Type: {session.session_type}</span>}
          {session.room && <span>Room: {session.room}</span>}
          {session.start_time && <span>Time: {session.start_time}</span>}
        </div>
        {session.description && <p className="mt-3 text-gray-600">{session.description}</p>}
      </div>

      <section>
        <h2 className="text-lg font-semibold text-gray-700 mb-3">Presentations</h2>
        <table className="w-full text-sm">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-3 py-2 text-left text-gray-600 font-medium">#</th>
              <th className="px-3 py-2 text-left text-gray-600 font-medium">Title</th>
              <th className="px-3 py-2 text-left text-gray-600 font-medium">Presenter</th>
              <th className="px-3 py-2 text-left text-gray-600 font-medium">Type</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {presentations?.items?.map((p) => (
              <tr key={p.id} className="hover:bg-gray-50">
                <td className="px-3 py-2 text-gray-400">{p.position_in_session || "-"}</td>
                <td className="px-3 py-2"><Link to={`/presentations/${p.id}`} className="text-blue-600 hover:underline">{p.title}</Link></td>
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