import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AppShell } from './components/layout/AppShell';
import { SetupPage } from './pages/SetupPage';
import { CookPage } from './pages/CookPage';
import { ReportPage } from './pages/ReportPage';
import { useCookSession } from './hooks/useCookSession';

export default function App() {
  const cookSession = useCookSession();

  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AppShell />}>
          <Route path="/" element={<SetupPage cookSession={cookSession} />} />
          <Route path="/cook" element={<CookPage cookSession={cookSession} />} />
          <Route path="/report" element={<ReportPage cookSession={cookSession} />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
