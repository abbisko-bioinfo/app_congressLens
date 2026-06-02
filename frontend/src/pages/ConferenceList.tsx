import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import { api } from "../api/client";

export default function ConferenceList() {
  const { data } = useQuery({ queryKey: ["conferences"], queryFn: () => api.conferences.list(0, 200) });

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Conferences</h1>
      <table className="w-full text-sm">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-3 py-2 text-left text-gray-600 font-medium">Acronym</th>
            <th className="px-3 py-2 text-left text-gray-600 font-medium">Name</th>
            <th className="px-3 py-2 text-left text-gray-600 font-medium">Year</th>
            <th className="px-3 py-2 text-left text-gray-600 font-medium">Location</th>
            <th className="px-3 py-2 text-left text-gray-600 font-medium">Dates</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-100">
          {data?.items?.map((c) => (
            <tr key={c.id} className="hover:bg-gray-50">
              <td className="px-3 py-2"><Link to={`/conferences/${c.id}`} className="text-blue-600 hover:underline font-semibold">{c.acronym}</Link></td>
              <td className="px-3 py-2">{c.name}</td>
              <td className="px-3 py-2">{c.year}</td>
              <td className="px-3 py-2 text-gray-600">{c.location || "-"}</td>
              <td className="px-3 py-2 text-gray-600">{c.start_date ? `${c.start_date} - ${c.end_date}` : "-"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}