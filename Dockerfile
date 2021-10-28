FROM python:3.9-alpine

# Set any env values we need
ENV PYTHONPATH=/app \
    SYS_VARS_PATH=/app/secrets \
    FLASK_APP=wsgi.py \
    TIMES_FAILED_THRESHOLD=10 \
    ENABLE_DISCORD_LOGGING=false

# Copy the app files into the container
RUN mkdir -p /app
COPY . /app
WORKDIR /app

# Install required deps
RUN apk add --no-cache g++ && \
    python3 -m pip install pip --upgrade && \
    pip3 install --no-cache-dir toml && \
    python3 ./get-requirements.py && \
    pip3 install --no-cache-dir -r requirements.txt && \
    rm ./requirements.txt && \
    chmod u+x ./run-app.sh && \
    apk del g++

# Start the app
ENTRYPOINT [ "sh", "./run-app.sh" ]
