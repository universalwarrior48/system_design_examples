# E-Commerce System - Phase 7: Kubernetes & HPA

This folder contains the Phase 7 implementation of the E-Commerce system.

## Phase Overview

**Goal**: Deploy to Kubernetes with Horizontal Pod Autoscaler (HPA) for automatic scaling

## New Components

### Kubernetes (Container Orchestration)
- Deployments for each service
- Services for networking
- ConfigMaps for configuration
- Secrets for sensitive data
- Ingress for external access

### Horizontal Pod Autoscaler (HPA)
- Automatic scaling based on CPU/memory
- Custom metrics scaling (requests per second)
- Scale up/down policies
- Resource quotas

### Additional K8s Components
- **ConfigMaps**: Environment configuration
- **Secrets**: Sensitive data (passwords, API keys)
- **Ingress**: External traffic routing
- **Persistent Volumes**: Database storage
- **Namespaces**: Environment isolation

## Technology Stack

### Backend (Kubernetes Deployments)
- FastAPI (Python) in Docker containers
- SQLAlchemy
- Pydantic
- PostgreSQL

### Infrastructure (Kubernetes Native or External)
- **Redis**: Caching (StatefulSet or external)
- **RabbitMQ**: Message broker (StatefulSet or external)
- **Nginx Ingress**: API Gateway
- **Prometheus**: Metrics collection
- **Grafana**: Visualization
- **PostgreSQL**: StatefulSet or managed service

## Project Structure

```
ecommerce_7/
├── gateway/
│   └── nginx.conf
├── services/
│   ├── user_service/
│   │   ├── app/
│   │   ├── Dockerfile
│   │   └── k8s/                # NEW: Kubernetes manifests
│   │       ├── deployment.yaml
│   │       ├── service.yaml
│   │       ├── configmap.yaml
│   │       ├── hpa.yaml
│   │       └── ingress.yaml
│   ├── inventory_service/
│   │   ├── app/
│   │   ├── Dockerfile
│   │   └── k8s/
│   │       ├── deployment.yaml
│   │       ├── service.yaml
│   │       ├── configmap.yaml
│   │       └── hpa.yaml
│   ├── order_service/
│   │   ├── app/
│   │   ├── Dockerfile
│   │   └── k8s/
│   │       ├── deployment.yaml
│   │       ├── service.yaml
│   │       ├── configmap.yaml
│   │       └── hpa.yaml
│   └── payment_service/
│       ├── app/
│       ├── Dockerfile
│       └── k8s/
│           ├── deployment.yaml
│           ├── service.yaml
│           └── configmap.yaml
├── shared/
│   ├── common/
│   ├── events/
│   └── auth/
├── infra/
│   ├── redis/
│   ├── rabbitmq/
│   ├── postgres/
│   ├── prometheus/
│   └── grafana/
├── k8s/                      # NEW: Root Kubernetes configurations
│   ├── namespace.yaml
│   ├── ingress.yaml
│   ├── secrets.yaml
│   └── rbac/
├── helm/                     # Optional: Helm charts
│   └── ecommerce/
├── kustomize/                # Optional: Kustomize overlays
│   ├── base/
│   └── overlays/
│       ├── dev/
│       └── prod/
└── tests/
```

## Key Changes from Phase 6

1. **Kubernetes Manifests**:
   - Deployment configurations for each service
   - Service definitions for internal networking
   - ConfigMaps for non-sensitive configuration
   - Secrets management
   - Ingress rules for external access

2. **Horizontal Pod Autoscaler**:
   - CPU-based scaling (target: 70% utilization)
   - Memory-based scaling (target: 80% utilization)
   - Custom metrics (requests per second)
   - Min/max replica counts
   - Scale up/down stabilization windows

3. **Production Readiness**:
   - Health checks (liveness, readiness, startup probes)
   - Resource requests and limits
   - Pod disruption budgets
   - Network policies
   - Security contexts

## Getting Started

### Prerequisites
- Kubernetes cluster (minikube, kind, EKS, GKE, AKS)
- kubectl configured
- Helm (optional, for easier deployments)

### Deployment Steps

1. Create namespace:
   ```bash
   kubectl apply -f k8s/namespace.yaml
   ```

2. Apply ConfigMaps and Secrets:
   ```bash
   kubectl apply -f k8s/configmaps.yaml
   kubectl apply -f k8s/secrets.yaml
   ```

3. Deploy infrastructure:
   ```bash
   kubectl apply -f infra/redis/k8s/
   kubectl apply -f infra/rabbitmq/k8s/
   kubectl apply -f infra/postgres/k8s/
   ```

4. Deploy services:
   ```bash
   kubectl apply -f services/user_service/k8s/
   kubectl apply -f services/inventory_service/k8s/
   kubectl apply -f services/order_service/k8s/
   kubectl apply -f services/payment_service/k8s/
   ```

5. Deploy ingress:
   ```bash
   kubectl apply -f k8s/ingress.yaml
   ```

6. Verify deployment:
   ```bash
   kubectl get pods -n ecommerce
   kubectl get services -n ecommerce
   kubectl get hpa -n ecommerce
   ```

## Learning Objectives

- Kubernetes fundamentals (Pods, Deployments, Services)
- Configuration management (ConfigMaps, Secrets)
- Horizontal Pod Autoscaler (HPA)
- Vertical Pod Autoscaler (VPA) concepts
- Ingress controllers and rules
- Persistent volumes and claims
- StatefulSets for stateful applications
- Network policies
- RBAC (Role-Based Access Control)
- Helm package manager
- Kustomize for environment overlays
- Monitoring and logging in K8s
- Production best practices

## Kubernetes Commands Reference

```bash
# View resources
kubectl get pods -n ecommerce
kubectl get deployments -n ecommerce
kubectl get services -n ecommerce
kubectl get hpa -n ecommerce
kubectl get ingress -n ecommerce

# View detailed information
kubectl describe pod <pod-name> -n ecommerce
kubectl describe deployment <deployment-name> -n ecommerce

# View logs
kubectl logs -f <pod-name> -n ecommerce

# Scale manually
kubectl scale deployment user-service --replicas=3 -n ecommerce

# View HPA status
kubectl top pods -n ecommerce
kubectl top nodes

# Apply configurations
kubectl apply -f <file-or-directory>

# Delete resources
kubectl delete -f <file-or-directory>
```

## Sample HPA Configuration

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: user-service-hpa
  namespace: ecommerce
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: user-service
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 100
        periodSeconds: 60
```

## Production Considerations

- **Multi-zone deployment** for high availability
- **Pod Disruption Budgets** to prevent downtime during updates
- **Resource quotas** to prevent resource exhaustion
- **Network policies** for security isolation
- **Service mesh** (Istio/Linkerd) for advanced traffic management
- **CI/CD integration** for automated deployments
- **Backup strategies** for persistent data
- **Disaster recovery** planning

## Summary

You've completed all 7 phases of the E-Commerce system journey:

1. ✅ **Phase 1**: Monolithic application
2. ✅ **Phase 2**: Microservices architecture
3. ✅ **Phase 3**: Caching (Redis) & Message Queue (RabbitMQ)
4. ✅ **Phase 4**: API Gateway & Load Balancer (Nginx)
5. ✅ **Phase 5**: Monitoring (Prometheus & Grafana)
6. ✅ **Phase 6**: Containerization (Docker & Docker Compose)
7. ✅ **Phase 7**: Orchestration (Kubernetes & HPA)

Congratulations on building a production-ready microservices architecture!
