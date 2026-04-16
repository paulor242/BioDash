import { SENA_COLORS } from "../../constants/colors";

function formatHeaderLabel(key) {
  return key
    .replace(/_/g, " ")
    .replace(/([a-z])([A-Z])/g, "$1 $2")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function ChartDataTable({ data }) {
  if (!data?.length) {
    return null;
  }

  const columns = Object.keys(data[0]);

  return (
    <div
      style={{
        marginTop: 28,
        border: `1px solid ${SENA_COLORS.softGray}`,
        borderRadius: 16,
        overflow: "hidden",
        background: "#fff",
      }}
    >
      <div
        style={{
          padding: "14px 18px",
          background: SENA_COLORS.softGray,
          borderBottom: `1px solid ${SENA_COLORS.gray}`,
        }}
      >
        <h3
          style={{
            margin: 0,
            fontSize: 15,
            fontWeight: 700,
            color: SENA_COLORS.darkGreen,
          }}
        >
          Tabla de datos
        </h3>
      </div>

      <div style={{ overflowX: "auto" }}>
        <table
          style={{
            width: "100%",
            borderCollapse: "collapse",
            minWidth: 520,
          }}
        >
          <thead>
            <tr style={{ background: "#F9FCF7" }}>
              {columns.map((column) => (
                <th
                  key={column}
                  style={{
                    textAlign: "left",
                    padding: "12px 18px",
                    fontSize: 12,
                    fontWeight: 700,
                    color: SENA_COLORS.darkGreen,
                    borderBottom: `1px solid ${SENA_COLORS.gray}`,
                  }}
                >
                  {formatHeaderLabel(column)}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.map((row, index) => (
              <tr
                key={`${columns[0]}-${row[columns[0]]}-${index}`}
                style={{
                  background: index % 2 === 0 ? "#fff" : "#FCFDFB",
                }}
              >
                {columns.map((column) => (
                  <td
                    key={`${column}-${index}`}
                    style={{
                      padding: "12px 18px",
                      fontSize: 13,
                      color: SENA_COLORS.darkGray,
                      borderBottom: `1px solid ${SENA_COLORS.gray}`,
                    }}
                  >
                    {row[column]}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default ChartDataTable;
