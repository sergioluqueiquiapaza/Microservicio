import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';

// Importación de Páginas (Las crearemos abajo)
import LandingPage from './pages/landing/LandingPage';
import RegisterCompany from './pages/auth/RegisterCompany';
import SelectPlan from './pages/auth/SelectPlan';
import PaymentQR from './pages/auth/PaymentQR';
import DashboardHome from './pages/dashboard/DashboardHome';

// Componente para proteger rutas privadas
import ProtectedRoute from './routes/ProtectedRoute';

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* Rutas Públicas */}
          <Route path="/" element={<LandingPage />} />
          <Route path="/registro" element={<RegisterCompany />} />
          
          {/* Rutas del proceso de Onboarding (Registro paso a paso) */}
          <Route path="/seleccionar-plan" element={<SelectPlan />} />
          <Route path="/pago-suscripcion" element={<PaymentQR />} />

          {/* Rutas Privadas (Solo usuarios logueados) */}
          <Route element={<ProtectedRoute />}>
             <Route path="/dashboard" element={<DashboardHome />} />
             {/* Aquí irán /ventas, /inventario, etc. */}
          </Route>

          {/* Ruta 404 por defecto */}
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;