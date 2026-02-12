import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';

interface Props {
  data: { elapsed: number; temp: number }[];
}

export function SlopeChart({ data }: Props) {
  if (data.length < 3) {
    return (
      <div className="card" style={{ textAlign: 'center', color: 'var(--color-text-muted)', padding: 32 }}>
        Need more readings for slope chart
      </div>
    );
  }

  // Compute slopes
  const slopeData = data.slice(1).map((point, i) => ({
    elapsed: point.elapsed,
    slope: point.temp - data[i].temp,
  }));

  return (
    <div className="card">
      <h3 style={{ fontSize: '0.875rem', color: 'var(--color-text-muted)', marginBottom: 12 }}>
        Temperature Slope (&deg;F/reading)
      </h3>
      <ResponsiveContainer width="100%" height={150}>
        <LineChart data={slopeData}>
          <CartesianGrid strokeDasharray="3 3" stroke="var(--color-surface-2)" />
          <XAxis dataKey="elapsed" stroke="var(--color-text-muted)" fontSize={12} />
          <YAxis stroke="var(--color-text-muted)" fontSize={12} />
          <Tooltip contentStyle={{ background: 'var(--color-surface)', border: 'none', borderRadius: 8 }} />
          <ReferenceLine y={0.02} stroke="var(--color-warning)" strokeDasharray="3 3" label="Stall" />
          <Line type="monotone" dataKey="slope" stroke="var(--color-info)" dot={false} strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
