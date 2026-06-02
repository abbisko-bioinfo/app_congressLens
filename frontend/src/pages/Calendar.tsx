import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import { api } from "../api/client";

export default function Calendar() {
  const { data: eventsData } = useQuery({ queryKey: ["calendar"], queryFn: () => api.calendar.events() });

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Calendar</h1>
      {eventsData?.events?.length === 0 && <p className="text-gray-500">No watched items. Add items to your watchlist to see them here.</p>}
      <div className="space-y-4">
        {eventsData?.events?.map((ev: any, i: number) => (
          <div key={i} className="bg-white border border-gray-200 rounded-lg p-4">
            <div className="flex items-center gap-3">
              <span className="text-xs px-2 py-0.5 rounded bg-blue-100 text-blue-700">{ev.target_type}</span>
              <span className="font-semibold text-gray-900">{ev.title}</span>
            </div>
            <div className="mt-2 text-sm text-gray-500">
              {ev.start && <span>Start: {ev.start}</span>}
              {ev.end && <span className="ml-4">End: {ev.end}</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}