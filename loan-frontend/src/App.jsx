import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Navbar from "./components/Navbar";
import Dashboard from "./pages/Dashboard";
import CreateLoan from "./pages/CreateLoan";
import ViewLoans from "./pages/ViewLoans";
import ClientReplies from "./pages/ClientReplies";
import Login from "./pages/Login";

const PrivateRoute = ({ children }) => {
  const token = localStorage.getItem("token");
  return token ? children : <Navigate to="/login" />;
};

function App() {
  return (
    <Router>
      <Navbar />

      <div style={{ padding: "40px", background: "#f1f5f9", minHeight: "100vh" }}>
        <Routes>
          <Route path="/login" element={<Login />} />

          <Route
            path="/dashboard"
            element={
              <PrivateRoute>
                <Dashboard />
              </PrivateRoute>
            }
          />

          <Route
            path="/create"
            element={
              <PrivateRoute>
                <CreateLoan />
              </PrivateRoute>
            }
          />

          <Route
            path="/loans"
            element={
              <PrivateRoute>
                <ViewLoans />
              </PrivateRoute>
            }
          />

          <Route
            path="/replies"
            element={
              <PrivateRoute>
                <ClientReplies />
              </PrivateRoute>
            }
          />

          <Route path="*" element={<Navigate to="/dashboard" />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;