import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';

interface Props {
  residuals: number[];
}

export function ResidualChart({ residuals }: Props) {
  if (residuals.length < 2) return null;

  const data = residuals.map((r, i) => ({ index: i + 1, residual: r }));

  return (
    <div className="card">
      <h3 style={{ fontSize: '0.875rem', color: 'var(--color-text-muted)', marginBottom: 12 }}>
        Prediction Residuals (&deg;F)
      </h3>
      <ResponsiveContainer width="100%" height={150}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="var(--color-surface-2)" />
          <XAxis dataKey="index" stroke="var(--color-text-muted)" fontSize={12} />
          <YAxis stroke="var(--color-text-muted)" fontSize={12} />
          <Tooltip contentStyle={{ background: 'var(--color-surface)', border: 'none', borderRadius: 8 }} />
          <ReferenceLine y={0} stroke="var(--color-text-muted)" />
          <Bar dataKey="residual" fill="var(--color-primary)" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
