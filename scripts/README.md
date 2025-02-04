# GitHub Actions Secrets Management

This directory contains scripts for managing GitHub Actions secrets for your iOS app workflows.

## Upload Secrets Script

The `upload_secrets.sh` script helps you upload all necessary secrets to GitHub Actions from a local `.env` file.

### Prerequisites

1. Install GitHub CLI:
```bash
brew install gh
```

2. Login to GitHub CLI:
```bash
gh auth login
```

### Usage

1. Copy the `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Fill in your secrets in the `.env` file

3. Make the script executable:
```bash
chmod +x scripts/upload_secrets.sh
```

4. Run the script:
```bash
./scripts/upload_secrets.sh
```

### Required Secrets

The following secrets are required for the workflows to function properly:

#### App Store Connect API Keys
- `APP_STORE_CONNECT_ISSUER_ID`: Your App Store Connect API issuer ID
- `APP_STORE_CONNECT_API_KEY_ID`: Your App Store Connect API key ID
- `APP_STORE_CONNECT_API_PRIVATE_KEY`: Your App Store Connect API private key

#### Appetize.io
- `APPETIZE_API_TOKEN`: Your Appetize.io API token

#### Certificates and Provisioning
- `BUILD_CERTIFICATE_BASE64`: Base64-encoded distribution certificate
- `P12_PASSWORD`: Password for the certificate
- `BUILD_PROVISION_PROFILE_BASE64`: Base64-encoded provisioning profile
- `KEYCHAIN_PASSWORD`: Password for the temporary keychain

#### Notifications
- `WEBHOOK_URL`: URL for failure notifications (e.g., Slack webhook)

### Generating Required Values

#### Base64 Encoding Certificates
For the certificate and provisioning profile, use these commands:

```bash
# For the distribution certificate
base64 -i Certificates.p12 | tr -d '\n' > certificate.txt

# For the provisioning profile
base64 -i profile.mobileprovision | tr -d '\n' > profile.txt
```

#### App Store Connect API Key
1. Go to App Store Connect > Users and Access > Keys
2. Generate a new API Key with App Manager role
3. Download the key and note the Issuer ID and Key ID

### Security Notes

- The `.env` file is automatically added to `.gitignore` to prevent accidental commits
- Never commit secrets to version control
- Rotate secrets periodically for security
- Use different certificates for development and production 