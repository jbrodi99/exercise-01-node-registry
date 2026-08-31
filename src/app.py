"""
Exercise 01 — Node Registry API

Implement a FastAPI application with the following endpoints:

GET    /health          → health check with DB status
POST   /api/nodes       → register a new node
GET    /api/nodes       → list all nodes
GET    /api/nodes/{name} → get a node by name
PUT    /api/nodes/{name} → update a node
DELETE /api/nodes/{name} → soft-delete a node (set status=inactive)

See README.md for full specification.
"""

from fastapi import FastAPI, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy import func

from src.database import engine, Base, get_db
from src.models import Node
from src.schemas import NodeCreate, NodeUpdate, NodeResponse

Base.metadata.create_all(bind=engine)  

app = FastAPI()

@app.get("/health")
def health(db: Session = Depends(get_db)):
    count = db.query(Node).filter(Node.status == "active").count()
    return {"status": "ok", "db": "connected", "nodes_count": count}


@app.post("/api/nodes", response_model=NodeResponse, status_code=201)
def create_node(data: NodeCreate, db: Session = Depends(get_db)):
    existing = db.query(Node).filter(Node.name == data.name).first()
    if existing:
        raise HTTPException(status_code=409, detail="Node already exists")

    node = Node(name=data.name, host=data.host, port=data.port)
    db.add(node)
    db.commit()
    db.refresh(node)
    return node


@app.get("/api/nodes", response_model=list[NodeResponse])
def list_nodes(db: Session = Depends(get_db)):
    return db.query(Node).all()


@app.get("/api/nodes/{name}", response_model=NodeResponse)
def get_node(name: str, db: Session = Depends(get_db)):
    node = db.query(Node).filter(Node.name == name).first()
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    return node


@app.put("/api/nodes/{name}", response_model=NodeResponse)
def update_node(name: str, data: NodeUpdate, db: Session = Depends(get_db)):
    node = db.query(Node).filter(Node.name == name).first()
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(node, key, value)

    db.commit()
    db.refresh(node)
    return node


@app.delete("/api/nodes/{name}", status_code=204)
def delete_node(name: str, db: Session = Depends(get_db)):
    node = db.query(Node).filter(Node.name == name).first()
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")

    node.status = "inactive"
    db.commit()
    return Response(status_code=204)

