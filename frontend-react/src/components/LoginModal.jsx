// import { useState } from 'react';
// import { useAuth } from '../../context/AuthContext';
// import { useNavigate } from 'react-router-dom';

// const LoginModal = ({ onClose }) => {
//   const { login } = useAuth();
//   const navigate = useNavigate();
  
//   // Estados para el formulario
//   const [email, setEmail] = useState('');
//   const [password, setPassword] = useState('');

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     // 1. AQUÍ LLAMARÍAS A TU BACKEND: fetch('http://localhost:5000/auth/login'...)
//     // 2. Simulamos respuesta exitosa por ahora:
//     const mockResponse = {
//         token: "xyz123",
//         user: { 
//             nombre: "Juan Perez", 
//             rol: "PROPIETARIO", // O "VENDEDOR"
//             id_empresa: "emp-001" 
//         }
//     };
    
//     // 3. Guardamos en el contexto
//     login(mockResponse.user, mockResponse.token);
    
//     // 4. Redirección inteligente
//     navigate('/dashboard');
//     onClose();
//   };

//   return (
//     <div style={{ position: 'fixed', top:0, left:0, right:0, bottom:0, background: 'rgba(0,0,0,0.5)', display:'flex', justifyContent:'center', alignItems:'center' }}>
//       <div style={{ background: 'white', padding: '2rem', borderRadius: '8px', width: '300px' }}>
//         <h3>Bienvenido</h3>
//         <form onSubmit={handleSubmit}>
//           <div style={{ marginBottom: '10px' }}>
//             <label>Email:</label>
//             <input type="email" value={email} onChange={(e)=>setEmail(e.target.value)} required style={{width: '100%'}}/>
//           </div>
//           <div style={{ marginBottom: '10px' }}>
//             <label>Contraseña:</label>
//             <input type="password" value={password} onChange={(e)=>setPassword(e.target.value)} required style={{width: '100%'}}/>
//           </div>
//           <button type="submit" style={{width: '100%'}}>Entrar</button>
//         </form>
//         <button onClick={onClose} style={{marginTop: '10px', background: 'transparent', border: 'none', cursor: 'pointer'}}>Cerrar</button>
//       </div>
//     </div>
//   );
// };

// export default LoginModal;