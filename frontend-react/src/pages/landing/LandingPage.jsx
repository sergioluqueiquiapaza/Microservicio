// src/pages/landing/LandingPage.jsx
import React, { useState } from 'react';
import { Container, Navbar, Nav, Button, Row, Col, Card } from 'react-bootstrap';
import {
  FaChartLine,
  FaBoxes,
  FaUsers,
  FaCheckCircle,
  FaRocket
} from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import LoginModal from '../../components/auth/LoginModal';
import './LandingPage.css';

const LandingPage = () => {
  const navigate = useNavigate();
  const [showLoginModal, setShowLoginModal] = useState(false);

  const features = [
    {
      icon: <FaBoxes size={40} />,
      title: 'Gestión de Inventario',
      description: 'Control completo de productos, stock y categorías en tiempo real'
    },
    {
      icon: <FaChartLine size={40} />,
      title: 'Reportes Avanzados',
      description: 'Analiza tus ventas y toma decisiones basadas en datos'
    },
    {
      icon: <FaUsers size={40} />,
      title: 'Gestión de Usuarios',
      description: 'Administra roles y permisos de tu equipo fácilmente'
    }
  ];

  const plans = [
    {
      name: 'FREE',
      price: '0',
      features: ['3 Usuarios', '50 Productos', 'Reportes Básicos'],
      variant: 'outline-primary'
    },
    {
      name: 'BASIC',
      price: '49.99',
      features: ['5 Usuarios', '200 Productos', 'Reportes Básicos', 'Soporte Email'],
      variant: 'outline-success',
      popular: true
    },
    {
      name: 'PREMIUM',
      price: '99.99',
      features: ['10 Usuarios', '1000 Productos', 'Reportes Avanzados', 'Soporte Prioritario'],
      variant: 'outline-dark'
    }
  ];

  return (
    <div className="landing-page">
      {/* NAVBAR */}
      <Navbar bg="white" expand="lg" className="shadow-sm sticky-top">
        <Container>
          <Navbar.Brand className="fw-bold fs-4" style={{ cursor: 'pointer' }} onClick={() => navigate('/')}>
            <FaRocket className="me-2 text-primary" />
            Sistema SaaS
          </Navbar.Brand>
          <Navbar.Toggle aria-controls="navbar-nav" />
          <Navbar.Collapse id="navbar-nav">
            <Nav className="ms-auto align-items-center gap-3">
              <Nav.Link href="#features">Características</Nav.Link>
              <Nav.Link href="#plans">Planes</Nav.Link>
              <Button
                variant="outline-primary"
                onClick={() => setShowLoginModal(true)}
              >
                Iniciar Sesión
              </Button>
              <Button
                variant="primary"
                onClick={() => navigate('/registro-empresa')}
              >
                Registrar Empresa
              </Button>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>

      {/* HERO SECTION */}
      <section className="hero-section py-5 bg-light">
        <Container>
          <Row className="align-items-center min-vh-75">
            <Col lg={6} className="text-center text-lg-start">
              <h1 className="display-3 fw-bold mb-4">
                Gestiona tu empresa
                <span className="text-primary"> en la nube</span>
              </h1>
              <p className="lead text-muted mb-4">
                Sistema completo de inventario, ventas y gestión empresarial.
                Accede desde cualquier lugar, en cualquier momento.
              </p>
              <div className="d-flex gap-3 justify-content-center justify-content-lg-start">
                <Button 
                  variant="primary" 
                  size="lg" 
                  onClick={() => navigate('/registro-empresa')}
                >
                  Comenzar Gratis
                </Button>
                <Button
                  variant="outline-primary"
                  size="lg"
                  onClick={() => setShowLoginModal(true)}
                >
                  Ver Demo
                </Button>
              </div>
            </Col>
            <Col lg={6} className="d-none d-lg-block">
              {/* Mockup 3D con Iconos Flotantes */}
              <div className="position-relative" style={{ height: '400px' }}>
                {/* Círculo de fondo */}
                <div 
                  style={{
                    position: 'absolute',
                    width: '350px',
                    height: '350px',
                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                    borderRadius: '50%',
                    top: '50%',
                    left: '50%',
                    transform: 'translate(-50%, -50%)',
                    opacity: '0.1',
                    animation: 'pulse 3s ease-in-out infinite'
                  }}
                />
                
                {/* Tarjeta principal */}
                <div 
                  className="shadow-lg bg-white rounded-3 p-4 position-absolute"
                  style={{
                    width: '280px',
                    top: '50%',
                    left: '50%',
                    transform: 'translate(-50%, -50%)',
                    animation: 'float 3s ease-in-out infinite'
                  }}
                >
                  <div className="d-flex align-items-center gap-3 mb-3">
                    <div 
                      className="bg-primary bg-opacity-10 p-3 rounded-circle"
                      style={{ width: '60px', height: '60px' }}
                    >
                      <FaChartLine size={30} className="text-primary" />
                    </div>
                    <div>
                      <div className="fw-bold">Ventas del Mes</div>
                      <div className="text-success fw-bold fs-4">+24.5%</div>
                    </div>
                  </div>
                  <div className="bg-light rounded p-2 mb-2">
                    <div className="d-flex justify-content-between mb-1">
                      <small className="text-muted">Productos</small>
                      <small className="fw-semibold">156</small>
                    </div>
                    <div style={{ height: '4px', background: '#e9ecef', borderRadius: '2px' }}>
                      <div style={{ width: '75%', height: '100%', background: '#0d6efd', borderRadius: '2px' }}></div>
                    </div>
                  </div>
                  <div className="bg-light rounded p-2">
                    <div className="d-flex justify-content-between mb-1">
                      <small className="text-muted">Clientes</small>
                      <small className="fw-semibold">48</small>
                    </div>
                    <div style={{ height: '4px', background: '#e9ecef', borderRadius: '2px' }}>
                      <div style={{ width: '60%', height: '100%', background: '#198754', borderRadius: '2px' }}></div>
                    </div>
                  </div>
                </div>

                {/* Tarjeta flotante 1 - Superior derecha */}
                <div 
                  className="shadow bg-white rounded-3 p-3 position-absolute"
                  style={{
                    width: '140px',
                    top: '10%',
                    right: '5%',
                    animation: 'float 4s ease-in-out infinite 0.5s'
                  }}
                >
                  <div className="text-center">
                    <FaBoxes size={24} className="text-success mb-2" />
                    <div className="small text-muted">Inventario</div>
                    <div className="fw-bold">En Tiempo Real</div>
                  </div>
                </div>

                {/* Tarjeta flotante 2 - Inferior izquierda */}
                <div 
                  className="shadow bg-white rounded-3 p-3 position-absolute"
                  style={{
                    width: '140px',
                    bottom: '10%',
                    left: '5%',
                    animation: 'float 4s ease-in-out infinite 1s'
                  }}
                >
                  <div className="text-center">
                    <FaUsers size={24} className="text-primary mb-2" />
                    <div className="small text-muted">Usuarios</div>
                    <div className="fw-bold">Multi-Rol</div>
                  </div>
                </div>

                {/* Añadir animaciones CSS */}
                <style>
                  {`
                    @keyframes float {
                      0%, 100% { transform: translate(-50%, -50%) translateY(0); }
                      50% { transform: translate(-50%, -50%) translateY(-20px); }
                    }
                    @keyframes pulse {
                      0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.1; }
                      50% { transform: translate(-50%, -50%) scale(1.05); opacity: 0.15; }
                    }
                  `}
                </style>
              </div>
            </Col>
          </Row>
        </Container>
      </section>

      {/* FEATURES SECTION */}
      <section id="features" className="py-5">
        <Container>
          <h2 className="text-center mb-5 fw-bold">
            Todo lo que necesitas para crecer
          </h2>
          <Row className="g-4">
            {features.map((feature, index) => (
              <Col md={4} key={index}>
                <Card className="h-100 border-0 shadow-sm text-center p-4">
                  <Card.Body>
                    <div className="text-primary mb-3">
                      {feature.icon}
                    </div>
                    <Card.Title className="fw-semibold">
                      {feature.title}
                    </Card.Title>
                    <Card.Text className="text-muted">
                      {feature.description}
                    </Card.Text>
                  </Card.Body>
                </Card>
              </Col>
            ))}
          </Row>
        </Container>
      </section>

      {/* PLANS SECTION */}
      <section id="plans" className="py-5 bg-light">
        <Container>
          <h2 className="text-center mb-5 fw-bold">
            Elige el plan perfecto para ti
          </h2>
          <Row className="g-4 justify-content-center">
            {plans.map((plan, index) => (
              <Col md={4} key={index}>
                <Card className={`h-100 ${plan.popular ? 'border-success shadow' : 'border-0 shadow-sm'}`}>
                  {plan.popular && (
                    <div className="bg-success text-white text-center py-1 small fw-medium">
                      Más Popular
                    </div>
                  )}
                  <Card.Body className="text-center p-4">
                    <h4 className="fw-bold mb-3">{plan.name}</h4>
                    <div className="mb-4">
                      <span className="display-4 fw-bold">{plan.price}</span>
                      <span className="text-muted"> Bs/mes</span>
                    </div>
                    <ul className="list-unstyled mb-4">
                      {plan.features.map((feature, i) => (
                        <li key={i} className="mb-2">
                          <FaCheckCircle className="text-success me-2" />
                          {feature}
                        </li>
                      ))}
                    </ul>
                    <Button
                      variant={plan.variant}
                      className="w-100"
                      size="lg"
                      onClick={() => navigate('/registro-empresa')}
                    >
                      {plan.name === 'FREE' ? 'Comenzar Gratis' : 'Seleccionar Plan'}
                    </Button>
                  </Card.Body>
                </Card>
              </Col>
            ))}
          </Row>
        </Container>
      </section>

      {/* FOOTER */}
      <footer className="bg-dark text-white py-4">
        <Container>
          <Row>
            <Col md={6}>
              <p className="mb-0">
                © 2025 Sistema SaaS. Todos los derechos reservados.
              </p>
            </Col>
            <Col md={6} className="text-md-end">
              <Nav className="justify-content-md-end">
                <Nav.Link href="#" className="text-white">Términos</Nav.Link>
                <Nav.Link href="#" className="text-white">Privacidad</Nav.Link>
                <Nav.Link href="#" className="text-white">Contacto</Nav.Link>
              </Nav>
            </Col>
          </Row>
        </Container>
      </footer>

      {/* MODAL DE LOGIN */}
      <LoginModal
        show={showLoginModal}
        handleClose={() => setShowLoginModal(false)}
      />
    </div>
  );
};

export default LandingPage;