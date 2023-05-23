ARG PYTHON_BASE_IMAGE="python"
ARG PYTHON_BASE_VERSION="3.10-slim"
FROM ${PYTHON_BASE_IMAGE}:${PYTHON_BASE_VERSION} AS python

# set the working directory
WORKDIR /app


# Install missing dependencies.
RUN apt-get update &&  \
    apt-get upgrade -y &&  \
    apt-get install -y \
    wget \
    vim \
    && rm -rf /var/lib/apt/lists/*

COPY ./config/requirements.txt ./

RUN pip install --no-cache-dir --upgrade -r requirements.txt

# start the server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]