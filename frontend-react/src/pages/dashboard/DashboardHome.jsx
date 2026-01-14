// src/pages/dashboard/DashboardHome.jsx
import React from 'react';
import { Row, Col, Card, Badge, Button, Table, ProgressBar } from 'react-bootstrap';
import {
  FaShoppingCart,
  FaBoxes,
  FaUsers,
  FaMoneyBillWave,
  FaArrowUp,
  FaArrowDown,
  FaExclamationTriangle,
  FaEye
} from 'react-icons/fa';
import { useAuth } from '../../context/AuthContext';
import './DashboardHome.css';

const DashboardHome = () => {
  const { user, getUserRole } = useAuth();
  const role = getUserRole();

  // Datos de ejemplo (en producción vendrían del backend)
  const stats = {
    ventasMes: { valor: 15420, cambio: 12.5, tipo: 'aumento' },
    productosStock: { valor: 156, cambio: -3.2, tipo: 'disminucion' },
    clientes: { valor: 48, cambio: 8.0, tipo: 'aumento' },
    comprasMes: { valor: 8500, cambio: 5.3, tipo: 'aumento' }
  };

  const productosStockBajo = [
    { id: 1, nombre: 'Producto A', stock: 3, minimo: 10, porcentaje: 30 },
    { id: 2, nombre: 'Producto B', stock: 5, minimo: 15, porcentaje: 33 },
    { id: 3, nombre: 'Producto C', stock: 2, minimo: 8, porcentaje: 25 }
  ];

  const ultimasVentas = [
    { id: 'V-001', cliente: 'Juan Pérez', total: 150, fecha: '2025-01-13 10:30' },
    { id: 'V-002', cliente: 'María López', total: 320, fecha: '2025-01-13 09:15' },
    { id: 'V-003', cliente: 'Carlos Ruiz', total: 85, fecha: '2025-01-13 08:45' }
  ];

  const productosTop = [
    { nombre: 'Producto X', ventas: 45, monto: 4500 },
    { nombre: 'Producto Y', ventas: 38, monto: 3800 },
    { nombre: 'Producto Z', ventas: 32, monto: 3200 }
  ];

  return (
    <div className="dashboard-home">
      {/* Saludo personalizado */}
      <div className="mb-4">
        <h2 className="fw-bold mb-1">
          ¡Hola, {user?.nombres || user?.nombre || 'Usuario'}! 👋
        </h2>
        <p className="text-muted mb-0">
          Aquí está el resumen de tu negocio hoy
        </p>
      </div>

      {/* Tarjetas de KPIs */}
      <Row className="g-3 mb-4">
        {/* Ventas del Mes */}
        <Col xs={12} sm={6} lg={3}>
          <Card className="stat-card border-0 shadow-sm h-100">
            <Card.Body>
              <div className="d-flex justify-content-between align-items-start mb-3">
                <div className="stat-icon bg-primary-subtle text-primary">
                  <FaShoppingCart size={24} />
                </div>
                <Badge 
                  bg={stats.ventasMes.tipo === 'aumento' ? 'success' : 'danger'}
                  className="d-flex align-items-center gap-1"
                >
                  {stats.ventasMes.tipo === 'aumento' ? <FaArrowUp /> : <FaArrowDown />}
                  {stats.ventasMes.cambio}%
                </Badge>
              </div>
              <h3 className="fw-bold mb-1">
                {stats.ventasMes.valor.toLocaleString()} Bs
              </h3>
              <p className="text-muted mb-0 small">Ventas del Mes</p>
            </Card.Body>
          </Card>
        </Col>

        {/* Productos en Stock */}
        <Col xs={12} sm={6} lg={3}>
          <Card className="stat-card border-0 shadow-sm h-100">
            <Card.Body>
              <div className="d-flex justify-content-between align-items-start mb-3">
                <div className="stat-icon bg-success-subtle text-success">
                  <FaBoxes size={24} />
                </div>
                <Badge 
                  bg={stats.productosStock.tipo === 'aumento' ? 'success' : 'danger'}
                  className="d-flex align-items-center gap-1"
                >
                  {stats.productosStock.tipo === 'aumento' ? <FaArrowUp /> : <FaArrowDown />}
                  {Math.abs(stats.productosStock.cambio)}%
                </Badge>
              </div>
              <h3 className="fw-bold mb-1">{stats.productosStock.valor}</h3>
              <p className="text-muted mb-0 small">Productos en Stock</p>
            </Card.Body>
          </Card>
        </Col>

        {/* Clientes */}
        <Col xs={12} sm={6} lg={3}>
          <Card className="stat-card border-0 shadow-sm h-100">
            <Card.Body>
              <div className="d-flex justify-content-between align-items-start mb-3">
                <div className="stat-icon bg-info-subtle text-info">
                  <FaUsers size={24} />
                </div>
                <Badge 
                  bg="success"
                  className="d-flex align-items-center gap-1"
                >
                  <FaArrowUp />
                  {stats.clientes.cambio}%
                </Badge>
              </div>
              <h3 className="fw-bold mb-1">{stats.clientes.valor}</h3>
              <p className="text-muted mb-0 small">Clientes Registrados</p>
            </Card.Body>
          </Card>
        </Col>

        {/* Compras del Mes - Solo PROPIETARIO y ADMIN */}
        {(role === 'PROPIETARIO' || role === 'ADMIN') && (
          <Col xs={12} sm={6} lg={3}>
            <Card className="stat-card border-0 shadow-sm h-100">
              <Card.Body>
                <div className="d-flex justify-content-between align-items-start mb-3">
                  <div className="stat-icon bg-warning-subtle text-warning">
                    <FaMoneyBillWave size={24} />
                  </div>
                  <Badge 
                    bg="success"
                    className="d-flex align-items-center gap-1"
                  >
                    <FaArrowUp />
                    {stats.comprasMes.cambio}%
                  </Badge>
                </div>
                <h3 className="fw-bold mb-1">
                  {stats.comprasMes.valor.toLocaleString()} Bs
                </h3>
                <p className="text-muted mb-0 small">Compras del Mes</p>
              </Card.Body>
            </Card>
          </Col>
        )}
      </Row>

      <Row className="g-3">
        {/* Alertas de Stock Bajo */}
        <Col xs={12} lg={6}>
          <Card className="border-0 shadow-sm h-100">
            <Card.Header className="bg-white border-bottom">
              <div className="d-flex justify-content-between align-items-center">
                <div className="d-flex align-items-center gap-2">
                  <FaExclamationTriangle className="text-warning" />
                  <h5 className="mb-0 fw-semibold">Stock Bajo</h5>
                </div>
                <Badge bg="warning">{productosStockBajo.length}</Badge>
              </div>
            </Card.Header>
            <Card.Body className="p-0">
              {productosStockBajo.length > 0 ? (
                <div className="list-group list-group-flush">
                  {productosStockBajo.map((producto) => (
                    <div key={producto.id} className="list-group-item">
                      <div className="d-flex justify-content-between align-items-center mb-2">
                        <span className="fw-medium">{producto.nombre}</span>
                        <Badge bg="danger" pill>
                          {producto.stock} / {producto.minimo}
                        </Badge>
                      </div>
                      <ProgressBar 
                        now={producto.porcentaje} 
                        variant="danger"
                        className="progress-thin"
                      />
                    </div>
                  ))}
                </div>
              ) : (
                <div className="p-4 text-center text-muted">
                  <FaBoxes size={48} className="mb-3 opacity-25" />
                  <p className="mb-0">No hay productos con stock bajo</p>
                </div>
              )}
            </Card.Body>
          </Card>
        </Col>

        {/* Últimas Ventas */}
        <Col xs={12} lg={6}>
          <Card className="border-0 shadow-sm h-100">
            <Card.Header className="bg-white border-bottom">
              <div className="d-flex justify-content-between align-items-center">
                <h5 className="mb-0 fw-semibold">Últimas Ventas</h5>
                <Button variant="link" size="sm" className="text-decoration-none">
                  Ver todas →
                </Button>
              </div>
            </Card.Header>
            <Card.Body className="p-0">
              <Table hover className="mb-0">
                <thead className="bg-light">
                  <tr>
                    <th className="border-0">N° Factura</th>
                    <th className="border-0">Cliente</th>
                    <th className="border-0 text-end">Total</th>
                    <th className="border-0 text-center">Acción</th>
                  </tr>
                </thead>
                <tbody>
                  {ultimasVentas.map((venta) => (
                    <tr key={venta.id}>
                      <td className="fw-medium">{venta.id}</td>
                      <td>
                        <div>{venta.cliente}</div>
                        <small className="text-muted">{venta.fecha}</small>
                      </td>
                      <td className="text-end fw-semibold">
                        {venta.total} Bs
                      </td>
                      <td className="text-center">
                        <Button variant="link" size="sm" className="p-0">
                          <FaEye />
                        </Button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </Table>
            </Card.Body>
          </Card>
        </Col>

        {/* Productos Más Vendidos */}
        <Col xs={12}>
          <Card className="border-0 shadow-sm">
            <Card.Header className="bg-white border-bottom">
              <h5 className="mb-0 fw-semibold">Productos Más Vendidos (Este Mes)</h5>
            </Card.Header>
            <Card.Body>
              <Row className="g-3">
                {productosTop.map((producto, index) => (
                  <Col xs={12} md={4} key={index}>
                    <div className="product-top-card p-3 border rounded">
                      <div className="d-flex justify-content-between align-items-start mb-2">
                        <Badge bg="primary" className="fs-6">#{index + 1}</Badge>
                        <div className="text-end">
                          <div className="fw-bold">{producto.ventas}</div>
                          <small className="text-muted">unidades</small>
                        </div>
                      </div>
                      <h6 className="mb-2">{producto.nombre}</h6>
                      <div className="text-primary fw-semibold">
                        {producto.monto.toLocaleString()} Bs
                      </div>
                    </div>
                  </Col>
                ))}
              </Row>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default DashboardHome;