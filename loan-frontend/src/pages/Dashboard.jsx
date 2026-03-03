import { useEffect, useState } from "react";
import api from "../api";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from "recharts";

function Dashboard() {
  const [data, setData] = useState(null);

  useEffect(() => {
    api.get("/api/dashboard-summary")
      .then(res => setData(res.data))
      .catch(err => console.log(err));
  }, []);

  if (!data) return <h2>Loading Dashboard...</h2>;

  const chartData = [
    { name: "Upcoming", value: data.upcoming },
    { name: "Due", value: data.due },
    { name: "Overdue", value: data.overdue },
    { name: "Paid", value: data.paid },
  ];

  const COLORS = ["#3b82f6", "#f59e0b", "#ef4444", "#10b981"];

  return (
    <div>
      <h1 style={{ marginBottom: "30px" }}>Analytics Dashboard</h1>

      {/* SUMMARY CARDS */}
      <div style={gridStyle}>
        {Object.entries(data).map(([key, value]) => (
          <div key={key} style={cardStyle}>
            <h4 style={{ color: "#64748b" }}>
              {key.replace("_", " ").toUpperCase()}
            </h4>
            <h2 style={{ marginTop: "10px" }}>{value}</h2>
          </div>
        ))}
      </div>

      {/* CHART SECTION */}
      <div style={{ display: "flex", gap: "40px", marginTop: "50px" }}>
        
        {/* BAR CHART */}
        <div style={chartCard}>
          <h3>Status Overview</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={chartData}>
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="#3b82f6" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* PIE CHART */}
        <div style={chartCard}>
          <h3>Loan Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={chartData}
                dataKey="value"
                nameKey="name"
                outerRadius={100}
              >
                {chartData.map((entry, index) => (
                  <Cell key={index} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

      </div>
    </div>
  );
}

const gridStyle = {
  display: "grid",
  gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
  gap: "25px"
};

const cardStyle = {
  background: "white",
  padding: "30px",
  borderRadius: "12px",
  boxShadow: "0 8px 20px rgba(0,0,0,0.05)",
};

const chartCard = {
  flex: 1,
  background: "white",
  padding: "30px",
  borderRadius: "12px",
  boxShadow: "0 8px 20px rgba(0,0,0,0.05)",
};

export default Dashboard;