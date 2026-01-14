// import { useNavigate } from 'react-router-dom';

// const PaymentQR = () => {
//   const navigate = useNavigate();

//   const handleSimulatePayment = () => {
//     // Aquí llamarías al backend para activar la suscripción
//     alert("Pago recibido. ¡Bienvenido!");
//     navigate('/dashboard'); // O al login si prefieres que se loguee de nuevo
//   };

//   return (
//     <div style={{ padding: '2rem', textAlign: 'center' }}>
//       <h2>Paso 3: Realiza el Pago</h2>
//       <p>Escanea este código para activar tu cuenta:</p>
//       <div style={{ height: '200px', width: '200px', background: '#ccc', margin: '0 auto', display:'flex', alignItems:'center', justifyContent:'center' }}>
//         [IMAGEN QR AQUÍ]
//       </div>
//       <br/>
//       <button onClick={handleSimulatePayment} style={{ background: 'green', color: 'white' }}>
//         Simular Pago Exitoso
//       </button>
//     </div>
//   );
// };

// export default PaymentQR;