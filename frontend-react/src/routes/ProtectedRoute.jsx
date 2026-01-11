import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const ProtectedRoute = () => {
    const { isAuthenticated, loading } = useAuth();

    if (loading) return <div>Cargando...</div>;
    
    // Si no está logueado, mándalo a la landing
    if (!isAuthenticated) return <Navigate to="/" replace />;

    return <Outlet />; // Renderiza la ruta hija (el Dashboard)
};

export default ProtectedRoute;