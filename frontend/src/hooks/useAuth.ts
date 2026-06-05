import { createContext, useContext } from "react";

export interface AuthUser {
  id: string;
  display_name: string;
  email?: string;
  is_admin: boolean;
}

interface AuthContextValue {
  user: AuthUser | null;
  isAuthenticated: boolean;
  isAdmin: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
}

const defaultContext: AuthContextValue = {
  user: null,
  isAuthenticated: false,
  isAdmin: false,
  login: async () => {},
  logout: async () => {},
};

const AuthContext = createContext<AuthContextValue>(defaultContext);

export function useAuth(): AuthContextValue {
  return useContext(AuthContext);
}

export { AuthContext };