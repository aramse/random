# Kubernetes Resource Version Checker

## Summary
Kubernetes API resource versions can be deprecated with every release, however your Kubernetes cluster will not warn you when deploying a deprecated or alpha/beta resource.

This tool scans files for defined Kubernetes resources, compares the API version for each against the current/recommended version according to the Kubernetes API server (via `kubectl explain`), and reports on any differences.

### Prerequisites
- [yq](https://github.com/kislyuk/yq) (a yaml wrapper for `jq`) and [kubectl](https://kubernetes.io/docs/tasks/tools/) are installed
- `kubectl` is configured to point to the Kubernetes cluster you would like to query for recommended resource versions

## Usage
Use this tool by simply running the following command from this directory, optionally supplying a directory in which to scan for Kubernetes resource manifests (defaults to `resources`).

```sh
./check.sh [RESOURCES_DIR]
```

The output will be similar to the following:

```
 $ ./check.sh

Checking version support for resources defined in files in directory: resources

WARN: resources/CronJob.yaml: Found deprecated/non-current version batch/v1beta2 for resource CronJob --> current supported version is batch/v1beta1
WARN: resources/Deployment-api2.yaml: Found deprecated/non-current version extensions/v1beta1 for resource Deployment --> current supported version is apps/v1
INFO: resources/HorizontalPodAutoscaler-api2.yaml: Found deprecated/non-current version autoscaling/v2beta2 for resource HorizontalPodAutoscaler --> ignored due to exception in exceptions.yaml
WARN: resources/app.yaml: Found deprecated/non-current version extensions/v1beta1 for resource Deployment --> current supported version is apps/v1
INFO: resources/app.yaml: Found deprecated/non-current version autoscaling/v2beta2 for resource HorizontalPodAutoscaler --> ignored due to exception in exceptions.yaml

Finished resource version checking with 0 failures and 3 warnings
```

## Exceptions
Sometimes you want to use a newer API version for a given resource than what's recommended by the Kubernetes API server. To accommodate this, exceptions can be made in the `exceptions.yaml` file.
