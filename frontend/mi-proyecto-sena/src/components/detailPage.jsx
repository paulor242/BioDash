import { useRef } from "react";
import { PRUEBAS, DESCRIPTIONS } from "../constants/pruebas";
import { DATA } from "../constants/data";
import { SENA_COLORS } from "../constants/colors";
import ChartYoyosq from "./charts/ChartYoyosq";
import ChartEncoderLineal from "./charts/ChartEncoderLineal";
import ChartOptogate from "./charts/ChartOptogate";
import ChartBioimpedancia from "./charts/ChartBioimpedancia";
import ChartIsosinetica from "./charts/ChartIsosinetica";
import ChartDataTable from "./charts/ChartDataTable";

const CHART_COMPONENTS = {
  yoyosq: ChartYoyosq,
  isosinetica: ChartIsosinetica,
  encoder_lineal: ChartEncoderLineal,
  optogate: ChartOptogate,
  BioImpedancia: ChartBioimpedancia,
};

function DetailPage({ pruebaId, userName }) {
  const chartRef = useRef(null);
  const prueba = PRUEBAS.find((p) => p.id === pruebaId);
  const ChartComponent = CHART_COMPONENTS[pruebaId];
  const chartData = DATA[pruebaId];

  const downloadxlsx = () => {
    const headers = Object.keys(chartData[0]).join(",");
    const rows = chartData.map((r) => Object.values(r).join(",")).join("\n");
    const blob = new Blob([`${headers}\n${rows}`], {
      type: "text/csv;charset=utf-8;",
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `SENA_${prueba.label.replace(/ /g, "_")}_${userName.replace(/ /g, "_")}.xls`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div style={{ padding: "36px 32px" }}>
      <div
        style={{
          background: "#fff",
          borderRadius: 18,
          boxShadow: "0 4px 20px rgba(0,0,0,0.07)",
          overflow: "hidden",
        }}
      >
        <div
          style={{
            padding: "22px 26px",
            borderBottom: "1px solid #f0f0f0",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            flexWrap: "wrap",
            gap: 14,
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
            <span style={{ fontSize: 30 }}>{prueba.icon}</span>
            <div>
              <h2
                style={{
                  margin: 0,
                  fontSize: 19,
                  fontWeight: 800,
                  color: SENA_COLORS.darkGreen,
                }}
              >
                {prueba.label}
              </h2>
              <p
                style={{ margin: 0, fontSize: 13, color: SENA_COLORS.midGray }}
              >
                {DESCRIPTIONS[pruebaId]}
              </p>
            </div>
          </div>
          <div style={{ display: "flex", gap: 10 }}>
            <button
              onClick={downloadxlsx}
              style={{
                background: SENA_COLORS.softGray,
                border: `1.5px solid ${SENA_COLORS.green}`,
                color: SENA_COLORS.darkGreen,
                borderRadius: 10,
                padding: "8px 18px",
                cursor: "pointer",
                fontWeight: 600,
                fontSize: 13,
              }}
            >
              📥 Descargar xlsx
            </button>
          </div>
        </div>
        <div ref={chartRef} style={{ padding: "28px 26px" }}>
          <ChartComponent data={chartData} />
          <ChartDataTable data={chartData} />
        </div>
        <div
          style={{
            padding: "14px 26px",
            background: SENA_COLORS.softGray,
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
          }}
        >
          <span style={{ fontSize: 13, color: SENA_COLORS.midGray }}>
            👤 Resultados de:{" "}
            <strong style={{ color: SENA_COLORS.darkGreen }}>{userName}</strong>
          </span>
          <span style={{ fontSize: 13, color: SENA_COLORS.midGray }}>
            📅{" "}
            {new Date().toLocaleDateString("es-CO", {
              year: "numeric",
              month: "long",
              day: "numeric",
            })}
          </span>
        </div>
      </div>
    </div>
  );
}

export default DetailPage;
