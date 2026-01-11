import { useAuth } from '../../context/AuthContext';

const DashboardHome = () => {
  const { user, logout } = useAuth();

  return (
    <div style={{ display: 'flex' }}>
      {/* Sidebar simulado */}
      <aside style={{ width: '200px', background: '#333', color: '#fff', height: '100vh', padding: '1rem' }}>
        <h3>Menú</h3>
        <ul style={{ listStyle: 'none', padding: 0 }}>
          <li>Inicio</li>
          <li>Ventas</li>
          <li>Inventario</li>
          
          {/* LÓGICA DE ROLES VISUAL */}
          {user?.rol === 'PROPIETARIO' && (
             <li style={{ color: 'gold', fontWeight: 'bold' }}>Configuración (Solo Dueño)</li>
          )}
        </ul>
        <button onClick={logout} style={{ marginTop: '20px', background: 'red', color: 'white' }}>
            Cerrar Sesión
        </button>
      </aside>

      {/* Contenido Principal */}
      <main style={{ padding: '2rem', flex: 1 }}>
        <h1>Bienvenido, {user?.nombre}</h1>
        <p>Tu rol es: <strong>{user?.rol}</strong></p>
        <p>Aquí verás tus tablas y estadísticas.</p>
      </main>
    </div>
  );
};

export default DashboardHome;