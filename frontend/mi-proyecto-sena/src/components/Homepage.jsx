import { useState } from "react";
import { PRUEBAS } from "../constants/pruebas";
import { SENA_COLORS } from "../constants/colors";

function HomePage({ onSelect, userName }) {
  const [hovered, setHovered] = useState(null);
  return (
    <div style={{ padding: "36px 32px" }}>
      <div style={{ marginBottom: 32 }}>
        <h2
          style={{
            margin: 0,
            fontSize: 26,
            fontWeight: 800,
            color: SENA_COLORS.darkGreen,
          }}
        >
          ¡Bienvenido, {userName.split("")[0]}! 
        </h2>
        <p
          style={{
            margin: "6px 0 0",
            color: SENA_COLORS.midGray,
            fontSize: 15,
          }}
        >
          Selecciona una prueba para ver tus resultados y gráficas.
        </p>
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fill, minmax(220px, 1fr))",
          gap: 22,
        }}
      >
        {PRUEBAS.map((p) => (
          <button
            key={p.id}
            onClick={() => onSelect(p.id)}
            onMouseEnter={() => setHovered(p.id)}
            onMouseLeave={() => setHovered(null)}
            style={{
              background: "#fff",
              border: `2px solid ${hovered === p.id ? SENA_COLORS.green : "#e5e7eb"}`,
              borderRadius: 18,
              padding: "28px 22px",
              cursor: "pointer",
              textAlign: "left",
              boxShadow:
                hovered === p.id
                  ? `0 8px 28px rgba(57,169,0,0.18)`
                  : "0 2px 12px rgba(0,0,0,0.07)",
              transform:
                hovered === p.id ? "translateY(-3px)" : "translateY(0)",
              transition: "all 0.22s",
              display: "flex",
              flexDirection: "column",
              gap: 12,
            }}
          >
            <div
              style={{
                width: 54,
                height: 54,
                borderRadius: 14,
                background: SENA_COLORS.softGray,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontSize: 28,
              }}
            >
              {p.icon}
            </div>
            <div>
              <div
                style={{
                  fontWeight: 700,
                  fontSize: 15,
                  color: SENA_COLORS.darkGreen,
                  marginBottom: 6,
                }}
              >
                {p.label}
              </div>
              <div
                style={{
                  fontSize: 13,
                  color: SENA_COLORS.midGray,
                  lineHeight: 1.5,
                }}
              >
                {p.desc}
              </div>
            </div>
            <div
              style={{
                marginTop: 4,
                display: "flex",
                alignItems: "center",
                gap: 6,
                color: SENA_COLORS.green,
                fontWeight: 600,
                fontSize: 13,
              }}
            >
              Ver resultados <span>→</span>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}

export default HomePage;
