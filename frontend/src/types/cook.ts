// TypeScript interfaces matching backend models

export type MeatCategory = 'beef' | 'pork' | 'poultry' | 'lamb';

export type CutType =
  | 'brisket' | 'pork_butt' | 'pork_ribs' | 'beef_ribs'
  | 'chicken_whole' | 'turkey_breast' | 'leg_of_lamb';

export type CookState =
  | 'setup' | 'preheat' | 'early_cook' | 'pre_stall' | 'stall'
  | 'post_stall' | 'approaching_target' | 'rest' | 'done';

export type ConfidenceTier = 'high' | 'moderate' | 'low' | 'very_low';
export type EquipmentType = 'offset' | 'pellet' | 'kamado' | 'wsm' | 'custom';
export type WrapType = 'none' | 'foil' | 'butcher_paper' | 'foil_boat';
export type QualityRating = 'excellent' | 'good' | 'fair' | 'poor';

// Request types
export interface CookSetupRequest {
  meat_category: MeatCategory;
  cut_type: CutType;
  weight_lbs: number;
  thickness_inches: number;
  equipment_type: EquipmentType;
  smoker_temp_f: number;
  target_temp_f: number;
  dinner_time?: string;
  altitude_ft: number;
  latitude?: number;
  longitude?: number;
}

export interface ProbeReadingRequest {
  temp_f: number;
  smoker_temp_f?: number;
}

export interface WrapRequest {
  wrap_type: WrapType;
}

export interface FinishCookRequest {
  quality_rating?: QualityRating;
  quality_notes?: string;
}

// Response types
export interface PredictionResponse {
  p10_minutes: number;
  p50_minutes: number;
  p90_minutes: number;
  p10_time?: string;
  p50_time?: string;
  p90_time?: string;
  confidence: ConfidenceTier;
  current_state: CookState;
  stall_probability: number;
  readings_count: number;
}

export interface StateResponse {
  current_state: CookState;
  confidence: ConfidenceTier;
  stall_active: boolean;
  stall_duration_minutes: number;
  wrap_type: WrapType;
  readings_count: number;
  elapsed_minutes: number;
}

export interface BackwardPlanResponse {
  dinner_time: string;
  fire_start_time: string;
  meat_on_time: string;
  estimated_cook_minutes_p90: number;
  rest_minutes: number;
  preheat_minutes: number;
}

export interface CookSetupResponse {
  session_id: string;
  prediction: PredictionResponse;
  backward_plan?: BackwardPlanResponse;
}

export interface ReadingResponse {
  elapsed_minutes: number;
  prediction: PredictionResponse;
  state: StateResponse;
}

export interface WrapResponse {
  wrap_type: WrapType;
  prediction: PredictionResponse;
  message: string;
}

export interface ReportResponse {
  session_id: string;
  total_cook_minutes: number;
  final_temp_f: number;
  stall_occurred: boolean;
  stall_duration_minutes: number;
  was_wrapped: boolean;
  wrap_type: WrapType;
  prediction_accuracy_minutes: number;
  readings_count: number;
  lid_opens_count: number;
  quality_rating?: QualityRating;
  quality_notes?: string;
  predicted_temps: number[];
  actual_temps: number[];
  residuals: number[];
}

export interface EquipmentPresetResponse {
  equipment_type: EquipmentType;
  name: string;
  temp_variance: number;
  recovery_time_min: number;
  temp_drop_on_lid_open: number;
  insulation_factor: number;
}

// Cut display info
export const CUT_INFO: Record<CutType, { label: string; category: MeatCategory; defaultTarget: number; defaultThickness: number }> = {
  brisket:        { label: 'Brisket',          category: 'beef',    defaultTarget: 203, defaultThickness: 5.0 },
  pork_butt:      { label: 'Pork Butt',        category: 'pork',    defaultTarget: 203, defaultThickness: 6.0 },
  pork_ribs:      { label: 'Pork Ribs',        category: 'pork',    defaultTarget: 195, defaultThickness: 1.5 },
  beef_ribs:      { label: 'Beef Ribs',         category: 'beef',    defaultTarget: 203, defaultThickness: 2.5 },
  chicken_whole:  { label: 'Whole Chicken',     category: 'poultry', defaultTarget: 165, defaultThickness: 4.0 },
  turkey_breast:  { label: 'Turkey Breast',     category: 'poultry', defaultTarget: 165, defaultThickness: 4.5 },
  leg_of_lamb:    { label: 'Leg of Lamb',       category: 'lamb',    defaultTarget: 145, defaultThickness: 4.0 },
};
