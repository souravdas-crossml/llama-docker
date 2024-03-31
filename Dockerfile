FROM ubuntu:20.04

# Set the working directory in the container
WORKDIR /app

# Copy all other files
COPY . .

# Install Python and pip
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
    && apt-get install -y --no-install-recommends libpython3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install build dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        wget \
        gcc \
        g++ \
        procps \
    && rm -rf /var/lib/apt/lists/*

# Install the needed packages
RUN pip install --no-cache-dir --default-timeout=1000 -r  requirements.txt
RUN /bin/python3 -m pip install "fastapi[all]"

# Install uvicorn
RUN pip install uvicorn

# Expose port 8000 for uvicorn
EXPOSE 8000

# Run uvicorn with FastAPI app when the container launches
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
