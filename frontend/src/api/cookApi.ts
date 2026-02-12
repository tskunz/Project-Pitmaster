import { apiFetch } from './client';
import type {
  CookSetupRequest,
  CookSetupResponse,
  ProbeReadingRequest,
  ReadingResponse,
  WrapRequest,
  WrapResponse,
  PredictionResponse,
  StateResponse,
  ReportResponse,
  FinishCookRequest,
  EquipmentPresetResponse,
} from '../types/cook';

export const cookApi = {
  setup(data: CookSetupRequest) {
    return apiFetch<CookSetupResponse>('/cook/setup', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  addReading(sessionId: string, data: ProbeReadingRequest) {
    return apiFetch<ReadingResponse>(`/cook/${sessionId}/reading`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  lidOpen(sessionId: string, durationSeconds = 30) {
    return apiFetch<{ status: string }>(`/cook/${sessionId}/lid-open`, {
      method: 'POST',
      body: JSON.stringify({ duration_seconds: durationSeconds }),
    });
  },

  wrap(sessionId: string, data: WrapRequest) {
    return apiFetch<WrapResponse>(`/cook/${sessionId}/wrap`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  getPrediction(sessionId: string) {
    return apiFetch<PredictionResponse>(`/cook/${sessionId}/prediction`);
  },

  getState(sessionId: string) {
    return apiFetch<StateResponse>(`/cook/${sessionId}/state`);
  },

  finish(sessionId: string, data: FinishCookRequest = {}) {
    return apiFetch<ReportResponse>(`/cook/${sessionId}/finish`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  getReport(sessionId: string) {
    return apiFetch<ReportResponse>(`/cook/${sessionId}/report`);
  },

  getEquipmentPresets() {
    return apiFetch<EquipmentPresetResponse[]>('/equipment/presets');
  },
};
