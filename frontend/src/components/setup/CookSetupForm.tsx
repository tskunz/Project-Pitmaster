import { useState } from 'react';
import type { CookSetupRequest, CutType, EquipmentType } from '../../types/cook';
import { CUT_INFO } from '../../types/cook';
import { EquipmentPicker } from './EquipmentPicker';
import { DinnerTimePicker } from './DinnerTimePicker';

interface Props {
  onSubmit: (data: CookSetupRequest) => void;
  loading: boolean;
}

export function CookSetupForm({ onSubmit, loading }: Props) {
  const [cutType, setCutType] = useState<CutType>('brisket');
  const [weightLbs, setWeightLbs] = useState(10);
  const [thicknessInches, setThicknessInches] = useState(CUT_INFO.brisket.defaultThickness);
  const [equipment, setEquipment] = useState<EquipmentType>('offset');
  const [smokerTemp, setSmokerTemp] = useState(250);
  const [targetTemp, setTargetTemp] = useState(CUT_INFO.brisket.defaultTarget);
  const [dinnerTime, setDinnerTime] = useState('');
  const [altitudeFt, setAltitudeFt] = useState(0);

  const handleCutChange = (cut: CutType) => {
    setCutType(cut);
    const info = CUT_INFO[cut];
    setTargetTemp(info.defaultTarget);
    setThicknessInches(info.defaultThickness);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const info = CUT_INFO[cutType];
    onSubmit({
      meat_category: info.category,
      cut_type: cutType,
      weight_lbs: weightLbs,
      thickness_inches: thicknessInches,
      equipment_type: equipment,
      smoker_temp_f: smokerTemp,
      target_temp_f: targetTemp,
      dinner_time: dinnerTime || undefined,
      altitude_ft: altitudeFt,
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="form-group">
        <label>What are you cooking?</label>
        <select value={cutType} onChange={(e) => handleCutChange(e.target.value as CutType)}>
          {Object.entries(CUT_INFO).map(([key, info]) => (
            <option key={key} value={key}>{info.label}</option>
          ))}
        </select>
      </div>

      <div className="form-row">
        <div className="form-group">
          <label>Weight (lbs)</label>
          <input
            type="number"
            min={0.5}
            max={30}
            step={0.5}
            value={weightLbs}
            onChange={(e) => setWeightLbs(Number(e.target.value))}
          />
        </div>
        <div className="form-group">
          <label>Thickness (in)</label>
          <input
            type="number"
            min={0.5}
            max={12}
            step={0.5}
            value={thicknessInches}
            onChange={(e) => setThicknessInches(Number(e.target.value))}
          />
        </div>
      </div>

      <EquipmentPicker value={equipment} onChange={setEquipment} />

      <div className="form-row">
        <div className="form-group">
          <label>Smoker Temp (&deg;F)</label>
          <input
            type="number"
            min={180}
            max={400}
            value={smokerTemp}
            onChange={(e) => setSmokerTemp(Number(e.target.value))}
          />
        </div>
        <div className="form-group">
          <label>Target Temp (&deg;F)</label>
          <input
            type="number"
            min={140}
            max={212}
            value={targetTemp}
            onChange={(e) => setTargetTemp(Number(e.target.value))}
          />
        </div>
      </div>

      <div className="form-group">
        <label>Altitude (ft)</label>
        <input
          type="number"
          min={0}
          max={15000}
          value={altitudeFt}
          onChange={(e) => setAltitudeFt(Number(e.target.value))}
        />
      </div>

      <DinnerTimePicker value={dinnerTime} onChange={setDinnerTime} />

      <button type="submit" className="btn-primary" style={{ width: '100%' }} disabled={loading}>
        {loading ? 'Starting...' : 'Start Cook'}
      </button>
    </form>
  );
}
