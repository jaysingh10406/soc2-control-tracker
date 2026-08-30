import { useState } from "react";

const CATEGORIES = ["security", "availability", "confidentiality", "processing_integrity", "privacy"];

export default function AddControlForm({ onAdd }) {
  const [open, setOpen] = useState(false);
  const [name, setName] = useState("");
  const [category, setCategory] = useState("security");
  const [owner, setOwner] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    if (!name.trim()) return;
    onAdd({ name: name.trim(), category, owner: owner.trim(), status: "not_started" });
    setName("");
    setOwner("");
    setOpen(false);
  }

  if (!open) {
    return (
      <button className="primary-button" onClick={() => setOpen(true)}>
        + Add control
      </button>
    );
  }

  return (
    <form className="add-control-form" onSubmit={handleSubmit}>
      <input
        autoFocus
        placeholder="Control name (e.g. Penetration testing)"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <select value={category} onChange={(e) => setCategory(e.target.value)}>
        {CATEGORIES.map((c) => (
          <option key={c} value={c}>
            {c.replace("_", " ")}
          </option>
        ))}
      </select>
      <input placeholder="Owner" value={owner} onChange={(e) => setOwner(e.target.value)} />
      <button type="submit" className="primary-button">
        Save
      </button>
      <button type="button" className="link-button" onClick={() => setOpen(false)}>
        Cancel
      </button>
    </form>
  );
}
