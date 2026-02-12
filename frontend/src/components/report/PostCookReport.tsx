import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import type { ReportResponse } from '../../types/cook';
import { ResidualChart } from './ResidualChart';

interface Props {
  report: ReportResponse;
}

export function PostCookReport({ report }: Props) {
  // Build overlay chart data
  const chartData = report.actual_temps.map((actual, i) => ({
    index: i + 1,
    actual,
    predicted: report.predicted_temps[i] ?? null,
  }));

  return (
    <div>
      <div className="card">
        <h3 style={{ marginBottom: 12 }}>Cook Summary</h3>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12, fontSize: '0.875rem' }}>
          <div>
            <span style={{ color: 'var(--color-text-muted)' }}>Total Time</span>
            <div style={{ fontWeight: 700 }}>{Math.round(report.total_cook_minutes)} min</div>
          </div>
          <div>
            <span style={{ color: 'var(--color-text-muted)' }}>Final Temp</span>
            <div style={{ fontWeight: 700 }}>{report.final_temp_f}&deg;F</div>
          </div>
          <div>
            <span style={{ color: 'var(--color-text-muted)' }}>Readings</span>
            <div style={{ fontWeight: 700 }}>{report.readings_count}</div>
          </div>
          <div>
            <span style={{ color: 'var(--color-text-muted)' }}>Lid Opens</span>
            <div style={{ fontWeight: 700 }}>{report.lid_opens_count}</div>
          </div>
          <div>
            <span style={{ color: 'var(--color-text-muted)' }}>Stall</span>
            <div style={{ fontWeight: 700 }}>
              {report.stall_occurred ? `${Math.round(report.stall_duration_minutes)}m` : 'None'}
            </div>
          </div>
          <div>
            <span style={{ color: 'var(--color-text-muted)' }}>Wrapped</span>
            <div style={{ fontWeight: 700 }}>
              {report.was_wrapped ? report.wrap_type.replace('_', ' ') : 'No'}
            </div>
          </div>
          <div style={{ gridColumn: '1 / -1' }}>
            <span style={{ color: 'var(--color-text-muted)' }}>Prediction Accuracy</span>
            <div style={{ fontWeight: 700 }}>
              {'\u00B1'}{Math.round(report.prediction_accuracy_minutes)} minutes
            </div>
          </div>
        </div>
      </div>

      {chartData.length > 1 && (
        <div className="card">
          <h3 style={{ fontSize: '0.875rem', color: 'var(--color-text-muted)', marginBottom: 12 }}>
            Predicted vs Actual Temperature
          </h3>
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--color-surface-2)" />
              <XAxis dataKey="index" stroke="var(--color-text-muted)" fontSize={12} />
              <YAxis stroke="var(--color-text-muted)" fontSize={12} />
              <Tooltip contentStyle={{ background: 'var(--color-surface)', border: 'none', borderRadius: 8 }} />
              <Legend />
              <Line type="monotone" dataKey="actual" stroke="var(--color-primary-light)" strokeWidth={2} dot={false} name="Actual" />
              <Line type="monotone" dataKey="predicted" stroke="var(--color-info)" strokeWidth={2} dot={false} strokeDasharray="5 5" name="Predicted" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}

      <ResidualChart residuals={report.residuals} />
    </div>
  );
}
