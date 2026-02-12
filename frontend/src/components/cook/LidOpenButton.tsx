interface Props {
  onLidOpen: () => void;
}

export function LidOpenButton({ onLidOpen }: Props) {
  return (
    <button
      className="btn-secondary"
      style={{ width: '100%', marginTop: 8 }}
      onClick={onLidOpen}
      type="button"
    >
      I Opened the Lid
    </button>
  );
}
