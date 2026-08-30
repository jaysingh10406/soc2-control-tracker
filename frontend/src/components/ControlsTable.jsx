const STATUS_LABELS = {
  not_started: "Not started",
  in_progress: "In progress",
  implemented: "Implemented",
  verified: "Verified",
};

const CATEGORY_LABELS = {
  security: "Security",
  availability: "Availability",
  confidentiality: "Confidentiality",
  processing_integrity: "Processing integrity",
  privacy: "Privacy",
};

export default function ControlsTable({ controls, onStatusChange, onDelete }) {
  if (controls.length === 0) {
    return <p className="empty-state">No controls yet. Add your first one above.</p>;
  }

  return (
    <table className="controls-table">
      <thead>
        <tr>
          <th>Control</th>
          <th>Category</th>
          <th>Owner</th>
          <th>Status</th>
          <th>Last reviewed</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        {controls.map((c) => (
          <tr key={c.id}>
            <td>
              <div className="controls-table__name">{c.name}</div>
              {c.description && <div className="controls-table__desc">{c.description}</div>}
            </td>
            <td>{CATEGORY_LABELS[c.category] || c.category}</td>
            <td>{c.owner || "—"}</td>
            <td>
              <select
                className={`status-select status-select--${c.status}`}
                value={c.status}
                onChange={(e) => onStatusChange(c.id, e.target.value)}
              >
                {Object.entries(STATUS_LABELS).map(([value, label]) => (
                  <option key={value} value={value}>
                    {label}
                  </option>
                ))}
              </select>
            </td>
            <td className="controls-table__date">
              {new Date(c.last_reviewed).toLocaleDateString()}
            </td>
            <td>
              <button className="link-button" onClick={() => onDelete(c.id)} aria-label={`Delete ${c.name}`}>
                Remove
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
