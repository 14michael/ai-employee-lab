"""Personal AI Workbench API prototype. Local development only; not production hosting."""
import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

DB_PATH = os.getenv("WORKBENCH_DB", str(Path(__file__).with_name("workbench.db")))
TOKEN = os.getenv("WORKBENCH_TOKEN")
KINDS = {"tasks", "knowledge", "skills", "agents", "handbook", "assignments", "notes"}
app = FastAPI(title="個人 AI 工作台 API", version="0.3.0")

@contextmanager
def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("""CREATE TABLE IF NOT EXISTS records (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      kind TEXT NOT NULL,
      title TEXT NOT NULL,
      body TEXT NOT NULL DEFAULT '',
      status TEXT NOT NULL DEFAULT 'open',
      created_at TEXT NOT NULL
    )""")
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def authorize(authorization: str | None):
    if not TOKEN:
        raise HTTPException(503, "WORKBENCH_TOKEN 尚未設定，拒絕服務")
    if authorization != "Bearer " + TOKEN:
        raise HTTPException(401, "未授權")

class RecordIn(BaseModel):
    kind: str
    title: str = Field(min_length=1, max_length=200)
    body: str = Field(default="", max_length=100000)

class RecordPatch(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    body: str = Field(default="", max_length=100000)

class StatusPatch(BaseModel):
    status: str

@app.get("/api/health")
def health():
    return {"ok": True, "version": "0.3.0", "storage": "sqlite-local"}

@app.get("/api/records/{kind}")
def list_records(kind: str, authorization: str | None = Header(default=None)):
    authorize(authorization)
    if kind not in KINDS:
        raise HTTPException(400, "未知資料類型")
    with db() as conn:
        return [dict(row) for row in conn.execute(
            "SELECT * FROM records WHERE kind=? ORDER BY id DESC", (kind,)
        )]

@app.post("/api/records", status_code=201)
def create_record(item: RecordIn, authorization: str | None = Header(default=None)):
    authorize(authorization)
    if item.kind not in KINDS:
        raise HTTPException(400, "未知資料類型")
    with db() as conn:
        cursor = conn.execute(
            "INSERT INTO records(kind,title,body,created_at) VALUES(?,?,?,?)",
            (item.kind, item.title, item.body, datetime.now(timezone.utc).isoformat())
        )
        return {"id": cursor.lastrowid}

@app.put("/api/records/{record_id}")
def update_record(record_id: int, item: RecordPatch, authorization: str | None = Header(default=None)):
    authorize(authorization)
    with db() as conn:
        result = conn.execute("UPDATE records SET title=?,body=? WHERE id=?",
                              (item.title, item.body, record_id))
        if not result.rowcount:
            raise HTTPException(404, "找不到資料")
        return {"ok": True}

@app.patch("/api/records/{record_id}/status")
def update_status(record_id: int, item: StatusPatch, authorization: str | None = Header(default=None)):
    authorize(authorization)
    if item.status not in {"open", "doing", "done", "hold", "fail"}:
        raise HTTPException(400, "不合法的狀態")
    with db() as conn:
        result = conn.execute("UPDATE records SET status=? WHERE id=?", (item.status, record_id))
        if not result.rowcount:
            raise HTTPException(404, "找不到資料")
        return {"ok": True}

@app.delete("/api/records/{record_id}")
def delete_record(record_id: int, authorization: str | None = Header(default=None)):
    authorize(authorization)
    with db() as conn:
        result = conn.execute("DELETE FROM records WHERE id=?", (record_id,))
        if not result.rowcount:
            raise HTTPException(404, "找不到資料")
        return {"ok": True}
