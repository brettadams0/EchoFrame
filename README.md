# EchoFrame

Start with one idea, then keep asking "and then what?". EchoFrame takes a single statement, asks a
model for its consequences, counterpoints and open questions, and renders the result as a graph you
can keep expanding by clicking any node.

![EchoFrame](Example.png)

FastAPI backend, D3.js frontend, and OpenRouter for the model calls.

## Running it

```sh
pip install -r requirements.txt
```

Set an [OpenRouter](https://openrouter.ai/keys) key — the free tier is enough:

```sh
export OPENROUTER_API_KEY=sk-or-...
```

The backend imports its siblings by bare module name (`from graph import ThoughtGraph`), so it has
to be started from inside `server/`:

```sh
cd server
uvicorn app:app --reload
```

Then open <http://localhost:8000>. FastAPI serves the frontend itself, so there is nothing to build
and no second process to run.

## Layout

```
server/app.py         FastAPI app; serves the API and the frontend
server/generator.py   Prompts OpenRouter for expansions of a node
server/graph.py       Node and edge bookkeeping
frontend/index.html   D3.js force-directed graph, no build step
```

Click a node and the frontend posts it back to the API, which asks the model for the next layer and
returns the new nodes and edges to splice into the graph.

## Notes

Each expansion is a fresh API call, so a deep graph is a lot of calls — worth watching if you are
past the free tier. There is no persistence: the graph lives in the server process, and restarting
`uvicorn` clears it. Node text comes straight from the model, so the usual caveat applies — it is a
brainstorming aid, not a source.

## License

MIT — see [LICENSE](LICENSE).
