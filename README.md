# kc-booth

kc-booth is a homelab application for managing SSH keys, servers, and certificates.

## Features

- SSH key store and management
- Server management
- Certificate management with step-ca
- Automated certificate rotation
- Monitoring and distribution

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mylaniakea/kc-booth.git
   ```
2. Navigate to the project directory:
   ```bash
   cd kc-booth
   ```
3. Build and run the application:
   ```bash
   docker compose up --build -d
   ```

The API will be available at `http://localhost:8001`.

### Running the tests

```bash
docker compose run --rm test
```

## API Documentation

The API documentation is available at `http://localhost:8001/docs`.