interface Props {
  label: string;
  minutes: number;
  time?: string;
  highlight?: boolean;
}

function formatMinutes(min: number): string {
  const h = Math.floor(min / 60);
  const m = Math.round(min % 60);
  if (h === 0) return `${m}m`;
  return `${h}h ${m}m`;
}

function formatTime(iso: string): string {
  const d = new Date(iso);
  return d.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' });
}

export function TimeDisplay({ label, minutes, time, highlight }: Props) {
  return (
    <div style={{ textAlign: 'center', padding: '8px 0' }}>
      <div style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)', marginBottom: 4 }}>
        {label}
      </div>
      <div className={highlight ? 'big-number' : ''} style={highlight ? {} : { fontSize: '1.5rem', fontWeight: 700 }}>
        {formatMinutes(minutes)}
      </div>
      {time && (
        <div style={{ fontSize: '0.875rem', color: 'var(--color-text-muted)', marginTop: 2 }}>
          {formatTime(time)}
        </div>
      )}
    </div>
  );
}
