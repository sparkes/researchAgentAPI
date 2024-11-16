FROM python:3.9-slim

# Install git for submodule operations
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the entire repository including .git
COPY . .

# Initialize and update submodules
RUN git submodule update --init --recursive

# Install dependencies
RUN pip install -r requirements.txt

# Add researchAgent to PYTHONPATH
ENV PYTHONPATH="/app:${PYTHONPATH}"

CMD ["python", "app.py"]
