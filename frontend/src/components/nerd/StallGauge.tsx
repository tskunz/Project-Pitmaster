interface Props {
  probability: number;
}

export function StallGauge({ probability }: Props) {
  const pct = Math.round(probability * 100);
  const color = pct > 70 ? 'var(--color-danger)' : pct > 40 ? 'var(--color-warning)' : 'var(--color-success)';

  return (
    <div className="card">
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
        <span style={{ fontSize: '0.875rem', color: 'var(--color-text-muted)' }}>Stall Probability</span>
        <span style={{ fontWeight: 700, color }}>{pct}%</span>
      </div>
      <div style={{
        height: 8,
        borderRadius: 4,
        background: 'var(--color-surface-2)',
        overflow: 'hidden',
      }}>
        <div style={{
          height: '100%',
          width: `${pct}%`,
          background: color,
          borderRadius: 4,
          transition: 'width 0.3s',
        }} />
      </div>
    </div>
  );
}
