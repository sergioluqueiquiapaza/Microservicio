import { createContext, useState, useContext, useEffect } from 'react';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth debe usarse dentro de un AuthProvider');
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null); // Aquí guardamos datos del usuario y rol
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  // Simular verificar sesión al cargar la app (puedes mejorar esto luego con localStorage)
  useEffect(() => {
    const storedUser = localStorage.getItem('user_data');
    if (storedUser) {
        setUser(JSON.parse(storedUser));
        setIsAuthenticated(true);
    }
    setLoading(false);
  }, []);

  const login = (userData, token) => {
    // Aquí recibimos la respuesta de tu backend Flask (/auth/login)
    // userData debe incluir: { nombre, rol, empresa_activa, etc }
    localStorage.setItem('token', token);
    localStorage.setItem('user_data', JSON.stringify(userData));
    setUser(userData);
    setIsAuthenticated(true);
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user_data');
    setUser(null);
    setIsAuthenticated(false);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, isAuthenticated, loading }}>
      {children}
    </AuthContext.Provider>
  );
};