// src/main.jsx
import React from 'react'
import ReactDOM from 'react-dom/client'

// Importar Bootstrap CSS
import 'bootstrap/dist/css/bootstrap.min.css'

// Importar nuestros estilos personalizados
import './styles/variables.css'
import './styles/hotfix.css'
import './index.css'

import App from './App.jsx'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)