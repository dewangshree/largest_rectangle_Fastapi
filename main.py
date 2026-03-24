import json
import time

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from db import get_connection
from solution import largest_rectangle

app = FastAPI()


class MatrixInput(BaseModel):
    matrix: list[list[int]]


class RectangleResponse(BaseModel):
    number: int | None
    area: int
    time_taken: float


@app.post("/largest-rectangle", response_model=RectangleResponse)
def compute(data: MatrixInput) -> RectangleResponse:
    try:
        start = time.perf_counter()
        number, area = largest_rectangle(data.matrix)
        time_taken = time.perf_counter() - start
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    with get_connection() as conn:
        conn.execute(
            "INSERT INTO logs (input, output, time_taken) VALUES (?, ?, ?)",
            (
                json.dumps(data.matrix),
                json.dumps({"number": number, "area": area}),
                time_taken,
            ),
        )

    return RectangleResponse(number=number, area=area, time_taken=time_taken)