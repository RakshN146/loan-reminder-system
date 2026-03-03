import { Link, useNavigate } from "react-router-dom";

function Navbar() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <nav style={navStyle}>
      <div style={logoStyle}>Loan Reminder System</div>

      <div style={linkContainer}>
        <Link style={linkStyle} to="/dashboard">Dashboard</Link>
        <Link style={linkStyle} to="/create">Create Loan</Link>
        <Link style={linkStyle} to="/loans">View Loans</Link>
        <Link style={linkStyle} to="/replies">Client Replies</Link>

        <button onClick={handleLogout} style={logoutBtn}>
          Logout
        </button>
      </div>
    </nav>
  );
}

const navStyle = {
  background: "#0f172a",
  padding: "15px 40px",
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  color: "white"
};

const logoStyle = {
  fontWeight: "bold",
  fontSize: "18px"
};

const linkContainer = {
  display: "flex",
  gap: "20px",
  alignItems: "center"
};

const linkStyle = {
  color: "white",
  textDecoration: "none"
};

const logoutBtn = {
  background: "#ef4444",
  border: "none",
  padding: "8px 15px",
  color: "white",
  borderRadius: "6px",
  cursor: "pointer"
};

export default Navbar;