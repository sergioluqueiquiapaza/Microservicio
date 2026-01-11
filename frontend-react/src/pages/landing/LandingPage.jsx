import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import LoginModal from '../../components/modals/LoginModal';

const LandingPage = () => {
  const [showLogin, setShowLogin] = useState(false);
  const navigate = useNavigate();

  return (
    <div className="landing-container">
      {/* Navbar Simple */}
      <nav style={{ padding: '1rem', display: 'flex', justifyContent: 'space-between', background: '#eee' }}>
        <h1>MiSaaS Inventario</h1>
        <div>
          <button onClick={() => setShowLogin(true)} style={{ marginRight: '10px' }}>Iniciar Sesión</button>
          <button onClick={() => navigate('/registro')}>Registrar mi Empresa</button>
        </div>
      </nav>

      {/* Hero Section */}
      <header style={{ textAlign: 'center', marginTop: '50px' }}>
        <h2>Gestiona tu negocio de forma inteligente</h2>
        <p>Inventario, Ventas y Reportes en un solo lugar.</p>
        <p>¡Suscríbete ahora!</p>
      </header>

      {/* MODAL DE LOGIN (Se muestra si showLogin es true) */}
      {showLogin && <LoginModal onClose={() => setShowLogin(false)} />}
    </div>
  );
};

export default LandingPage;