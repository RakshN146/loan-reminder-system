import { useEffect, useState } from "react";
import api from "../api";

function ClientReplies() {
  const [replies, setReplies] = useState([]);

  useEffect(() => {
    const fetchReplies = async () => {
      try {
        const res = await api.get("/api/client-replies");
        setReplies(res.data);
      } catch (err) {
        console.log(err);
      }
    };

    fetchReplies();
  }, []);

  return (
    <div style={container}>
      <h2 style={{ marginBottom: "20px" }}>Client Replies</h2>

      {replies.length === 0 ? (
        <p>No client replies found.</p>
      ) : (
        <div style={tableWrapper}>
          <table style={table}>
            <thead>
              <tr>
                <th style={th}>Client Email</th>
                <th style={th}>Subject</th>
                <th style={th}>Message</th>
                <th style={th}>Date</th>
              </tr>
            </thead>

            <tbody>
              {replies.map((reply) => (
                <tr key={reply.id}>
                  <td style={td}>{reply.recipient_email}</td>
                  <td style={td}>{reply.subject}</td>
                  <td style={td}>
                    {reply.body.substring(0, 100)}...
                  </td>
                  <td style={td}>
                    {new Date(reply.sent_at).toLocaleString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

/* ---------- STYLES ---------- */

const container = {
  padding: "30px"
};

const tableWrapper = {
  overflowX: "auto",
  background: "white",
  borderRadius: "12px",
  boxShadow: "0 5px 15px rgba(0,0,0,0.05)"
};

const table = {
  width: "100%",
  borderCollapse: "collapse"
};

const th = {
  textAlign: "left",
  padding: "12px",
  background: "#f3f4f6",
  borderBottom: "1px solid #e5e7eb",
  fontSize: "14px"
};

const td = {
  padding: "12px",
  borderBottom: "1px solid #f1f5f9",
  fontSize: "14px"
};

export default ClientReplies;