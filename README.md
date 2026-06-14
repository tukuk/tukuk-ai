# Tukuk AI

Tukuk AI is a free public AI agent website for students. It runs as a static GitHub Pages app and also includes a free Kilo-style agent stack with container, pipeline, MCP-compatible tools, terminal/console/shell launcher, Python AI library engine, workflow engine, and defensive cyber security diagnostic.

## Main website

Open the public website:

```text
https://tukuk.github.io/tukuk-ai/
```

Main file:

```text
index.html
```

## Public AI engines

- AI Brain request processor
- Student learning dashboard
- App builder and live code editor
- HTML/CSS/JavaScript/React/Node/NPM/Java engines
- Python AI library engine
- Container and Docker Compose engine
- GitHub Actions pipeline engine
- MCP-compatible tool server
- Terminal/console/shell launcher
- Kilo Free Agent UI
- Defensive cyber security diagnostic
- Music, video, image, read aloud, calculator, dictionary, color, typing, and workflow engines

## Run the free agent stack locally

From any terminal, console, shell, Git Bash, WSL, Linux, macOS, or Windows with Docker:

```bash
cd agent-stack
./tukuk-agent.sh docker
```

Windows:

```bat
tukuk-agent.bat docker
```

Run local pipeline check:

```bash
./tukuk-agent.sh pipeline
```

Run agent request:

```bash
./tukuk-agent.sh agent "Build a student web app"
```

Run defensive security diagnostic:

```bash
python security/diagnostic.py --url https://example.com --output diagnostic-report.json
```

## GitHub Actions

Active workflows:

- `tukuk-agent-stack.yml`: compile Python, self-test, and build Docker image
- `pages.yml`: deploy static website to GitHub Pages
- `defensive-security-diagnostic.yml`: run defensive website diagnostic
- `codeql.yml`: GitHub CodeQL analysis

Imported KiloCode workflow templates are stored in:

```text
agent-stack/kilocode-workflows/
```

## Safety

The cyber diagnostic is defensive only. It checks HTTPS, TLS, reachability, and security headers. It does not exploit systems or perform aggressive scanning.
