# # Stage 1: Install dependencies
# FROM python:3.11-slim as requirements-stage
# WORKDIR /tmp

# # Copy only the requirements file and install dependencies
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Stage 2: Build the final image
# FROM python:3.11-slim as runtime-stage
# WORKDIR /app

# # Copy installed dependencies from the requirements stage
# COPY --from=requirements-stage /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# # Copy the rest of your application code
# COPY . .

# # Expose the port the app runs on (FastAPI default is 80)
# EXPOSE 80

# # Command to run the application with Uvicorn, listening on all interfaces (0.0.0.0)
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]



# Stage 1: Install dependencies
FROM python:3.11-slim AS builder

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app

# Copy installed packages from builder (includes binaries)
COPY --from=builder /root/.local /home/appuser/.local

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Add local bin to PATH
ENV PATH=/home/appuser/.local/bin:$PATH

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]