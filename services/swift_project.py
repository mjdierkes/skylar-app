import os
import re
import subprocess
from config import Config

# Path to the swift template files (relative to this file)
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "templates", "swift")

def sanitize_name(app_name: str) -> str:
    """Remove non-alphanumeric characters for directory and target names."""
    return re.sub(r"[^A-Za-z0-9]", "", app_name)

def create_swift_project(app_name: str):
    sanitized_name = sanitize_name(app_name)
    if not sanitized_name:
        raise ValueError("Invalid app name provided.")

    project_dir = os.path.join(Config.PROJECTS_ROOT, sanitized_name)
    if os.path.exists(project_dir):
        raise FileExistsError("A project with this name already exists.")

    os.makedirs(project_dir)
    sources_dir = os.path.join(project_dir, "Sources")
    os.makedirs(sources_dir, exist_ok=True)

    # Create .github/workflows directory
    workflows_dir = os.path.join(project_dir, ".github", "workflows")
    os.makedirs(workflows_dir, exist_ok=True)

    # Create GitHub Actions workflow file
    workflow_path = os.path.join(workflows_dir, "ios_build_and_deploy.yml")
    workflow_contents = f"""name: iOS Build

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  issues: write

env:
  XCODE_VERSION: '15.2'
  DEVELOPER_DIR: /Applications/Xcode_15.2.app/Contents/Developer

jobs:
  build:
    name: Build and Test
    runs-on: macos-14
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Select Xcode Version
        run: |
          sudo xcode-select -s /Applications/Xcode_15.2.app
          xcodebuild -version
          echo "Selected Xcode path: $(xcode-select -p)"

      - name: Cache Homebrew
        uses: actions/cache@v4
        with:
          path: |
            ~/Library/Caches/Homebrew
            ~/Library/Caches/Homebrew/downloads
          key: ${{{{ runner.os }}}}-brew-${{{{ hashFiles('.github/workflows/ios_build_and_deploy.yml') }}}}
          restore-keys: |
            ${{{{ runner.os }}}}-brew-

      - name: Install XcodeGen
        run: brew install xcodegen

      - name: Cache Swift packages
        uses: actions/cache@v4
        with:
          path: |
            .build
            ~/Library/Developer/Xcode/DerivedData/**/SourcePackages/checkouts
          key: ${{{{ runner.os }}}}-spm-${{{{ hashFiles('**/Package.resolved') }}}}
          restore-keys: |
            ${{{{ runner.os }}}}-spm-

      - name: Cache DerivedData
        uses: actions/cache@v4
        with:
          path: ~/Library/Developer/Xcode/DerivedData
          key: ${{{{ runner.os }}}}-derived-data-${{{{ hashFiles('project.yml') }}}}
          restore-keys: |
            ${{{{ runner.os }}}}-derived-data-

      - name: Generate Xcode project
        run: xcodegen generate

      - name: Build iOS App
        id: build
        run: |
          set -o pipefail && xcodebuild clean build \\
            -project {sanitized_name}.xcodeproj \\
            -scheme {sanitized_name} \\
            -sdk iphonesimulator \\
            -destination 'platform=iOS Simulator,name=iPhone 15,OS=17.2' \\
            -configuration Debug \\
            -derivedDataPath ~/Library/Developer/Xcode/DerivedData \\
            CODE_SIGN_IDENTITY="" \\
            CODE_SIGNING_REQUIRED=NO \\
            CODE_SIGNING_ALLOWED=NO | xcpretty

      - name: Upload Build Artifacts
        if: success()
        uses: actions/upload-artifact@v4
        with:
          name: debug-build
          path: ~/Library/Developer/Xcode/DerivedData/**/Build/**/*.app
          retention-days: 5

      - name: Notify Webhook on Failure
        if: failure()
        uses: distributhor/workflow-webhook@v3
        env:
          webhook_url: ${{{{ secrets.WEBHOOK_URL }}}}
          webhook_secret: ${{{{ secrets.WEBHOOK_SECRET }}}}
          data: '{{"repository": "${{{{ github.repository }}}}", "workflow": "${{{{ github.workflow }}}}", "run_id": "${{{{ github.run_id }}}}", "run_number": "${{{{ github.run_number }}}}"}}'"""
    with open(workflow_path, "w") as f:
        f.write(workflow_contents)

    # Create ExportOptions.plist for development builds
    export_options_path = os.path.join(project_dir, "ExportOptions.plist")
    export_options_contents = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>method</key>
    <string>development</string>
    <key>compileBitcode</key>
    <false/>
    <key>stripSwiftSymbols</key>
    <true/>
</dict>
</plist>"""
    with open(export_options_path, "w") as f:
        f.write(export_options_contents)

    # --- Copy and process the MainApp.swift template ---
    main_app_template_path = os.path.join(TEMPLATE_DIR, "MainApp.swift")
    with open(main_app_template_path, "r") as f:
        main_app_contents = f.read()
    # Replace placeholder {APP_NAME} with the sanitized app name.
    main_app_contents = main_app_contents.replace("{APP_NAME}", sanitized_name)
    main_app_file = os.path.join(sources_dir, f"{sanitized_name}.swift")
    with open(main_app_file, "w") as f:
        f.write(main_app_contents)

    # --- Copy the ContentView.swift template ---
    content_view_template_path = os.path.join(TEMPLATE_DIR, "ContentView.swift")
    with open(content_view_template_path, "r") as f:
        content_view_contents = f.read()
    content_view_file = os.path.join(sources_dir, "ContentView.swift")
    with open(content_view_file, "w") as f:
        f.write(content_view_contents)

    # --- Generate XcodeGen project spec (project.yml) ---
    bundle_identifier = f"{Config.COMPANY_IDENTIFIER}.{sanitized_name.lower()}"
    project_yml_file = os.path.join(project_dir, "project.yml")
    project_yml_contents = f"""name: {sanitized_name}
options:
  bundleIdPrefix: {Config.COMPANY_IDENTIFIER}
  createIntermediateGroups: true
  deploymentTarget:
    iOS: "16.0"
targets:
  {sanitized_name}:
    type: application
    platform: iOS
    sources:
      - Sources
    info:
      path: Info.plist
      properties:
        CFBundleName: {sanitized_name}
        CFBundleIdentifier: {bundle_identifier}
        UILaunchStoryboardName: LaunchScreen
        UISupportedInterfaceOrientations:
          - UIInterfaceOrientationPortrait
        UIApplicationSceneManifest:
          UIApplicationSupportsMultipleScenes: false
"""
    with open(project_yml_file, "w") as f:
        f.write(project_yml_contents)

    # Create Info.plist file
    info_plist_path = os.path.join(project_dir, "Info.plist")
    info_plist_contents = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict/>
</plist>"""
    with open(info_plist_path, "w") as f:
        f.write(info_plist_contents)

    # --- Run XcodeGen to generate the Xcode project ---
    try:
        subprocess.run([Config.XCODEGEN_PATH, "generate"],
                       cwd=project_dir, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"XcodeGen failed: {str(e)}")

    # --- Initialize Git only if GitHub token is available ---
    if Config.GITHUB_TOKEN and Config.GITHUB_TOKEN != "YOUR_GITHUB_PERSONAL_ACCESS_TOKEN":
        try:
            subprocess.run(["git", "init"], cwd=project_dir, check=True)
            subprocess.run(["git", "add", "."], cwd=project_dir, check=True)
            subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=project_dir, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Git initialization failed: {str(e)}")

    return project_dir, sanitized_name, bundle_identifier 