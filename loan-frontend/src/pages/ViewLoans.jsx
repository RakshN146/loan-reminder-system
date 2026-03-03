import { useEffect, useState } from "react";
import api from "../api";

function ViewLoans() {
  const [loans, setLoans] = useState([]);

  const fetchLoans = async () => {
    try {
      const res = await api.get("/api/loans");
      setLoans(res.data);
    } catch (err) {
      console.log(err);
    }
  };

  useEffect(() => {
    fetchLoans();
  }, []);

  const sendManualReminder = async (loanId) => {
    try {
      await api.post("/api/run-status-update");
      alert("Reminder triggered (if eligible)");
      fetchLoans();
    } catch (err) {
      console.log(err);
    }
  };

  const markAsPaid = async (loanId, amount) => {
    try {
      await api.post(`/api/mark-paid/${loanId}?paid_amount=${amount}`);
      alert("Loan marked as paid");
      fetchLoans();
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <div style={{ padding: "30px" }}>
      <h2 style={{ marginBottom: "20px" }}>All Loans</h2>

      <div style={tableWrapper}>
        <table style={table}>
          <thead>
            <tr>
              <th style={th}>Client</th>
              <th style={th}>Email</th>
              <th style={th}>Amount</th>
              <th style={th}>Due Date</th>
              <th style={th}>Status</th>
              <th style={th}>Actions</th>
            </tr>
          </thead>

          <tbody>
            {loans.map((loan) => (
              <tr key={loan.id}>
                <td style={td}>{loan.client_name}</td>
                <td style={td}>{loan.email}</td>
                <td style={td}>₹{loan.amount}</td>
                <td style={td}>{loan.due_date}</td>
                <td style={td}>
                  <span style={statusStyle(loan.status)}>
                    {loan.status}
                  </span>
                </td>

                <td style={td}>
                  <button
                    style={reminderBtn}
                    onClick={() => sendManualReminder(loan.id)}
                  >
                    Send Mail
                  </button>

                  <button
                    style={paidBtn}
                    onClick={() => markAsPaid(loan.id, loan.amount)}
                  >
                    Mark Paid
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

/* ---------- Styles ---------- */

const tableWrapper = {
  background: "white",
  borderRadius: "14px",
  boxShadow: "0 8px 20px rgba(0,0,0,0.08)",
  overflow: "hidden"
};

const table = {
  width: "100%",
  borderCollapse: "collapse"
};

const th = {
  padding: "14px 16px",
  background: "#f8fafc",
  textAlign: "left",
  fontSize: "14px",
  fontWeight: "600",
  color: "#334155",
  borderBottom: "2px solid #e2e8f0"
};

const td = {
  padding: "14px 16px",
  borderBottom: "1px solid #f1f5f9",
  fontSize: "14px",
  color: "#334155"
};

const reminderBtn = {
  padding: "6px 12px",
  marginRight: "8px",
  background: "#2563eb",
  color: "white",
  border: "none",
  borderRadius: "6px",
  cursor: "pointer",
  fontSize: "13px"
};

const paidBtn = {
  padding: "6px 12px",
  background: "#16a34a",
  color: "white",
  border: "none",
  borderRadius: "6px",
  cursor: "pointer",
  fontSize: "13px"
};

const statusStyle = (status) => {
  if (status === "OVERDUE") {
    return { color: "#dc2626", fontWeight: "600" };
  }
  if (status === "DUE") {
    return { color: "#f59e0b", fontWeight: "600" };
  }
  if (status === "PAID") {
    return { color: "#16a34a", fontWeight: "600" };
  }
  return { color: "#475569" };
};
export default ViewLoans;