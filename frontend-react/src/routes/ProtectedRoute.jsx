// src/routes/ProtectedRoute.jsx
import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const ProtectedRoute = ({ children, roles, adminOnly = false }) => {
  const { isAuthenticated, hasRole, isAdminSaas, isEmpresaUser } = useAuth();

  // Verificar autenticación
  if (!isAuthenticated()) {
    return <Navigate to="/" replace />;
  }

  // Si la ruta es solo para Admin SaaS
  if (adminOnly && !isAdminSaas()) {
    return <Navigate to="/dashboard" replace />;
  }

  // Si la ruta es solo para usuarios de empresa
  if (!adminOnly && !isEmpresaUser()) {
    return <Navigate to="/saas-admin/panel" replace />;
  }

  // Verificar roles específicos
  if (roles && !hasRole(roles)) {
    return (
      <div className="container mt-5">
        <div className="alert alert-danger">
          <h4>Acceso Denegado</h4>
          <p>No tienes permisos para acceder a esta sección.</p>
        </div>
      </div>
    );
  }

  return children;
};

export default ProtectedRoute;