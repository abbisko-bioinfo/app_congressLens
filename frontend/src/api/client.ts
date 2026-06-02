const API_BASE = "/api";

export interface ApiResponse<T> {
  items?: T[];
  total?: number;
}

export interface Conference {
  id: string;
  acronym: string;
  name: string;
  year: number;
  location?: string;
  start_date?: string;
  end_date?: string;
  timezone?: string;
  website?: string;
  description?: string;
}

export interface Session {
  id: string;
  conference_id: string;
  title: string;
  session_type?: string;
  track?: string;
  room?: string;
  start_time?: string;
  end_time?: string;
  description?: string;
}

export interface Author {
  id: string;
  display_name: string;
  organization?: string;
  author_order?: number;
  is_first_author: boolean;
  is_presenter: boolean;
}

export interface Presentation {
  id: string;
  conference_id: string;
  session_id?: string;
  title: string;
  abstract_text?: string;
  abstract_html?: string;
  presentation_number?: string;
  abstract_number?: string;
  presentation_type?: string;
  presenter_name?: string;
  first_author_name?: string;
  institution_block?: string;
  doi?: string;
  start_time?: string;
  end_time?: string;
  has_abstract: boolean;
  has_slides: boolean;
  has_posters: boolean;
  has_videos: boolean;
  summary_status: string;
  authors: Author[];
}

export interface Comment {
  id: string;
  author?: string;
  body: string;
  created_at: string;
}

export interface Annotation {
  id: string;
  note: string;
  color?: string;
  page_number?: number;
  created_by?: string;
  created_at: string;
}

export interface Attachment {
  id: string;
  original_filename: string;
  content_type?: string;
  file_size?: number;
  preview_status: string;
  uploaded_at: string;
}

export interface WatchlistItem {
  id: string;
  target_type: string;
  target_id: string;
  note?: string;
}

async function fetchApi<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, init);
  if (!res.ok) throw new Error(`${res.status}: ${res.statusText}`);
  return res.json();
}

export const api = {
  conferences: {
    list: (skip = 0, limit = 50) => fetchApi<{ items: Conference[]; total: number }>(`/conferences?skip=${skip}&limit=${limit}`),
    get: (id: string) => fetchApi<Conference>(`/conferences/${id}`),
  },
  sessions: {
    list: (conferenceId?: string) => fetchApi<{ items: Session[]; total: number }>(`/sessions${conferenceId ? `?conference_id=${conferenceId}` : ""}`),
    get: (id: string) => fetchApi<Session>(`/sessions/${id}`),
  },
  presentations: {
    list: (params?: Record<string, string>) => {
      const qs = params ? "?" + new URLSearchParams(params).toString() : "";
      return fetchApi<{ items: Presentation[]; total: number }>(`/presentations${qs}`);
    },
    get: (id: string) => fetchApi<Presentation>(`/presentations/${id}`),
  },
  comments: {
    list: (presId: string) => fetchApi<Comment[]>(`/presentations/${presId}/comments`),
    create: (presId: string, data: { author?: string; body: string }) =>
      fetchApi<Comment>(`/presentations/${presId}/comments`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) }),
    delete: (id: string) => fetch(`/api/comments/${id}`, { method: "DELETE" }),
  },
  annotations: {
    list: (presId: string) => fetchApi<Annotation[]>(`/presentations/${presId}/annotations`),
    create: (presId: string, data: { note: string; color?: string }) =>
      fetchApi<Annotation>(`/presentations/${presId}/annotations`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) }),
    delete: (id: string) => fetch(`/api/annotations/${id}`, { method: "DELETE" }),
  },
  attachments: {
    list: (presId: string) => fetchApi<Attachment[]>(`/presentations/${presId}/attachments`),
    upload: (presId: string, file: File) => {
      const form = new FormData();
      form.append("file", file);
      return fetchApi<Attachment>(`/presentations/${presId}/attachments`, { method: "POST", body: form });
    },
    preview: (id: string) => fetchApi<{ url: string }>(`/presentations/attachments/${id}/preview`),
    download: (id: string) => fetchApi<{ url: string; filename: string }>(`/presentations/attachments/${id}/download`),
  },
  watchlist: {
    list: (userId?: string) => fetchApi<WatchlistItem[]>(`/watchlist${userId ? `?user_id=${userId}` : ""}`),
    add: (data: { target_type: string; target_id: string; note?: string }) =>
      fetchApi<WatchlistItem>("/watchlist", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) }),
    remove: (id: string) => fetch(`/api/watchlist/${id}`, { method: "DELETE" }),
  },
  calendar: {
    events: (userId?: string) => fetchApi<{ events: any[] }>(`/watchlist/calendar/events${userId ? `?user_id=${userId}` : ""}`),
  },
};