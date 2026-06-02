import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import './index.css'
import Layout from './components/Layout.tsx'
import Dashboard from './pages/Dashboard.tsx'
import ConferenceList from './pages/ConferenceList.tsx'
import ConferenceDetail from './pages/ConferenceDetail.tsx'
import SessionDetail from './pages/SessionDetail.tsx'
import PresentationList from './pages/PresentationList.tsx'
import PresentationDetail from './pages/PresentationDetail.tsx'
import Calendar from './pages/Calendar.tsx'

const queryClient = new QueryClient()

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route element={<Layout />}>
            <Route path="/" element={<Dashboard />} />
            <Route path="/conferences" element={<ConferenceList />} />
            <Route path="/conferences/:id" element={<ConferenceDetail />} />
            <Route path="/sessions/:id" element={<SessionDetail />} />
            <Route path="/presentations" element={<PresentationList />} />
            <Route path="/presentations/:id" element={<PresentationDetail />} />
            <Route path="/calendar" element={<Calendar />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  </StrictMode>,
)