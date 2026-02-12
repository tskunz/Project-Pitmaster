import { useEffect, useRef } from 'react';
import { cookApi } from '../api/cookApi';
import type { PredictionResponse } from '../types/cook';

/**
 * Auto-poll prediction endpoint every `intervalMs` while a session is active.
 */
export function usePrediction(
  sessionId: string | null,
  onUpdate: (pred: PredictionResponse) => void,
  intervalMs = 30000,
) {
  const timerRef = useRef<ReturnType<typeof setInterval>>();

  useEffect(() => {
    if (!sessionId) return;

    const poll = async () => {
      try {
        const pred = await cookApi.getPrediction(sessionId);
        onUpdate(pred);
      } catch {
        // Silently fail — network may be offline
      }
    };

    timerRef.current = setInterval(poll, intervalMs);
    return () => clearInterval(timerRef.current);
  }, [sessionId, onUpdate, intervalMs]);
}
