#!/bin/bash

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "GitHub CLI (gh) is not installed. Please install it first:"
    echo "  brew install gh"
    exit 1
fi

# Check if gh is authenticated
if ! gh auth status &> /dev/null; then
    echo "Please login to GitHub CLI first:"
    echo "  gh auth login"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "No .env file found. Creating a template..."
    cat > .env << EOL
# App Store Connect API Keys
APP_STORE_CONNECT_ISSUER_ID=
APP_STORE_CONNECT_API_KEY_ID=
APP_STORE_CONNECT_API_PRIVATE_KEY=

# Appetize.io
APPETIZE_API_TOKEN=

# Certificates and Provisioning
BUILD_CERTIFICATE_BASE64=
P12_PASSWORD=
BUILD_PROVISION_PROFILE_BASE64=
KEYCHAIN_PASSWORD=

# Notifications
WEBHOOK_URL=
EOL
    echo ".env template created. Please fill in the values and run this script again."
    exit 1
fi

# Get repository name
REPO_NAME=$(gh repo view --json nameWithOwner -q .nameWithOwner)
if [ -z "$REPO_NAME" ]; then
    echo "Could not determine repository name. Are you in a git repository?"
    exit 1
fi

echo "🔐 Uploading secrets to $REPO_NAME..."

# Read .env file and upload each secret
while IFS='=' read -r key value || [ -n "$key" ]; do
    # Skip comments and empty lines
    if [[ $key =~ ^#.*$ ]] || [ -z "$key" ]; then
        continue
    fi
    
    # Trim whitespace
    key=$(echo "$key" | xargs)
    value=$(echo "$value" | xargs)
    
    # Skip if value is empty
    if [ -z "$value" ]; then
        echo "⚠️  Warning: No value for $key, skipping..."
        continue
    fi
    
    echo "📤 Uploading secret: $key"
    echo "$value" | gh secret set "$key" --repo="$REPO_NAME" 2>/dev/null
    
    if [ $? -eq 0 ]; then
        echo "✅ Successfully set $key"
    else
        echo "❌ Failed to set $key"
    fi
done < .env

echo "
🎉 Secret upload complete!

To use these secrets in your workflows, reference them like this:
\${{ secrets.SECRET_NAME }}

For example:
\${{ secrets.APP_STORE_CONNECT_API_KEY_ID }}

Remember to add .env to your .gitignore to keep your secrets safe!
"

# Check if .env is in .gitignore
if ! grep -q "^\.env$" .gitignore 2>/dev/null; then
    echo ".env" >> .gitignore
    echo "Added .env to .gitignore for security"
fi 