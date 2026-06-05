import { Link } from "react-router-dom";
import { Presentation } from "../api/client";

function fmtDate(value: string): string {
  return new Date(value + "T00:00:00").toLocaleDateString("en-US", {
    month: "short",
    day: "2-digit",
    year: "numeric",
  });
}

interface PresentationTableProps {
  rows: Presentation[];
  congress: string;
  showConference?: boolean;
}

export default function PresentationTable({
  rows,
  congress,
  showConference = false,
}: PresentationTableProps) {
  return (
    <div
      className="bg-surface-container-lowest border border-outline-variant rounded-2xl overflow-hidden shadow-sm"
    >
      <div className="overflow-x-auto custom-scrollbar max-h-[calc(100vh-260px)]">
        <table className="w-full min-w-[1060px] text-left table-sticky">
          <thead className="bg-surface-container-low border-b border-outline-variant">
            <tr className="text-xs uppercase text-on-surface-variant font-label">
              <th className="px-4 py-3 bg-surface-container-low">Star</th>
              {showConference && (
                <th className="px-4 py-3 bg-surface-container-low">
                  Congress
                </th>
              )}
              <th className="px-4 py-3 bg-surface-container-low">Time</th>
              <th className="px-4 py-3 bg-surface-container-low">Type</th>
              <th className="px-4 py-3 bg-surface-container-low">Title</th>
              <th className="px-4 py-3 bg-surface-container-low">Presenter</th>
              <th className="px-4 py-3 bg-surface-container-low">Topic</th>
              <th className="px-4 py-3 bg-surface-container-low">Files</th>
              <th className="px-4 py-3 bg-surface-container-low">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-outline-variant">
            {rows.map((p) => {
              const dateStr = p.start_time
                ? p.start_time.split("T")[0]
                : "";
              const timeStr = p.start_time
                ? p.start_time.split("T")[1]?.slice(0, 5) ?? ""
                : "";
              const topicNames = p.topics
                .map((t) => t.name)
                .join(", ");
              const fileCount = p.attachments.length;

              return (
                <tr
                  key={p.id}
                  className="hover:bg-surface-container-low transition-colors"
                >
                  <td className="px-4 py-4">
                    <span
                      className={`material-symbols-outlined ${
                        p.is_watched
                          ? "material-symbols-filled text-secondary"
                          : "text-outline"
                      }`}
                    >
                      star
                    </span>
                  </td>
                  {showConference && (
                    <td className="px-4 py-4 font-mono text-xs text-primary font-bold">
                      {congress}
                    </td>
                  )}
                  <td className="px-4 py-4 whitespace-nowrap">
                    {dateStr && (
                      <div className="text-sm font-bold">
                        {fmtDate(dateStr)}
                      </div>
                    )}
                    {timeStr && (
                      <div className="text-xs text-on-surface-variant">
                        {timeStr}
                      </div>
                    )}
                  </td>
                  <td className="px-4 py-4">
                    {p.presentation_type && (
                      <span
                        className="px-2 py-1 bg-secondary/10 text-secondary rounded-full text-[10px] font-bold uppercase"
                      >
                        {p.presentation_type}
                      </span>
                    )}
                  </td>
                  <td className="px-4 py-4 max-w-md">
                    <Link
                      to={`/presentations/${congress}/${p.id}`}
                      className="font-bold text-on-surface hover:text-primary leading-snug"
                    >
                      {p.title}
                    </Link>
                    {p.abstract_text && (
                      <p className="text-xs text-on-surface-variant mt-1 line-clamp-1">
                        {p.abstract_text}
                      </p>
                    )}
                  </td>
                  <td className="px-4 py-4">
                    {p.presenter_name && (
                      <div className="font-semibold text-sm">
                        {p.presenter_name}
                      </div>
                    )}
                    {p.institution_block && (
                      <div className="text-xs text-on-surface-variant">
                        {p.institution_block}
                      </div>
                    )}
                  </td>
                  <td className="px-4 py-4 text-sm text-on-surface-variant">
                    {topicNames || "-"}
                  </td>
                  <td className="px-4 py-4 text-sm font-mono text-on-surface-variant">
                    {fileCount}
                  </td>
                  <td className="px-4 py-4">
                    <Link
                      to={`/presentations/${congress}/${p.id}`}
                      className="inline-flex items-center gap-1 px-3 py-1.5 rounded-lg bg-primary text-on-primary text-xs font-bold hover:bg-primary/90"
                    >
                      <span className="material-symbols-outlined text-sm">
                        open_in_new
                      </span>
                      Detail
                    </Link>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}