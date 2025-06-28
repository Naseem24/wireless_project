// frontend/src/App.jsx
import { Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from './components/Sidebar.jsx';
import WirelessSystemPage from './pages/WirelessSystemPage.jsx';
import OfdmPage from './pages/OfdmPage.jsx';
import LinkBudgetPage from './pages/LinkBudgetPage.jsx';
import CellularDesignPage from './pages/CellularDesignPage.jsx';
import './App.css';

function App() {
  return (
    <div className="app-container">
      <Sidebar />
      <main className="main-content">
        <Routes>
          {/* By default, redirect from the homepage "/" to the first calculator */}
          <Route path="/" element={<Navigate to="/wireless-system" />} />
          
          <Route path="/wireless-system" element={<WirelessSystemPage />} />
          <Route path="/ofdm-systems" element={<OfdmPage />} />
          <Route path="/link-budget" element={<LinkBudgetPage />} />
          <Route path="/cellular-design" element={<CellularDesignPage />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;