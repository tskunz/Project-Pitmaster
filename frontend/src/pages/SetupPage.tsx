import { useNavigate } from 'react-router-dom';
import { CookSetupForm } from '../components/setup/CookSetupForm';
import { cookApi } from '../api/cookApi';
import type { CookSetupRequest } from '../types/cook';
import { useCookSession } from '../hooks/useCookSession';

interface Props {
  cookSession: ReturnType<typeof useCookSession>;
}

export function SetupPage({ cookSession }: Props) {
  const navigate = useNavigate();
  const { state, dispatch, setLoading, setError } = cookSession;

  const handleSubmit = async (data: CookSetupRequest) => {
    setLoading(true);
    try {
      const response = await cookApi.setup(data);
      dispatch({ type: 'SETUP_SUCCESS', payload: response });
      navigate('/cook');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Setup failed');
    }
  };

  return (
    <div className="page">
      <h1>The Predictive Pitmaster</h1>
      {state.error && (
        <div className="card" style={{ borderLeft: '4px solid var(--color-danger)', marginBottom: 16 }}>
          {state.error}
        </div>
      )}
      <CookSetupForm onSubmit={handleSubmit} loading={state.loading} />
    </div>
  );
}
