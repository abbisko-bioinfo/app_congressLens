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
  normalized_name?: string;
  role?: string;
  organization?: string;
  author_order?: number;
  city?: string;
  country?: string;
  is_first_author: boolean;
  is_presenter: boolean;
}

export interface Topic {
  id: string;
  name: string;
  normalized_name: string;
  type: string;
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
  poster_board_number?: string;
  presentation_type?: string;
  activity?: string;
  status?: string;
  position_in_session?: number;
  start_time?: string;
  end_time?: string;
  timezone?: string;
  presenter_name?: string;
  first_author_name?: string;
  author_block_html?: string;
  institution_block?: string;
  disclosure_block_html?: string;
  funding_sources?: string[];
  additional_funding_source?: string;
  doi?: string;
  journal_citation?: string;
  clinical_trial_registry_number?: string;
  source_url?: string;
  disclosure_url?: string;
  has_abstract: boolean;
  has_slides: boolean;
  has_posters: boolean;
  has_videos: boolean;
  summary_status: string;
  authors: Author[];
  attachments: Attachment[];
  topics: Topic[];
  comments: Comment[];
  annotations: Annotation[];
  is_watched: boolean;
}

export interface Comment {
  id: string;
  presentation_id: string;
  author?: string;
  body: string;
  created_at: string;
  updated_at: string;
}

export interface Annotation {
  id: string;
  presentation_id: string;
  attachment_id?: string;
  selected_text?: string;
  note: string;
  color?: string;
  page_number?: number;
  anchor_data?: Record<string, unknown>;
  created_by?: string;
  created_at: string;
  updated_at: string;
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
  user_id?: string;
  target_type: string;
  target_id: string;
  note?: string;
  created_at: string;
}

export interface CalendarEvent {
  watchlist_id: string;
  target_type: string;
  target_id: string;
  title?: string;
  start?: string;
  end?: string;
}

async function fetchApi<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, init);
  if (!res.ok) throw new Error(`${res.status}: ${res.statusText}`);
  return res.json();
}

async function deleteApi(path: string): Promise<void> {
  const res = await fetch(`${API_BASE}${path}`, { method: "DELETE" });
  if (!res.ok && res.status !== 204) throw new Error(`${res.status}: ${res.statusText}`);
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
    get: (id: string, userId?: string) => fetchApi<Presentation>(`/presentations/${id}${userId ? `?user_id=${userId}` : ""}`),
    authors: (id: string) => fetchApi<Author[]>(`/presentations/${id}/authors`),
  },
  comments: {
    list: (presId: string) => fetchApi<Comment[]>(`/presentations/${presId}/comments`),
    create: (presId: string, data: { author?: string; body: string }) =>
      fetchApi<Comment>(`/presentations/${presId}/comments`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) }),
    update: (id: string, data: { author?: string; body?: string }) =>
      fetchApi<Comment>(`/comments/${id}`, { method: "PATCH", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) }),
    delete: (id: string) => deleteApi(`/comments/${id}`),
  },
  annotations: {
    list: (presId: string) => fetchApi<Annotation[]>(`/presentations/${presId}/annotations`),
    create: (presId: string, data: { note: string; color?: string }) =>
      fetchApi<Annotation>(`/presentations/${presId}/annotations`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) }),
    update: (id: string, data: { note?: string; color?: string }) =>
      fetchApi<Annotation>(`/annotations/${id}`, { method: "PATCH", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) }),
    delete: (id: string) => deleteApi(`/annotations/${id}`),
  },
  attachments: {
    list: (presId: string) => fetchApi<Attachment[]>(`/presentations/${presId}/attachments`),
    upload: (presId: string, file: File) => {
      const form = new FormData();
      form.append("file", file);
      return fetchApi<Attachment>(`/presentations/${presId}/attachments`, { method: "POST", body: form });
    },
    preview: (id: string) => fetchApi<{ url: string }>(`/attachments/${id}/preview`),
    download: (id: string) => fetchApi<{ url: string; filename: string; content_type?: string }>(`/attachments/${id}/download`),
    delete: (id: string) => deleteApi(`/attachments/${id}`),
  },
  watchlist: {
    list: (userId?: string) => fetchApi<WatchlistItem[]>(`/watchlist${userId ? `?user_id=${userId}` : ""}`),
    add: (data: { user_id?: string; target_type: string; target_id: string; note?: string }) =>
      fetchApi<WatchlistItem>("/watchlist", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) }),
    remove: (id: string) => deleteApi(`/watchlist/${id}`),
  },
  calendar: {
    events: (userId?: string) => fetchApi<{ events: CalendarEvent[] }>(`/calendar/events${userId ? `?user_id=${userId}` : ""}`),
  },
};