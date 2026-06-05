import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { AuthContext } from "./hooks/useAuth";
import type { AuthUser } from "./hooks/useAuth";
import "./index.css";
import Header from "./components/Header.tsx";
import Footer from "./components/Footer.tsx";
import Dashboard from "./pages/Dashboard.tsx";
import SessionList from "./pages/SessionList.tsx";
import PresentationList from "./pages/PresentationList.tsx";
import PresentationDetail from "./pages/PresentationDetail.tsx";
import StarPage from "./pages/StarPage.tsx";

const queryClient = new QueryClient();

// Auth stub — will be fully implemented with AuthProvider in Task 13
const authStub = {
  user: null as AuthUser | null,
  isAuthenticated: false,
  isAdmin: false,
  login: async (_username: string, _password: string) => {},
  logout: async () => {},
};

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <AuthContext.Provider value={authStub}>
        <BrowserRouter>
          <div className="min-h-screen flex flex-col bg-background">
            <Header />
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/session/:congress" element={<SessionList />} />
              <Route path="/presentations/:congress" element={<PresentationList />} />
              <Route path="/presentations/:congress/:id" element={<PresentationDetail />} />
              <Route path="/star" element={<StarPage />} />
              <Route path="*" element={<Dashboard />} />
            </Routes>
            <Footer />
          </div>
        </BrowserRouter>
      </AuthContext.Provider>
    </QueryClientProvider>
  </StrictMode>,
);