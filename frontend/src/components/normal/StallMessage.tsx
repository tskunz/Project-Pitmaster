interface Props {
  stallActive: boolean;
  stallDuration: number;
  stallProbability: number;
}

export function StallMessage({ stallActive, stallDuration, stallProbability }: Props) {
  if (!stallActive && stallProbability < 0.3) return null;

  if (stallActive) {
    return (
      <div className="card" style={{ borderLeft: '4px solid var(--color-warning)' }}>
        <strong>Stall in progress</strong>
        <p style={{ color: 'var(--color-text-muted)', marginTop: 4 }}>
          Your meat has been in the stall for {Math.round(stallDuration)} minutes.
          This is normal — evaporative cooling is fighting the heat. Hang tight!
        </p>
      </div>
    );
  }

  return (
    <div className="card" style={{ borderLeft: '4px solid var(--color-info)' }}>
      <strong>Stall approaching</strong>
      <p style={{ color: 'var(--color-text-muted)', marginTop: 4 }}>
        {Math.round(stallProbability * 100)}% chance of entering the stall soon.
        The temperature may plateau for a while — this is expected.
      </p>
    </div>
  );
}
