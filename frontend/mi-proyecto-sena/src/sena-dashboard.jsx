import { useState } from "react";
import Sidebar from "./components/Sidebar.jsx";
import HomePage from "./components/Homepage.jsx";
import DetailPage from "./components/detailPage.jsx";
import { SENA_COLORS } from "./constants/colors.js";
import { PRUEBAS } from "./constants/pruebas.js";

const PIE_COLORS = [
  SENA_COLORS.green,
  SENA_COLORS.yellow,
  SENA_COLORS.lightGreen,
  SENA_COLORS.darkGreen,
  SENA_COLORS.darkYellow,
];

export default function SenaDashboard() {
  const [activeTab, setActiveTab] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [userName, setUserName] = useState("");
  const [editingName, setEditingName] = useState(false);
  const [tempName, setTempName] = useState("");

  return (
    <div
      style={{
        display: "flex",
        minHeight: "100vh",
        fontFamily: "'Segoe UI', sans-serif",
        background: SENA_COLORS.gray,
      }}
    >
      {activeTab !== null && (
        <Sidebar
          activeTab={activeTab}
          onSelect={setActiveTab}
          sidebarOpen={sidebarOpen}
          setSidebarOpen={setSidebarOpen}
          userName={userName}
        />
      )}

      <main
        style={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
          overflow: "auto",
        }}
      >
        <header
          style={{
            background: "#fff",
            borderBottom: `3px solid ${SENA_COLORS.green}`,
            padding: "14px 28px",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            boxShadow: "0 2px 10px rgba(0,0,0,0.06)",
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            {activeTab && (
              <button
                onClick={() => setActiveTab(null)}
                style={{
                  background: SENA_COLORS.softGray,
                  border: "none",
                  borderRadius: 8,
                  padding: "6px 12px",
                  cursor: "pointer",
                  color: SENA_COLORS.darkGreen,
                  fontWeight: 600,
                  fontSize: 13,
                }}
              >
                ← Inicio
              </button>
            )}
            <div>
              <h1
                style={{
                  margin: 0,
                  fontSize: 19,
                  fontWeight: 800,
                  color: SENA_COLORS.darkGreen,
                }}
              >
                {activeTab
                  ? PRUEBAS.find((p) => p.id === activeTab)?.label
                  : "Panel de Evaluaciones"}
              </h1>
              <p
                style={{ margin: 0, fontSize: 12, color: SENA_COLORS.midGray }}
              >
                {activeTab
                  ? "Resultados detallados"
                  : "Selecciona una prueba para comenzar"}
              </p>
            </div>
          </div>

          {editingName ? (
            <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
              <input
                value={tempName}
                onChange={(e) => setTempName(e.target.value)}
                onKeyDown={(e) =>
                  e.key === "Enter" &&
                  (setUserName(tempName.trim() || userName),
                  setEditingName(false))
                }
                style={{
                  border: `2px solid ${SENA_COLORS.green}`,
                  borderRadius: 8,
                  padding: "6px 10px",
                  fontSize: 13,
                  outline: "none",
                }}
                autoFocus
              />
              <button
                onClick={() => {
                  if (tempName.trim()) setUserName(tempName.trim());
                  setEditingName(false);
                }}
                style={{
                  background: SENA_COLORS.green,
                  color: "#fff",
                  border: "none",
                  borderRadius: 8,
                  padding: "6px 14px",
                  cursor: "pointer",
                  fontWeight: 600,
                }}
              >
                Guardar
              </button>
            </div>
          ) : (
            <div
              onClick={() => {
                setTempName(userName);
                setEditingName(true);
              }}
              style={{
                display: "flex",
                alignItems: "center",
                gap: 10,
                background: SENA_COLORS.softGray,
                borderRadius: 30,
                padding: "7px 16px",
                cursor: "pointer",
              }}
            >
              <div
                style={{
                  width: 30,
                  height: 30,
                  borderRadius: "50%",
                  background: SENA_COLORS.green,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  color: "#fff",
                  fontWeight: 700,
                  fontSize: 12,
                }}
              >
                {userName
                  .split(" ")
                  .map((n) => n[0])
                  .slice(0, 2)
                  .join("")}
              </div>
              <span
                style={{
                  fontWeight: 600,
                  color: SENA_COLORS.darkGreen,
                  fontSize: 14,
                }}
              >
                {userName}
              </span>
              <span style={{ fontSize: 12 }}>✏️</span>
            </div>
          )}
        </header>

        {activeTab === null ? (
          <HomePage onSelect={setActiveTab} userName={userName} />
        ) : (
          <DetailPage pruebaId={activeTab} userName={userName} />
        )}
      </main>
    </div>
  );
}
