interface Props {
  value: string;
  onChange: (v: string) => void;
}

export function DinnerTimePicker({ value, onChange }: Props) {
  return (
    <div className="form-group">
      <label>Dinner Time (optional)</label>
      <input
        type="datetime-local"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="When do you want to eat?"
      />
    </div>
  );
}
