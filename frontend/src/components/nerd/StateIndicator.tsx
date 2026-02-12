import type { CookState } from '../../types/cook';

const STATE_LABELS: Record<CookState, { label: string; color: string }> = {
  setup: { label: 'Setup', color: 'var(--color-text-muted)' },
  preheat: { label: 'Preheating', color: 'var(--color-info)' },
  early_cook: { label: 'Early Cook', color: 'var(--color-info)' },
  pre_stall: { label: 'Pre-Stall', color: 'var(--color-warning)' },
  stall: { label: 'STALL', color: 'var(--color-danger)' },
  post_stall: { label: 'Post-Stall', color: 'var(--color-success)' },
  approaching_target: { label: 'Almost There!', color: 'var(--color-primary-light)' },
  rest: { label: 'Resting', color: 'var(--color-success)' },
  done: { label: 'DONE', color: 'var(--color-success)' },
};

export function StateIndicator({ state }: { state: CookState }) {
  const info = STATE_LABELS[state];
  return (
    <div style={{
      display: 'inline-flex',
      alignItems: 'center',
      gap: 8,
      padding: '4px 12px',
      borderRadius: 20,
      background: 'var(--color-surface)',
      border: `2px solid ${info.color}`,
      fontSize: '0.875rem',
      fontWeight: 600,
    }}>
      <span style={{
        width: 8, height: 8, borderRadius: '50%',
        background: info.color,
      }} />
      {info.label}
    </div>
  );
}
