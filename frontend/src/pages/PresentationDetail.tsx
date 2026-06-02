import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useParams } from "react-router-dom";
import { api } from "../api/client";

export default function PresentationDetail() {
  const { id } = useParams<{ id: string }>();
  const qc = useQueryClient();
  const [commentBody, setCommentBody] = useState("");
  const [commentAuthor, setCommentAuthor] = useState("");

  const { data: pres } = useQuery({ queryKey: ["presentation", id], queryFn: () => api.presentations.get(id!) });
  const { data: comments } = useQuery({ queryKey: ["comments", id], queryFn: () => api.comments.list(id!) });
  const { data: attachments } = useQuery({ queryKey: ["attachments", id], queryFn: () => api.attachments.list(id!) });

  const addComment = useMutation({
    mutationFn: () => api.comments.create(id!, { body: commentBody, author: commentAuthor }),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ["comments", id] }); setCommentBody(""); setCommentAuthor(""); },
  });

  if (!pres) return <div className="p-6 text-gray-500">Loading...</div>;

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">{pres.title}</h1>
        <div className="mt-2 flex gap-4 text-sm text-gray-600">
          {pres.presentation_number && <span># {pres.presentation_number}</span>}
          {pres.abstract_number && <span>Abstract: {pres.abstract_number}</span>}
          {pres.presentation_type && <span>Type: {pres.presentation_type}</span>}
          {pres.doi && <a href={`https://doi.org/${pres.doi}`} className="text-blue-600 hover:underline">DOI</a>}
        </div>
      </div>

      {pres.authors?.length > 0 && (
        <section>
          <h2 className="text-lg font-semibold text-gray-700 mb-2">Authors</h2>
          <div className="space-y-1">
            {pres.authors.sort((a, b) => (a.author_order ?? 0) - (b.author_order ?? 0)).map((author) => (
              <div key={author.id} className="text-sm flex items-center gap-2">
                <span className="text-gray-900">{author.display_name}</span>
                {author.organization && <span className="text-gray-500">({author.organization})</span>}
                {author.is_presenter && <span className="text-xs bg-blue-100 text-blue-700 px-1 rounded">Presenter</span>}
                {author.is_first_author && <span className="text-xs bg-green-100 text-green-700 px-1 rounded">First Author</span>}
              </div>
            ))}
          </div>
        </section>
      )}

      {pres.abstract_html && (
        <section>
          <h2 className="text-lg font-semibold text-gray-700 mb-2">Abstract</h2>
          <div className="prose prose-sm max-w-none text-gray-700" dangerouslySetInnerHTML={{ __html: pres.abstract_html }} />
        </section>
      )}

      {pres.abstract_text && !pres.abstract_html && (
        <section>
          <h2 className="text-lg font-semibold text-gray-700 mb-2">Abstract</h2>
          <p className="text-sm text-gray-700">{pres.abstract_text}</p>
        </section>
      )}

      {attachments?.length > 0 && (
        <section>
          <h2 className="text-lg font-semibold text-gray-700 mb-2">Attachments</h2>
          <div className="space-y-2">
            {attachments.map((att) => (
              <div key={att.id} className="flex items-center gap-3 text-sm">
                <span className="text-gray-900">{att.original_filename}</span>
                <span className="text-gray-500">{att.content_type}</span>
                <span className="text-xs px-2 py-0.5 rounded bg-gray-100 text-gray-600">{att.preview_status}</span>
              </div>
            ))}
          </div>
        </section>
      )}

      <section>
        <h2 className="text-lg font-semibold text-gray-700 mb-2">Comments</h2>
        <div className="space-y-3">
          {comments?.map((c) => (
            <div key={c.id} className="bg-white border border-gray-200 rounded-md p-3">
              <div className="text-xs text-gray-400">{c.author || "Anonymous"} - {new Date(c.created_at).toLocaleDateString()}</div>
              <p className="text-sm text-gray-700 mt-1">{c.body}</p>
            </div>
          ))}
        </div>
        <div className="mt-3 flex gap-2">
          <input value={commentAuthor} onChange={(e) => setCommentAuthor(e.target.value)} placeholder="Author" className="px-2 py-1 border rounded text-sm w-24" />
          <input value={commentBody} onChange={(e) => setCommentBody(e.target.value)} placeholder="Add a comment..." className="px-2 py-1 border rounded text-sm flex-1" />
          <button onClick={() => addComment.mutate()} disabled={!commentBody} className="px-3 py-1 bg-blue-600 text-white rounded text-sm hover:bg-blue-700 disabled:bg-gray-300">Add</button>
        </div>
      </section>

      {pres.summary_status !== "none" && (
        <section>
          <h2 className="text-lg font-semibold text-gray-700 mb-2">AI Summary</h2>
          <div className="text-sm text-gray-500 italic">AI summary placeholder (status: {pres.summary_status})</div>
        </section>
      )}
    </div>
  );
}