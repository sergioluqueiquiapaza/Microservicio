// src/services/usuarioService.js
import api from './api';

const usuarioService = {
    // Obtener todos los usuarios activos de la empresa
    getUsuarios: async () => {
        try {
            const response = await api.get('/usuarios');
            return response.data;
        } catch (error) {
            throw error.response?.data || { error: 'Error al obtener usuarios' };
        }
    },

    // Obtener usuarios inactivos de la empresa
    getUsuariosInactivos: async () => {
        try {
            const response = await api.get('/usuarios/inactivos');
            return response.data;
        } catch (error) {
            throw error.response?.data || { error: 'Error al obtener usuarios inactivos' };
        }
    },

    // Obtener un usuario por ID
    getUsuarioById: async (id) => {
        try {
            const response = await api.get(`/usuarios/${id}`);
            return response.data;
        } catch (error) {
            throw error.response?.data || { error: 'Error al obtener usuario' };
        }
    },

    // Crear un nuevo usuario
    createUsuario: async (userData) => {
        try {
            const response = await api.post('/usuarios', userData);
            return response.data;
        } catch (error) {
            throw error.response?.data || { error: 'Error al crear usuario' };
        }
    },

    // Actualizar un usuario
    updateUsuario: async (id, userData) => {
        try {
            const response = await api.put(`/usuarios/${id}`, userData);
            return response.data;
        } catch (error) {
            throw error.response?.data || { error: 'Error al actualizar usuario' };
        }
    },

    // Desactivar un usuario (eliminación lógica)
    desactivarUsuario: async (id) => {
        try {
            const response = await api.put(`/usuarios/${id}/desactivar`);
            return response.data;
        } catch (error) {
            throw error.response?.data || { error: 'Error al desactivar usuario' };
        }
    },

    // Activar un usuario
    activarUsuario: async (id) => {
        try {
            const response = await api.put(`/usuarios/${id}/activar`);
            return response.data;
        } catch (error) {
            throw error.response?.data || { error: 'Error al activar usuario' };
        }
    },

    // Eliminar un usuario (eliminación física - solo SUPER_ADMIN)
    deleteUsuario: async (id) => {
        try {
            const response = await api.delete(`/usuarios/${id}`);
            return response.data;
        } catch (error) {
            throw error.response?.data || { error: 'Error al eliminar usuario' };
        }
    },

    // Obtener roles disponibles
    getRoles: async () => {
        try {
            const response = await api.get('/roles');
            return response.data;
        } catch (error) {
            throw error.response?.data || { error: 'Error al obtener roles' };
        }
    }
};

export default usuarioService;