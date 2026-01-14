// src/services/api.js
import axios from 'axios';

// URL base de tu backend Flask
const API_URL = 'http://localhost:5000/api';

// Crear instancia de axios con configuración base
const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
    withCredentials: false,
});

// Interceptor para agregar el token JWT a todas las peticiones
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        
        console.log('📤 Request:', config.method.toUpperCase(), config.url);
        return config;
    },
    (error) => {
        console.error('❌ Request error:', error);
        return Promise.reject(error);
    }
);

// Interceptor para manejar errores de respuesta globalmente
api.interceptors.response.use(
    (response) => {
        console.log('📥 Response:', response.status, response.config.url);
        return response;
    },
    (error) => {
        console.error('❌ Response error:', error.response?.status, error.config?.url);
        
        // Si el token expiró (401) Y no es un intento de login, redirigir al login
        if (error.response && error.response.status === 401) {
            // NO redirigir si es un intento de login o logout
            const isLoginAttempt = error.config.url.includes('/auth/login') || 
                                   error.config.url.includes('/saas/login');
            const isLogoutAttempt = error.config.url.includes('/logout');
            
            if (!isLoginAttempt && !isLogoutAttempt) {
                console.warn('⚠️ Token expirado - Redirigiendo al login');
                localStorage.removeItem('token');
                localStorage.removeItem('user');
                localStorage.removeItem('userType');
                window.location.href = '/';
            }
        }
        
        return Promise.reject(error);
    }
);

export default api;