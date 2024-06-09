FROM python:3.11-slim

# Set any env values we need
ENV PYTHONPATH=/app \
    SYS_VARS_PATH=/app/secrets \
    FLASK_APP=wsgi.py \
    FLASK_SKIP_DOTENV=1 \
    TIMES_FAILED_THRESHOLD=10 \
    ENABLE_DISCORD_LOGGING=false \
    FILTER_INCLUDE_ROTTED=true \
    FILTER_EXCLUDE_ORIGIN=true

# Copy the app files into the container
RUN mkdir -p /app
COPY . /app
WORKDIR /app

# Install required deps
RUN python -m pip install pip --upgrade && \
    python ./get-requirements.py && \
    pip install --no-cache-dir -r requirements.txt && \
    rm ./requirements.txt && \
    chmod u+x ./run-app.sh

# Start the app
ENTRYPOINT [ "sh", "./run-app.sh" ]
