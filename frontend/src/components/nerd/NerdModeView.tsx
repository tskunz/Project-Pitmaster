import type { PredictionResponse, StateResponse } from '../../types/cook';
import { TimelineChart } from './TimelineChart';
import { StallGauge } from './StallGauge';
import { SlopeChart } from './SlopeChart';
import { StateIndicator } from './StateIndicator';
import { ConfidenceBadge } from '../normal/ConfidenceBadge';
import { TimeDisplay } from '../normal/TimeDisplay';

interface Props {
  prediction: PredictionResponse;
  state: StateResponse | null;
  tempHistory: { elapsed: number; temp: number }[];
  predictionHistory: { elapsed: number; p10: number; p50: number; p90: number }[];
}

export function NerdModeView({ prediction, state, tempHistory, predictionHistory }: Props) {
  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
          <StateIndicator state={prediction.current_state} />
          <ConfidenceBadge confidence={prediction.confidence} />
        </div>
      </div>

      <div className="card">
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', textAlign: 'center' }}>
          <TimeDisplay label="P10" minutes={prediction.p10_minutes} time={prediction.p10_time} />
          <TimeDisplay label="P50" minutes={prediction.p50_minutes} time={prediction.p50_time} highlight />
          <TimeDisplay label="P90" minutes={prediction.p90_minutes} time={prediction.p90_time} />
        </div>
      </div>

      <TimelineChart data={predictionHistory} />
      <StallGauge probability={prediction.stall_probability} />
      <SlopeChart data={tempHistory} />

      {state && (
        <div className="card">
          <h3 style={{ fontSize: '0.875rem', color: 'var(--color-text-muted)', marginBottom: 8 }}>Session Details</h3>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8, fontSize: '0.875rem' }}>
            <div>
              <span style={{ color: 'var(--color-text-muted)' }}>Readings: </span>
              {state.readings_count}
            </div>
            <div>
              <span style={{ color: 'var(--color-text-muted)' }}>Elapsed: </span>
              {Math.round(state.elapsed_minutes)}m
            </div>
            <div>
              <span style={{ color: 'var(--color-text-muted)' }}>Wrap: </span>
              {state.wrap_type === 'none' ? 'None' : state.wrap_type}
            </div>
            <div>
              <span style={{ color: 'var(--color-text-muted)' }}>Stall: </span>
              {state.stall_active ? `${Math.round(state.stall_duration_minutes)}m` : 'No'}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
