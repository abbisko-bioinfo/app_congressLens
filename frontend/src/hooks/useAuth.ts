import { createContext, useContext } from "react";

export interface AuthUser {
  id: string;
  display_name: string;
  email?: string;
  is_admin: boolean;
}

export interface AuthContextValue {
  user: AuthUser | null;
  isAuthenticated: boolean;
  isAdmin: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    return {
      user: null,
      isAuthenticated: false,
      isAdmin: false,
      login: async () => {},
      logout: async () => {},
    };
  }
  return ctx;
}

export { AuthContext };