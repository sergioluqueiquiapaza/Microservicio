// src/pages/dashboard/Dashboard.jsx
import React from 'react';
import DashboardLayout from '../../components/layout/DashboardLayout';
import DashboardHome from './DashboardHome';

const Dashboard = () => {
  return (
    <DashboardLayout>
      <DashboardHome />
    </DashboardLayout>
  );
};

export default Dashboard;