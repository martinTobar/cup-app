FROM python:3.13-alpine
WORKDIR /CUP-APP
COPY pyproject.toml uv.lock  ./
RUN pip install uv
RUN uv sync --frozen --no-dev
COPY . .
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser
EXPOSE 8000
# Run the Alembic migrations and then start the FastAPI application
# Use --no-sync to avoid syncing the virtual environment again.
CMD ["sh", "-c", "uv run --no-sync alembic upgrade head && exec uv run --no-sync fastapi run main.py --port 8000"]
