# Use official Python lightweight runtime
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HEADLESS=true \
    AI_PROVIDER=mock \
    ENVIRONMENT=docker

# Set working directory inside container
WORKDIR /app

# Install system dependencies needed for Playwright browser dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    curl \
    gnupg \
    ca-certificates \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install python packages
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Install Playwright browser binaries
RUN python -m playwright install --with-deps chromium

# Copy full project codebase
COPY . .

# Create logs and reports directories
RUN mkdir -p logs reports

# Default command: Execute all tests with HTML report generation
CMD ["python", "-m", "pytest", "--html=reports/report.html", "--self-contained-html"]
