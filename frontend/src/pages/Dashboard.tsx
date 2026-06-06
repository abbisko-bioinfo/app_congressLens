import { useState, Fragment } from "react";
import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { api } from "../api/client";
import type { Conference, Session } from "../api/client";
import ConferenceBadge from "../components/ConferenceBadge";

function fmtDate(value: string): string {
  return new Date(value + "T00:00:00").toLocaleDateString("en-US", {
    month: "short",
    day: "2-digit",
    year: "numeric",
  });
}

function getCongressId(conf: Conference): string {
  return conf.acronym.toLowerCase().replace(/\s+/g, "") + "-" + conf.year;
}

function getCongressCode(conf: Conference): string {
  return `${conf.acronym}${conf.year}`;
}

export default function Dashboard() {
  const { data: confData } = useQuery({
    queryKey: ["conferences"],
    queryFn: () => api.conferences.list(),
  });

  const conferences: Conference[] = confData?.items ?? [];
  const [selected, setSelected] = useState<string>(
    conferences[0] ? getCongressId(conferences[0]) : ""
  );

  // Update selected when conferences load
  if (conferences.length > 0 && !selected) {
    setSelected(getCongressId(conferences[0]));
  }

  const conf = conferences.find((c) => getCongressId(c) === selected);

  const { data: sessionData } = useQuery({
    queryKey: ["sessions", conf?.id],
    queryFn: () => api.sessions.list(conf?.id),
    enabled: !!conf,
  });

  const confSessions: Session[] = sessionData?.items ?? [];

  // Group dates from sessions only.
  const groupedDays = [
    ...new Set([
      ...confSessions
        .filter((s) => s.start_time)
        .map((s) => s.start_time!.split("T")[0]),
    ]),
  ].sort();

  const timeSlots = ["08:00", "10:00", "13:00", "15:00"];

  return (
    <main className="min-h-[calc(100vh-112px)] bg-background p-5 sm:p-8 lg:p-10 max-w-[1360px] mx-auto w-full">
      <div className="space-y-8 pt-4">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-4">
          <div>
            <h3 className="text-3xl md:text-4xl font-bold text-brand-blue">
              Conference Workspace
            </h3>
            <p className="text-on-surface-variant mt-2">
              Left side lists imported congresses by date; right side shows the
              selected congress calendar.
            </p>
          </div>
        </div>

        <div className="grid grid-cols-12 gap-6">
          {/* Conference Cards */}
          <aside
            className="col-span-12 lg:col-span-4 bg-surface-container-lowest border border-outline-variant rounded-2xl p-6 shadow-sm"
          >
            <div className="space-y-4">
              {conferences.map((c) => (
                <button
                  key={c.id}
                  onClick={() => setSelected(getCongressId(c))}
                  className={`w-full text-left p-5 rounded-xl border transition-all group ${
                    selected === getCongressId(c)
                      ? "bg-primary/5 border-primary shadow-sm"
                      : "bg-surface-container-low border-outline-variant hover:border-primary/40"
                  }`}
                >
                  <div className="flex justify-between items-start gap-3 mb-3">
                    <div>
                      <p className="text-[12px] text-secondary uppercase font-bold">
                        {c.start_date && c.end_date
                          ? `${fmtDate(c.start_date)} – ${fmtDate(c.end_date)}`
                          : ""}
                      </p>
                      <h5
                        className="text-xl font-extrabold text-on-surface group-hover:text-primary leading-snug"
                      >
                        {getCongressCode(c)}
                      </h5>
                    </div>
                    <ConferenceBadge conf={c} />
                  </div>
                  <p className="text-sm font-medium text-on-surface mt-1 line-clamp-2">
                    {c.name}
                  </p>
                  <div
                    className="flex items-center gap-4 mt-4 text-xs text-on-surface-variant"
                  >
                    {c.location && (
                      <span className="flex items-center gap-1">
                        <span className="material-symbols-outlined text-sm">
                          location_on
                        </span>
                        {c.location}
                      </span>
                    )}
                    <span>{confSessions.length} sessions</span>
                  </div>
                </button>
              ))}
            </div>
          </aside>

          {/* Calendar Grid */}
          <section
            className="col-span-12 lg:col-span-8 bg-surface-container-lowest border border-outline-variant rounded-2xl overflow-hidden shadow-sm"
          >
            {conf ? (
              <>
                <div
                  className="p-6 border-b border-outline-variant bg-surface-container-low flex flex-col md:flex-row md:items-center md:justify-between gap-4"
                >
                  <div>
                    <div className="flex items-center gap-3 mb-1">
                      <span className="material-symbols-outlined text-brand-blue">
                        calendar_month
                      </span>
                      <h4 className="text-xl font-bold text-brand-blue">
                        {getCongressCode(conf)}
                      </h4>
                    </div>
                    <p className="text-sm text-on-surface-variant">
                      {conf.name}
                      {conf.description ? ` • ${conf.description}` : ""}
                    </p>
                    <p className="text-sm text-on-surface-variant">
                      {conf.start_date && conf.end_date
                        ? `${fmtDate(conf.start_date)} – ${fmtDate(conf.end_date)}`
                        : ""}
                      {conf.location ? ` • ${conf.location}` : ""}
                    </p>
                  </div>
                  <div className="flex gap-2">
                    <Link
                      to={`/session/${getCongressId(conf)}`}
                      className="px-4 py-2 bg-primary text-on-primary rounded-xl text-sm font-bold hover:bg-primary/90"
                    >
                      Sessions
                    </Link>
                    <Link
                      to={`/presentations/${getCongressId(conf)}`}
                      className="px-4 py-2 bg-primary text-on-primary rounded-xl text-sm font-bold hover:bg-primary/90"
                    >
                      Presentations
                    </Link>
                  </div>
                </div>
                <div className="overflow-x-auto custom-scrollbar">
                  <div className="min-w-[880px]">
                    <div
                      className="calendar-grid bg-surface-container-low border-b border-outline-variant"
                    >
                      <div className="h-12"></div>
                      {groupedDays.slice(0, 5).map((day) => (
                        <div
                          key={day}
                          className="h-12 flex items-center justify-center border-r border-outline-variant"
                        >
                          <span className="font-label text-xs text-on-surface-variant uppercase">
                            {fmtDate(day).replace(", 2026", "").replace(", 2025", "")}
                          </span>
                        </div>
                      ))}
                    </div>
                    <div className="calendar-grid bg-surface-container-lowest">
                      {timeSlots.map((slot) => (
                        <Fragment key={slot}>
                          <div
                            className="calendar-cell flex justify-end pr-4 pt-3 text-on-surface-variant font-label text-xs font-medium"
                          >
                            {slot}
                          </div>
                          {groupedDays.slice(0, 5).map((day) => {
                            const hitS = confSessions.find(
                              (s) =>
                                s.start_time &&
                                s.start_time.startsWith(day) &&
                                s.start_time.includes(slot.slice(0, 2))
                            );
                            return (
                              <div
                                key={day + slot}
                                className="calendar-cell relative p-2 min-h-[86px]"
                              >
                                {hitS && (
                                  <Link
                                    to={`/session/${selected}?session=${hitS.id}`}
                                    className="block bg-primary/5 border-l-4 border-primary p-2.5 rounded-lg hover:bg-primary/10"
                                  >
                                    <p className="text-[10px] font-bold text-primary uppercase">
                                      SESSION
                                    </p>
                                    <p className="text-xs font-bold line-clamp-2">
                                      {hitS.title}
                                    </p>
                                  </Link>
                                )}
                              </div>
                            );
                          })}
                        </Fragment>
                      ))}
                    </div>
                  </div>
                </div>
              </>
            ) : (
              <div className="p-12 text-center text-on-surface-variant">
                <span className="material-symbols-outlined text-4xl mb-4 block">
                  calendar_month
                </span>
                <p className="text-lg font-semibold">No conferences imported yet</p>
                <p className="text-sm mt-2">Import a congress to see the calendar grid.</p>
              </div>
            )}
          </section>
        </div>
      </div>
    </main>
  );
}
