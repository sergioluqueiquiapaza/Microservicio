// src/context/AuthContext.jsx
import React, { createContext, useState, useContext, useEffect } from 'react';
import authService from '../services/authService';
import { useNavigate } from 'react-router-dom';

// Crear el contexto
const AuthContext = createContext(null);

// Hook personalizado para usar el contexto fácilmente
export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth debe usarse dentro de un AuthProvider');
    }
    return context;
};

// Provider del contexto
export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [userType, setUserType] = useState(null); // 'empresa' o 'admin_saas'
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    // Cargar usuario al iniciar la aplicación
    useEffect(() => {
        const initializeAuth = () => {
            try {
                if (authService.isAuthenticated()) {
                    const currentUser = authService.getCurrentUser();
                    const type = authService.getUserType();
                    setUser(currentUser);
                    setUserType(type);
                }
            } catch (error) {
                console.error('Error inicializando autenticación:', error);
                authService.logout();
            } finally {
                setLoading(false);
            }
        };
        initializeAuth();
    }, []);

    // Login de Usuario de Empresa
    const loginUsuario = async (email, password) => {
        try {
            const data = await authService.loginUsuario(email, password);
            
            if (data && data.usuario && data.token) {
                setUser(data.usuario);
                setUserType('empresa');
                
                // Redirigir según el rol
                const rol = data.usuario.rol || data.usuario.id_rol;
                redirectByRole(rol);
                
                return { success: true, data };
            } else {
                return { 
                    success: false, 
                    error: 'Respuesta inválida del servidor' 
                };
            }
        } catch (error) {
            console.error('Error en loginUsuario:', error);
            // Retornar el error para que el componente lo muestre, NO redirigir
            return {
                success: false,
                error: error.error || error.message || 'Credenciales inválidas'
            };
        }
    };

    // Login de Admin SaaS
    const loginAdminSaas = async (email, password) => {
        try {
            const data = await authService.loginAdminSaas(email, password);
            
            if (data && data.admin && data.token) {
                setUser(data.admin);
                setUserType('admin_saas');
                
                // Redirigir al panel de Admin SaaS
                navigate('/saas-admin/panel');
                
                return { success: true, data };
            } else {
                return { 
                    success: false, 
                    error: 'Respuesta inválida del servidor' 
                };
            }
        } catch (error) {
            console.error('Error en loginAdminSaas:', error);
            // Retornar el error para que el componente lo muestre, NO redirigir
            return {
                success: false,
                error: error.error || error.message || 'Credenciales inválidas'
            };
        }
    };

    // Cerrar sesión
    const logout = () => {
        authService.logout();
        setUser(null);
        setUserType(null);
        navigate('/');
    };

    // Redirigir según el rol del usuario
    const redirectByRole = (rol) => {
        const roleRoutes = {
            'PROPIETARIO': '/dashboard',
            'ADMIN': '/dashboard',
            'VENDEDOR': '/dashboard',
            'SUPER_ADMIN': '/saas-admin/panel'
        };
        const route = roleRoutes[rol] || '/dashboard';
        navigate(route);
    };

    // Verificar si el usuario tiene un rol específico
    const hasRole = (roles) => {
        if (!user) return false;
        
        const userRole = authService.getUserRole();
        
        // Convertir a array si es un solo rol
        const allowedRoles = Array.isArray(roles) ? roles : [roles];
        
        return allowedRoles.includes(userRole);
    };

    // Verificar si es Admin SaaS
    const isAdminSaas = () => {
        return userType === 'admin_saas';
    };

    // Verificar si es usuario de empresa
    const isEmpresaUser = () => {
        return userType === 'empresa';
    };

    const value = {
        user,
        userType,
        loading,
        loginUsuario,
        loginAdminSaas,
        logout,
        isAuthenticated: authService.isAuthenticated,
        hasRole,
        isAdminSaas,
        isEmpresaUser,
        getUserRole: authService.getUserRole,
    };

    return (
        <AuthContext.Provider value={value}>
            {!loading && children}
        </AuthContext.Provider>
    );
};