Deployment guide (simple)

This repo uses two environments: staging and production.

Files added:
docs/DEPLOYMENT.md
.github/workflows/deploy-staging.yml
.github/workflows/deploy-production.yml
.github/workflows/rollback.yml

Key concepts:
- develop → staging
- main → production
- feature/* → PRs

Secrets are stored in GitHub Environments.
Rollback uses previous releases on the server.
