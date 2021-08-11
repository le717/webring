FROM python:3.9

# Set any env values we need
ENV PYTHONPATH=/app
ENV SYS_VARS_PATH=/app/secrets

# Copy the app files into the container
RUN mkdir -p /app
COPY . /app
WORKDIR /app

# Install required deps
RUN python3 -m pip install pip --upgrade && \
    pip3 install --no-cache-dir toml && \
    python3 ./get-requirements.py && \
    pip3 install --no-cache-dir -r requirements.txt && \
    rm ./requirements.txt && \
    chmod u+x ./run-app.sh

# Start the app
ENTRYPOINT [ "sh", "./run-app.sh" ]
