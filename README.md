# kc-booth

kc-booth is a homelab application for managing SSH keys, servers, and certificates.

## Features

- SSH key store and management with encryption
- Server management with encrypted credentials
- Certificate management with step-ca
- Automated certificate rotation
- Monitoring and distribution

## Security

kc-booth encrypts all sensitive data (passwords and private keys) before storing in the database using Fernet symmetric encryption (AES 128-bit).

## Getting Started

### Prerequisites

- Docker
- Docker Compose
- Python 3.8+ (for key generation)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mylaniakea/kc-booth.git
   ```

2. Navigate to the project directory:
   ```bash
   cd kc-booth
   ```

3. Generate an encryption key:
   ```bash
   python3 generate_encryption_key.py
   ```
   
   Copy the `ENCRYPTION_KEY` value and export it:
   ```bash
   export ENCRYPTION_KEY="your-generated-key-here"
   ```
   
   **IMPORTANT**: Store this key securely! Anyone with access to this key can decrypt all stored credentials. Never commit it to version control.

4. Build and run the application:
   ```bash
   docker compose up --build -d
   ```

The API will be available at `http://localhost:8001`.

### Running the tests

```bash
export ENCRYPTION_KEY="your-generated-key-here"
docker compose run --rm test
```

## API Documentation

The API documentation is available at `http://localhost:8001/docs`.

## Security Considerations

- **Encryption Key**: The encryption key must be kept secure. In production, use a secrets manager (e.g., HashiCorp Vault, AWS Secrets Manager, etc.)
- **Key Rotation**: If the encryption key is compromised, you'll need to:
  1. Generate a new key
  2. Decrypt all data with the old key
  3. Re-encrypt with the new key
  4. Update the environment variable
- **Sensitive Fields**: Private keys and passwords are never returned in API responses (write-only fields)
- **Transport Security**: Always use HTTPS in production to protect data in transit

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `ENCRYPTION_KEY`: Fernet encryption key (required)
- `STEP_PROVISIONER_PASSWORD`: Password for step-ca provisioner
