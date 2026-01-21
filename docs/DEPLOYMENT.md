# Deployment Guide

This repository uses two deployment environments: **staging** and **production**.

## Environments
- **staging**: used for testing and validation
- **production**: live environment

## Branch Strategy
- `develop` → staging
- `main` → production
- `feature/*` → pull requests

## Workflow Files
The following GitHub Actions workflows are used:

- `.github/workflows/deploy-staging.yml`
- `.github/workflows/deploy-production.yml`
- `.github/workflows/rollback.yml`

## Secrets
Secrets are stored in **GitHub Environments** and injected during workflow execution.

## Rollback
Rollback deployments use **previous releases available on the server**.

