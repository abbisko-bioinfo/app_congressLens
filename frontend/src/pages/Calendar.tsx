import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import { api, CalendarEvent } from "../api/client";

const TYPE_COLORS: Record<string, { bg: string; text: string; border: string }> = {
  conference: { bg: "bg-purple-100", text: "text-purple-700", border: "border-purple-300" },
  session: { bg: "bg-green-100", text: "text-green-700", border: "border-green-300" },
  presentation: { bg: "bg-blue-100", text: "text-blue-700", border: "border-blue-300" },
};

function getMonthGrid(events: CalendarEvent[]) {
  const months: Record<string, CalendarEvent[]> = {};
  for (const ev of events) {
    const key = ev.start ? ev.start.slice(0, 7) : "unknown";
    if (!months[key]) months[key] = [];
    months[key].push(ev);
  }
  return months;
}

function formatDate(dateStr?: string) {
  if (!dateStr) return "-";
  try {
    return new Date(dateStr).toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" });
  } catch {
    return dateStr;
  }
}

export default function Calendar() {
  const { data: eventsData } = useQuery({ queryKey: ["calendar"], queryFn: () => api.calendar.events() });

  const events = eventsData?.events || [];
  const months = getMonthGrid(events);

  if (events.length === 0) {
    return (
      <div className="p-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">Calendar</h1>
        <p className="text-gray-500">No watched items. Add items to your watchlist to see them here.</p>
      </div>
    );
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Calendar</h1>

      <div className="flex gap-4 mb-6">
        <div className="flex items-center gap-2"><span className="w-3 h-3 rounded-full bg-purple-400" /> Conference</div>
        <div className="flex items-center gap-2"><span className="w-3 h-3 rounded-full bg-green-400" /> Session</div>
        <div className="flex items-center gap-2"><span className="w-3 h-3 rounded-full bg-blue-400" /> Presentation</div>
      </div>

      <div className="space-y-8">
        {Object.entries(months).sort().map(([monthKey, monthEvents]) => (
          <div key={monthKey}>
            <h2 className="text-lg font-semibold text-gray-800 mb-3">{monthKey}</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3">
              {monthEvents.map((ev) => {
                const colors = TYPE_COLORS[ev.target_type] || TYPE_COLORS.presentation;
                const linkPath = ev.target_type === "conference" ? `/conferences/${ev.target_id}`
                  : ev.target_type === "session" ? `/sessions/${ev.target_id}`
                  : `/presentations/${ev.target_id}`;
                return (
                  <Link key={ev.watchlist_id} to={linkPath} className={`block p-3 rounded-lg border ${colors.border} hover:shadow-md transition-shadow`}>
                    <div className="flex items-center gap-2 mb-1">
                      <span className={`text-xs px-2 py-0.5 rounded ${colors.bg} ${colors.text}`}>{ev.target_type}</span>
                      <span className="font-medium text-gray-900 text-sm truncate">{ev.title || ev.target_id.slice(0, 8)}</span>
                    </div>
                    <div className="text-xs text-gray-500">
                      {formatDate(ev.start)} - {formatDate(ev.end)}
                    </div>
                  </Link>
                );
              })}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}