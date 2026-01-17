# Deployment checklist

## Pre-deploy (staging)
- Ensure the branch to deploy is merged into `develop`.
- Confirm staging environment secrets are present:
  - DEPLOY_USER, DEPLOY_HOST, APP_DIR, SSH_PRIVATE_KEY (if used)
- Confirm CI (build-and-test) passes on the commit.
- Notify stakeholders if required.

## Deploy to staging (automated)
- Merge MR → develop or trigger the staging workflow manually (Actions → Deploy to Staging → Run workflow).
- Monitor Actions logs for:
  - dependency install errors
  - test failures
  - SSH/rsync errors
  - service restart errors
  - health-check failures
- On success: verify the UI or /health endpoint returns OK.

## Promote to production
- Create and push a tag that matches the production workflow pattern (e.g., `v1.0.0`) or use Actions → Deploy to Production → Run workflow.
- Production environment requires manual approval via the Environments UI.

## Rollback (production)
- If production is unhealthy after deploy:
  - Go to Actions → Production rollback → Run workflow.
  - This triggers the remote rollback script: `/opt/deploy/rollback.sh`
  - Verify service health and logs after rollback.

## Post-deploy
- Verify metrics/alerts and run smoke tests.
- Tag the release and update release notes if appropriate.

## Contacts
- Primary on-call: <name> — <contact>
- Secondary on-call: <name> — <contact>
