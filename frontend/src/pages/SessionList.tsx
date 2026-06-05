import { useState, useEffect } from "react";
import { useParams, useLocation, Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { api, Conference, Session, Presentation } from "../api/client";
import PageShell from "../components/PageShell";
import PresentationTable from "../components/PresentationTable";

function getCongressId(conf: Conference): string {
  return conf.acronym.toLowerCase().replace(/\s+/g, "") + "-" + conf.year;
}

function fmtDate(value: string): string {
  return new Date(value + "T00:00:00").toLocaleDateString("en-US", {
    month: "short",
    day: "2-digit",
    year: "numeric",
  });
}

export default function SessionList() {
  const { congress } = useParams<{ congress: string }>();
  const location = useLocation();
  const querySession = new URLSearchParams(location.search).get("session");
  const [open, setOpen] = useState<string | null>(querySession);

  useEffect(() => {
    if (querySession) setOpen(querySession);
  }, [querySession]);

  const { data: confData } = useQuery({
    queryKey: ["conferences"],
    queryFn: () => api.conferences.list(),
  });

  const conferences: Conference[] = confData?.items ?? [];
  const conf = conferences.find((c) => getCongressId(c) === congress);

  const { data: sessionData } = useQuery({
    queryKey: ["sessions", conf?.id],
    queryFn: () => api.sessions.list(conf?.id),
    enabled: !!conf,
  });

  const { data: presData } = useQuery({
    queryKey: ["presentations", conf?.id],
    queryFn: () =>
      api.presentations.list({
        conference_id: conf?.id ?? "",
        limit: "200",
      }),
    enabled: !!conf,
  });

  const sessions: Session[] = sessionData?.items ?? [];
  const allPresentations: Presentation[] = presData?.items ?? [];

  return (
    <PageShell
      title="Sessions"
      subtitle="Sessions are sorted by time. Click a session row to expand all linked presentations and jump to presentation detail pages."
      congress={congress}
    >
      <div
        className="bg-surface-container-lowest border border-outline-variant rounded-2xl overflow-hidden shadow-sm divide-y divide-outline-variant"
      >
        {sessions.length === 0 ? (
          <div className="p-8 text-center text-on-surface-variant">
            <span className="material-symbols-outlined text-4xl mb-4 block">
              list_alt
            </span>
            <p className="text-lg font-semibold">No sessions found</p>
            <p className="text-sm mt-2">
              Import data for this conference to see sessions.
            </p>
          </div>
        ) : (
          sessions.map((s) => {
            const ps = allPresentations.filter(
              (p) => p.session_id === s.id
            );
            const isOpen = open === s.id;
            const dateStr = s.start_time
              ? s.start_time.split("T")[0]
              : "";
            const timeStr = s.start_time
              ? s.start_time.split("T")[1]?.slice(0, 5) ?? ""
              : "";
            const endStr = s.end_time
              ? s.end_time.split("T")[1]?.slice(0, 5) ?? ""
              : "";

            return (
              <div key={s.id}>
                <button
                  onClick={() => setOpen(isOpen ? null : s.id)}
                  className="w-full p-5 hover:bg-surface-container-low transition-colors text-left grid grid-cols-12 gap-4 items-center"
                >
                  <div className="col-span-12 md:col-span-2">
                    {dateStr && (
                      <p className="font-mono text-xs text-secondary font-bold">
                        {fmtDate(dateStr)}
                      </p>
                    )}
                    <p className="text-sm font-bold">
                      {timeStr} - {endStr}
                    </p>
                  </div>
                  <div className="col-span-12 md:col-span-2">
                    {s.session_type && (
                      <span
                        className="px-2 py-1 bg-primary/10 text-primary rounded-full text-[10px] font-bold uppercase"
                      >
                        {s.session_type}
                      </span>
                    )}
                  </div>
                  <div className="col-span-12 md:col-span-5">
                    <h3 className="text-lg font-bold text-on-surface hover:text-primary">
                      {s.title}
                    </h3>
                    <p className="text-sm text-on-surface-variant">
                      {s.track || ""}
                      {s.track && s.room ? " • " : ""}
                      {s.room || ""}
                    </p>
                  </div>
                  <div className="col-span-8 md:col-span-2 text-sm text-on-surface-variant">
                    {ps.length} presentations
                  </div>
                  <div className="col-span-4 md:col-span-1 text-right">
                    <span className="material-symbols-outlined text-primary">
                      {isOpen ? "expand_less" : "expand_more"}
                    </span>
                  </div>
                </button>
                {isOpen && (
                  <div className="px-5 pb-5 bg-surface-container-low">
                    <div
                      className="rounded-xl border border-outline-variant overflow-hidden bg-surface"
                    >
                      <PresentationTable rows={ps} congress={congress ?? ""} />
                    </div>
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>
    </PageShell>
  );
}