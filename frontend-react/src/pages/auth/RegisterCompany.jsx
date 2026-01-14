// import { useNavigate } from 'react-router-dom';

// const RegisterCompany = () => {
//   const navigate = useNavigate();

//   const handleRegister = (e) => {
//     e.preventDefault();
//     // 1. Llamar al backend endpoint PUBLICO: /auth/registro-empresa
//     // 2. Si éxito:
//     navigate('/seleccionar-plan');
//   };

//   return (
//     <div style={{ padding: '2rem' }}>
//       <h2>Paso 1: Registra tu Empresa</h2>
//       <form onSubmit={handleRegister}>
//         <input placeholder="Nombre de Empresa" required /><br/><br/>
//         <input placeholder="Nombre del Dueño" required /><br/><br/>
//         <input placeholder="Email" type="email" required /><br/><br/>
//         <input placeholder="Contraseña" type="password" required /><br/><br/>
//         <button type="submit">Siguiente: Elegir Plan</button>
//       </form>
//     </div>
//   );
// };

// export default RegisterCompany;