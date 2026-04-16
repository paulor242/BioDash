import {
   AreaChart,
  Area,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { SENA_COLORS } from "../../constants/colors";

function ChartOptogate({ data }) {
  return (
    <ResponsiveContainer width="100%" height={340}>
      <AreaChart
        data={data}
        margin={{ top: 10, right: 20, left: 0, bottom: 5 }}
      >
        <defs>
          <linearGradient id="gb" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor={SENA_COLORS.green} stopOpacity={0.4} />
            <stop offset="95%" stopColor={SENA_COLORS.green} stopOpacity={0} />
          </linearGradient>
          <linearGradient id="gm" x1="0" y1="0" x2="0" y2="1">
            <stop
              offset="5%"
              stopColor={SENA_COLORS.yellow}
              stopOpacity={0.4}
            />
            <stop offset="95%" stopColor={SENA_COLORS.yellow} stopOpacity={0} />
          </linearGradient>
          <linearGradient id="ge" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#ef4444" stopOpacity={0.3} />
            <stop offset="95%" stopColor="#ef4444" stopOpacity={0} />
          </linearGradient>
        </defs>
        <CartesianGrid strokeDasharray="3 3" stroke="#d1e8c8" />
        <XAxis
          dataKey="factor"
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
        <Area
          type="monotone"
          dataKey="bienestar"
          name="fuerza promedio"
          stroke={SENA_COLORS.green}
          fill="url(#gb)"
          strokeWidth={2}
        />
        <Area
          type="monotone"
          dataKey="motivacion"
          name="velocidad"
          stroke={SENA_COLORS.yellow}
          fill="url(#gm)"
          strokeWidth={2}
        />
        <Area
          type="monotone"
          dataKey="estres"
          name="fuerza promedio"
          stroke="#ef4444"
          fill="url(#ge)"
          strokeWidth={2}
        />
      </AreaChart>
    </ResponsiveContainer>
  );
}

export default ChartOptogate;
