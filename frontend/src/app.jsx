import { useState, useEffect } from "react"
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts"

function App() {
  const [logs, setLogs] = useState([])
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch("http://localhost:8000/logs")
      .then(res => res.json())
      .then(data => setLogs(data))
      .catch(err => setError("Error al conectar con la API"))
  }, [])

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>API Monitor Dashboard</h1>

      {error && <p style={{ color: "red" }}>{error}</p>}

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