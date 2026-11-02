# Kubernetes deployment

This layout runs the stateless application tier on Kubernetes and expects
PostgreSQL and Redis to be managed services (RDS/Cloud SQL and ElastiCache or
equivalent). Keeping data services outside the cluster avoids single-node
storage and failover problems.

## Prerequisites

- Kubernetes 1.27+
- An ingress controller (the manifests use the `nginx` Ingress class)
- Metrics Server for the HPAs
- A pre-created `recommender-secrets` Secret in the target namespace

Create the secret without committing credentials:

```bash
kubectl -n recommender create secret generic recommender-secrets \
  --from-literal=DATABASE_URL='postgresql://user:password@db.example.com:5432/recommender_db' \
  --from-literal=REDIS_URL='redis://:password@redis.example.com:6379' \
  --from-literal=JWT_SECRET='replace-with-at-least-32-random-characters'
```

Set the public host and container image names in
`overlays/production/kustomization.yaml`, then deploy:

```bash
kubectl apply -k k8s/overlays/production
kubectl -n recommender rollout status deployment/backend
kubectl -n recommender rollout status deployment/frontend
```

Before a production rollout, replace the example image tags in the production
overlay with immutable image digests (`image@sha256:...`) from the trusted
registry and verify the image signature or provenance. The base manifests use
`imagePullPolicy: Always` to avoid silently running a stale cached image, but
image tags remain mutable unless the registry enforces tag immutability.

The application is exposed at `/`, with API traffic at `/api/*`. The backend
uses `/health` for liveness and `/readyz` for readiness. Redis is optional at
runtime because the application has an in-memory fallback; PostgreSQL is
required.

The NetworkPolicy allows database and Redis egress on their standard ports.
If those services use non-standard ports, update `base/network-policy.yaml`.
The ingress controller namespace must carry the
`kubernetes.io/metadata.name=ingress-nginx` label (the standard installation
does).
