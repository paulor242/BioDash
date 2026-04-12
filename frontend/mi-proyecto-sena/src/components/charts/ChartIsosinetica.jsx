import {
  LineChart,
  Line,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { SENA_COLORS } from "../../constants/colors";

function ChartIsosinetica({ data }) {
  return (
    <ResponsiveContainer width="100%" height={340}>
      <LineChart
        data={data}
        margin={{ top: 10, right: 20, left: 0, bottom: 5 }}
      >
        <CartesianGrid strokeDasharray="3 3" stroke="#d1e8c8" />
        <XAxis
          dataKey="mes"
          tick={{ fill: SENA_COLORS.darkGray, fontSize: 12 }}
        />
        <YAxis
          tick={{ fill: SENA_COLORS.midGray, fontSize: 12 }}
          domain={[0, 100]}
        />
        <Tooltip
          contentStyle={{
            borderRadius: 10,
            border: `1px solid ${SENA_COLORS.green}`,
          }}
        />
        <Legend />
        <Line
          type="monotone"
          dataKey="manual"
          name="fuerza maxima promedio"
          stroke={SENA_COLORS.darkGreen}
          strokeWidth={3}
          dot={{ r: 5 }}
        />
        <Line
          type="monotone"
          dataKey="digital"
          name="fuerza maxima"
          stroke={SENA_COLORS.yellow}
          strokeWidth={3}
          dot={{ r: 5 }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}

export default ChartIsosinetica;
