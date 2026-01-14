// src/routes/AppRouter.jsx
import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

// Páginas públicas
import LandingPage from '../pages/landing/LandingPage';
import LoginPage from '../pages/auth/LoginPage';
import RegistroEmpresaPage from '../pages/auth/RegistroEmpresaPage';

// Páginas del Dashboard de Empresa
import Dashboard from '../pages/dashboard/Dashboard';
import UsuariosLista from '../pages/dashboard/usuarios/UsuariosLista';
import UsuarioForm from '../pages/dashboard/usuarios/UsuarioForm';

// Páginas del Admin SaaS
import SaasAdminPanel from '../pages/saas-admin/SaasAdminPanel';

// Componentes de protección
import ProtectedRoute from './ProtectedRoute';

const AppRouter = () => {
  const { isAuthenticated } = useAuth();

  return (
    <Routes>
      {/* Rutas Públicas */}
      <Route
        path="/"
        element={
          isAuthenticated() ? <Navigate to="/dashboard" replace /> : <LandingPage />
        }
      />
      
      <Route
        path="/login"
        element={
          isAuthenticated() ? <Navigate to="/dashboard" replace /> : <LoginPage />
        }
      />

      <Route
        path="/registro-empresa"
        element={
          isAuthenticated() ? <Navigate to="/dashboard" replace /> : <RegistroEmpresaPage />
        }
      />

      {/* Rutas del Dashboard de Empresa */}
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        }
      />

      {/* Rutas de Gestión de Usuarios */}
      <Route
        path="/dashboard/usuarios"
        element={
          <ProtectedRoute roles={['PROPIETARIO', 'ADMIN']}>
            <UsuariosLista />
          </ProtectedRoute>
        }
      />

      <Route
        path="/dashboard/usuarios/nuevo"
        element={
          <ProtectedRoute roles={['PROPIETARIO', 'ADMIN']}>
            <UsuarioForm />
          </ProtectedRoute>
        }
      />

      <Route
        path="/dashboard/usuarios/:id/editar"
        element={
          <ProtectedRoute roles={['PROPIETARIO', 'ADMIN']}>
            <UsuarioForm />
          </ProtectedRoute>
        }
      />

      {/* Rutas del Admin SaaS */}
      <Route
        path="/saas-admin/panel"
        element={
          <ProtectedRoute adminOnly={true}>
            <SaasAdminPanel />
          </ProtectedRoute>
        }
      />

      {/* Ruta 404 */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
};

export default AppRouter;