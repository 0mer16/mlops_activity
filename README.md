# mlops-cd-demo

This is my repo for the MLOps class activity "Continuous Delivery (CD) for an ML Application".
I pushed after every step so the commits show the progress.

## What I did

- Made a small Flask API with `/health` and `/predict` (the "model" just multiplies the input by 2)
- Added pytest tests for both endpoints
- Wrote a Dockerfile and added a VERSION file
- Made a CD workflow that runs when I push a tag like `v1.0.0`. It runs the tests, builds the
  Docker image, pushes it to GHCR, deploys to staging and then waits for my approval before production
- Added a CI workflow so pull requests only run the tests
- Added a rollback workflow to put an older version back on production

I don't have a server, so I used the GitHub Actions runner as the staging/production server
instead of SSH. The deploy jobs pull the image from GHCR, run it and check `/health`.
Production is protected by a required reviewer (me).

## Releases

- `v1.0.0` - first release, went through staging and I approved production
- `v1.1.0` - changed the model version to 1.1 through a PR, then tagged and released it
- Rollback - ran the Rollback workflow with `1.0.0` to go back to the old image without rebuilding

## Run locally

```
pip install -r requirements.txt
python app.py
pytest
```
