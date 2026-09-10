# mlops-cd-demo

Class activity: Continuous Delivery (CD) for an ML Application.

A small Flask inference API that gets packaged as a Docker image, pushed to GHCR,
deployed to staging automatically and promoted to production after manual approval.

## Deployment setup

I don't have a separate Ubuntu VM for staging/production, so instead of deploying
over SSH (steps 16-18 of the tutorial) the deploy jobs use the GitHub Actions
runner itself as the "server". The runner already has Docker installed.

- **staging** and **production** are GitHub Environments (Settings -> Environments)
- **production** has a required reviewer, so the workflow waits for approval
- each deploy job logs in to GHCR, pulls the exact image built in the `build` job,
  runs it as a container and checks `GET /health`
- no SSH keys or host passwords are needed; the registry login uses the built-in
  `GITHUB_TOKEN` secret

The image is only built once and the same version tag is promoted from staging to
production (build once, deploy many).
