import { useState } from 'react';
import type { QualityRating } from '../../types/cook';

interface Props {
  onSubmit: (rating: QualityRating, notes: string) => void;
}

const RATINGS: { value: QualityRating; label: string }[] = [
  { value: 'excellent', label: 'Excellent' },
  { value: 'good', label: 'Good' },
  { value: 'fair', label: 'Fair' },
  { value: 'poor', label: 'Poor' },
];

export function QualityForm({ onSubmit }: Props) {
  const [rating, setRating] = useState<QualityRating>('good');
  const [notes, setNotes] = useState('');

  return (
    <div className="card">
      <h3 style={{ fontSize: '0.875rem', color: 'var(--color-text-muted)', marginBottom: 12 }}>
        How was it?
      </h3>
      <div style={{ display: 'flex', gap: 8, marginBottom: 12 }}>
        {RATINGS.map((r) => (
          <button
            key={r.value}
            className={rating === r.value ? 'btn-primary' : 'btn-secondary'}
            style={{ flex: 1, padding: '8px 4px', fontSize: '0.75rem' }}
            onClick={() => setRating(r.value)}
            type="button"
          >
            {r.label}
          </button>
        ))}
      </div>
      <textarea
        value={notes}
        onChange={(e) => setNotes(e.target.value)}
        placeholder="Notes (optional)"
        style={{
          width: '100%',
          minHeight: 80,
          background: 'var(--color-bg)',
          border: '1px solid var(--color-surface-2)',
          borderRadius: 'var(--radius)',
          padding: 12,
          color: 'var(--color-text)',
          resize: 'vertical',
        }}
      />
      <button
        className="btn-primary"
        style={{ width: '100%', marginTop: 12 }}
        onClick={() => onSubmit(rating, notes)}
      >
        Save Rating
      </button>
    </div>
  );
}
