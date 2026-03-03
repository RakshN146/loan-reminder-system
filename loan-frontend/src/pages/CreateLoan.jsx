import { useState } from "react";
import api from "../api";

function CreateLoan() {
  const [form, setForm] = useState({
    client_name: "",
    email: "",
    amount: "",
    due_date: ""
  });

  const [message, setMessage] = useState("");

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await api.post("/api/loans", {
        ...form,
        amount: Number(form.amount)
      });

      setMessage("Loan Created Successfully ✅");

      setForm({
        client_name: "",
        email: "",
        amount: "",
        due_date: ""
      });

    } catch (err) {
      console.log(err);
      setMessage("Error creating loan ❌");
    }
  };

  return (
    <div style={container}>
      <div style={card}>
        <h2 style={{ marginBottom: "20px" }}>Create Loan</h2>

        <form onSubmit={handleSubmit} style={{ width: "100%" }}>
          
          <input
            type="text"
            name="client_name"
            placeholder="Client Name"
            value={form.client_name}
            onChange={handleChange}
            required
            style={input}
          />

          <input
            type="email"
            name="email"
            placeholder="Client Email"
            value={form.email}
            onChange={handleChange}
            required
            style={input}
          />

          <input
            type="number"
            name="amount"
            placeholder="Loan Amount"
            value={form.amount}
            onChange={handleChange}
            required
            style={input}
          />

          <input
            type="date"
            name="due_date"
            value={form.due_date}
            onChange={handleChange}
            required
            style={input}
          />

          <button type="submit" style={button}>
            Create Loan
          </button>

          {message && (
            <p style={{ marginTop: "15px", fontWeight: "500" }}>
              {message}
            </p>
          )}

        </form>
      </div>
    </div>
  );
}

/* -------- STYLES -------- */

const container = {
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
  height: "80vh"
};

const card = {
  background: "white",
  padding: "40px",
  width: "400px",
  borderRadius: "16px",
  boxShadow: "0 10px 30px rgba(0,0,0,0.08)",
  textAlign: "center"
};

const input = {
  width: "100%",
  padding: "12px",
  marginBottom: "15px",
  borderRadius: "8px",
  border: "1px solid #e5e7eb",
  fontSize: "14px"
};

const button = {
  width: "100%",
  padding: "12px",
  background: "#3b82f6",
  color: "white",
  border: "none",
  borderRadius: "8px",
  cursor: "pointer",
  fontSize: "15px"
};

export default CreateLoan;