FROM python:3.9-slim

# Install git for submodule operations
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy only what's needed for git operations first
COPY .git ./.git
COPY .gitmodules .

# Initialize and update submodules
RUN git submodule update --init --recursive

# Now copy the rest of the application
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Install the researchAgent package in development mode
RUN pip install -e researchAgent/

CMD ["python", "app.py"]
