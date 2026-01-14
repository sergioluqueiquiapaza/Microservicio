// src/components/layout/DashboardHeader.jsx
import React, { useState } from 'react';
import { Navbar, Container, Nav, Dropdown, Badge, Button } from 'react-bootstrap';
import { 
  FaBell, 
  FaUser, 
  FaCog, 
  FaSignOutAlt,
  FaBuilding,
  FaSearch
} from 'react-icons/fa';
import { useAuth } from '../../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import './DashboardHeader.css';

const DashboardHeader = () => {
  const { user, logout, getUserRole, isEmpresaUser } = useAuth();
  const navigate = useNavigate();
  const [showSearch, setShowSearch] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  // Obtener el rol formateado para mostrar
  const getRoleName = () => {
    const role = getUserRole();
    const roleNames = {
      'PROPIETARIO': 'Propietario',
      'ADMIN': 'Administrador',
      'VENDEDOR': 'Vendedor'
    };
    return roleNames[role] || role;
  };

  // Obtener badge variant según el rol
  const getRoleBadgeVariant = () => {
    const role = getUserRole();
    const variants = {
      'PROPIETARIO': 'primary',
      'ADMIN': 'success',
      'VENDEDOR': 'info'
    };
    return variants[role] || 'secondary';
  };

  return (
    <Navbar bg="white" className="shadow-sm dashboard-header sticky-top">
      <Container fluid className="px-4">
        {/* Logo y nombre de empresa */}
        <Navbar.Brand className="d-flex align-items-center gap-2">
          <FaBuilding className="text-primary" size={24} />
          <div className="d-none d-md-block">
            <div className="fw-bold">Sistema SaaS</div>
            {isEmpresaUser() && (
              <small className="text-muted">
                {user?.id_empresa || 'Mi Empresa'}
              </small>
            )}
          </div>
        </Navbar.Brand>

        {/* Barra de búsqueda */}
        <div className="flex-grow-1 mx-3 d-none d-lg-block">
          <div className="search-container position-relative">
            <FaSearch className="search-icon" />
            <input
              type="text"
              className="form-control search-input"
              placeholder="Buscar productos, clientes, ventas..."
            />
          </div>
        </div>

        {/* Botón de búsqueda móvil */}
        <Button
          variant="link"
          className="d-lg-none text-dark"
          onClick={() => setShowSearch(!showSearch)}
        >
          <FaSearch size={20} />
        </Button>

        {/* Iconos de la derecha */}
        <Nav className="align-items-center gap-2">
          {/* Notificaciones */}
          <Dropdown align="end">
            <Dropdown.Toggle 
              variant="link" 
              className="nav-icon-btn position-relative"
              id="notifications-dropdown"
            >
              <FaBell size={20} />
              <Badge 
                bg="danger" 
                pill 
                className="position-absolute top-0 start-100 translate-middle"
              >
                3
              </Badge>
            </Dropdown.Toggle>

            <Dropdown.Menu className="notification-menu shadow">
              <Dropdown.Header>Notificaciones (3)</Dropdown.Header>
              <Dropdown.Divider />
              
              <Dropdown.Item className="notification-item">
                <div className="d-flex gap-2">
                  <div className="notification-icon bg-warning-subtle">
                    ⚠️
                  </div>
                  <div className="flex-grow-1">
                    <div className="fw-medium small">Stock bajo</div>
                    <div className="text-muted small">
                      Producto X tiene solo 3 unidades
                    </div>
                    <div className="text-muted" style={{fontSize: '0.75rem'}}>
                      Hace 2 horas
                    </div>
                  </div>
                </div>
              </Dropdown.Item>

              <Dropdown.Item className="notification-item">
                <div className="d-flex gap-2">
                  <div className="notification-icon bg-success-subtle">
                    💰
                  </div>
                  <div className="flex-grow-1">
                    <div className="fw-medium small">Nueva venta</div>
                    <div className="text-muted small">
                      Venta registrada por 150 Bs
                    </div>
                    <div className="text-muted" style={{fontSize: '0.75rem'}}>
                      Hace 5 horas
                    </div>
                  </div>
                </div>
              </Dropdown.Item>

              <Dropdown.Item className="notification-item">
                <div className="d-flex gap-2">
                  <div className="notification-icon bg-info-subtle">
                    📦
                  </div>
                  <div className="flex-grow-1">
                    <div className="fw-medium small">Compra recibida</div>
                    <div className="text-muted small">
                      Proveedor ABC - 50 productos
                    </div>
                    <div className="text-muted" style={{fontSize: '0.75rem'}}>
                      Ayer
                    </div>
                  </div>
                </div>
              </Dropdown.Item>

              <Dropdown.Divider />
              <Dropdown.Item className="text-center text-primary small">
                Ver todas las notificaciones
              </Dropdown.Item>
            </Dropdown.Menu>
          </Dropdown>

          {/* Perfil de usuario */}
          <Dropdown align="end">
            <Dropdown.Toggle 
              variant="link" 
              className="nav-profile-btn d-flex align-items-center gap-2"
              id="user-dropdown"
            >
              <div className="user-avatar">
                <FaUser />
              </div>
              <div className="d-none d-md-block text-start">
                <div className="fw-medium small">
                  {user?.nombres || user?.nombre || 'Usuario'}
                </div>
                <Badge bg={getRoleBadgeVariant()} className="small">
                  {getRoleName()}
                </Badge>
              </div>
            </Dropdown.Toggle>

            <Dropdown.Menu className="shadow">
              <Dropdown.Header>
                <div className="fw-bold">
                  {user?.nombre_completo_str || user?.nombres || 'Usuario'}
                </div>
                <div className="text-muted small">
                  {user?.email || 'email@ejemplo.com'}
                </div>
              </Dropdown.Header>
              
              <Dropdown.Divider />
              
              <Dropdown.Item onClick={() => navigate('/dashboard/mi-perfil')}>
                <FaUser className="me-2" />
                Mi Perfil
              </Dropdown.Item>
              
              {/* Solo para PROPIETARIO */}
              {getUserRole() === 'PROPIETARIO' && (
                <Dropdown.Item onClick={() => navigate('/dashboard/configuracion/empresa')}>
                  <FaCog className="me-2" />
                  Configuración
                </Dropdown.Item>
              )}
              
              <Dropdown.Divider />
              
              <Dropdown.Item 
                onClick={handleLogout}
                className="text-danger"
              >
                <FaSignOutAlt className="me-2" />
                Cerrar Sesión
              </Dropdown.Item>
            </Dropdown.Menu>
          </Dropdown>
        </Nav>
      </Container>

      {/* Barra de búsqueda móvil expandible */}
      {showSearch && (
        <div className="w-100 p-3 border-top d-lg-none">
          <div className="search-container position-relative">
            <FaSearch className="search-icon" />
            <input
              type="text"
              className="form-control search-input"
              placeholder="Buscar..."
              autoFocus
            />
          </div>
        </div>
      )}
    </Navbar>
  );
};

export default DashboardHeader;