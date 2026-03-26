import { BrowserRouter, Route, Routes } from "react-router-dom";
import Layout from "./components/Layout";
import DashboardPage from "./pages/DashboardPage";
import DocumentBrowserPage from "./pages/DocumentBrowserPage";
import RecordDetailPage from "./pages/RecordDetailPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/records/:recordId" element={<RecordDetailPage />} />
          <Route path="/documents" element={<DocumentBrowserPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
