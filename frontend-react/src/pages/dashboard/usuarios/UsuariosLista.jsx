// src/pages/dashboard/usuarios/UsuariosLista.jsx
import React, { useState, useEffect } from 'react';
import DashboardLayout from '../../../components/layout/DashboardLayout';
import {
    Container,
    Row,
    Col,
    Card,
    Table,
    Button,
    Badge,
    Form,
    InputGroup,
    Alert,
    Spinner,
    Modal,
    Tabs,
    Tab
} from 'react-bootstrap';
import {
    FaPlus,
    FaSearch,
    FaEdit,
    FaTrash,
    FaEye,
    FaUserCircle,
    FaExclamationTriangle,
    FaCheckCircle
} from 'react-icons/fa';
import { useAuth } from '../../../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import usuarioService from '../../../services/usuarioService';
import './UsuariosLista.css';

const UsuariosLista = () => {
    const { user, getUserRole } = useAuth();
    const navigate = useNavigate();
    const role = getUserRole();

    // Estados
    const [usuarios, setUsuarios] = useState([]);
    const [usuariosInactivos, setUsuariosInactivos] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [searchTerm, setSearchTerm] = useState('');
    const [filterRole, setFilterRole] = useState('');
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [usuarioToDelete, setUsuarioToDelete] = useState(null);
    const [activeTab, setActiveTab] = useState('activos');

    // Cargar usuarios al montar el componente
    useEffect(() => {
        loadUsuarios();
    }, []);

    const loadUsuarios = async () => {
        try {
            setLoading(true);
            setError('');
            const [activos, inactivos] = await Promise.all([
                usuarioService.getUsuarios(),
                usuarioService.getUsuariosInactivos()
            ]);
            setUsuarios(activos);
            setUsuariosInactivos(inactivos);
        } catch (err) {
            setError(err.error || 'Error al cargar usuarios');
        } finally {
            setLoading(false);
        }
    };

    // Filtrar usuarios activos
    const usuariosFiltrados = usuarios.filter(usuario => {
        const matchSearch =
            usuario.nombres?.toLowerCase().includes(searchTerm.toLowerCase()) ||
            usuario.email?.toLowerCase().includes(searchTerm.toLowerCase());
        const matchRole = filterRole ? usuario.id_rol === filterRole : true;
        return matchSearch && matchRole;
    });

    // Filtrar usuarios inactivos
    const usuariosInactivosFiltrados = usuariosInactivos.filter(usuario => {
        const matchSearch =
            usuario.nombres?.toLowerCase().includes(searchTerm.toLowerCase()) ||
            usuario.email?.toLowerCase().includes(searchTerm.toLowerCase());
        const matchRole = filterRole ? usuario.id_rol === filterRole : true;
        return matchSearch && matchRole;
    });

    // Manejar desactivación
    const handleDesactivarClick = (usuario) => {
        setUsuarioToDelete(usuario);
        setShowDeleteModal(true);
    };

    const confirmDesactivar = async () => {
        try {
            await usuarioService.desactivarUsuario(usuarioToDelete.id_usuario);
            setShowDeleteModal(false);
            setUsuarioToDelete(null);
            setSuccess('Usuario desactivado correctamente');
            loadUsuarios();
            setTimeout(() => setSuccess(''), 3000);
        } catch (err) {
            setError(err.error || 'Error al desactivar usuario');
            setShowDeleteModal(false);
        }
    };

    // Manejar activación
    const handleActivar = async (id_usuario) => {
        try {
            await usuarioService.activarUsuario(id_usuario);
            setSuccess('Usuario activado correctamente');
            loadUsuarios();
            setTimeout(() => setSuccess(''), 3000);
        } catch (err) {
            setError(err.error || 'Error al activar usuario');
        }
    };

    // Obtener badge variant según rol
    const getRoleBadgeVariant = (rol) => {
        const variants = {
            'PROPIETARIO': 'primary',
            'ADMIN': 'success',
            'VENDEDOR': 'info'
        };
        return variants[rol] || 'secondary';
    };

    // Obtener nombre de rol formateado
    const getRoleName = (rol) => {
        const names = {
            'PROPIETARIO': 'Propietario',
            'ADMIN': 'Administrador',
            'VENDEDOR': 'Vendedor'
        };
        return names[rol] || rol;
    };

    return (
        <DashboardLayout>
            <Container fluid className="usuarios-lista-page">
                {/* Header */}
                <div className="page-header mb-4">
                    <Row className="align-items-center">
                        <Col>
                            <h2 className="fw-bold mb-1">Gestión de Usuarios</h2>
                            <p className="text-muted mb-0">
                                Administra los usuarios de tu empresa
                            </p>
                        </Col>
                        <Col xs="auto">
                            <Button
                                variant="primary"
                                size="lg"
                                onClick={() => navigate('/dashboard/usuarios/nuevo')}
                                className="d-flex align-items-center gap-2"
                            >
                                <FaPlus />
                                Nuevo Usuario
                            </Button>
                        </Col>
                    </Row>
                </div>

                {/* Alertas */}
                {error && (
                    <Alert variant="danger" dismissible onClose={() => setError('')}>
                        {error}
                    </Alert>
                )}
                {success && (
                    <Alert variant="success" dismissible onClose={() => setSuccess('')}>
                        {success}
                    </Alert>
                )}

                {/* Filtros */}
                <Card className="border-0 shadow-sm mb-4">
                    <Card.Body>
                        <Row className="g-3">
                            <Col md={6}>
                                <InputGroup>
                                    <InputGroup.Text>
                                        <FaSearch />
                                    </InputGroup.Text>
                                    <Form.Control
                                        type="text"
                                        placeholder="Buscar por nombre o email..."
                                        value={searchTerm}
                                        onChange={(e) => setSearchTerm(e.target.value)}
                                    />
                                </InputGroup>
                            </Col>
                            <Col md={4}>
                                <Form.Select
                                    value={filterRole}
                                    onChange={(e) => setFilterRole(e.target.value)}
                                >
                                    <option value="">Todos los roles</option>
                                    <option value="PROPIETARIO">Propietario</option>
                                    <option value="ADMIN">Administrador</option>
                                    <option value="VENDEDOR">Vendedor</option>
                                </Form.Select>
                            </Col>
                            <Col md={2}>
                                <div className="text-muted small">
                                    Activos: <strong>{usuariosFiltrados.length}</strong>
                                </div>
                            </Col>
                        </Row>
                    </Card.Body>
                </Card>

                {/* Tabs de Activos/Inactivos */}
                <Card className="border-0 shadow-sm">
                    <Card.Body className="p-0">
                        <Tabs
                            activeKey={activeTab}
                            onSelect={(k) => setActiveTab(k)}
                            className="mb-0"
                        >
                            <Tab eventKey="activos" title={`Activos (${usuarios.length})`}>
                                {loading ? (
                                    <div className="text-center py-5">
                                        <Spinner animation="border" variant="primary" />
                                        <p className="mt-3 text-muted">Cargando usuarios...</p>
                                    </div>
                                ) : usuariosFiltrados.length === 0 ? (
                                    <div className="text-center py-5">
                                        <FaUserCircle size={64} className="text-muted mb-3" />
                                        <h5 className="text-muted">No se encontraron usuarios</h5>
                                        <p className="text-muted">
                                            {searchTerm || filterRole
                                                ? 'Intenta ajustar los filtros de búsqueda'
                                                : 'Comienza agregando tu primer usuario'}
                                        </p>
                                    </div>
                                ) : (
                                    <Table hover responsive className="mb-0">
                                        <thead className="bg-light">
                                            <tr>
                                                <th className="border-0">Usuario</th>
                                                <th className="border-0">Email</th>
                                                <th className="border-0">Teléfono</th>
                                                <th className="border-0">Rol</th>
                                                {/* <th className="border-0">Último Acceso</th> */}
                                                <th className="border-0 text-center">Acciones</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {usuariosFiltrados.map((usuario) => (
                                                <tr key={usuario.id_usuario}>
                                                    <td>
                                                        <div className="d-flex align-items-center gap-2">
                                                            <div className="user-avatar-small">
                                                                <FaUserCircle />
                                                            </div>
                                                            <div>
                                                                <div className="fw-medium">
                                                                    {usuario.nombre_completo_str ||
                                                                        `${usuario.nombres} ${usuario.apellido_paterno}`}
                                                                </div>
                                                                {usuario.id_usuario === user.id_usuario && (
                                                                    <Badge bg="info" className="small">Tú</Badge>
                                                                )}
                                                            </div>
                                                        </div>
                                                    </td>
                                                    <td>{usuario.email}</td>
                                                    <td>{usuario.telefono || '-'}</td>
                                                    <td>
                                                        <Badge bg={getRoleBadgeVariant(usuario.id_rol)}>
                                                            {getRoleName(usuario.id_rol)}
                                                        </Badge>
                                                    </td>
                                                    {/* <td>
                                                        <small className="text-muted">
                                                            {usuario.ultimo_acceso
                                                                ? new Date(usuario.ultimo_acceso).toLocaleDateString()
                                                                : 'Nunca'}
                                                        </small>
                                                    </td> */}
                                                    <td>
                                                        <div className="d-flex justify-content-center gap-2">
                                                            <Button
                                                                variant="link"
                                                                size="sm"
                                                                className="p-0 text-primary"
                                                                title="Ver detalles"
                                                                onClick={() => navigate(`/dashboard/usuarios/${usuario.id_usuario}`)}
                                                            >
                                                                <FaEye />
                                                            </Button>
                                                            <Button
                                                                variant="link"
                                                                size="sm"
                                                                className="p-0 text-warning"
                                                                title="Editar"
                                                                onClick={() => navigate(`/dashboard/usuarios/${usuario.id_usuario}/editar`)}
                                                            >
                                                                <FaEdit />
                                                            </Button>
                                                            {role === 'PROPIETARIO' && usuario.id_rol !== 'PROPIETARIO' && (
                                                                <Button
                                                                    variant="link"
                                                                    size="sm"
                                                                    className="p-0 text-danger"
                                                                    title="Desactivar"
                                                                    onClick={() => handleDesactivarClick(usuario)}
                                                                >
                                                                    <FaTrash />
                                                                </Button>
                                                            )}
                                                        </div>
                                                    </td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </Table>
                                )}
                            </Tab>

                            <Tab eventKey="inactivos" title={`Desactivados (${usuariosInactivos.length})`}>
                                {loading ? (
                                    <div className="text-center py-5">
                                        <Spinner animation="border" variant="primary" />
                                        <p className="mt-3 text-muted">Cargando usuarios...</p>
                                    </div>
                                ) : usuariosInactivosFiltrados.length === 0 ? (
                                    <div className="text-center py-5">
                                        <FaUserCircle size={64} className="text-muted mb-3" />
                                        <h5 className="text-muted">No hay usuarios desactivados</h5>
                                    </div>
                                ) : (
                                    <Table hover responsive className="mb-0">
                                        <thead className="bg-light">
                                            <tr>
                                                <th className="border-0">Usuario</th>
                                                <th className="border-0">Email</th>
                                                <th className="border-0">Rol</th>
                                                <th className="border-0">Fecha Creación</th>
                                                <th className="border-0 text-center">Acciones</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {usuariosInactivosFiltrados.map((usuario) => (
                                                <tr key={usuario.id_usuario}>
                                                    <td className="text-muted">
                                                        {usuario.nombre_completo_str ||
                                                            `${usuario.nombres} ${usuario.apellido_paterno}`}
                                                    </td>
                                                    <td className="text-muted">{usuario.email}</td>
                                                    <td>
                                                        <Badge bg={getRoleBadgeVariant(usuario.id_rol)}>
                                                            {getRoleName(usuario.id_rol)}
                                                        </Badge>
                                                    </td>
                                                    <td className="text-muted">
                                                        {usuario.fecha_creacion
                                                            ? new Date(usuario.fecha_creacion).toLocaleDateString()
                                                            : '-'}
                                                    </td>
                                                    <td>
                                                        <div className="d-flex justify-content-center gap-2">
                                                            <Button
                                                                variant="success"
                                                                size="sm"
                                                                onClick={() => handleActivar(usuario.id_usuario)}
                                                            >
                                                                <FaCheckCircle className="me-1" />
                                                                Reactivar
                                                            </Button>
                                                        </div>
                                                    </td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </Table>
                                )}
                            </Tab>
                        </Tabs>
                    </Card.Body>
                </Card>
            </Container>

            {/* Modal de confirmación de desactivación */}
            <Modal show={showDeleteModal} onHide={() => setShowDeleteModal(false)} centered>
                <Modal.Header closeButton>
                    <Modal.Title>
                        <FaExclamationTriangle className="text-warning me-2" />
                        Confirmar Desactivación
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <p>
                        ¿Estás seguro de que deseas desactivar al usuario{' '}
                        <strong>{usuarioToDelete?.nombre_completo_str}</strong>?
                    </p>
                    <Alert variant="warning" className="mb-0">
                        <small>
                            El usuario perderá el acceso al sistema pero podrás reactivarlo
                            desde la pestaña de "Desactivados".
                        </small>
                    </Alert>
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={() => setShowDeleteModal(false)}>
                        Cancelar
                    </Button>
                    <Button variant="danger" onClick={confirmDesactivar}>
                        Sí, Desactivar
                    </Button>
                </Modal.Footer>
            </Modal>
        </DashboardLayout>
    );
};

export default UsuariosLista;