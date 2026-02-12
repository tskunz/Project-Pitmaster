import type { EquipmentType } from '../../types/cook';

const EQUIPMENT_OPTIONS: { value: EquipmentType; label: string }[] = [
  { value: 'offset', label: 'Offset Smoker' },
  { value: 'pellet', label: 'Pellet Grill' },
  { value: 'kamado', label: 'Kamado' },
  { value: 'wsm', label: 'Weber Smokey Mountain' },
  { value: 'custom', label: 'Custom / Other' },
];

interface Props {
  value: EquipmentType;
  onChange: (v: EquipmentType) => void;
}

export function EquipmentPicker({ value, onChange }: Props) {
  return (
    <div className="form-group">
      <label>Equipment</label>
      <select value={value} onChange={(e) => onChange(e.target.value as EquipmentType)}>
        {EQUIPMENT_OPTIONS.map((opt) => (
          <option key={opt.value} value={opt.value}>{opt.label}</option>
        ))}
      </select>
    </div>
  );
}
