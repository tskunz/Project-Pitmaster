import type { ConfidenceTier } from '../../types/cook';

const LABELS: Record<ConfidenceTier, string> = {
  high: 'High',
  moderate: 'Moderate',
  low: 'Low',
  very_low: 'Very Low',
};

export function ConfidenceBadge({ confidence }: { confidence: ConfidenceTier }) {
  return <span className={`badge badge-${confidence}`}>{LABELS[confidence]}</span>;
}
