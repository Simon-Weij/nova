FROM python:3.13-slim AS builder
RUN pip install uv==0.10.12

WORKDIR /app
COPY pyproject.toml uv.lock ./
COPY . ./

RUN uv export --frozen --no-dev -o requirements.txt
RUN pip install --no-cache-dir --target=/install -r requirements.txt
RUN pip install --no-cache-dir --target=/install .

FROM gcr.io/distroless/python3-debian13

COPY --from=builder /install /install
COPY --from=builder /app/main.py /app/main.py

ENV PYTHONPATH=/install

WORKDIR /app
USER nonroot

CMD ["-m", "fastapi", "run", "main.py", "--port", "8000"]