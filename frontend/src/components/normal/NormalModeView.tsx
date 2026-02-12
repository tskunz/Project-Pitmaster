import type { PredictionResponse, StateResponse, WrapType } from '../../types/cook';
import { ConfidenceBadge } from './ConfidenceBadge';
import { TimeDisplay } from './TimeDisplay';
import { StallMessage } from './StallMessage';
import { WrapPrompt } from './WrapPrompt';

interface Props {
  prediction: PredictionResponse;
  state: StateResponse | null;
  onWrap: (wrapType: WrapType) => void;
}

export function NormalModeView({ prediction, state, onWrap }: Props) {
  const showWrap =
    state?.stall_active === true &&
    state.stall_duration_minutes > 30 &&
    state.wrap_type === 'none';

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <h2>Cook Progress</h2>
        <ConfidenceBadge confidence={prediction.confidence} />
      </div>

      <div className="card">
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', textAlign: 'center' }}>
          <TimeDisplay label="Optimistic" minutes={prediction.p10_minutes} time={prediction.p10_time} />
          <TimeDisplay label="Best Estimate" minutes={prediction.p50_minutes} time={prediction.p50_time} highlight />
          <TimeDisplay label="Safe Bet" minutes={prediction.p90_minutes} time={prediction.p90_time} />
        </div>
      </div>

      <StallMessage
        stallActive={state?.stall_active ?? false}
        stallDuration={state?.stall_duration_minutes ?? 0}
        stallProbability={prediction.stall_probability}
      />

      <WrapPrompt onWrap={onWrap} visible={showWrap} />

      {state && (
        <div className="card" style={{ marginTop: 16 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <span style={{ color: 'var(--color-text-muted)' }}>Readings</span>
            <span>{state.readings_count}</span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 8 }}>
            <span style={{ color: 'var(--color-text-muted)' }}>Elapsed</span>
            <span>{Math.round(state.elapsed_minutes)}m</span>
          </div>
        </div>
      )}
    </div>
  );
}
