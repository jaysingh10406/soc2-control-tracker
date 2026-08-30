import { useEffect, useState, useCallback } from "react";
import { api } from "./api";
import StatCard from "./components/StatCard";
import ControlsTable from "./components/ControlsTable";
import AddControlForm from "./components/AddControlForm";

const FILTERS = [
  { key: "all", label: "All" },
  { key: "not_started", label: "Not started" },
  { key: "in_progress", label: "In progress" },
  { key: "implemented", label: "Implemented" },
  { key: "verified", label: "Verified" },
];

export default function App() {
  const [controls, setControls] = useState([]);
  const [summary, setSummary] = useState(null);
  const [filter, setFilter] = useState("all");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const refresh = useCallback(async () => {
    try {
      const [controlsData, summaryData] = await Promise.all([
        api.listControls(),
        api.getSummary(),
      ]);
      setControls(controlsData);
      setSummary(summaryData);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  async function handleStatusChange(id, status) {
    await api.updateControl(id, { status });
    refresh();
  }

  async function handleDelete(id) {
    await api.deleteControl(id);
    refresh();
  }

  async function handleAdd(data) {
    await api.createControl(data);
    refresh();
  }

  const visibleControls = filter === "all" ? controls : controls.filter((c) => c.status === filter);

  return (
    <div className="app">
      <header className="app-header">
        <div>
          <h1>SOC 2 Control Tracker</h1>
          <p className="app-subtitle">
            Trust-service controls, ownership, and audit-readiness at a glance.
            {api.demoMode && <span className="demo-badge">Demo mode — data resets on reload</span>}
          </p>
        </div>
      </header>

      {error && <div className="error-banner">Couldn't reach the API: {error}</div>}

      {summary && (
        <section className="stats-row">
          <StatCard label="Total controls" value={summary.total} />
          <StatCard label="Verified" value={summary.verified} tone="verified" />
          <StatCard label="Implemented" value={summary.implemented} tone="implemented" />
          <StatCard label="In progress" value={summary.in_progress} tone="in_progress" />
          <StatCard label="Not started" value={summary.not_started} tone="not_started" />
          <StatCard label="Audit-ready" value={`${summary.percent_complete}%`} tone="verified" />
        </section>
      )}

      <section className="toolbar">
        <div className="filter-pills">
          {FILTERS.map((f) => (
            <button
              key={f.key}
              className={`filter-pill ${filter === f.key ? "filter-pill--active" : ""}`}
              onClick={() => setFilter(f.key)}
            >
              {f.label}
            </button>
          ))}
        </div>
        <AddControlForm onAdd={handleAdd} />
      </section>

      {loading ? (
        <p className="empty-state">Loading controls…</p>
      ) : (
        <ControlsTable controls={visibleControls} onStatusChange={handleStatusChange} onDelete={handleDelete} />
      )}

      <footer className="app-footer">
        Built by Jaskaran Singh — a working model of the SOC 2 controls I built and ran in-house.
      </footer>
    </div>
  );
}
