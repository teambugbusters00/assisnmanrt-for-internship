"""Run with: pip install fastapi uvicorn; uvicorn app:app --reload"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel,Field
from pathlib import Path
import json
app=FastAPI(title="Internship Assistant")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
DB=Path("applications.json")
def load():return json.loads(DB.read_text()) if DB.exists() else []
def save(rows):DB.write_text(json.dumps(rows,indent=2))
class Application(BaseModel):company:str=Field(min_length=1);role:str=Field(min_length=1);deadline:str|None=None;status:str="Applied";notes:str=""
@app.get("/applications")
def list_apps():return load()
@app.post("/applications")
def add_app(item:Application):
 rows=load();row=item.model_dump();row["id"]=max([r.get("id",0) for r in rows],default=0)+1;rows.append(row);save(rows);return row
@app.delete("/applications/{app_id}")
def delete_app(app_id:int):
 rows=[r for r in load() if r["id"]!=app_id];save(rows);return {"remaining":len(rows)}