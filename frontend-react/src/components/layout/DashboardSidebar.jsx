// src/components/layout/DashboardSidebar.jsx
import React, { useState } from 'react';
import { Nav, Badge, Collapse } from 'react-bootstrap';
import { NavLink } from 'react-router-dom';
import {
  FaHome,
  FaBoxes,
  FaShoppingCart,
  FaShoppingBag,
  FaUsers,
  FaChartBar,
  FaCog,
  FaBell,
  FaChevronDown,
  FaChevronRight,
  FaList,
  FaTags,
  FaWarehouse,
  FaTruck,
  FaFileInvoiceDollar,
  FaUserFriends,
  FaMoneyBillWave,
  FaUsersCog,
  FaShieldAlt
} from 'react-icons/fa';
import { useAuth } from '../../context/AuthContext';
import './DashboardSidebar.css';

const DashboardSidebar = ({ isOpen, toggleSidebar }) => {
  const { getUserRole } = useAuth();
  const role = getUserRole();

  // Estados para controlar submenús expandibles
  const [openMenus, setOpenMenus] = useState({
    inventario: false,
    ventas: false,
    compras: false,
    reportes: false,
    configuracion: false
  });

  // Toggle de submenús
  const toggleMenu = (menu) => {
    setOpenMenus({
      ...openMenus,
      [menu]: !openMenus[menu]
    });
  };

  // Configuración de menús según rol
  const menuConfig = {
    PROPIETARIO: {
      showInventario: true,
      showVentas: true,
      showCompras: true,
      showUsuarios: true,
      showReportes: true,
      showConfiguracion: true
    },
    ADMIN: {
      showInventario: true,
      showVentas: true,
      showCompras: true,
      showUsuarios: true,
      showReportes: true,
      showConfiguracion: false
    },
    VENDEDOR: {
      showInventario: 'readonly', // Solo lectura
      showVentas: true,
      showCompras: false,
      showUsuarios: false,
      showReportes: false,
      showConfiguracion: false
    }
  };

  const config = menuConfig[role] || menuConfig.VENDEDOR;

  return (
    <>
      {/* Overlay para móvil */}
      {isOpen && (
        <div 
          className="sidebar-overlay d-lg-none"
          onClick={toggleSidebar}
        />
      )}

      {/* Sidebar */}
      <aside className={`dashboard-sidebar ${isOpen ? 'open' : ''}`}>
        <Nav className="flex-column sidebar-nav">
          {/* Dashboard */}
          <Nav.Link 
            as={NavLink} 
            to="/dashboard" 
            end
            className="sidebar-link"
          >
            <FaHome className="me-2" />
            <span>Dashboard</span>
          </Nav.Link>

          {/* INVENTARIO */}
          {config.showInventario && (
            <>
              <div
                className="sidebar-link sidebar-dropdown-toggle"
                onClick={() => toggleMenu('inventario')}
              >
                <div className="d-flex align-items-center">
                  <FaBoxes className="me-2" />
                  <span>Inventario</span>
                </div>
                {openMenus.inventario ? <FaChevronDown /> : <FaChevronRight />}
              </div>

              <Collapse in={openMenus.inventario}>
                <div className="sidebar-submenu">
                  <Nav.Link 
                    as={NavLink} 
                    to="/dashboard/productos"
                    className="sidebar-sublink"
                  >
                    <FaList className="me-2" size={14} />
                    Productos
                  </Nav.Link>

                  <Nav.Link 
                    as={NavLink} 
                    to="/dashboard/categorias"
                    className="sidebar-sublink"
                  >
                    <FaTags className="me-2" size={14} />
                    Categorías
                  </Nav.Link>

                  <Nav.Link 
                    as={NavLink} 
                    to="/dashboard/inventario"
                    className="sidebar-sublink"
                  >
                    <FaWarehouse className="me-2" size={14} />
                    Stock
                  </Nav.Link>

                  {config.showInventario !== 'readonly' && (
                    <Nav.Link 
                      as={NavLink} 
                      to="/dashboard/proveedores"
                      className="sidebar-sublink"
                    >
                      <FaTruck className="me-2" size={14} />
                      Proveedores
                    </Nav.Link>
                  )}
                </div>
              </Collapse>
            </>
          )}

          {/* VENTAS */}
          {config.showVentas && (
            <>
              <div
                className="sidebar-link sidebar-dropdown-toggle"
                onClick={() => toggleMenu('ventas')}
              >
                <div className="d-flex align-items-center">
                  <FaShoppingCart className="me-2" />
                  <span>Ventas</span>
                </div>
                {openMenus.ventas ? <FaChevronDown /> : <FaChevronRight />}
              </div>

              <Collapse in={openMenus.ventas}>
                <div className="sidebar-submenu">
                  <Nav.Link 
                    as={NavLink} 
                    to="/dashboard/ventas/nueva"
                    className="sidebar-sublink"
                  >
                    <FaFileInvoiceDollar className="me-2" size={14} />
                    Nueva Venta
                  </Nav.Link>

                  <Nav.Link 
                    as={NavLink} 
                    to="/dashboard/ventas"
                    className="sidebar-sublink"
                  >
                    <FaList className="me-2" size={14} />
                    Historial
                  </Nav.Link>

                  <Nav.Link 
                    as={NavLink} 
                    to="/dashboard/clientes"
                    className="sidebar-sublink"
                  >
                    <FaUserFriends className="me-2" size={14} />
                    Clientes
                  </Nav.Link>

                  {role !== 'VENDEDOR' && (
                    <Nav.Link 
                      as={NavLink} 
                      to="/dashboard/pagos"
                      className="sidebar-sublink"
                    >
                      <FaMoneyBillWave className="me-2" size={14} />
                      Pagos
                    </Nav.Link>
                  )}
                </div>
              </Collapse>
            </>
          )}

          {/* COMPRAS */}
          {config.showCompras && (
            <>
              <div
                className="sidebar-link sidebar-dropdown-toggle"
                onClick={() => toggleMenu('compras')}
              >
                <div className="d-flex align-items-center">
                  <FaShoppingBag className="me-2" />
                  <span>Compras</span>
                </div>
                {openMenus.compras ? <FaChevronDown /> : <FaChevronRight />}
              </div>

              <Collapse in={openMenus.compras}>
                <div className="sidebar-submenu">
                  <Nav.Link 
                    as={NavLink} 
                    to="/dashboard/compras/nueva"
                    className="sidebar-sublink"
                  >
                    <FaFileInvoiceDollar className="me-2" size={14} />
                    Nueva Compra
                  </Nav.Link>

                  <Nav.Link 
                    as={NavLink} 
                    to="/dashboard/compras"
                    className="sidebar-sublink"
                  >
                    <FaList className="me-2" size={14} />
                    Historial
                  </Nav.Link>
                </div>
              </Collapse>
            </>
          )}

          {/* USUARIOS */}
          {config.showUsuarios && (
            <>
              <div
                className="sidebar-link sidebar-dropdown-toggle"
                onClick={() => toggleMenu('usuarios')}
              >
                <div className="d-flex align-items-center">
                  <FaUsers className="me-2" />
                  <span>Usuarios</span>
                </div>
                {openMenus.usuarios ? <FaChevronDown /> : <FaChevronRight />}
              </div>

              <Collapse in={openMenus.usuarios}>
                <div className="sidebar-submenu">
                  <Nav.Link 
                    as={NavLink} 
                    to="/dashboard/usuarios"
                    className="sidebar-sublink"
                  >
                    <FaUsersCog className="me-2" size={14} />
                    Lista de Usuarios
                  </Nav.Link>

                  <Nav.Link 
                    as={NavLink} 
                    to="/dashboard/roles"
                    className="sidebar-sublink"
                  >
                    <FaShieldAlt className="me-2" size={14} />
                    Roles y Permisos
                  </Nav.Link>
                </div>
              </Collapse>
            </>
          )}

          {/* REPORTES */}
          {config.showReportes && (
            <>
              <div
                className="sidebar-link sidebar-dropdown-toggle"
                onClick={() => toggleMenu('reportes')}
              >
                <div className="d-flex align-items-center">
                  <FaChartBar className="me-2" />
                  <span>Reportes</span>
                </div>
                {openMenus.reportes ? <FaChevronDown /> : <FaChevronRight />}
              </div>

              <Collapse in={openMenus.reportes}>
                <div className="sidebar-submenu">
                  <Nav.Link 
                    as={NavLink} 
                    to="/dashboard/reportes/ventas"
                    className="sidebar-sublink"
                  >
                    <FaShoppingCart className="me-2" size={14} />
                    Reporte de Ventas
                  </Nav.Link>

                  <Nav.Link 
                    as={NavLink} 
                    to="/dashboard/reportes/inventario"
                    className="sidebar-sublink"
                  >
                    <FaBoxes className="me-2" size={14} />
                    Reporte de Inventario
                  </Nav.Link>

                  <Nav.Link 
                    as={NavLink} 
                    to="/dashboard/reportes/financiero"
                    className="sidebar-sublink"
                  >
                    <FaMoneyBillWave className="me-2" size={14} />
                    Reporte Financiero
                  </Nav.Link>
                </div>
              </Collapse>
            </>
          )}

          {/* CONFIGURACIÓN */}
          {config.showConfiguracion && (
            <>
              <div
                className="sidebar-link sidebar-dropdown-toggle"
                onClick={() => toggleMenu('configuracion')}
              >
                <div className="d-flex align-items-center">
                  <FaCog className="me-2" />
                  <span>Configuración</span>
                </div>
                {openMenus.configuracion ? <FaChevronDown /> : <FaChevronRight />}
              </div>

              <Collapse in={openMenus.configuracion}>
                <div className="sidebar-submenu">
                  <Nav.Link 
                    as={NavLink} 
                    to="/dashboard/configuracion/empresa"
                    className="sidebar-sublink"
                  >
                    Datos de Empresa
                  </Nav.Link>

                  <Nav.Link 
                    as={NavLink} 
                    to="/dashboard/configuracion/general"
                    className="sidebar-sublink"
                  >
                    Configuración General
                  </Nav.Link>

                  <Nav.Link 
                    as={NavLink} 
                    to="/dashboard/configuracion/suscripcion"
                    className="sidebar-sublink"
                  >
                    Suscripción y Planes
                    <Badge bg="primary" className="ms-2">PRO</Badge>
                  </Nav.Link>

                  <Nav.Link 
                    as={NavLink} 
                    to="/dashboard/configuracion/auditoria"
                    className="sidebar-sublink"
                  >
                    Auditoría
                  </Nav.Link>
                </div>
              </Collapse>
            </>
          )}

          {/* NOTIFICACIONES */}
          <Nav.Link 
            as={NavLink} 
            to="/dashboard/notificaciones"
            className="sidebar-link"
          >
            <FaBell className="me-2" />
            <span>Notificaciones</span>
            <Badge bg="danger" className="ms-auto">3</Badge>
          </Nav.Link>
        </Nav>
      </aside>
    </>
  );
};

export default DashboardSidebar;