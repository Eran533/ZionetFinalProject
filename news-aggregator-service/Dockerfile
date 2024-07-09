FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install Dapr CLI and runtime
RUN apt-get update && \
    apt-get install -y wget ca-certificates && \
    wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.sh -O - | /bin/bash && \
    dapr init --slim

# Copy application code
COPY . .

# Expose the service port
EXPOSE 5002

# Set environment variables
ENV DAPR_HOME=/root/.dapr
ENV PATH=$PATH:$DAPR_HOME/bin

CMD ["dapr", "run", "--app-id", "news-aggregator-service", "--app-port", "5002", "--", "python", "NewsAggregatorService.py"]
