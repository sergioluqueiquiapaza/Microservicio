// src/pages/dashboard/usuarios/UsuarioForm.jsx
import React, { useState, useEffect } from 'react';
import DashboardLayout from '../../../components/layout/DashboardLayout';
import {
  Container,
  Row,
  Col,
  Card,
  Form,
  Button,
  Alert,
  Spinner,
  Badge
} from 'react-bootstrap';
import { FaSave, FaTimes, FaUser, FaEnvelope, FaPhone, FaLock, FaShieldAlt } from 'react-icons/fa';
import { useNavigate, useParams } from 'react-router-dom';
import { useAuth } from '../../../context/AuthContext';
import usuarioService from '../../../services/usuarioService';
import './UsuarioForm.css';

const UsuarioForm = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const isEdit = Boolean(id);

  const [loading, setLoading] = useState(false);
  const [loadingData, setLoadingData] = useState(isEdit);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [roles, setRoles] = useState([]);
  
  const [formData, setFormData] = useState({
    nombres: '',
    apellido_paterno: '',
    apellido_materno: '',
    email: '',
    telefono: '',
    id_rol: '',
    password: '',
    confirmar_password: '',
    activo: true
  });
  const [errors, setErrors] = useState({});

  useEffect(() => {
    loadRoles();
    if (isEdit) {
      loadUsuario();
    }
  }, [id]);

  const loadRoles = async () => {
    try {
      const data = await usuarioService.getRoles();
      const rolesDisponibles = data.filter(rol => rol.id_rol !== 'PROPIETARIO');
      setRoles(rolesDisponibles);
    } catch (err) {
      console.error('Error al cargar roles:', err);
    }
  };

  const loadUsuario = async () => {
    try {
      setLoadingData(true);
      const data = await usuarioService.getUsuarioById(id);
      setFormData({
        nombres: data.nombres || '',
        apellido_paterno: data.apellido_paterno || '',
        apellido_materno: data.apellido_materno || '',
        email: data.email || '',
        telefono: data.telefono || '',
        id_rol: data.id_rol || '',
        password: '',
        confirmar_password: '',
        activo: data.activo !== undefined ? data.activo : true
      });
    } catch (err) {
      setError(err.error || 'Error al cargar usuario');
    } finally {
      setLoadingData(false);
    }
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value
    });

    if (errors[name]) {
      setErrors({
        ...errors,
        [name]: ''
      });
    }
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.nombres.trim()) {
      newErrors.nombres = 'Los nombres son obligatorios';
    }

    if (!formData.apellido_paterno.trim()) {
      newErrors.apellido_paterno = 'El apellido paterno es obligatorio';
    }

    if (!formData.email.trim()) {
      newErrors.email = 'El email es obligatorio';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'El email no es válido';
    }

    if (!formData.id_rol) {
      newErrors.id_rol = 'Debes seleccionar un rol';
    }

    if (!isEdit) {
      if (!formData.password) {
        newErrors.password = 'La contraseña es obligatoria';
      } else if (formData.password.length < 6) {
        newErrors.password = 'La contraseña debe tener al menos 6 caracteres';
      }

      if (formData.password !== formData.confirmar_password) {
        newErrors.confirmar_password = 'Las contraseñas no coinciden';
      }
    } else if (formData.password) {
      if (formData.password.length < 6) {
        newErrors.password = 'La contraseña debe tener al menos 6 caracteres';
      }
      if (formData.password !== formData.confirmar_password) {
        newErrors.confirmar_password = 'Las contraseñas no coinciden';
      }
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (!validateForm()) {
      return;
    }

    setLoading(true);

    try {
      const dataToSend = {
        nombres: formData.nombres,
        apellido_paterno: formData.apellido_paterno,
        apellido_materno: formData.apellido_materno || '',
        email: formData.email,
        telefono: formData.telefono || null,
        id_rol: formData.id_rol,
        id_empresa: user.id_empresa,
        activo: formData.activo
      };

      if (formData.password) {
        dataToSend.password = formData.password;
      }

      if (isEdit) {
        await usuarioService.updateUsuario(id, dataToSend);
        setSuccess('Usuario actualizado exitosamente');
      } else {
        await usuarioService.createUsuario(dataToSend);
        setSuccess('Usuario creado exitosamente');
      }

      setTimeout(() => {
        navigate('/dashboard/usuarios');
      }, 1500);
    } catch (err) {
      setError(err.error || `Error al ${isEdit ? 'actualizar' : 'crear'} usuario`);
    } finally {
      setLoading(false);
    }
  };

  if (loadingData) {
    return (
      <DashboardLayout>
        <Container fluid className="text-center py-5">
          <Spinner animation="border" variant="primary" />
          <p className="mt-3 text-muted">Cargando datos...</p>
        </Container>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <Container fluid className="usuario-form-page">
        <div className="page-header mb-4">
          <h2 className="fw-bold mb-1">
            {isEdit ? 'Editar Usuario' : 'Nuevo Usuario'}
          </h2>
          <p className="text-muted mb-0">
            {isEdit
              ? 'Actualiza los datos del usuario'
              : 'Completa el formulario para crear un nuevo usuario'}
          </p>
        </div>

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

        <Row>
          <Col lg={8} xl={6}>
            <Card className="border-0 shadow-sm">
              <Card.Body className="p-4">
                <Form onSubmit={handleSubmit}>
                  <Row className="mb-3">
                    <Col md={12}>
                      <Form.Group>
                        <Form.Label className="fw-medium">
                          <FaUser className="me-2" />
                          Nombres *
                        </Form.Label>
                        <Form.Control
                          type="text"
                          name="nombres"
                          value={formData.nombres}
                          onChange={handleChange}
                          isInvalid={!!errors.nombres}
                          placeholder="Ej: Juan Carlos"
                        />
                        <Form.Control.Feedback type="invalid">
                          {errors.nombres}
                        </Form.Control.Feedback>
                      </Form.Group>
                    </Col>
                  </Row>

                  <Row className="mb-3">
                    <Col md={6}>
                      <Form.Group>
                        <Form.Label className="fw-medium">
                          Apellido Paterno *
                        </Form.Label>
                        <Form.Control
                          type="text"
                          name="apellido_paterno"
                          value={formData.apellido_paterno}
                          onChange={handleChange}
                          isInvalid={!!errors.apellido_paterno}
                          placeholder="Ej: Pérez"
                        />
                        <Form.Control.Feedback type="invalid">
                          {errors.apellido_paterno}
                        </Form.Control.Feedback>
                      </Form.Group>
                    </Col>
                    <Col md={6}>
                      <Form.Group>
                        <Form.Label className="fw-medium">
                          Apellido Materno
                        </Form.Label>
                        <Form.Control
                          type="text"
                          name="apellido_materno"
                          value={formData.apellido_materno}
                          onChange={handleChange}
                          placeholder="Ej: García (opcional)"
                        />
                      </Form.Group>
                    </Col>
                  </Row>

                  <Row className="mb-3">
                    <Col md={6}>
                      <Form.Group>
                        <Form.Label className="fw-medium">
                          <FaEnvelope className="me-2" />
                          Email *
                        </Form.Label>
                        <Form.Control
                          type="email"
                          name="email"
                          value={formData.email}
                          onChange={handleChange}
                          isInvalid={!!errors.email}
                          placeholder="usuario@ejemplo.com"
                        />
                        <Form.Control.Feedback type="invalid">
                          {errors.email}
                        </Form.Control.Feedback>
                        <Form.Text className="text-muted">
                          El email será su usuario de acceso
                        </Form.Text>
                      </Form.Group>
                    </Col>
                    <Col md={6}>
                      <Form.Group>
                        <Form.Label className="fw-medium">
                          <FaPhone className="me-2" />
                          Teléfono
                        </Form.Label>
                        <Form.Control
                          type="tel"
                          name="telefono"
                          value={formData.telefono}
                          onChange={handleChange}
                          placeholder="70123456 (opcional)"
                        />
                      </Form.Group>
                    </Col>
                  </Row>

                  <Row className="mb-3">
                    <Col md={12}>
                      <Form.Group>
                        <Form.Label className="fw-medium">
                          <FaShieldAlt className="me-2" />
                          Rol *
                        </Form.Label>
                        <Form.Select
                          name="id_rol"
                          value={formData.id_rol}
                          onChange={handleChange}
                          isInvalid={!!errors.id_rol}
                        >
                          <option value="">Selecciona un rol...</option>
                          {roles.map((rol) => (
                            <option key={rol.id_rol} value={rol.id_rol}>
                              {rol.nombre}
                            </option>
                          ))}
                        </Form.Select>
                        <Form.Control.Feedback type="invalid">
                          {errors.id_rol}
                        </Form.Control.Feedback>
                        <Form.Text className="text-muted">
                          Define los permisos del usuario
                        </Form.Text>
                      </Form.Group>
                    </Col>
                  </Row>

                  {!isEdit && (
                    <Alert variant="info" className="mb-3">
                      <small>
                        <strong>Nota:</strong> La contraseña será enviada al email del usuario.
                        Se recomienda que el usuario la cambie en su primer acceso.
                      </small>
                    </Alert>
                  )}

                  {isEdit && (
                    <Alert variant="warning" className="mb-3">
                      <small>
                        Deja los campos de contraseña vacíos si no deseas cambiarla.
                      </small>
                    </Alert>
                  )}

                  <Row className="mb-3">
                    <Col md={6}>
                      <Form.Group>
                        <Form.Label className="fw-medium">
                          <FaLock className="me-2" />
                          {isEdit ? 'Nueva Contraseña' : 'Contraseña *'}
                        </Form.Label>
                        <Form.Control
                          type="password"
                          name="password"
                          value={formData.password}
                          onChange={handleChange}
                          isInvalid={!!errors.password}
                          placeholder="Mínimo 6 caracteres"
                        />
                        <Form.Control.Feedback type="invalid">
                          {errors.password}
                        </Form.Control.Feedback>
                      </Form.Group>
                    </Col>
                    <Col md={6}>
                      <Form.Group>
                        <Form.Label className="fw-medium">
                          Confirmar Contraseña {!isEdit && '*'}
                        </Form.Label>
                        <Form.Control
                          type="password"
                          name="confirmar_password"
                          value={formData.confirmar_password}
                          onChange={handleChange}
                          isInvalid={!!errors.confirmar_password}
                          placeholder="Repite la contraseña"
                        />
                        <Form.Control.Feedback type="invalid">
                          {errors.confirmar_password}
                        </Form.Control.Feedback>
                      </Form.Group>
                    </Col>
                  </Row>

                  <Row className="mb-4">
                    <Col md={12}>
                      <Form.Check
                        type="switch"
                        id="activo-switch"
                        name="activo"
                        label="Usuario activo"
                        checked={formData.activo}
                        onChange={handleChange}
                      />
                      <Form.Text className="text-muted">
                        Los usuarios inactivos no podrán acceder al sistema
                      </Form.Text>
                    </Col>
                  </Row>

                  <div className="d-flex gap-2 justify-content-end">
                    <Button
                      variant="outline-secondary"
                      onClick={() => navigate('/dashboard/usuarios')}
                      disabled={loading}
                    >
                      <FaTimes className="me-2" />
                      Cancelar
                    </Button>
                    <Button
                      type="submit"
                      variant="primary"
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
                          Guardando...
                        </>
                      ) : (
                        <>
                          <FaSave className="me-2" />
                          {isEdit ? 'Actualizar Usuario' : 'Crear Usuario'}
                        </>
                      )}
                    </Button>
                  </div>
                </Form>
              </Card.Body>
            </Card>
          </Col>

          <Col lg={4} xl={6} className="d-none d-lg-block">
            <Card className="border-0 shadow-sm">
              <Card.Header className="bg-primary text-white">
                <h6 className="mb-0">
                  <FaShieldAlt className="me-2" />
                  Roles y Permisos
                </h6>
              </Card.Header>
              <Card.Body>
                <div className="role-info mb-3">
                  <h6 className="text-success">
                    <FaShieldAlt className="me-2" />
                    Administrador
                  </h6>
                  <ul className="small text-muted mb-0">
                    <li>Gestión operativa completa</li>
                    <li>Acceso a productos e inventario</li>
                    <li>Registro de ventas y compras</li>
                    <li>Gestión de usuarios</li>
                    <li>Reportes básicos</li>
                  </ul>
                </div>
                <div className="role-info">
                  <h6 className="text-info">
                    <FaShieldAlt className="me-2" />
                    Vendedor
                  </h6>
                  <ul className="small text-muted mb-0">
                    <li>Registro de ventas</li>
                    <li>Gestión de clientes</li>
                    <li>Consulta de productos</li>
                    <li>Consulta de inventario</li>
                  </ul>
                </div>
              </Card.Body>
            </Card>

            <Card className="border-0 shadow-sm mt-3">
              <Card.Body>
                <h6 className="mb-3">💡 Consejos</h6>
                <ul className="small text-muted mb-0">
                  <li className="mb-2">
                    Asigna el rol apropiado según las responsabilidades
                  </li>
                  <li className="mb-2">
                    El email debe ser único en el sistema
                  </li>
                  <li className="mb-2">
                    Recomienda al usuario cambiar su contraseña en el primer acceso
                  </li>
                  <li>
                    Puedes desactivar usuarios temporalmente sin eliminarlos
                  </li>
                </ul>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </Container>
    </DashboardLayout>
  );
};

export default UsuarioForm;