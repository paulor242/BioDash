import { PRUEBAS } from "../constants/pruebas";
import { SENA_COLORS } from "../constants/colors";

function Sidebar({
  activeTab,
  onSelect,
  sidebarOpen,
  setSidebarOpen,
  userName,
}) {
  return (
    <aside
      style={{
        width: sidebarOpen ? 256 : 64,
        background: `linear-gradient(180deg, ${SENA_COLORS.darkGreen} 0%, ${SENA_COLORS.green} 100%)`,
        transition: "width 0.3s ease",
        overflow: "hidden",
        display: "flex",
        flexDirection: "column",
        boxShadow: "4px 0 20px rgba(0,0,0,0.15)",
        flexShrink: 0,
      }}
    >
      <div
        style={{
          padding: "18px 14px",
          display: "flex",
          alignItems: "center",
          gap: 10,
          borderBottom: "1px solid rgba(255,255,255,0.15)",
        }}
      >
        <button
          onClick={() => setSidebarOpen(!sidebarOpen)}
          style={{
            background: "rgba(255,255,255,0.15)",
            border: "none",
            borderRadius: 8,
            cursor: "pointer",
            width: 34,
            height: 34,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            flexShrink: 0,
          }}
        >
          <span style={{ color: "#fff", fontSize: 18 }}>☰</span>
        </button>
        {sidebarOpen && (
          <div>
            <div
              style={{
                color: "#fff",
                fontWeight: 800,
                fontSize: 20,
                letterSpacing: 1,
              }}
            >
              SENA
            </div>
            <div style={{ color: "rgba(255,255,255,0.65)", fontSize: 11 }}>
              Sistema de Evaluación
            </div>
          </div>
        )}
      </div>

      {sidebarOpen && (
        <div
          style={{
            padding: "14px",
            borderBottom: "1px solid rgba(255,255,255,0.15)",
            display: "flex",
            alignItems: "center",
            gap: 10,
          }}
        >
          <div
            style={{
              width: 38,
              height: 38,
              borderRadius: "50%",
              background: SENA_COLORS.yellow,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontWeight: 700,
              color: SENA_COLORS.darkGreen,
              fontSize: 15,
              flexShrink: 0,
            }}
          >
            {userName
              .split(" ")
              .map((n) => n[0])
              .slice(0, 2)
              .join("")}
          </div>
          <div>
            <div style={{ color: "#fff", fontWeight: 600, fontSize: 13 }}>
              {userName}
            </div>
            <div style={{ color: "rgba(255,255,255,0.6)", fontSize: 11 }}>
              Aprendiz SENA
            </div>
          </div>
        </div>
      )}

      <nav style={{ flex: 1, padding: "10px 8px" }}>
        <button
          onClick={() => onSelect(null)}
          style={{
            display: "flex",
            alignItems: "center",
            gap: 12,
            width: "100%",
            padding: "11px 12px",
            background:
              activeTab === null ? "rgba(255,255,255,0.2)" : "transparent",
            border:
              activeTab === null
                ? "1px solid rgba(255,255,255,0.3)"
                : "1px solid transparent",
            borderRadius: 10,
            cursor: "pointer",
            marginBottom: 4,
            transition: "all 0.2s",
          }}
        >
          <span style={{ fontSize: 19, flexShrink: 0 }}></span>
          {sidebarOpen && (
            <span
              style={{
                color: "#fff",
                fontSize: 13,
                fontWeight: activeTab === null ? 700 : 400,
              }}
            >
              🏠 Inicio
            </span>
          )}
        </button>
        {PRUEBAS.map((p) => (
          <button
            key={p.id}
            onClick={() => onSelect(p.id)}
            style={{
              display: "flex",
              alignItems: "center",
              gap: 12,
              width: "100%",
              padding: "11px 12px",
              background:
                activeTab === p.id ? "rgba(255,255,255,0.2)" : "transparent",
              border:
                activeTab === p.id
                  ? "1px solid rgba(255,255,255,0.3)"
                  : "1px solid transparent",
              borderRadius: 10,
              cursor: "pointer",
              marginBottom: 4,
              transition: "all 0.2s",
            }}
          >
            <span style={{ fontSize: 19, flexShrink: 0 }}>{p.icon}</span>
            {sidebarOpen && (
              <span
                style={{
                  color: "#fff",
                  fontSize: 13,
                  fontWeight: activeTab === p.id ? 700 : 400,
                  textAlign: "left",
                  lineHeight: 1.3,
                }}
              >
                {p.label}
              </span>
            )}
          </button>
        ))}
      </nav>

      {sidebarOpen && (
        <div
          style={{
            padding: "12px 16px",
            borderTop: "1px solid rgba(255,255,255,0.15)",
          }}
        >
          <div
            style={{
              color: "rgba(255,255,255,0.45)",
              fontSize: 11,
              textAlign: "center",
            }}
          >
            © 2024 SENA Colombia
          </div>
        </div>
      )}
    </aside>
  );
}

export default Sidebar;
