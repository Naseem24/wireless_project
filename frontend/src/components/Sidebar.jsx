// frontend/src/components/Sidebar.jsx
import React from 'react';
import { NavLink } from 'react-router-dom';
import './Sidebar.css'; // This line correctly imports the CSS file

function Sidebar() {
  return (
    <div className="sidebar">
      <h2>AI Wireless Toolkit</h2>
      <nav>
        <NavLink to="/wireless-system">Wireless Comm. System</NavLink>
        <NavLink to="/ofdm-systems">OFDM System</NavLink>
        <NavLink to="/link-budget">Link Budget</NavLink>
        <NavLink to="/cellular-design">Cellular System Design</NavLink>
      </nav>
    </div>
  );
}

export default Sidebar;