import { useReducer, useCallback } from 'react';
import type {
  CookSetupResponse,
  PredictionResponse,
  StateResponse,
  ReadingResponse,
  ReportResponse,
  BackwardPlanResponse,
  WrapType,
} from '../types/cook';

interface CookSessionState {
  sessionId: string | null;
  prediction: PredictionResponse | null;
  state: StateResponse | null;
  backwardPlan: BackwardPlanResponse | null;
  report: ReportResponse | null;
  nerdMode: boolean;
  loading: boolean;
  error: string | null;
  tempHistory: { elapsed: number; temp: number }[];
  predictionHistory: { elapsed: number; p10: number; p50: number; p90: number }[];
}

type Action =
  | { type: 'SETUP_SUCCESS'; payload: CookSetupResponse }
  | { type: 'READING_SUCCESS'; payload: ReadingResponse; temp: number }
  | { type: 'WRAP_SUCCESS'; payload: { prediction: PredictionResponse; wrap_type: WrapType } }
  | { type: 'FINISH_SUCCESS'; payload: ReportResponse }
  | { type: 'PREDICTION_UPDATE'; payload: PredictionResponse }
  | { type: 'STATE_UPDATE'; payload: StateResponse }
  | { type: 'TOGGLE_NERD' }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string }
  | { type: 'RESET' };

const initialState: CookSessionState = {
  sessionId: null,
  prediction: null,
  state: null,
  backwardPlan: null,
  report: null,
  nerdMode: false,
  loading: false,
  error: null,
  tempHistory: [],
  predictionHistory: [],
};

function reducer(state: CookSessionState, action: Action): CookSessionState {
  switch (action.type) {
    case 'SETUP_SUCCESS':
      return {
        ...state,
        sessionId: action.payload.session_id,
        prediction: action.payload.prediction,
        backwardPlan: action.payload.backward_plan ?? null,
        loading: false,
        error: null,
      };
    case 'READING_SUCCESS': {
      const { prediction, state: cookState } = action.payload;
      const elapsed = action.payload.elapsed_minutes;
      return {
        ...state,
        prediction,
        state: cookState,
        loading: false,
        tempHistory: [...state.tempHistory, { elapsed, temp: action.temp }],
        predictionHistory: [
          ...state.predictionHistory,
          { elapsed, p10: prediction.p10_minutes, p50: prediction.p50_minutes, p90: prediction.p90_minutes },
        ],
      };
    }
    case 'WRAP_SUCCESS':
      return { ...state, prediction: action.payload.prediction, loading: false };
    case 'FINISH_SUCCESS':
      return { ...state, report: action.payload, loading: false };
    case 'PREDICTION_UPDATE':
      return { ...state, prediction: action.payload };
    case 'STATE_UPDATE':
      return { ...state, state: action.payload };
    case 'TOGGLE_NERD':
      return { ...state, nerdMode: !state.nerdMode };
    case 'SET_LOADING':
      return { ...state, loading: action.payload };
    case 'SET_ERROR':
      return { ...state, error: action.payload, loading: false };
    case 'RESET':
      return initialState;
    default:
      return state;
  }
}

export function useCookSession() {
  const [state, dispatch] = useReducer(reducer, initialState);

  const toggleNerdMode = useCallback(() => dispatch({ type: 'TOGGLE_NERD' }), []);
  const setLoading = useCallback((v: boolean) => dispatch({ type: 'SET_LOADING', payload: v }), []);
  const setError = useCallback((e: string) => dispatch({ type: 'SET_ERROR', payload: e }), []);
  const reset = useCallback(() => dispatch({ type: 'RESET' }), []);

  return { state, dispatch, toggleNerdMode, setLoading, setError, reset };
}
