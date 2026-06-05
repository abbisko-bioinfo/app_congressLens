import { useState, useEffect, useCallback, type ReactNode } from "react";
import { AuthContext, type AuthUser, type AuthContextValue } from "../hooks/useAuth";

const API_BASE = "/api";

interface SessionResponse {
  user: AuthUser | null;
}

async function fetchSession(): Promise<AuthUser | null> {
  try {
    const res = await fetch(`${API_BASE}/auth/session`);
    if (!res.ok) return null;
    const data: SessionResponse = await res.json();
    return data.user ?? null;
  } catch {
    return null;
  }
}

export default function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSession().then((u) => {
      setUser(u);
      setLoading(false);
    });
  }, []);

  const login = useCallback(async (username: string, password: string) => {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
    if (!res.ok) {
      throw new Error("Invalid credentials");
    }
    const data: SessionResponse = await res.json();
    setUser(data.user ?? null);
  }, []);

  const logout = useCallback(async () => {
    await fetch(`${API_BASE}/auth/logout`, { method: "POST" });
    setUser(null);
  }, []);

  if (loading) {
    return <>{children}</>;
  }

  const value: AuthContextValue = {
    user,
    isAuthenticated: user !== null,
    isAdmin: user?.is_admin ?? false,
    login,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}