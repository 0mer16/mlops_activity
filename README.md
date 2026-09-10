# mlops-cd-demo

This repo is for my MLOps class activity where we had to follow the tutorial
"Continuous Delivery (CD) for an ML Application". I pushed after every step so the
commit history shows how I built it up.

## What I built

I made a small Flask API that acts like an ML model. It has a `/health` endpoint and
a `/predict` endpoint (the "model" just multiplies the input by 2, since the point of
the activity is the delivery pipeline and not the model itself). I also wrote two
pytest tests for it.

After that I wrote a Dockerfile so the app can be packaged as an image, and added a
`VERSION` file starting at 1.0.0.

## The CD pipeline

I then built `.github/workflows/cd.yml` one step at a time. It only runs when I push
a version tag like `v1.0.0`, not on every commit. The jobs are:

1. **test** - installs the requirements and runs pytest
2. **build** - takes the version from the tag (v1.0.0 -> 1.0.0), builds the Docker
   image and pushes it to GHCR with both the version tag and `latest`
3. **deploy-staging** - deploys that same image to staging automatically
4. **deploy-production** - waits for my manual approval before deploying

Before adding the deploy jobs I pushed a test tag `v1.0.0-rc.1` to make sure the
test and build jobs actually worked. Both passed and the image showed up in GHCR,
so I knew the Dockerfile was fine (I don't have Docker installed on my laptop so
this was the first time it was really built).

## How I handled staging/production

The tutorial deploys to an Ubuntu server over SSH (steps 16-18), but I don't have a
VM, so I used the GitHub Actions runner itself as the server. The runner already
has Docker on it, so the deploy jobs just log in to GHCR, pull the image, run it as
a container and then check that `/health` responds.

I created two environments in Settings -> Environments:

- `staging` - no protection, so it deploys straight away
- `production` - I added myself as a required reviewer, so the workflow stops and
  waits until I approve it

Because of this I didn't need SSH keys or host secrets. The only secret used is the
built-in `GITHUB_TOKEN` for logging in to the registry.

One thing I learned from this is the "build once, deploy many" idea. The image is
only built once in the build job, and the exact same version gets promoted from
staging to production instead of being rebuilt.
