FROM python:3.9-slim

# Install git for submodule operations
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the entire repository including .git
COPY . .

# Force update submodule to latest main branch
RUN git submodule deinit -f researchAgent && \
    git submodule update --init --recursive && \
    cd researchAgent && \
    git checkout main && \
    git pull origin main

# Install dependencies
RUN pip install -r requirements.txt

# Set PYTHONPATH
ENV PYTHONPATH=/app

CMD ["python", "app.py"]
