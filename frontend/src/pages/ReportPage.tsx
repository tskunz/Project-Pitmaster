import { useNavigate } from 'react-router-dom';
import { PostCookReport } from '../components/report/PostCookReport';
import { QualityForm } from '../components/report/QualityForm';
import { useCookSession } from '../hooks/useCookSession';
import type { QualityRating } from '../types/cook';

interface Props {
  cookSession: ReturnType<typeof useCookSession>;
}

export function ReportPage({ cookSession }: Props) {
  const navigate = useNavigate();
  const { state, reset } = cookSession;

  if (!state.report) {
    return (
      <div className="page">
        <h1>No Report</h1>
        <p style={{ color: 'var(--color-text-muted)' }}>Finish a cook to see the report.</p>
      </div>
    );
  }

  const handleQuality = (_rating: QualityRating, _notes: string) => {
    // In a full implementation, this would POST to the API
    // For now, just acknowledge
  };

  const handleNewCook = () => {
    reset();
    navigate('/');
  };

  return (
    <div className="page">
      <h1>Cook Report</h1>
      <PostCookReport report={state.report} />
      <QualityForm onSubmit={handleQuality} />
      <button
        className="btn-primary"
        style={{ width: '100%', marginTop: 24 }}
        onClick={handleNewCook}
      >
        Start New Cook
      </button>
    </div>
  );
}
