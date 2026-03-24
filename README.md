# Largest Rectangle in Matrix — FastAPI

A FastAPI service that finds the largest rectangle of identical elements in a 2D integer matrix. All requests and responses are logged to a SQLite database for turnaround time analysis.

---

## Problem Statement

Given a 2D matrix of integers, find the largest rectangle formed by identical numbers. Return the number itself and the area of the rectangle.

**Example:**
```
Input:
[1, 1, 0, 1, -9]
[1, 1, 1, 1, -9]
[1, 1, 1, 1, -9]
[1, 0, 0, 5, -9]
[5, 0, 0, 0,  5]

Output: (1, 8)  →  2 rows × 4 columns of 1s
```

---

## Algorithm

For each unique value in the matrix:
1. Build a **histogram of consecutive row heights** — each cell increments if it matches the target value, resets to 0 otherwise
2. Apply a **monotonic stack** to find the largest rectangle in the histogram in O(m) time
3. Track the best `(value, area)` pair across all values and rows

> Each bar in the histogram is pushed and popped from the stack exactly once, guaranteeing O(m) time per row regardless of input shape.

| Complexity | Value |
|---|---|
| Time | `O(k × n × m)` — k unique values, n rows, m columns |
| Space | `O(m)` — stack and heights array, cleared per row |

---

## Project Structure

```
├── solution.py        # Core algorithm — monotonic stack histogram approach
├── main.py            # FastAPI app, endpoint, request/response models
├── db.py              # SQLite connection and schema initialisation
├── requirements.txt   # Dependencies
└── README.md
```

---

## Setup

**1. Clone the repository**
```bash
git clone https://github.com/dewangshree/largest_rectangle_Fastapi.git
cd largest_rectangle_Fastapi
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

---

## Running the Server

```bash
uvicorn main:app --reload
```

| URL | Description |
|---|---|
| `http://127.0.0.1:8000` | Base URL |
| `http://127.0.0.1:8000/docs` | Interactive Swagger UI |
| `http://127.0.0.1:8000/redoc` | ReDoc API docs |

---

## API Reference

### `POST /largest-rectangle`

Finds the largest rectangle of identical elements in the given matrix.

**Request Body**
```json
{
  "matrix": [
    [1, 1, 0, 1, -9],
    [1, 1, 1, 1, -9],
    [1, 1, 1, 1, -9],
    [1, 0, 0, 5, -9],
    [5, 0, 0, 0,  5]
  ]
}
```

**Success Response `200`**
```json
{
  "number": 1,
  "area": 8,
  "time_taken": 0.000129
}
```

| Field | Type | Description |
|---|---|---|
| `number` | `int \| null` | The value forming the largest rectangle |
| `area` | `int` | Area of the largest rectangle |
| `time_taken` | `float` | Computation time in seconds |

**Error Response `422`** — returned for jagged or invalid matrices
```json
{
  "detail": "All rows must have the same length."
}
```

---

## Database Logging

Every request is automatically logged to `logs.db` (SQLite):

```sql
CREATE TABLE logs (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    input       TEXT NOT NULL,    -- JSON matrix input
    output      TEXT NOT NULL,    -- JSON result {number, area}
    time_taken  REAL NOT NULL     -- computation time in seconds
)
```

Connections are created per request to ensure **thread safety** under FastAPI's concurrent request handling.

---

## Edge Cases Handled

| Input | Behaviour |
|---|---|
| Empty matrix | Returns `(null, 0)` |
| Jagged matrix | Raises `422` with descriptive error |
| Single element | Returns that element with area `1` |
| Negative integers | Handled correctly |
| All identical values | Returns full matrix area |

---
> **Tie-breaking:** If multiple values form rectangles of equal maximum area, the solution returns the first value encountered during iteration. This is consistent with the problem statement which asks for *the* largest rectangle.

## Constraints

- Matrix size: `1 ≤ rows, columns ≤ 100`
- Matrix contains integers (positive, negative, or zero)
- All rows must have equal length
