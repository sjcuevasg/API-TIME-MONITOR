import { useState, useEffect } from "react"
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts"

function App() {
  const [logs, setLogs] = useState([])
  const [error, setError] = useState(null)
  const [stats, setStats] = useState([])
  const [UltActualizacion, setUltActualizacion] = useState(null)
  
  const fethData = () => {
    fetch("http://localhost:8000/logs")
      .then(res => res.json())
      .then(data => {
        setLogs(data)
        setUltActualizacion(new Date().toLocaleTimeString())
      })
      .catch(() => setError("Error al conectar con la API"))
  
      
      //fetch stats
      fetch("http://localhost:8000/stats")
      .then(res => res.json())
      .then(data => setStats(data))
      .catch(() => setError("Error al obtener estadisticas"))
    }
  
  useEffect(() => {
    fethData()
    const intervalo = setInterval (() => {
      fethData()
    }, 10000) // Actualiza cada 5 segundos

    return () => clearInterval(intervalo) // Limpia el intervalo al desmontar el componente
   }, [])

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <div style={{display: "flex", justifyContent: "space-between", alignItems: "center"}}>
        <h1>API Monitor Dashboard</h1>
        {UltActualizacion && (
          <p style={{color:"grey"}}>Última actualización: {UltActualizacion}</p>
        )}
      </div>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {/* Tabla de estadísticas por endpoint */}
      <h2>Uso por endpoint</h2>
      <table border="1" cellPadding="8" style={{ width: "100%", borderCollapse: "collapse", marginBottom: "2rem" }}>
        <thead style={{ background: "#f0f0f0" }}>
          <tr>
            <th>Endpoint</th>
            <th>Método</th>
            <th>Hora</th>
            <th>Visitas</th>
            <th>Promedio (ms)</th>
          </tr>
        </thead>
        <tbody>
          {stats.map((row, index) => (
            <tr key={`${row.endpoint}-${row.method}-${index}`}>
              <td>{row.endpoint}</td>
              <td>{row.method}</td>
              <td>{row.hora}</td>
              <td>{row.total_visitas}</td>
              <td>{row.promedio_ms}</td>
            </tr>
          ))}
        </tbody>
      </table>






      {/* Tabla de logs */}
      <h2>Logs recientes</h2>
      <table border="1" cellPadding="8" style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead style={{ background: "#f0f0f0" }}>
          <tr>
            <th>Endpoint</th>
            <th>Método</th>
            <th>Status</th>
            <th>Tiempo (ms)</th>
            <th>Timestamp</th>
          </tr>
        </thead>
        <tbody>
          {logs.map(log => (
            <tr key={log.id} style={{ background: log.status_code >= 400 ? "#ffe0e0" : "white" }}>
              <td>{log.endpoint}</td>
              <td>{log.method}</td>
              <td>{log.status_code}</td>
              <td>{log.response_time.toFixed(2)}</td>
              <td>{log.timestamp}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Gráfica de tiempos de respuesta */}
      <h2>Tiempos de respuesta por endpoint</h2>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={logs}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="endpoint" />
          <YAxis unit="ms" />
          <Tooltip />
          <Bar dataKey="response_time" fill="#4f86f7" name="Tiempo (ms)" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

export default App