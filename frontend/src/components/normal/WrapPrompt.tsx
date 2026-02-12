import type { WrapType } from '../../types/cook';

interface Props {
  onWrap: (wrapType: WrapType) => void;
  visible: boolean;
}

const WRAP_OPTIONS: { type: WrapType; label: string; desc: string }[] = [
  { type: 'foil', label: 'Foil', desc: 'Fastest — softer bark' },
  { type: 'butcher_paper', label: 'Butcher Paper', desc: 'Balanced — keeps bark' },
  { type: 'foil_boat', label: 'Foil Boat', desc: 'Moderate protection' },
];

export function WrapPrompt({ onWrap, visible }: Props) {
  if (!visible) return null;

  return (
    <div className="card" style={{ borderLeft: '4px solid var(--color-primary)' }}>
      <strong>Consider wrapping?</strong>
      <p style={{ color: 'var(--color-text-muted)', margin: '8px 0' }}>
        Wrapping can help push through the stall faster.
      </p>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
        {WRAP_OPTIONS.map((opt) => (
          <button key={opt.type} className="btn-secondary" onClick={() => onWrap(opt.type)}>
            {opt.label} — <span style={{ fontWeight: 400 }}>{opt.desc}</span>
          </button>
        ))}
      </div>
    </div>
  );
}
