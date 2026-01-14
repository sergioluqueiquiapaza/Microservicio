// src/pages/auth/LoginPage.jsx
import React, { useState } from 'react';
import { Container, Row, Col, Card, Button, Form, Alert, Spinner } from 'react-bootstrap';
import { FaUser, FaUserShield, FaEnvelope, FaLock, FaArrowLeft } from 'react-icons/fa';
import { useAuth } from '../../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import './LoginPage.css';

const LoginPage = () => {
  const { loginUsuario, loginAdminSaas } = useAuth();
  const navigate = useNavigate();
  
  const [loginType, setLoginType] = useState(null);
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    if (!formData.email || !formData.password) {
      setError('Por favor completa todos los campos');
      setLoading(false);
      return;
    }

    try {
      let result;
      if (loginType === 'empresa') {
        result = await loginUsuario(formData.email, formData.password);
      } else {
        result = await loginAdminSaas(formData.email, formData.password);
      }

      if (!result.success) {
        setError(result.error);
      }
    } catch (err) {
      setError('Error de conexión');
    } finally {
      setLoading(false);
    }
  };

  const handleBack = () => {
    setLoginType(null);
    setError('');
    setFormData({ email: '', password: '' });
  };

  return (
    <div className="login-page">
      <Container>
        <Row className="justify-content-center align-items-center min-vh-100">
          <Col md={8} lg={6} xl={5}>
            <div className="text-center mb-4">
              <Button 
                variant="link" 
                onClick={() => navigate('/')}
                className="text-decoration-none"
              >
                <FaArrowLeft className="me-2" />
                Volver al inicio
              </Button>
            </div>

            <Card className="shadow-lg border-0">
              <Card.Body className="p-5">
                {!loginType ? (
                  <>
                    <h3 className="text-center mb-4 fw-bold">
                      Selecciona tu tipo de acceso
                    </h3>
                    <div className="d-grid gap-3">
                      <Button
                        variant="outline-primary"
                        size="lg"
                        className="py-3 d-flex align-items-center justify-content-start gap-3"
                        onClick={() => setLoginType('empresa')}
                      >
                        <FaUser size={28} />
                        <div className="text-start">
                          <div className="fw-semibold">Usuario de Empresa</div>
                          <small className="text-muted">Accede a tu sistema empresarial</small>
                        </div>
                      </Button>

                      <Button
                        variant="outline-dark"
                        size="lg"
                        className="py-3 d-flex align-items-center justify-content-start gap-3"
                        onClick={() => setLoginType('admin_saas')}
                      >
                        <FaUserShield size={28} />
                        <div className="text-start">
                          <div className="fw-semibold">Administrador del Sistema</div>
                          <small className="text-muted">Panel de administración SaaS</small>
                        </div>
                      </Button>
                    </div>
                  </>
                ) : (
                  <>
                    <Button 
                      variant="link" 
                      onClick={handleBack}
                      className="mb-3 text-decoration-none p-0"
                    >
                      <FaArrowLeft className="me-2" />
                      Volver
                    </Button>

                    <h3 className="mb-4 fw-bold">
                      {loginType === 'empresa' ? 'Iniciar Sesión' : 'Acceso Administrativo'}
                    </h3>

                    {loginType === 'admin_saas' && (
                      <Alert variant="warning" className="d-flex align-items-center gap-2">
                        <FaUserShield />
                        <small>Área de acceso restringido</small>
                      </Alert>
                    )}

                    {error && (
                      <Alert variant="danger" dismissible onClose={() => setError('')}>
                        {error}
                      </Alert>
                    )}

                    <Form onSubmit={handleSubmit}>
                      <Form.Group className="mb-3">
                        <Form.Label className="fw-medium">
                          <FaEnvelope className="me-2" />
                          Correo Electrónico
                        </Form.Label>
                        <Form.Control
                          type="email"
                          name="email"
                          placeholder="tu@correo.com"
                          value={formData.email}
                          onChange={handleChange}
                          disabled={loading}
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

                      <Button
                        type="submit"
                        variant={loginType === 'admin_saas' ? 'dark' : 'primary'}
                        className="w-100 py-2 mt-3"
                        disabled={loading}
                      >
                        {loading ? (
                          <>
                            <Spinner animation="border" size="sm" className="me-2" />
                            Ingresando...
                          </>
                        ) : (
                          loginType === 'admin_saas' ? 'Acceso Seguro' : 'Iniciar Sesión'
                        )}
                      </Button>
                    </Form>
                  </>
                )}
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </Container>
    </div>
  );
};

export default LoginPage;