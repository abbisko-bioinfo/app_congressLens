import { Link, useNavigate } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { api, Conference } from "../api/client";

interface PageShellProps {
  title: string;
  subtitle: string;
  congress?: string;
  children: React.ReactNode;
}

export default function PageShell({
  title,
  subtitle,
  congress,
  children,
}: PageShellProps) {
  const navigate = useNavigate();

  const { data: confData } = useQuery({
    queryKey: ["conferences"],
    queryFn: () => api.conferences.list(),
  });

  const conferences: Conference[] = confData?.items ?? [];
  const conf = congress
    ? conferences.find(
        (c) =>
          c.acronym.toLowerCase().replace(/\s+/g, "") +
            "-" +
            c.year ===
          congress
      ) || conferences[0]
    : conferences[0];

  const handleCongressChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const routePrefix = title.toLowerCase().startsWith("session")
      ? "/session"
      : "/presentations";
    navigate(`${routePrefix}/${e.target.value}`);
  };

  return (
    <main className="flex-1 p-5 sm:p-8 lg:p-10 max-w-[1360px] mx-auto w-full">
      <header className="mb-8 flex flex-col md:flex-row md:items-end md:justify-between gap-4">
        <div className="min-w-0">
          {conf && (
            <p className="text-[12px] text-brand-magenta uppercase mb-1 font-bold">
              {conf.name}
            </p>
          )}
          <h1 className="text-3xl md:text-4xl font-bold text-primary">
            {title}
          </h1>
          <p className="text-on-surface-variant mt-2 max-w-3xl">{subtitle}</p>
        </div>
        {congress && conferences.length > 0 && (
          <select
            value={congress}
            onChange={handleCongressChange}
            className="rounded-xl border-outline-variant bg-surface-container-lowest text-sm font-semibold w-full md:w-auto"
          >
            {conferences.map((c) => {
              const congressId =
                c.acronym.toLowerCase().replace(/\s+/g, "") + "-" + c.year;
              return (
                <option key={c.id} value={congressId}>
                  {c.name}
                </option>
              );
            })}
          </select>
        )}
      </header>
      {children}
    </main>
  );
}