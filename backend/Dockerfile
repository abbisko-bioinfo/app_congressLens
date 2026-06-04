FROM python:3.12-slim

WORKDIR /app

RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ && \
    pip install --no-cache-dir uv

COPY pyproject.toml .
RUN uv pip install --system --index-url https://mirrors.aliyun.com/pypi/simple/ ".[dev]"

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
