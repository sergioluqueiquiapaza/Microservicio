// src/services/authService.js
import api from './api';

const authService = {
    // Login para usuarios de empresa
    loginUsuario: async (email, password) => {
        try {
            const response = await api.post('/auth/login', { email, password });
            
            if (response.data.token) {
                localStorage.setItem('token', response.data.token);
                localStorage.setItem('user', JSON.stringify(response.data.usuario));
                localStorage.setItem('userType', 'empresa');
                return response.data;
            }
            
            throw new Error('Respuesta inválida del servidor');
        } catch (error) {
            // NO lanzar el error, retornarlo para que el componente lo maneje
            console.error('Error en loginUsuario:', error);
            throw error.response?.data || { error: 'Error al iniciar sesión' };
        }
    },

    // Login para administradores SaaS
    loginAdminSaas: async (email, password) => {
        try {
            const response = await api.post('/saas/login', { email, password });
            
            if (response.data.token) {
                localStorage.setItem('token', response.data.token);
                localStorage.setItem('user', JSON.stringify(response.data.admin));
                localStorage.setItem('userType', 'admin_saas');
                return response.data;
            }
            
            throw new Error('Respuesta inválida del servidor');
        } catch (error) {
            // NO lanzar el error, retornarlo para que el componente lo maneje
            console.error('Error en loginAdminSaas:', error);
            throw error.response?.data || { error: 'Error al iniciar sesión' };
        }
    },

    // Logout
    logout: () => {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        localStorage.removeItem('userType');
    },

    // Verificar si está autenticado
    isAuthenticated: () => {
        return !!localStorage.getItem('token');
    },

    // Obtener usuario actual
    getCurrentUser: () => {
        const user = localStorage.getItem('user');
        return user ? JSON.parse(user) : null;
    },

    // Obtener tipo de usuario
    getUserType: () => {
        return localStorage.getItem('userType');
    },

    // Obtener rol del usuario
    getUserRole: () => {
        const user = authService.getCurrentUser();
        return user?.rol || user?.id_rol || null;
    }
};

export default authService;