// src/components/layout/DashboardLayout.jsx
import React, { useState } from 'react';
import { Container, Button } from 'react-bootstrap';
import { FaBars } from 'react-icons/fa';
import DashboardHeader from './DashboardHeader';
import DashboardSidebar from './DashboardSidebar';
import './DashboardLayout.css';

const DashboardLayout = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  return (
    <div className="dashboard-layout">
      {/* Header */}
      <DashboardHeader />

      {/* Sidebar */}
      <DashboardSidebar isOpen={sidebarOpen} toggleSidebar={toggleSidebar} />

      {/* Main Content */}
      <main className="dashboard-main">
        {/* Botón para abrir sidebar en móvil */}
        <Button
          variant="light"
          className="sidebar-toggle-btn d-lg-none"
          onClick={toggleSidebar}
        >
          <FaBars />
        </Button>

        <Container fluid className="dashboard-content">
          {children}
        </Container>
      </main>
    </div>
  );
};

export default DashboardLayout;