import { useState } from "react";
import { useParams, Link } from "react-router-dom";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "../api/client";
import { useAuth } from "../hooks/useAuth";

function fmtDate(value: string): string {
  return new Date(value + "T00:00:00").toLocaleDateString("en-US", {
    month: "short",
    day: "2-digit",
    year: "numeric",
  });
}

export default function PresentationDetail() {
  const { congress, id } = useParams<{ congress: string; id: string }>();
  const qc = useQueryClient();
  const { isAuthenticated } = useAuth();
  const [commentBody, setCommentBody] = useState("");

  const { data: pres } = useQuery({
    queryKey: ["presentation", id],
    queryFn: () => api.presentations.get(id!),
  });

  const { data: comments } = useQuery({
    queryKey: ["comments", id],
    queryFn: () => api.comments.list(id!),
  });

  const { data: sessionData } = useQuery({
    queryKey: ["session", pres?.session_id],
    queryFn: () => api.sessions.get(pres!.session_id!),
    enabled: !!pres?.session_id,
  });

  const addComment = useMutation({
    mutationFn: () => api.comments.create(id!, { body: commentBody }),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["comments", id] });
      setCommentBody("");
    },
  });

  const toggleWatch = useMutation({
    mutationFn: async () => {
      if (pres?.is_watched) {
        const items = await api.watchlist.list();
        const match = items.find(
          (w) => w.target_type === "presentation" && w.target_id === id!
        );
        if (match) await api.watchlist.remove(match.id);
      } else {
        await api.watchlist.add({
          target_type: "presentation",
          target_id: id!,
        });
      }
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["presentation", id] }),
  });

  if (!pres)
    return <div className="p-6 text-on-surface-variant">Loading...</div>;

  const dateStr = pres.start_time ? pres.start_time.split("T")[0] : "";
  const timeStr = pres.start_time
    ? pres.start_time.split("T")[1]?.slice(0, 5) ?? ""
    : "";
  const sessionTitle = sessionData?.title ?? "Unassigned Session";

  return (
    <main className="flex-1 p-5 sm:p-8 lg:p-10 max-w-[1360px] mx-auto w-full">
      <div className="mb-6">
        <Link
          to={`/presentations/${congress}`}
          className="text-sm font-bold text-primary hover:underline flex items-center gap-1"
        >
          <span className="material-symbols-outlined text-sm">arrow_back</span>
          Back to presentations
        </Link>
      </div>

      <article
        className="bg-surface-container-lowest border border-outline-variant rounded-2xl overflow-hidden shadow-sm"
      >
        {/* Header */}
        <header
          className="p-5 sm:p-8 bg-surface-container-low border-b border-outline-variant"
        >
          <div className="flex items-start justify-between gap-4 mb-4">
            {pres.presentation_type && (
              <span
                className="px-3 py-1 bg-secondary/10 text-secondary rounded-full text-[10px] font-bold uppercase border border-secondary/20"
              >
                {pres.presentation_type} • {pres.presentation_number || pres.abstract_number || id}
              </span>
            )}
            <span
              className={`material-symbols-outlined text-3xl cursor-pointer ${
                pres.is_watched
                  ? "material-symbols-filled text-secondary"
                  : "text-outline"
              }`}
              onClick={() => {
                if (isAuthenticated) toggleWatch.mutate();
              }}
            >
              star
            </span>
          </div>
          <h1 className="text-2xl md:text-4xl font-extrabold text-primary mb-4">
            {pres.title}
          </h1>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-sm">
            <div>
              <p className="text-xs uppercase text-on-surface-variant font-bold">
                Presenter
              </p>
              <p className="font-bold">{pres.presenter_name || "-"}</p>
              {pres.institution_block && (
                <p className="text-on-surface-variant">{pres.institution_block}</p>
              )}
            </div>
            <div>
              <p className="text-xs uppercase text-on-surface-variant font-bold">
                Schedule
              </p>
              <p className="font-bold">
                {dateStr ? fmtDate(dateStr) : "-"} {timeStr}
              </p>
            </div>
            <div>
              <p className="text-xs uppercase text-on-surface-variant font-bold">
                Session
              </p>
              <p className="font-bold">{sessionTitle}</p>
            </div>
            <div>
              <p className="text-xs uppercase text-on-surface-variant font-bold">
                Topic
              </p>
              <p className="font-bold">
                {pres.topics.map((t) => t.name).join(", ") || "-"}
              </p>
            </div>
          </div>
        </header>

        {/* Content + Sidebar Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-0">
          {/* Main Content */}
          <section className="lg:col-span-2 p-5 sm:p-8 space-y-8">
            <div>
              <h2 className="text-xl font-bold text-primary mb-3">
                Full Text / Abstract
              </h2>
              {pres.abstract_html ? (
                <div
                  className="text-on-surface-variant leading-relaxed bg-surface-container-low rounded-xl p-5 border border-outline-variant"
                  dangerouslySetInnerHTML={{ __html: pres.abstract_html }}
                />
              ) : pres.abstract_text ? (
                <p
                  className="text-on-surface-variant leading-relaxed bg-surface-container-low rounded-xl p-5 border border-outline-variant"
                >
                  {pres.abstract_text}
                </p>
              ) : (
                <p
                  className="text-on-surface-variant bg-surface-container-low rounded-xl p-5 border border-outline-variant"
                >
                  No abstract available.
                </p>
              )}
            </div>

            {/* Intelligence Notes */}
            <div>
              <h2 className="text-xl font-bold text-primary mb-3">
                Structured Intelligence Notes
              </h2>
              <div className="grid md:grid-cols-2 gap-4">
                <div
                  className="p-5 rounded-xl bg-surface-container-low border border-outline-variant"
                >
                  <p className="text-xs uppercase text-secondary font-bold mb-2">
                    Evidence
                  </p>
                  <p className="text-sm text-on-surface-variant">
                    Clinical relevance, biomarker signal, target/pathway context
                    and competitive implication can be stored here.
                  </p>
                </div>
                <div
                  className="p-5 rounded-xl bg-surface-container-low border border-outline-variant"
                >
                  <p className="text-xs uppercase text-secondary font-bold mb-2">
                    Follow-up
                  </p>
                  <p className="text-sm text-on-surface-variant">
                    Add tasks for patent review, guideline mapping, company
                    tracking or expert interview.
                  </p>
                </div>
              </div>
            </div>

            {/* Authors */}
            {pres.authors?.length > 0 && (
              <div>
                <h2 className="text-xl font-bold text-primary mb-3">Authors</h2>
                <div className="space-y-1">
                  {pres.authors
                    .sort(
                      (a, b) => (a.author_order ?? 0) - (b.author_order ?? 0)
                    )
                    .map((author) => (
                      <div
                        key={author.id}
                        className="text-sm flex items-center gap-2"
                      >
                        <span className="text-on-surface">
                          {author.display_name}
                        </span>
                        {author.organization && (
                          <span className="text-on-surface-variant">
                            ({author.organization})
                          </span>
                        )}
                        {author.is_presenter && (
                          <span
                            className="text-xs bg-primary/10 text-primary px-1 rounded"
                          >
                            Presenter
                          </span>
                        )}
                      </div>
                    ))}
                </div>
              </div>
            )}
          </section>

          {/* Sidebar */}
          <aside
            className="p-5 sm:p-8 border-t lg:border-t-0 lg:border-l border-outline-variant bg-surface"
          >
            <h2 className="text-xl font-bold text-primary mb-4">
              Supporting Attachments
            </h2>
            <div className="space-y-3 mb-8">
              {pres.attachments.length > 0
                ? pres.attachments.map((file) => (
                    <div
                      key={file.id}
                      className="p-3 rounded-xl bg-surface-container-lowest border border-outline-variant flex items-center justify-between gap-3"
                    >
                      <span
                        className="flex items-center gap-2 text-sm font-semibold min-w-0 break-all"
                      >
                        <span className="material-symbols-outlined text-primary shrink-0">
                          attach_file
                        </span>
                        {file.original_filename}
                      </span>
                      <button
                        onClick={() =>
                          api.attachments
                            .download(file.id)
                            .then((r) => {
                              const a = document.createElement("a");
                              a.href = r.url;
                              a.download = r.filename;
                              a.click();
                            })
                        }
                        className="material-symbols-outlined text-on-surface-variant text-sm shrink-0"
                      >
                        download
                      </button>
                    </div>
                  ))
                : (
                  <p className="text-sm text-on-surface-variant">
                    No attachments.
                  </p>
                )}
            </div>

            <h2 className="text-xl font-bold text-primary mb-4">
              User Comments
            </h2>
            <div className="space-y-3">
              {(comments?.length ?? 0) > 0
                ? comments!.map((c) => (
                    <div
                      key={c.id}
                      className="p-4 rounded-xl bg-surface-container-low border border-outline-variant text-sm text-on-surface-variant"
                    >
                      {c.body}
                    </div>
                  ))
                : [
                    <div
                      key="empty"
                      className="p-4 rounded-xl bg-surface-container-low border border-outline-variant text-sm text-on-surface-variant"
                    >
                      No comments yet.
                    </div>,
                  ]}
            </div>
            <textarea
              className="mt-4 w-full rounded-xl border-outline-variant bg-surface text-sm"
              rows={4}
              placeholder="Add comment..."
              value={commentBody}
              onChange={(e) => setCommentBody(e.target.value)}
            />
            <button
              className="mt-3 w-full bg-primary text-on-primary rounded-xl py-2.5 text-sm font-bold"
              onClick={() => addComment.mutate()}
              disabled={!commentBody}
            >
              Save Comment
            </button>
          </aside>
        </div>
      </article>
    </main>
  );
}