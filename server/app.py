# server/app.py
# 🚀 FastAPI backend for EchoFrame (serves API + frontend index)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os

from graph import ThoughtGraph

app = FastAPI()
graph = ThoughtGraph()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static frontend directory
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

class ThoughtInput(BaseModel):
    content: str

class NodeIDInput(BaseModel):
    node_id: str

@app.post("/init")
def initialize_root(thought: ThoughtInput):
    if graph.get_root():
        raise HTTPException(status_code=400, detail="Graph already has a root.")
    node = graph.add_node(thought.content)
    return {"root_id": node.id, "node": node.to_dict()}

@app.post("/expand")
def expand_node(req: NodeIDInput):
    expanded = graph.expand_node(req.node_id)
    if not expanded:
        raise HTTPException(status_code=404, detail="Node not found or no expansions.")
    return {"new_nodes": expanded}

@app.get("/graph")
def get_graph():
    return {"nodes": graph.get_full_graph()}

@app.get("/")
def serve_index():
    index_path = os.path.join(frontend_path, "index.html")
    return FileResponse(index_path)

@app.on_event("startup")
def auto_init_graph():
    if not graph.get_root():
        graph.add_node("AI will replace most jobs")
