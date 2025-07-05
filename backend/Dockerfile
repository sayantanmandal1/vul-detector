# Use Python 3.10 slim image for smaller size and better security
FROM python:3.10-slim as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies including C compiler and development tools
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    gcc \
    g++ \
    make \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Create and set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app ./app
COPY build_tree_sitter.py ./build_tree_sitter.py

# Remove any existing tree-sitter directories and clone fresh ones
RUN cd /app/app/services && \
    rm -rf tree-sitter-python tree-sitter-c tree-sitter-cpp tree-sitter-javascript tree-sitter-java && \
    git clone https://github.com/tree-sitter/tree-sitter-python.git && \
    git clone https://github.com/tree-sitter/tree-sitter-c.git && \
    git clone https://github.com/tree-sitter/tree-sitter-cpp.git && \
    git clone https://github.com/tree-sitter/tree-sitter-javascript.git && \
    git clone https://github.com/tree-sitter/tree-sitter-java.git

# Set C compiler flags for compatibility
ENV CC=gcc
ENV CXX=g++
ENV CFLAGS="-fPIC -O2 -std=c99"
ENV CXXFLAGS="-fPIC -O2 -std=c++11"

# Build Tree-sitter grammars using the build script
RUN cd /app/app/services && \
    python /app/build_tree_sitter.py

# Verify the build was successful (just list the directory)
RUN ls -la /app/app/services/build/

# Production stage
FROM python:3.10-slim as production

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    DOCKER_ENV=true

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set working directory
WORKDIR /app

# Copy Python dependencies from builder stage
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code and built grammars
COPY --from=builder /app/app ./app
COPY pytest.ini .
COPY requirements.txt .

# Create necessary directories and set permissions
RUN mkdir -p /app/app/static && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 