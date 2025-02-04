from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
import hmac
import hashlib
import logging
from config import Config

router = APIRouter()
logging.basicConfig(level=logging.INFO)

def verify_github_signature(payload_body: bytes, signature_header: str) -> bool:
    """Verify that the webhook is from GitHub using the webhook secret."""
    if not Config.GITHUB_WEBHOOK_SECRET:
        logging.warning("GITHUB_WEBHOOK_SECRET not configured")
        return False
        
    if not signature_header:
        return False

    hash_object = hmac.new(
        Config.GITHUB_WEBHOOK_SECRET.encode('utf-8'),
        msg=payload_body,
        digestmod=hashlib.sha256
    )
    expected_signature = "sha256=" + hash_object.hexdigest()
    
    return hmac.compare_digest(signature_header, expected_signature)

@router.post("/webhook")
async def github_webhook(request: Request):
    """Handle GitHub webhook events, particularly workflow run failures."""
    # Verify webhook signature
    payload_body = await request.body()
    signature_header = request.headers.get("X-Hub-Signature-256")
    
    if not verify_github_signature(payload_body, signature_header):
        raise HTTPException(status_code=401, detail="Invalid signature")

    # Parse the webhook payload
    event_type = request.headers.get("X-GitHub-Event")
    payload = await request.json()

    if event_type == "workflow_run":
        workflow_run = payload.get("workflow_run", {})
        conclusion = workflow_run.get("conclusion")
        status = workflow_run.get("status")
        
        if status == "completed" and conclusion == "failure":
            # Extract relevant information about the failure
            repo_name = payload.get("repository", {}).get("full_name")
            workflow_name = workflow_run.get("name")
            run_number = workflow_run.get("run_number")
            html_url = workflow_run.get("html_url")
            jobs_url = workflow_run.get("jobs_url")
            logs_url = workflow_run.get("logs_url")
            
            # Log the failure details
            failure_message = (
                f"⚠️ Workflow failure in {repo_name}\n"
                f"Workflow: {workflow_name}\n"
                f"Run Number: {run_number}\n"
                f"Details: {html_url}\n"
                f"Jobs URL: {jobs_url}\n"
                f"Logs URL: {logs_url}\n"
                f"Steps:"
            )
            logging.error(failure_message)

            # Log any step failures if available
            steps = workflow_run.get("steps", [])
            for step in steps:
                if step.get("conclusion") == "failure":
                    step_message = (
                        f"  - Step '{step.get('name')}' failed:\n"
                        f"    Output: {step.get('output', 'No output available')}"
                    )
                    logging.error(step_message)
            
            # Here you could add additional notification methods:
            # - Send email notifications
            # - Post to Slack/Discord
            # - Create a GitHub issue
            # - etc.
            
            return JSONResponse(
                status_code=200,
                content={
                    "message": "Workflow failure processed",
                    "details": {
                        "repository": repo_name,
                        "workflow": workflow_name,
                        "run_number": run_number,
                        "url": html_url
                    }
                }
            )
    
    return JSONResponse(status_code=200, content={"message": "Event received"}) 