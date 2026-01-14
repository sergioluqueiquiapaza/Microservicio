// src/components/auth/LoginModal.jsx
import React, { useState } from 'react';
import { Modal, Button, Form, Alert, Spinner } from 'react-bootstrap';
import { FaUser, FaUserShield, FaEnvelope, FaLock } from 'react-icons/fa';
import { useAuth } from '../../context/AuthContext';

const LoginModal = ({ show, handleClose }) => {
  const { loginUsuario, loginAdminSaas } = useAuth();
  
  // Estado para controlar qué tipo de login mostrar
  const [loginType, setLoginType] = useState(null); // null, 'empresa', 'admin_saas'
  
  // Estados del formulario
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Manejar cambios en inputs
  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
    setError(''); // Limpiar error al escribir
  };

  // Manejar envío del formulario
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    // Validaciones básicas
    if (!formData.email || !formData.password) {
      setError('Por favor completa todos los campos');
      setLoading(false);
      return;
    }

    try {
      let result;
      
      if (loginType === 'empresa') {
        result = await loginUsuario(formData.email, formData.password);
      } else if (loginType === 'admin_saas') {
        result = await loginAdminSaas(formData.email, formData.password);
      }

      if (!result.success) {
        setError(result.error);
      } else {
        // Login exitoso - el redirect lo maneja AuthContext
        handleClose();
        resetForm();
      }
    } catch (err) {
      setError('Error de conexión. Intenta nuevamente.');
    } finally {
      setLoading(false);
    }
  };

  // Resetear formulario
  const resetForm = () => {
    setFormData({ email: '', password: '' });
    setError('');
    setLoginType(null);
  };

  // Volver a la selección de tipo
  const handleBack = () => {
    setLoginType(null);
    setError('');
    setFormData({ email: '', password: '' });
  };

  // Cerrar modal y resetear
  const handleModalClose = () => {
    resetForm();
    handleClose();
  };

  return (
    <Modal 
      show={show} 
      onHide={handleModalClose} 
      centered
      backdrop="static"
    >
      <Modal.Header closeButton className="border-0 pb-0">
        <Modal.Title className="w-100 text-center">
          {loginType ? (
            <div>
              <Button 
                variant="link" 
                onClick={handleBack}
                className="position-absolute start-0 top-0 mt-3 ms-3 text-decoration-none"
              >
                ← Volver
              </Button>
              <h4 className="mb-0 mt-2">
                {loginType === 'empresa' ? 'Iniciar Sesión' : 'Acceso Administrativo'}
              </h4>
            </div>
          ) : (
            <h4 className="mb-0">Selecciona tu tipo de acceso</h4>
          )}
        </Modal.Title>
      </Modal.Header>

      <Modal.Body className="px-4 pb-4">
        {!loginType ? (
          // VISTA DE SELECCIÓN DE TIPO
          <div className="d-grid gap-3 mt-3">
            <Button
              variant="outline-primary"
              size="lg"
              className="py-3 d-flex align-items-center justify-content-center gap-3"
              onClick={() => setLoginType('empresa')}
            >
              <FaUser size={24} />
              <div className="text-start">
                <div className="fw-semibold">Usuario de Empresa</div>
                <small className="text-muted">Accede a tu sistema empresarial</small>
              </div>
            </Button>

            <Button
              variant="outline-dark"
              size="lg"
              className="py-3 d-flex align-items-center justify-content-center gap-3"
              onClick={() => setLoginType('admin_saas')}
            >
              <FaUserShield size={24} />
              <div className="text-start">
                <div className="fw-semibold">Administrador del Sistema</div>
                <small className="text-muted">Panel de administración SaaS</small>
              </div>
            </Button>
          </div>
        ) : (
          // VISTA DE FORMULARIO DE LOGIN
          <div>
            {loginType === 'admin_saas' && (
              <Alert variant="warning" className="d-flex align-items-center gap-2 mt-3">
                <FaUserShield />
                <small>Área de acceso restringido para administradores del sistema</small>
              </Alert>
            )}

            {error && (
              <Alert variant="danger" dismissible onClose={() => setError('')}>
                {error}
              </Alert>
            )}

            <Form onSubmit={handleSubmit} className="mt-3">
              <Form.Group className="mb-3">
                <Form.Label className="fw-medium">
                  <FaEnvelope className="me-2" />
                  Correo Electrónico
                </Form.Label>
                <Form.Control
                  type="email"
                  name="email"
                  placeholder={loginType === 'admin_saas' ? 'admin@sistema.com' : 'tu@correo.com'}
                  value={formData.email}
                  onChange={handleChange}
                  disabled={loading}
                  autoFocus
                  required
                />
              </Form.Group>

              <Form.Group className="mb-3">
                <Form.Label className="fw-medium">
                  <FaLock className="me-2" />
                  Contraseña
                </Form.Label>
                <Form.Control
                  type="password"
                  name="password"
                  placeholder="••••••••"
                  value={formData.password}
                  onChange={handleChange}
                  disabled={loading}
                  required
                />
              </Form.Group>

              {loginType === 'empresa' && (
                <div className="text-end mb-3">
                  <a href="#" className="text-decoration-none small">
                    ¿Olvidaste tu contraseña?
                  </a>
                </div>
              )}

              <Button
                type="submit"
                variant={loginType === 'admin_saas' ? 'dark' : 'primary'}
                className="w-100 py-2"
                disabled={loading}
              >
                {loading ? (
                  <>
                    <Spinner
                      as="span"
                      animation="border"
                      size="sm"
                      role="status"
                      className="me-2"
                    />
                    Ingresando...
                  </>
                ) : (
                  loginType === 'admin_saas' ? 'Acceso Seguro' : 'Iniciar Sesión'
                )}
              </Button>
            </Form>

            {loginType === 'empresa' && (
              <div className="text-center mt-3">
                <small className="text-muted">
                  ¿No tienes una cuenta?{' '}
                  <a href="#" className="text-decoration-none">
                    Registra tu empresa
                  </a>
                </small>
              </div>
            )}
          </div>
        )}
      </Modal.Body>
    </Modal>
  );
};

export default LoginModal;