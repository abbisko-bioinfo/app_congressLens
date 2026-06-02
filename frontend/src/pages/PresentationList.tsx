import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import { api } from "../api/client";

export default function PresentationList() {
  const [search, setSearch] = useState("");
  const [confFilter, setConfFilter] = useState("");
  const [typeFilter, setTypeFilter] = useState("");

  const { data: conferences } = useQuery({ queryKey: ["conferences"], queryFn: () => api.conferences.list(0, 200) });
  const params: Record<string, string> = {};
  if (search) params.query = search;
  if (confFilter) params.conference_id = confFilter;
  if (typeFilter) params.presentation_type = typeFilter;

  const { data } = useQuery({ queryKey: ["presentations", params], queryFn: () => api.presentations.list(params) });

  return (
    <div className="p-6 space-y-4">
      <h1 className="text-2xl font-bold text-gray-900">Presentations</h1>

      <div className="flex gap-4">
        <input
          type="text"
          placeholder="Search..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
        />
        <select value={confFilter} onChange={(e) => setConfFilter(e.target.value)} className="px-3 py-2 border border-gray-300 rounded-md text-sm">
          <option value="">All conferences</option>
          {conferences?.items?.map((c) => <option key={c.id} value={c.id}>{c.acronym} {c.year}</option>)}
        </select>
        <select value={typeFilter} onChange={(e) => setTypeFilter(e.target.value)} className="px-3 py-2 border border-gray-300 rounded-md text-sm">
          <option value="">All types</option>
          <option value="Oral">Oral</option>
          <option value="Poster">Poster</option>
          <option value="Plenary">Plenary</option>
        </select>
      </div>

      <table className="w-full text-sm">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-3 py-2 text-left text-gray-600 font-medium">Title</th>
            <th className="px-3 py-2 text-left text-gray-600 font-medium">Presenter</th>
            <th className="px-3 py-2 text-left text-gray-600 font-medium">First Author</th>
            <th className="px-3 py-2 text-left text-gray-600 font-medium">Type</th>
            <th className="px-3 py-2 text-left text-gray-600 font-medium">Abstract#</th>
            <th className="px-3 py-2 text-left text-gray-600 font-medium">Attachments</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-100">
          {data?.items?.map((p) => (
            <tr key={p.id} className="hover:bg-gray-50">
              <td className="px-3 py-2"><Link to={`/presentations/${p.id}`} className="text-blue-600 hover:underline">{p.title}</Link></td>
              <td className="px-3 py-2 text-gray-600">{p.presenter_name || "-"}</td>
              <td className="px-3 py-2 text-gray-600">{p.first_author_name || "-"}</td>
              <td className="px-3 py-2 text-gray-600">{p.presentation_type || "-"}</td>
              <td className="px-3 py-2 text-gray-600">{p.abstract_number || "-"}</td>
              <td className="px-3 py-2 text-gray-600">{[p.has_slides && "Slides", p.has_posters && "Poster", p.has_videos && "Video"].filter(Boolean).join(", ") || "-"}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <div className="text-sm text-gray-500">{data?.total ?? 0} presentations</div>
    </div>
  );
}