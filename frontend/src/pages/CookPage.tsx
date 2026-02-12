import { useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { cookApi } from '../api/cookApi';
import { useCookSession } from '../hooks/useCookSession';
import { usePrediction } from '../hooks/usePrediction';
import { ProbeInput } from '../components/cook/ProbeInput';
import { LidOpenButton } from '../components/cook/LidOpenButton';
import { NormalModeView } from '../components/normal/NormalModeView';
import { NerdModeView } from '../components/nerd/NerdModeView';
import type { WrapType } from '../types/cook';

interface Props {
  cookSession: ReturnType<typeof useCookSession>;
}

export function CookPage({ cookSession }: Props) {
  const navigate = useNavigate();
  const { state, dispatch, toggleNerdMode, setLoading, setError } = cookSession;

  const handlePredictionUpdate = useCallback(
    (pred: Parameters<typeof dispatch>[0] extends { type: 'PREDICTION_UPDATE'; payload: infer P } ? P : never) => {
      dispatch({ type: 'PREDICTION_UPDATE', payload: pred });
    },
    [dispatch],
  );

  usePrediction(state.sessionId, handlePredictionUpdate);

  if (!state.sessionId || !state.prediction) {
    return (
      <div className="page">
        <h1>No Active Cook</h1>
        <p style={{ color: 'var(--color-text-muted)' }}>Go to Setup to start a cook.</p>
      </div>
    );
  }

  const handleReading = async (tempF: number) => {
    setLoading(true);
    try {
      const res = await cookApi.addReading(state.sessionId!, { temp_f: tempF });
      dispatch({ type: 'READING_SUCCESS', payload: res, temp: tempF });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to log reading');
    }
  };

  const handleLidOpen = async () => {
    try {
      await cookApi.lidOpen(state.sessionId!);
    } catch {
      // non-critical
    }
  };

  const handleWrap = async (wrapType: WrapType) => {
    setLoading(true);
    try {
      const res = await cookApi.wrap(state.sessionId!, { wrap_type: wrapType });
      dispatch({ type: 'WRAP_SUCCESS', payload: res });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to apply wrap');
    }
  };

  const handleFinish = async () => {
    setLoading(true);
    try {
      const report = await cookApi.finish(state.sessionId!);
      dispatch({ type: 'FINISH_SUCCESS', payload: report });
      navigate('/report');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to finish cook');
    }
  };

  return (
    <div className="page">
      <div className="toggle-container">
        <span style={{ fontSize: '0.875rem', color: 'var(--color-text-muted)' }}>Nerd Mode</span>
        <button
          className={`toggle ${state.nerdMode ? 'active' : ''}`}
          onClick={toggleNerdMode}
          type="button"
          aria-label="Toggle nerd mode"
        />
      </div>

      {state.error && (
        <div className="card" style={{ borderLeft: '4px solid var(--color-danger)', marginBottom: 16 }}>
          {state.error}
        </div>
      )}

      {state.nerdMode ? (
        <NerdModeView
          prediction={state.prediction}
          state={state.state}
          tempHistory={state.tempHistory}
          predictionHistory={state.predictionHistory}
        />
      ) : (
        <NormalModeView
          prediction={state.prediction}
          state={state.state}
          onWrap={handleWrap}
        />
      )}

      <ProbeInput onSubmit={handleReading} loading={state.loading} />
      <LidOpenButton onLidOpen={handleLidOpen} />

      <button
        className="btn-danger"
        style={{ width: '100%', marginTop: 24 }}
        onClick={handleFinish}
        disabled={state.loading}
      >
        Finish Cook
      </button>
    </div>
  );
}
