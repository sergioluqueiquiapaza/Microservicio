// src/services/saasService.js
import api from './api';

const saasService = {
  // ==========================================
  // ESTADÍSTICAS DASHBOARD
  // ==========================================
  getEstadisticasDashboard: async () => {
    try {
      const response = await api.get('/saas/dashboard/estadisticas');
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Error al obtener estadísticas' };
    }
  },

  getEmpresasRecientes: async (limit = 10) => {
    try {
      const response = await api.get(`/saas/dashboard/empresas-recientes?limit=${limit}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Error al obtener empresas recientes' };
    }
  },

  getPagosPendientes: async () => {
    try {
      const response = await api.get('/saas/dashboard/pagos-pendientes');
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Error al obtener pagos pendientes' };
    }
  },

  // ==========================================
  // ADMINISTRADORES SAAS
  // ==========================================
  getAdminsSaas: async () => {
    try {
      const response = await api.get('/saas/admins');
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Error al obtener administradores' };
    }
  },

  getAdminsSaasInactivos: async () => {
    try {
      const response = await api.get('/saas/admins/inactivos');
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Error al obtener administradores inactivos' };
    }
  },

  getAdminSaasById: async (id) => {
    try {
      const response = await api.get(`/saas/admins/${id}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Error al obtener administrador' };
    }
  },

  createAdminSaas: async (data) => {
    try {
      const response = await api.post('/saas/admin', data);
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Error al crear administrador' };
    }
  },

  updateAdminSaas: async (id, data) => {
    try {
      const response = await api.put(`/saas/admins/${id}`, data);
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Error al actualizar administrador' };
    }
  },

  desactivarAdminSaas: async (id) => {
    try {
      const response = await api.put(`/saas/admins/${id}/desactivar`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Error al desactivar administrador' };
    }
  },

  activarAdminSaas: async (id) => {
    try {
      const response = await api.put(`/saas/admins/${id}/activar`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Error al activar administrador' };
    }
  },

  // ==========================================
  // PLANES
  // ==========================================
  getPlanes: async () => {
    try {
      const response = await api.get('/planes');
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Error al obtener planes' };
    }
  },

  getPlanById: async (id) => {
    try {
      const response = await api.get(`/planes/${id}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Error al obtener plan' };
    }
  },

  createPlan: async (data) => {
    try {
      const response = await api.post('/planes', data);
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Error al crear plan' };
    }
  },

  updatePlan: async (id, data) => {
    try {
      const response = await api.put(`/planes/${id}`, data);
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Error al actualizar plan' };
    }
  },

  deletePlan: async (id) => {
    try {
      const response = await api.delete(`/planes/${id}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Error al eliminar plan' };
    }
  },

  // ==========================================
  // SUSCRIPCIONES
  // ==========================================
  getSuscripciones: async () => {
    try {
      const response = await api.get('/suscripciones');
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Error al obtener suscripciones' };
    }
  },

  createSuscripcion: async (data) => {
    try {
      const response = await api.post('/suscripciones', data);
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Error al crear suscripción' };
    }
  },

  updateSuscripcion: async (id, data) => {
    try {
      const response = await api.put(`/suscripciones/${id}`, data);
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Error al actualizar suscripción' };
    }
  },

  aprobarPago: async (id_suscripcion) => {
    try {
      const response = await api.put(`/suscripciones/${id_suscripcion}`, {
        estado: true
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Error al aprobar pago' };
    }
  },

  rechazarPago: async (id_suscripcion) => {
    try {
      const response = await api.put(`/suscripciones/${id_suscripcion}`, {
        estado: false
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Error al rechazar pago' };
    }
  },

  // ==========================================
  // EMPRESAS (desde perspectiva SaaS)
  // ==========================================
  getEmpresas: async () => {
    try {
      const response = await api.get('/empresas');
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Error al obtener empresas' };
    }
  },
  // Agregar esta función al archivo saasService.js existente

    // ==========================================
    // EMPRESAS CON PROPIETARIOS
    // ==========================================
  getEmpresasConPropietarios: async () => {
    try {
        const response = await api.get('/saas/empresas');
        return response.data;
    } catch (error) {
        throw error.response?.data || { error: 'Error al obtener empresas' };
    }
  }
};

export default saasService;