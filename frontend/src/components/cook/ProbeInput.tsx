import { useState } from 'react';

interface Props {
  onSubmit: (tempF: number) => void;
  loading: boolean;
}

export function ProbeInput({ onSubmit, loading }: Props) {
  const [value, setValue] = useState('');

  const handleNum = (n: string) => {
    if (n === 'del') {
      setValue((v) => v.slice(0, -1));
    } else if (n === 'go') {
      const temp = parseFloat(value);
      if (temp >= 32 && temp <= 212) {
        onSubmit(temp);
        setValue('');
      }
    } else {
      setValue((v) => {
        if (v.length >= 5) return v; // max "212.5"
        return v + n;
      });
    }
  };

  return (
    <div className="card">
      <label>Probe Temperature</label>
      <div style={{
        fontSize: '2.5rem',
        fontWeight: 700,
        textAlign: 'center',
        padding: '8px 0',
        minHeight: 56,
        color: value ? 'var(--color-primary-light)' : 'var(--color-text-muted)',
      }}>
        {value || '---'}&deg;F
      </div>
      <div className="numpad">
        {['1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '0', 'del'].map((n) => (
          <button key={n} onClick={() => handleNum(n)} type="button">
            {n === 'del' ? '\u232B' : n}
          </button>
        ))}
      </div>
      <button
        className="btn-primary"
        style={{ width: '100%', marginTop: 12 }}
        onClick={() => handleNum('go')}
        disabled={loading || !value}
      >
        {loading ? 'Logging...' : 'Log Reading'}
      </button>
    </div>
  );
}
