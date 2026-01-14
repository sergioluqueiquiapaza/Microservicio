// src/pages/auth/RegistroEmpresaPage.jsx
import React, { useState } from 'react';
import { Container, Row, Col, Card, Form, Button, Alert, Spinner } from 'react-bootstrap';
import { FaBuilding, FaUser, FaEnvelope, FaLock, FaPhone, FaArrowLeft } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import api from '../../services/api';

const RegistroEmpresaPage = () => {
  const navigate = useNavigate();
  const { loginUsuario } = useAuth();
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    nombre_empresa: '',
    nombres: '',
    paterno: '',
    materno: '',
    email: '',
    password: '',
    confirmarPassword: '',
    telefono: ''
  });
  const [formErrors, setFormErrors] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
    
    // Limpiar error del campo al escribir
    if (formErrors[name]) {
      setFormErrors({ ...formErrors, [name]: '' });
    }
  };

  const validateForm = () => {
    const errors = {};

    // Validar nombre de empresa
    if (!formData.nombre_empresa.trim()) {
      errors.nombre_empresa = 'El nombre de la empresa es obligatorio';
    }

    // Validar nombres
    if (!formData.nombres.trim()) {
      errors.nombres = 'Los nombres son obligatorios';
    }

    // Validar apellido paterno
    if (!formData.paterno.trim()) {
      errors.paterno = 'El apellido paterno es obligatorio';
    }

    // Validar email
    if (!formData.email.trim()) {
      errors.email = 'El email es obligatorio';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      errors.email = 'El email no es válido';
    }

    // Validar contraseña
    if (!formData.password) {
      errors.password = 'La contraseña es obligatoria';
    } else if (formData.password.length < 6) {
      errors.password = 'La contraseña debe tener al menos 6 caracteres';
    }

    // Validar confirmación de contraseña
    if (formData.password !== formData.confirmarPassword) {
      errors.confirmarPassword = 'Las contraseñas no coinciden';
    }

    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!validateForm()) {
      return;
    }

    setLoading(true);

    try {
      // Preparar datos para enviar (sin confirmarPassword)
      const dataToSend = {
        nombre_empresa: formData.nombre_empresa,
        nombres: formData.nombres,
        paterno: formData.paterno,
        materno: formData.materno,
        email: formData.email,
        password: formData.password,
        telefono: formData.telefono
      };

      // Llamar al endpoint de registro
      const response = await api.post('/auth/registro-empresa', dataToSend);

      if (response.data.token) {
        // Guardar token y datos del usuario
        localStorage.setItem('token', response.data.token);
        localStorage.setItem('user', JSON.stringify(response.data.usuario));
        localStorage.setItem('userType', 'empresa');

        // Redirigir al dashboard
        navigate('/dashboard');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Error al registrar la empresa');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="registro-empresa-page min-vh-100 d-flex align-items-center" 
         style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}>
      <Container>
        <Row className="justify-content-center">
          <Col md={10} lg={8}>
            <div className="text-center mb-4">
              <Button
                variant="link"
                onClick={() => navigate('/')}
                className="text-white text-decoration-none"
              >
                <FaArrowLeft className="me-2" />
                Volver al inicio
              </Button>
            </div>

            <Card className="shadow-lg border-0">
              <Card.Body className="p-5">
                <div className="text-center mb-4">
                  <h2 className="fw-bold mb-2">Registra tu Empresa</h2>
                  <p className="text-muted">
                    Comienza gratis con el Plan FREE - Sin tarjeta de crédito
                  </p>
                </div>

                {error && (
                  <Alert variant="danger" dismissible onClose={() => setError('')}>
                    {error}
                  </Alert>
                )}

                <Form onSubmit={handleSubmit}>
                  {/* Sección: Datos de la Empresa */}
                  <div className="mb-4">
                    <h5 className="fw-semibold mb-3 text-primary">
                      <FaBuilding className="me-2" />
                      Datos de la Empresa
                    </h5>

                    <Form.Group className="mb-3">
                      <Form.Label className="fw-medium">Nombre de la Empresa *</Form.Label>
                      <Form.Control
                        type="text"
                        name="nombre_empresa"
                        placeholder="Ej: Mi Empresa S.A."
                        value={formData.nombre_empresa}
                        onChange={handleChange}
                        isInvalid={!!formErrors.nombre_empresa}
                        disabled={loading}
                      />
                      <Form.Control.Feedback type="invalid">
                        {formErrors.nombre_empresa}
                      </Form.Control.Feedback>
                    </Form.Group>
                  </div>

                  {/* Sección: Datos del Propietario */}
                  <div className="mb-4">
                    <h5 className="fw-semibold mb-3 text-primary">
                      <FaUser className="me-2" />
                      Datos del Propietario
                    </h5>

                    <Row>
                      <Col md={12} className="mb-3">
                        <Form.Group>
                          <Form.Label className="fw-medium">Nombres *</Form.Label>
                          <Form.Control
                            type="text"
                            name="nombres"
                            placeholder="Ej: Juan Carlos"
                            value={formData.nombres}
                            onChange={handleChange}
                            isInvalid={!!formErrors.nombres}
                            disabled={loading}
                          />
                          <Form.Control.Feedback type="invalid">
                            {formErrors.nombres}
                          </Form.Control.Feedback>
                        </Form.Group>
                      </Col>

                      <Col md={6} className="mb-3">
                        <Form.Group>
                          <Form.Label className="fw-medium">Apellido Paterno *</Form.Label>
                          <Form.Control
                            type="text"
                            name="paterno"
                            placeholder="Ej: Pérez"
                            value={formData.paterno}
                            onChange={handleChange}
                            isInvalid={!!formErrors.paterno}
                            disabled={loading}
                          />
                          <Form.Control.Feedback type="invalid">
                            {formErrors.paterno}
                          </Form.Control.Feedback>
                        </Form.Group>
                      </Col>

                      <Col md={6} className="mb-3">
                        <Form.Group>
                          <Form.Label className="fw-medium">Apellido Materno</Form.Label>
                          <Form.Control
                            type="text"
                            name="materno"
                            placeholder="Ej: García (opcional)"
                            value={formData.materno}
                            onChange={handleChange}
                            disabled={loading}
                          />
                        </Form.Group>
                      </Col>

                      <Col md={6} className="mb-3">
                        <Form.Group>
                          <Form.Label className="fw-medium">
                            <FaEnvelope className="me-2" />
                            Email *
                          </Form.Label>
                          <Form.Control
                            type="email"
                            name="email"
                            placeholder="tu@correo.com"
                            value={formData.email}
                            onChange={handleChange}
                            isInvalid={!!formErrors.email}
                            disabled={loading}
                          />
                          <Form.Control.Feedback type="invalid">
                            {formErrors.email}
                          </Form.Control.Feedback>
                          <Form.Text className="text-muted">
                            Será tu usuario de acceso
                          </Form.Text>
                        </Form.Group>
                      </Col>

                      <Col md={6} className="mb-3">
                        <Form.Group>
                          <Form.Label className="fw-medium">
                            <FaPhone className="me-2" />
                            Teléfono
                          </Form.Label>
                          <Form.Control
                            type="tel"
                            name="telefono"
                            placeholder="70123456"
                            value={formData.telefono}
                            onChange={handleChange}
                            disabled={loading}
                          />
                        </Form.Group>
                      </Col>
                    </Row>
                  </div>

                  {/* Sección: Contraseña */}
                  <div className="mb-4">
                    <h5 className="fw-semibold mb-3 text-primary">
                      <FaLock className="me-2" />
                      Seguridad
                    </h5>

                    <Row>
                      <Col md={6} className="mb-3">
                        <Form.Group>
                          <Form.Label className="fw-medium">Contraseña *</Form.Label>
                          <Form.Control
                            type="password"
                            name="password"
                            placeholder="Mínimo 6 caracteres"
                            value={formData.password}
                            onChange={handleChange}
                            isInvalid={!!formErrors.password}
                            disabled={loading}
                          />
                          <Form.Control.Feedback type="invalid">
                            {formErrors.password}
                          </Form.Control.Feedback>
                        </Form.Group>
                      </Col>

                      <Col md={6} className="mb-3">
                        <Form.Group>
                          <Form.Label className="fw-medium">Confirmar Contraseña *</Form.Label>
                          <Form.Control
                            type="password"
                            name="confirmarPassword"
                            placeholder="Repite tu contraseña"
                            value={formData.confirmarPassword}
                            onChange={handleChange}
                            isInvalid={!!formErrors.confirmarPassword}
                            disabled={loading}
                          />
                          <Form.Control.Feedback type="invalid">
                            {formErrors.confirmarPassword}
                          </Form.Control.Feedback>
                        </Form.Group>
                      </Col>
                    </Row>
                  </div>

                  {/* Plan Incluido */}
                  <Alert variant="success" className="mb-4">
                    <div className="d-flex align-items-center">
                      <div className="me-3 fs-3">🎉</div>
                      <div>
                        <strong>Plan FREE Incluido</strong>
                        <div className="small">
                          ✓ Hasta 3 usuarios &nbsp;|&nbsp; ✓ Hasta 50 productos &nbsp;|&nbsp; ✓ Soporte básico
                        </div>
                      </div>
                    </div>
                  </Alert>

                  {/* Términos */}
                  <Form.Group className="mb-4">
                    <Form.Check
                      type="checkbox"
                      label={
                        <span className="small">
                          Acepto los{' '}
                          <a href="#" className="text-decoration-none">
                            Términos y Condiciones
                          </a>{' '}
                          y la{' '}
                          <a href="#" className="text-decoration-none">
                            Política de Privacidad
                          </a>
                        </span>
                      }
                      required
                      disabled={loading}
                    />
                  </Form.Group>

                  {/* Botones */}
                  <div className="d-grid gap-2">
                    <Button
                      type="submit"
                      variant="primary"
                      size="lg"
                      disabled={loading}
                    >
                      {loading ? (
                        <>
                          <Spinner
                            as="span"
                            animation="border"
                            size="sm"
                            className="me-2"
                          />
                          Creando cuenta...
                        </>
                      ) : (
                        'Crear mi Cuenta Gratis'
                      )}
                    </Button>
                  </div>

                  {/* Link a login */}
                  <div className="text-center mt-3">
                    <small className="text-muted">
                      ¿Ya tienes una cuenta?{' '}
                      <a
                        href="#"
                        onClick={(e) => {
                          e.preventDefault();
                          navigate('/login');
                        }}
                        className="text-decoration-none"
                      >
                        Inicia sesión
                      </a>
                    </small>
                  </div>
                </Form>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </Container>
    </div>
  );
};

export default RegistroEmpresaPage;