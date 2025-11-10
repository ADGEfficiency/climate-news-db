# Build stage
FROM golang:1.21-bookworm AS builder

WORKDIR /app

# Copy go module files
COPY src/webapp/go.mod src/webapp/go.sum src/webapp/
RUN cd src/webapp && go mod download

# Copy source code
COPY src/webapp/*.go src/webapp/

# Build the application with CGO enabled for sqlite3
RUN cd src/webapp && CGO_ENABLED=1 go build -o /app/webapp .

# Runtime stage
FROM debian:bookworm-slim

# Install SQLite runtime library
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the binary from builder
COPY --from=builder /app/webapp .

# Copy application files
COPY data/db.sqlite ./data/db.sqlite
COPY data/climate-news-db-dataset.zip ./data/climate-news-db-dataset.zip
COPY static ./static
COPY src/webapp/templates ./src/webapp/templates

EXPOSE 8080

CMD ["./webapp"]
