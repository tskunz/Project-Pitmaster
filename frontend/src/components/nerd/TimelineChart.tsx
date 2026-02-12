import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

interface DataPoint {
  elapsed: number;
  p10: number;
  p50: number;
  p90: number;
}

interface Props {
  data: DataPoint[];
}

export function TimelineChart({ data }: Props) {
  if (data.length < 2) {
    return (
      <div className="card" style={{ textAlign: 'center', color: 'var(--color-text-muted)', padding: 32 }}>
        Need more readings for timeline chart
      </div>
    );
  }

  return (
    <div className="card">
      <h3 style={{ fontSize: '0.875rem', color: 'var(--color-text-muted)', marginBottom: 12 }}>
        Prediction Timeline (minutes remaining)
      </h3>
      <ResponsiveContainer width="100%" height={200}>
        <AreaChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="var(--color-surface-2)" />
          <XAxis
            dataKey="elapsed"
            stroke="var(--color-text-muted)"
            fontSize={12}
            tickFormatter={(v: number) => `${Math.round(v)}m`}
          />
          <YAxis stroke="var(--color-text-muted)" fontSize={12} />
          <Tooltip
            contentStyle={{ background: 'var(--color-surface)', border: 'none', borderRadius: 8 }}
            labelFormatter={(v: number) => `${Math.round(v)} min elapsed`}
          />
          <Area type="monotone" dataKey="p90" stroke="var(--color-danger)" fill="var(--color-danger)" fillOpacity={0.1} name="P90" />
          <Area type="monotone" dataKey="p50" stroke="var(--color-primary-light)" fill="var(--color-primary-light)" fillOpacity={0.2} name="P50" />
          <Area type="monotone" dataKey="p10" stroke="var(--color-success)" fill="var(--color-success)" fillOpacity={0.1} name="P10" />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
