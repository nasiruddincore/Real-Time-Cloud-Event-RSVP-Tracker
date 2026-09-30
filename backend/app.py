from datetime import datetime
import sqlite3
import uuid
from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI(title="Real-Time Event Planning & RSVP Tracker")
templates = Jinja2Templates(directory="frontend/templates")

DB_PATH = "backend/events.db"


def init_db():
  conn = sqlite3.connect(DB_PATH)
  cursor = conn.cursor()
  # Events Table
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            event_id TEXT PRIMARY KEY,
            event_name TEXT NOT NULL,
            description TEXT,
            event_date TEXT,
            venue TEXT,
            capacity INTEGER,
            status TEXT DEFAULT 'PUBLISHED'
        )
    """)
  # RSVPs Table with unique constraint on event and user/token to prevent duplicates
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS rsvps (
            rsvp_id TEXT PRIMARY KEY,
            event_id TEXT,
            token TEXT,
            guest_name TEXT,
            answer TEXT, -- 'yes', 'maybe', 'no', 'waitlist'
            guests INTEGER DEFAULT 0,
            updated_at TEXT,
            UNIQUE(event_id, token)
        )
    """)
  conn.commit()
  conn.close()


init_db()


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
  conn = sqlite3.connect(DB_PATH)
  conn.row_factory = sqlite3.Row
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM events")
  events = cursor.fetchall()
  conn.close()
  return templates.TemplateResponse(
      "index.html", {"request": request, "events": events}
  )


@app.post("/api/events")
def create_event(
    event_name: str = Form(...),
    description: str = Form(...),
    event_date: str = Form(...),
    venue: str = Form(...),
    capacity: int = Form(...),
):
  event_id = str(uuid.uuid4())[:8]
  conn = sqlite3.connect(DB_PATH)
  cursor = conn.cursor()
  try:
    cursor.execute(
        "INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            event_id,
            event_name,
            description,
            event_date,
            venue,
            capacity,
            "PUBLISHED",
        ),
    )
    conn.commit()
  except Exception as e:
    raise HTTPException(status_code=400, detail=str(e))
  finally:
    conn.close()
  return {"message": "Event created successfully", "event_id": event_id}


@app.post("/api/rsvp")
def submit_rsvp(
    event_id: str = Form(...),
    token: str = Form(...),
    guest_name: str = Form(...),
    answer: str = Form(...),
    guests: int = Form(0),
):
  conn = sqlite3.connect(DB_PATH)
  cursor = conn.cursor()

  # Fetch event capacity
  cursor.execute("SELECT capacity FROM events WHERE event_id = ?", (event_id,))
  row = cursor.fetchone()
  if not row:
    conn.close()
    raise HTTPException(status_code=404, detail="Event not found")
  capacity = row[0]

  # Check current confirmed 'yes' count
  cursor.execute(
      "SELECT SUM(guests + 1) FROM rsvps WHERE event_id = ? AND answer = 'yes'",
      (event_id,),
  )
  current_yes = cursor.fetchone()[0] or 0

  final_answer = answer
  if answer == "yes":
    # Enforce capacity & waitlist logic atomically
    if (current_yes + guests + 1) > capacity:
      final_answer = "waitlist"

  rsvp_id = str(uuid.uuid4())[:8]
  now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

  try:
    cursor.execute(
        """
            INSERT INTO rsvps (rsvp_id, event_id, token, guest_name, answer, guests, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(event_id, token) 
            DO UPDATE SET answer=excluded.answer, guests=excluded.guests, updated_at=excluded.updated_at
        """,
        (rsvp_id, event_id, token, guest_name, final_answer, guests, now),
    )
    conn.commit()
  except Exception as e:
    raise HTTPException(status_code=400, detail=str(e))
  finally:
    conn.close()

  return {"status": final_answer, "message": f"RSVP recorded as {final_answer}"}


@app.get("/api/events/{event_id}/analytics")
def get_analytics(event_id: str):
  conn = sqlite3.connect(DB_PATH)
  cursor = conn.cursor()

  cursor.execute("SELECT capacity FROM events WHERE event_id = ?", (event_id,))
  ev = cursor.fetchone()
  if not ev:
    conn.close()
    raise HTTPException(status_code=404, detail="Event not found")
  capacity = ev[0]

  cursor.execute(
      "SELECT answer, COUNT(*) FROM rsvps WHERE event_id = ? GROUP BY answer",
      (event_id,),
  )
  counts = {row[0]: row[1] for row in cursor.fetchall()}
  conn.close()

  yes_count = counts.get("yes", 0)
  maybe_count = counts.get("maybe", 0)
  no_count = counts.get("no", 0)
  waitlist_count = counts.get("waitlist", 0)

  return {
      "capacity": capacity,
      "going": yes_count,
      "maybe": maybe_count,
      "not_going": no_count,
      "waitlist": waitlist_count,
      "available_seats": max(0, capacity - yes_count),
  }


if __name__ == "__main__":
  uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)