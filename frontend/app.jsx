// Manual-testing UI for the cup-app FastAPI backend.
//
// This is a plain React app (no JSX build step — Babel standalone transpiles
// it in the browser, see index.html). It only talks to two resources today:
// Player and Team, matching the endpoints exposed in main.py.

const { useState } = React;

// Small helper shared by every panel: calls the API, always resolves (never
// throws) and returns a uniform shape so the UI can render success/error the
// same way regardless of which endpoint was hit.
async function callApi(baseUrl, method, path, body) {
  try {
    const response = await fetch(`${baseUrl}${path}`, {
      method,
      headers: body ? { "Content-Type": "application/json" } : undefined,
      body: body ? JSON.stringify(body) : undefined,
    });

    const text = await response.text();
    const data = text ? JSON.parse(text) : null;

    return { ok: response.ok, status: response.status, data };
  } catch (err) {
    // Network error (e.g. API not running, wrong base URL, CORS issue).
    return { ok: false, status: 0, data: { detail: err.message } };
  }
}

// Renders a single past API call in the activity log at the bottom.
function LogEntry({ entry }) {
  return (
    <div className="log-entry">
      <span className="method">{entry.method}</span>
      <span>{entry.path}</span>
      <span className={`status-pill ${entry.ok ? "ok" : "fail"}`}>
        {entry.status || "ERR"}
      </span>
      <span className="timestamp">{entry.time}</span>
    </div>
  );
}

// Shows every API call made during this session, newest first. This is the
// closest thing to a "network tab" for whoever is doing the manual testing.
function ActivityLog({ entries }) {
  return (
    <div className="card log">
      <h2>Activity log</h2>
      {entries.length === 0 ? (
        <p className="empty-log">No requests yet. Try creating a player or team.</p>
      ) : (
        entries.map((entry) => <LogEntry key={entry.id} entry={entry} />)
      )}
    </div>
  );
}

// Generic "result box" used after both create and lookup actions: green for
// 2xx responses, red for anything else (404, validation errors, etc).
function ResultBox({ result }) {
  if (!result) return null;
  return (
    <div className={`result-box ${result.ok ? "success" : "error"}`}>
      {result.ok ? "Success" : "Error"} ({result.status || "no response"})
      <pre>{JSON.stringify(result.data, null, 2)}</pre>
    </div>
  );
}

// Players panel: a form to POST /player/, plus a lookup box to GET
// /player/{id}. Mirrors the fields on PlayerCreate in schemas/player_schema.py.
function PlayersPanel({ baseUrl, onLogged }) {
  const [form, setForm] = useState({
    name: "",
    last_name: "",
    dob: "",
    position: "",
    team_id: "",
    team_name: "",
  });
  const [createResult, setCreateResult] = useState(null);
  const [lookupId, setLookupId] = useState("");
  const [lookupResult, setLookupResult] = useState(null);

  const updateField = (field) => (event) =>
    setForm({ ...form, [field]: event.target.value });

  async function handleCreate(event) {
    event.preventDefault();
    const result = await callApi(baseUrl, "POST", "/player/", form);
    setCreateResult(result);
    onLogged("POST", "/player/", result);

    // Convenience: if creation worked, pre-fill the lookup box with the
    // new player's id so you can immediately verify the GET endpoint too.
    if (result.ok && result.data?.id) {
      setLookupId(result.data.id);
    }
  }

  async function handleLookup(event) {
    event.preventDefault();
    const result = await callApi(baseUrl, "GET", `/player/${lookupId}`);
    setLookupResult(result);
    onLogged("GET", `/player/${lookupId}`, result);
  }

  return (
    <div className="grid">
      <div className="card">
        <h2>Create player</h2>
        <p className="hint">POST /player/</p>
        <form onSubmit={handleCreate}>
          <div className="field">
            <label>Name</label>
            <input value={form.name} onChange={updateField("name")} required />
          </div>
          <div className="field">
            <label>Last name</label>
            <input value={form.last_name} onChange={updateField("last_name")} required />
          </div>
          <div className="field">
            <label>Date of birth</label>
            <input type="date" value={form.dob} onChange={updateField("dob")} required />
          </div>
          <div className="field">
            <label>Position</label>
            <input value={form.position} onChange={updateField("position")} required />
          </div>
          <div className="field">
            <label>Team ID</label>
            <input
              value={form.team_id}
              onChange={updateField("team_id")}
              placeholder="UUID of an existing team"
              required
            />
          </div>
          <div className="field">
            <label>Team name</label>
            <input value={form.team_name} onChange={updateField("team_name")} required />
          </div>
          <button type="submit">Create player</button>
        </form>
        <ResultBox result={createResult} />
      </div>

      <div className="card">
        <h2>Fetch player by ID</h2>
        <p className="hint">GET /player/{"{player_id}"}</p>
        <form onSubmit={handleLookup}>
          <div className="lookup-row">
            <input
              value={lookupId}
              onChange={(e) => setLookupId(e.target.value)}
              placeholder="Player UUID"
              required
            />
            <button type="submit" className="secondary">
              Fetch
            </button>
          </div>
        </form>
        <ResultBox result={lookupResult} />
      </div>
    </div>
  );
}

// Teams panel: a form to POST /team/, plus a lookup box to GET /team/{id}.
// Mirrors the fields on TeamCreate in schemas/team_schema.py.
function TeamsPanel({ baseUrl, onLogged }) {
  const [form, setForm] = useState({ name: "", foundation_date: "" });
  const [createResult, setCreateResult] = useState(null);
  const [lookupId, setLookupId] = useState("");
  const [lookupResult, setLookupResult] = useState(null);

  const updateField = (field) => (event) =>
    setForm({ ...form, [field]: event.target.value });

  async function handleCreate(event) {
    event.preventDefault();
    const result = await callApi(baseUrl, "POST", "/team/", form);
    setCreateResult(result);
    onLogged("POST", "/team/", result);

    if (result.ok && result.data?.id) {
      setLookupId(result.data.id);
    }
  }

  async function handleLookup(event) {
    event.preventDefault();
    const result = await callApi(baseUrl, "GET", `/team/${lookupId}`);
    setLookupResult(result);
    onLogged("GET", `/team/${lookupId}`, result);
  }

  return (
    <div className="grid">
      <div className="card">
        <h2>Create team</h2>
        <p className="hint">POST /team/</p>
        <form onSubmit={handleCreate}>
          <div className="field">
            <label>Name</label>
            <input value={form.name} onChange={updateField("name")} required />
          </div>
          <div className="field">
            <label>Foundation date</label>
            <input
              type="date"
              value={form.foundation_date}
              onChange={updateField("foundation_date")}
              required
            />
          </div>
          <button type="submit">Create team</button>
        </form>
        <ResultBox result={createResult} />
      </div>

      <div className="card">
        <h2>Fetch team by ID</h2>
        <p className="hint">GET /team/{"{team_id}"}</p>
        <form onSubmit={handleLookup}>
          <div className="lookup-row">
            <input
              value={lookupId}
              onChange={(e) => setLookupId(e.target.value)}
              placeholder="Team UUID"
              required
            />
            <button type="submit" className="secondary">
              Fetch
            </button>
          </div>
        </form>
        <ResultBox result={lookupResult} />
      </div>
    </div>
  );
}

function App() {
  // Editable base URL so the same UI can point at a local server, a
  // different port, or a deployed instance without touching the code.
  const [baseUrl, setBaseUrl] = useState("http://127.0.0.1:8000");
  const [activeTab, setActiveTab] = useState("players");
  const [log, setLog] = useState([]);

  // Every panel calls this after hitting the API, so all requests end up in
  // one shared activity log regardless of which tab made them.
  function handleLogged(method, path, result) {
    const entry = {
      id: `${Date.now()}-${Math.random()}`,
      method,
      path,
      ok: result.ok,
      status: result.status,
      time: new Date().toLocaleTimeString(),
    };
    setLog((previous) => [entry, ...previous]);
  }

  return (
    <div className="page">
      <header className="page-header">
        <h1>Cup App — Manual Test UI</h1>
        <p>Create and fetch players/teams against the FastAPI backend.</p>
        <div className="base-url-bar">
          <label htmlFor="base-url">API base URL</label>
          <input
            id="base-url"
            value={baseUrl}
            onChange={(e) => setBaseUrl(e.target.value)}
          />
        </div>
      </header>

      <div className="tabs">
        <button
          className={`tab-button ${activeTab === "players" ? "active" : ""}`}
          onClick={() => setActiveTab("players")}
        >
          Players
        </button>
        <button
          className={`tab-button ${activeTab === "teams" ? "active" : ""}`}
          onClick={() => setActiveTab("teams")}
        >
          Teams
        </button>
      </div>

      {activeTab === "players" ? (
        <PlayersPanel baseUrl={baseUrl} onLogged={handleLogged} />
      ) : (
        <TeamsPanel baseUrl={baseUrl} onLogged={handleLogged} />
      )}

      <ActivityLog entries={log} />
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);
