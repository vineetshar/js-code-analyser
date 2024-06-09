FROM python:3.10

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    cmake \
    pkg-config \
    python3-venv \
    libtool \
    autoconf \
    automake

# Clone the tree-sitter JavaScript grammar
RUN git clone https://github.com/tree-sitter/tree-sitter-javascript /app/tree-sitter-javascript

# Generate the parser
WORKDIR /app/tree-sitter-javascript
RUN tree-sitter generate

# Build the Tree-sitter language library
WORKDIR /app
RUN tree-sitter build-wasm /app/tree-sitter-javascript
RUN g++ -shared -o /app/build/my-languages.so -fPIC /app/tree-sitter-javascript/src/parser.c

# Copy and install Python dependencies
COPY requirements.txt .
RUN python -m venv venv
RUN . venv/bin/activate && pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
