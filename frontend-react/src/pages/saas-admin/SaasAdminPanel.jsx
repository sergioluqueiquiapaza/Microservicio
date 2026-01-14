import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Table, Badge, Button, Spinner, Alert, Modal, Form, Tabs, Tab } from 'react-bootstrap';
import {
  FaBuilding,
  FaUsers,
  FaMoneyBillWave,
  FaCheckCircle,
  FaClock,
  FaTimes,
  FaUserShield,
  FaUserPlus,
  FaEdit,
  FaTrash
} from 'react-icons/fa';
import { useAuth } from '../../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import saasService from '../../services/saasService';

const SaasAdminPanel = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  
  const [stats, setStats] = useState(null);
  const [empresasRecientes, setEmpresasRecientes] = useState([]);
  const [pagosPendientes, setPagosPendientes] = useState([]);
  const [admins, setAdmins] = useState([]);
  const [adminsInactivos, setAdminsInactivos] = useState([]);
  const [empresas, setEmpresas] = useState([]); // Agregado
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  
  const [showAdminModal, setShowAdminModal] = useState(false);
  const [showConfirmModal, setShowConfirmModal] = useState(false);
  const [adminToDelete, setAdminToDelete] = useState(null);
  const [editingAdmin, setEditingAdmin] = useState(null);
  
  const [adminFormData, setAdminFormData] = useState({
    nombre: '',
    email: '',
    password: '',
    confirmarPassword: ''
  });
  const [formErrors, setFormErrors] = useState({});

  useEffect(() => {
    loadDashboardData();
    loadEmpresas(); // Agregado
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      setError('');
      
      const statsData = await saasService.getEstadisticasDashboard();
      setStats(statsData);
      
      const empresas = await saasService.getEmpresasRecientes(5);
      setEmpresasRecientes(empresas);
      
      const pagos = await saasService.getPagosPendientes();
      setPagosPendientes(pagos);
      
      await loadAdmins();
      
    } catch (err) {
      setError(err.error || 'Error al cargar datos del dashboard');
    } finally {
      setLoading(false);
    }
  };

  // Agregado: Función para cargar empresas
  const loadEmpresas = async () => {
    try {
      const data = await saasService.getEmpresasConPropietarios();
      setEmpresas(data);
    } catch (err) {
      console.error('Error cargando empresas:', err);
    }
  };

  const loadAdmins = async () => {
    try {
      const [activos, inactivos] = await Promise.all([
        saasService.getAdminsSaas(),
        saasService.getAdminsSaasInactivos()
      ]);
      setAdmins(activos);
      setAdminsInactivos(inactivos);
    } catch (err) {
      console.error('Error cargando admins:', err);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const handleOpenAdminModal = (admin = null) => {
    if (admin) {
      setEditingAdmin(admin);
      setAdminFormData({
        nombre: admin.nombre || '',
        email: admin.email || '',
        password: '',
        confirmarPassword: ''
      });
    } else {
      setEditingAdmin(null);
      setAdminFormData({
        nombre: '',
        email: '',
        password: '',
        confirmarPassword: ''
      });
    }
    setFormErrors({});
    setShowAdminModal(true);
  };

  const handleCloseAdminModal = () => {
    setShowAdminModal(false);
    setEditingAdmin(null);
    setAdminFormData({
      nombre: '',
      email: '',
      password: '',
      confirmarPassword: ''
    });
    setFormErrors({});
  };

  const validateAdminForm = () => {
    const errors = {};
    
    if (!adminFormData.nombre.trim()) {
      errors.nombre = 'El nombre es obligatorio';
    }
    
    if (!adminFormData.email.trim()) {
      errors.email = 'El email es obligatorio';
    } else if (!/\S+@\S+\.\S+/.test(adminFormData.email)) {
      errors.email = 'El email no es válido';
    }
    
    if (!editingAdmin) {
      if (!adminFormData.password) {
        errors.password = 'La contraseña es obligatoria';
      } else if (adminFormData.password.length < 6) {
        errors.password = 'La contraseña debe tener al menos 6 caracteres';
      }
      
      if (adminFormData.password !== adminFormData.confirmarPassword) {
        errors.confirmarPassword = 'Las contraseñas no coinciden';
      }
    } else if (adminFormData.password) {
      if (adminFormData.password.length < 6) {
        errors.password = 'La contraseña debe tener al menos 6 caracteres';
      }
      if (adminFormData.password !== adminFormData.confirmarPassword) {
        errors.confirmarPassword = 'Las contraseñas no coinciden';
      }
    }
    
    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmitAdmin = async (e) => {
    e.preventDefault();
    
    if (!validateAdminForm()) return;
    
    try {
      setError('');
      setSuccess('');
      
      const dataToSend = {
        nombre: adminFormData.nombre,
        email: adminFormData.email
      };
      
      if (adminFormData.password) {
        dataToSend.password = adminFormData.password;
      }
      
      if (editingAdmin) {
        await saasService.updateAdminSaas(editingAdmin.id_admin, dataToSend);
        setSuccess('Administrador actualizado exitosamente');
      } else {
        await saasService.createAdminSaas(dataToSend);
        setSuccess('Administrador creado exitosamente');
      }
      
      handleCloseAdminModal();
      loadAdmins();
      
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError(err.error || 'Error al guardar administrador');
    }
  };

  const handleDesactivarAdmin = (admin) => {
    setAdminToDelete(admin);
    setShowConfirmModal(true);
  };

  const confirmDesactivar = async () => {
    try {
      await saasService.desactivarAdminSaas(adminToDelete.id_admin);
      setSuccess('Administrador desactivado correctamente');
      setShowConfirmModal(false);
      setAdminToDelete(null);
      loadAdmins();
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError(err.error || 'Error al desactivar administrador');
      setShowConfirmModal(false);
    }
  };

  const handleActivarAdmin = async (id_admin) => {
    try {
      await saasService.activarAdminSaas(id_admin);
      setSuccess('Administrador activado correctamente');
      loadAdmins();
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError(err.error || 'Error al activar administrador');
    }
  };

  const handleAprobarPago = async (id_suscripcion) => {
    try {
      await saasService.aprobarPago(id_suscripcion);
      setSuccess('Pago aprobado correctamente');
      loadDashboardData();
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError(err.error || 'Error al aprobar pago');
    }
  };

  if (loading) {
    return React.createElement('div', { className: 'saas-admin-panel' },
      React.createElement('div', { className: 'admin-header bg-dark text-white py-3 shadow-sm sticky-top' },
        React.createElement(Container, { fluid: true, className: 'px-4' },
          React.createElement('h4', { className: 'mb-0 fw-bold' }, 'Panel de Administración SaaS')
        )
      ),
      React.createElement(Container, { fluid: true, className: 'px-4 py-5 text-center' },
        React.createElement(Spinner, { animation: 'border', variant: 'primary' }),
        React.createElement('p', { className: 'mt-3 text-muted' }, 'Cargando datos...')
      )
    );
  }

  return React.createElement('div', { className: 'saas-admin-panel' },
    React.createElement('div', { className: 'admin-header bg-dark text-white py-3 shadow-sm sticky-top' },
      React.createElement(Container, { fluid: true, className: 'px-4' },
        React.createElement('div', { className: 'd-flex justify-content-between align-items-center' },
          React.createElement('div', null,
            React.createElement('h4', { className: 'mb-0 fw-bold' }, 'Panel de Administración SaaS'),
            React.createElement('small', { className: 'text-white-50' }, 
              'Bienvenido, ', user?.nombre || 'Administrador'
            )
          ),
          React.createElement(Button, { variant: 'outline-light', size: 'sm', onClick: handleLogout }, 
            'Cerrar Sesión'
          )
        )
      )
    ),

    React.createElement(Container, { fluid: true, className: 'px-4 py-4' },
      error && React.createElement(Alert, { 
        variant: 'danger', 
        dismissible: true, 
        onClose: () => setError('') 
      }, error),
      
      success && React.createElement(Alert, { 
        variant: 'success', 
        dismissible: true, 
        onClose: () => setSuccess('') 
      }, success),

      stats && React.createElement(Row, { className: 'g-3 mb-4' },
        React.createElement(Col, { xs: 12, sm: 6, lg: 3 },
          React.createElement(Card, { className: 'stat-card border-0 shadow-sm h-100' },
            React.createElement(Card.Body, null,
              React.createElement('div', { className: 'd-flex justify-content-between align-items-start mb-3' },
                React.createElement('div', { className: 'stat-icon bg-primary-subtle text-primary' },
                  React.createElement(FaBuilding, { size: 24 })
                )
              ),
              React.createElement('h3', { className: 'fw-bold mb-1' }, stats.empresas.total),
              React.createElement('p', { className: 'text-muted mb-2 small' }, 'Empresas Registradas'),
              React.createElement('div', { className: 'd-flex gap-2' },
                React.createElement(Badge, { bg: 'success' }, stats.empresas.activas, ' activas'),
                React.createElement(Badge, { bg: 'secondary' }, stats.empresas.inactivas, ' inactivas')
              )
            )
          )
        ),

        React.createElement(Col, { xs: 12, sm: 6, lg: 3 },
          React.createElement(Card, { className: 'stat-card border-0 shadow-sm h-100' },
            React.createElement(Card.Body, null,
              React.createElement('div', { className: 'd-flex justify-content-between align-items-start mb-3' },
                React.createElement('div', { className: 'stat-icon bg-success-subtle text-success' },
                  React.createElement(FaUsers, { size: 24 })
                )
              ),
              React.createElement('h3', { className: 'fw-bold mb-1' },
                stats.suscripciones.free + stats.suscripciones.basic + stats.suscripciones.premium
              ),
              React.createElement('p', { className: 'text-muted mb-2 small' }, 'Suscripciones Activas'),
              React.createElement('div', { className: 'd-flex gap-1 flex-wrap' },
                React.createElement(Badge, { bg: 'light', text: 'dark' }, stats.suscripciones.free, ' Free'),
                React.createElement(Badge, { bg: 'primary' }, stats.suscripciones.basic, ' Basic'),
                React.createElement(Badge, { bg: 'dark' }, stats.suscripciones.premium, ' Premium')
              )
            )
          )
        ),

        React.createElement(Col, { xs: 12, sm: 6, lg: 3 },
          React.createElement(Card, { className: 'stat-card border-0 shadow-sm h-100' },
            React.createElement(Card.Body, null,
              React.createElement('div', { className: 'd-flex justify-content-between align-items-start mb-3' },
                React.createElement('div', { className: 'stat-icon bg-warning-subtle text-warning' },
                  React.createElement(FaMoneyBillWave, { size: 24 })
                )
              ),
              React.createElement('h3', { className: 'fw-bold mb-1' }, stats.ingresos.toLocaleString(), ' Bs'),
              React.createElement('p', { className: 'text-muted mb-0 small' }, 'Ingresos Mensuales')
            )
          )
        ),

        React.createElement(Col, { xs: 12, sm: 6, lg: 3 },
          React.createElement(Card, { className: 'stat-card border-0 shadow-sm h-100 border-warning' },
            React.createElement(Card.Body, null,
              React.createElement('div', { className: 'd-flex justify-content-between align-items-start mb-3' },
                React.createElement('div', { className: 'stat-icon bg-danger-subtle text-danger' },
                  React.createElement(FaClock, { size: 24 })
                ),
                React.createElement(Badge, { bg: 'warning' }, stats.pagosPendientes)
              ),
              React.createElement('h3', { className: 'fw-bold mb-1' }, stats.pagosPendientes),
              React.createElement('p', { className: 'text-muted mb-0 small' }, 'Pagos Pendientes')
            )
          )
        )
      ),

      React.createElement(Tabs, { defaultActiveKey: 'dashboard', className: 'mb-4' },
        React.createElement(Tab, { eventKey: 'dashboard', title: 'Dashboard' },
          React.createElement(Row, { className: 'g-3' },
            React.createElement(Col, { xs: 12, lg: 7 },
              React.createElement(Card, { className: 'border-0 shadow-sm h-100' },
                React.createElement(Card.Header, { className: 'bg-white border-bottom' },
                  React.createElement('h5', { className: 'mb-0 fw-semibold' }, 
                    'Empresas Registradas Recientemente'
                  )
                ),
                React.createElement(Card.Body, { className: 'p-0' },
                  empresasRecientes.length > 0 ? 
                    React.createElement(Table, { hover: true, className: 'mb-0' },
                      React.createElement('thead', { className: 'bg-light' },
                        React.createElement('tr', null,
                          React.createElement('th', { className: 'border-0' }, 'Empresa'),
                          React.createElement('th', { className: 'border-0' }, 'Plan'),
                          React.createElement('th', { className: 'border-0' }, 'Fecha Registro'),
                          React.createElement('th', { className: 'border-0' }, 'Estado')
                        )
                      ),
                      React.createElement('tbody', null,
                        empresasRecientes.map((empresa) =>
                          React.createElement('tr', { key: empresa.id_empresa },
                            React.createElement('td', null, empresa.nombre_comercial),
                            React.createElement('td', null,
                              React.createElement(Badge, {
                                bg: empresa.plan === 'FREE' ? 'light' :
                                    empresa.plan === 'BASIC' ? 'primary' : 'dark',
                                text: empresa.plan === 'FREE' ? 'dark' : 'white'
                              }, empresa.plan)
                            ),
                            React.createElement('td', null, 
                              new Date(empresa.fecha_registro).toLocaleDateString()
                            ),
                            React.createElement('td', null,
                              React.createElement(Badge, { 
                                bg: empresa.activo ? 'success' : 'secondary' 
                              }, empresa.activo ? 'Activa' : 'Inactiva')
                            )
                          )
                        )
                      )
                    ) :
                    React.createElement('div', { className: 'p-4 text-center text-muted' },
                      React.createElement('p', null, 'No hay empresas registradas aún')
                    )
                )
              )
            ),

            React.createElement(Col, { xs: 12, lg: 5 },
              React.createElement(Card, { className: 'border-warning border-2 shadow-sm h-100' },
                React.createElement(Card.Header, { className: 'bg-warning bg-opacity-10 border-bottom' },
                  React.createElement('h5', { className: 'mb-0 fw-semibold' },
                    React.createElement(FaClock, { className: 'me-2' }),
                    'Pagos Pendientes de Validación'
                  )
                ),
                React.createElement(Card.Body, { className: 'p-0', style: {maxHeight: '400px', overflowY: 'auto'} },
                  pagosPendientes.length > 0 ?
                    React.createElement('div', { className: 'list-group list-group-flush' },
                      pagosPendientes.map((pago) =>
                        React.createElement('div', { key: pago.id_suscripcion, className: 'list-group-item' },
                          React.createElement('div', { className: 'd-flex justify-content-between align-items-start mb-2' },
                            React.createElement('div', null,
                              React.createElement('div', { className: 'fw-semibold' }, pago.empresa_nombre),
                              React.createElement('small', { className: 'text-muted' }, pago.id_suscripcion)
                            ),
                            React.createElement(Badge, { bg: 'warning' }, pago.plan_nombre)
                          ),
                          React.createElement('div', { className: 'd-flex justify-content-between align-items-center mt-2' },
                            React.createElement('span', { className: 'fw-bold text-primary' },
                              pago.monto, ' Bs'
                            ),
                            React.createElement('div', { className: 'd-flex gap-2' },
                              React.createElement(Button, {
                                variant: 'success',
                                size: 'sm',
                                onClick: () => handleAprobarPago(pago.id_suscripcion)
                              },
                                React.createElement(FaCheckCircle, { className: 'me-1' }),
                                'Aprobar'
                              ),
                              React.createElement(Button, { variant: 'danger', size: 'sm' },
                                React.createElement(FaTimes, null)
                              )
                            )
                          )
                        )
                      )
                    ) :
                    React.createElement('div', { className: 'p-4 text-center text-muted' },
                      React.createElement(FaCheckCircle, { size: 48, className: 'mb-3 opacity-25' }),
                      React.createElement('p', { className: 'mb-0' }, 'No hay pagos pendientes')
                    )
                )
              )
            )
          )
        ),

        React.createElement(Tab, { 
          eventKey: 'admins', 
          title: React.createElement('span', null,
            React.createElement(FaUserShield, { className: 'me-2' }),
            'Administradores SaaS'
          )
        },
          React.createElement(Card, { className: 'border-0 shadow-sm' },
            React.createElement(Card.Header, { className: 'bg-white border-bottom' },
              React.createElement('div', { className: 'd-flex justify-content-between align-items-center' },
                React.createElement('h5', { className: 'mb-0 fw-semibold' }, 
                  'Gestión de Administradores'
                ),
                React.createElement(Button, {
                  variant: 'primary',
                  onClick: () => handleOpenAdminModal()
                },
                  React.createElement(FaUserPlus, { className: 'me-2' }),
                  'Nuevo Administrador'
                )
              )
            ),
            React.createElement(Card.Body, null,
              React.createElement(Tabs, { defaultActiveKey: 'activos', className: 'mb-3' },
                React.createElement(Tab, { 
                  eventKey: 'activos', 
                  title: `Activos (${admins.length})` 
                },
                  admins.length > 0 ?
                    React.createElement(Table, { hover: true, responsive: true },
                      React.createElement('thead', { className: 'bg-light' },
                        React.createElement('tr', null,
                          React.createElement('th', null, 'Nombre'),
                          React.createElement('th', null, 'Email'),
                          React.createElement('th', null, 'Rol'),
                          React.createElement('th', null, 'Fecha Creación'),
                          React.createElement('th', { className: 'text-center' }, 'Acciones')
                        )
                      ),
                      React.createElement('tbody', null,
                        admins.map((admin) =>
                          React.createElement('tr', { key: admin.id_admin },
                            React.createElement('td', null, admin.nombre),
                            React.createElement('td', null, admin.email),
                            React.createElement('td', null,
                              React.createElement(Badge, { bg: 'dark' }, 'SUPER_ADMIN')
                            ),
                            React.createElement('td', null, 
                              new Date(admin.fecha_creacion).toLocaleDateString()
                            ),
                            React.createElement('td', { className: 'text-center' },
                              React.createElement(Button, {
                                variant: 'link',
                                size: 'sm',
                                className: 'p-0 me-3',
                                onClick: () => handleOpenAdminModal(admin)
                              },
                                React.createElement(FaEdit, null)
                              ),
                              React.createElement(Button, {
                                variant: 'link',
                                size: 'sm',
                                className: 'p-0 text-danger',
                                onClick: () => handleDesactivarAdmin(admin)
                              },
                                React.createElement(FaTrash, null)
                              )
                            )
                          )
                        )
                      )
                    ) :
                    React.createElement('div', { className: 'text-center py-4 text-muted' },
                      React.createElement('p', null, 'No hay administradores activos')
                    )
                ),

                React.createElement(Tab, { 
                  eventKey: 'inactivos', 
                  title: `Desactivados (${adminsInactivos.length})` 
                },
                  adminsInactivos.length > 0 ?
                    React.createElement(Table, { hover: true, responsive: true },
                      React.createElement('thead', { className: 'bg-light' },
                        React.createElement('tr', null,
                          React.createElement('th', null, 'Nombre'),
                          React.createElement('th', null, 'Email'),
                          React.createElement('th', null, 'Fecha Creación'),
                          React.createElement('th', { className: 'text-center' }, 'Acciones')
                        )
                      ),
                      React.createElement('tbody', null,
                        adminsInactivos.map((admin) =>
                          React.createElement('tr', { key: admin.id_admin },
                            React.createElement('td', { className: 'text-muted' }, admin.nombre),
                            React.createElement('td', { className: 'text-muted' }, admin.email),
                            React.createElement('td', { className: 'text-muted' }, 
                              new Date(admin.fecha_creacion).toLocaleDateString()
                            ),
                            React.createElement('td', { className: 'text-center' },
                              React.createElement(Button, {
                                variant: 'success',
                                size: 'sm',
                                onClick: () => handleActivarAdmin(admin.id_admin)
                              },
                                React.createElement(FaCheckCircle, { className: 'me-1' }),
                                'Reactivar'
                              )
                            )
                          )
                        )
                      )
                    ) :
                    React.createElement('div', { className: 'text-center py-4 text-muted' },
                      React.createElement('p', null, 'No hay administradores desactivados')
                    )
                )
              )
            )
          )
        ),

        // Agregado: Tab de Empresas Registradas
        React.createElement(Tab, { 
          eventKey: 'empresas', 
          title: React.createElement('span', null,
            React.createElement(FaBuilding, { className: 'me-2' }),
            'Empresas Registradas'
          )
        },
          React.createElement(Card, { className: 'border-0 shadow-sm' },
            React.createElement(Card.Header, { className: 'bg-white border-bottom' },
              React.createElement('h5', { className: 'mb-0 fw-semibold' },
                'Listado de Empresas y Propietarios'
              )
            ),
            React.createElement(Card.Body, { className: 'p-0' },
              empresas.length > 0 ? 
                React.createElement(Table, { hover: true, responsive: true },
                  React.createElement('thead', { className: 'bg-light' },
                    React.createElement('tr', null,
                      React.createElement('th', null, 'Empresa'),
                      React.createElement('th', null, 'Propietario'),
                      React.createElement('th', null, 'Email'),
                      React.createElement('th', null, 'Teléfono'),
                      React.createElement('th', null, 'Plan'),
                      React.createElement('th', null, 'Usuarios'),
                      React.createElement('th', null, 'Estado'),
                      React.createElement('th', null, 'Fecha Registro')
                    )
                  ),
                  React.createElement('tbody', null,
                    empresas.map((empresa) =>
                      React.createElement('tr', { key: empresa.id_empresa },
                        React.createElement('td', null,
                          React.createElement('div', null,
                            React.createElement('div', { className: 'fw-semibold' },
                              empresa.nombre_comercial
                            ),
                            empresa.razon_social && 
                            React.createElement('small', { className: 'text-muted' },
                              empresa.razon_social
                            )
                          )
                        ),
                        React.createElement('td', null,
                          empresa.propietario ? 
                            React.createElement('div', null,
                              React.createElement('div', { className: 'fw-medium' },
                                empresa.propietario.nombre_completo
                              ),
                              !empresa.propietario.activo && 
                              React.createElement(Badge, { bg: 'secondary', className: 'small' },
                                'Inactivo'
                              )
                            ) :
                            React.createElement('span', { className: 'text-muted' }, 'Sin propietario')
                        ),
                        React.createElement('td', null,
                          empresa.propietario?.email || empresa.email || '-'
                        ),
                        React.createElement('td', null,
                          empresa.propietario?.telefono || empresa.telefono || '-'
                        ),
                        React.createElement('td', null,
                          empresa.plan_actual ? 
                            React.createElement(Badge, {
                              bg: empresa.plan_actual.id_plan === 'FREE' ? 'light' :
                                  empresa.plan_actual.id_plan === 'BASIC' ? 'primary' : 'dark',
                              text: empresa.plan_actual.id_plan === 'FREE' ? 'dark' : 'white'
                            }, empresa.plan_actual.nombre) :
                            React.createElement(Badge, { bg: 'secondary' }, 'Sin plan')
                        ),
                        React.createElement('td', null,
                          React.createElement('div', null,
                            React.createElement('strong', null, 
                              empresa.estadisticas?.usuarios_activos || 0
                            ),
                            React.createElement('span', { className: 'text-muted' },
                              '/', empresa.estadisticas?.total_usuarios || 0
                            )
                          )
                        ),
                        React.createElement('td', null,
                          React.createElement(Badge, { bg: empresa.activo ? 'success' : 'secondary' },
                            empresa.activo ? 'Activa' : 'Inactiva'
                          )
                        ),
                        React.createElement('td', null,
                          empresa.fecha_registro ? 
                            new Date(empresa.fecha_registro).toLocaleDateString() : '-'
                        )
                      )
                    )
                  )
                ) :
                React.createElement('div', { className: 'text-center py-4 text-muted' },
                  React.createElement('p', null, 'No hay empresas registradas')
                )
            )
          )
        )
      )
    ),

    React.createElement(Modal, { 
      show: showAdminModal, 
      onHide: handleCloseAdminModal, 
      centered: true 
    },
      React.createElement(Modal.Header, { closeButton: true },
        React.createElement(Modal.Title, null,
          editingAdmin ? 'Editar Administrador' : 'Nuevo Administrador'
        )
      ),
      React.createElement(Modal.Body, null,
        React.createElement('div', { className: 'mb-3' },
          React.createElement('label', { className: 'form-label' }, 'Nombre *'),
          React.createElement('input', {
            type: 'text',
            className: `form-control ${formErrors.nombre ? 'is-invalid' : ''}`,
            value: adminFormData.nombre,
            onChange: (e) => setAdminFormData({...adminFormData, nombre: e.target.value})
          }),
          formErrors.nombre && React.createElement('div', { className: 'invalid-feedback d-block' }, 
            formErrors.nombre
          )
        ),

        React.createElement('div', { className: 'mb-3' },
          React.createElement('label', { className: 'form-label' }, 'Email *'),
          React.createElement('input', {
            type: 'email',
            className: `form-control ${formErrors.email ? 'is-invalid' : ''}`,
            value: adminFormData.email,
            onChange: (e) => setAdminFormData({...adminFormData, email: e.target.value})
          }),
          formErrors.email && React.createElement('div', { className: 'invalid-feedback d-block' }, 
            formErrors.email
          )
        ),

        React.createElement('div', { className: 'mb-3' },
          React.createElement('label', { className: 'form-label' }, 
            editingAdmin ? 'Nueva Contraseña (dejar vacío para no cambiar)' : 'Contraseña *'
          ),
          React.createElement('input', {
            type: 'password',
            className: `form-control ${formErrors.password ? 'is-invalid' : ''}`,
            value: adminFormData.password,
            onChange: (e) => setAdminFormData({...adminFormData, password: e.target.value})
          }),
          formErrors.password && React.createElement('div', { className: 'invalid-feedback d-block' }, 
            formErrors.password
          )
        ),

        React.createElement('div', { className: 'mb-3' },
          React.createElement('label', { className: 'form-label' }, 'Confirmar Contraseña'),
          React.createElement('input', {
            type: 'password',
            className: `form-control ${formErrors.confirmarPassword ? 'is-invalid' : ''}`,
            value: adminFormData.confirmarPassword,
            onChange: (e) => setAdminFormData({...adminFormData, confirmarPassword: e.target.value})
          }),
          formErrors.confirmarPassword && React.createElement('div', { className: 'invalid-feedback d-block' }, 
            formErrors.confirmarPassword
          )
        )
      ),
      React.createElement(Modal.Footer, null,
        React.createElement(Button, { variant: 'secondary', onClick: handleCloseAdminModal }, 
          'Cancelar'
        ),
        React.createElement(Button, { 
          variant: 'primary', 
          onClick: handleSubmitAdmin 
        }, 
          editingAdmin ? 'Actualizar' : 'Crear'
        )
      )
    ),

    React.createElement(Modal, { 
      show: showConfirmModal, 
      onHide: () => setShowConfirmModal(false), 
      centered: true 
    },
      React.createElement(Modal.Header, { closeButton: true },
        React.createElement(Modal.Title, null, 'Confirmar Desactivación')
      ),
      React.createElement(Modal.Body, null,
        React.createElement('p', null, 
          '¿Estás seguro de que deseas desactivar al administrador ',
          React.createElement('strong', null, adminToDelete?.nombre),
          '?'
        ),
        React.createElement(Alert, { variant: 'warning', className: 'mb-0' },
          React.createElement('small', null, 
            'El administrador no podrá acceder al sistema hasta que sea reactivado.'
          )
        )
      ),
      React.createElement(Modal.Footer, null,
        React.createElement(Button, { 
          variant: 'secondary', 
          onClick: () => setShowConfirmModal(false) 
        }, 
          'Cancelar'
        ),
        React.createElement(Button, { variant: 'danger', onClick: confirmDesactivar }, 
          'Sí, Desactivar'
        )
      )
    )
  );
};

export default SaasAdminPanel;