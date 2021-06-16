# GitOps automation for a SLATE instances

This repository provides a reference implementation of GitOps style automation for SLATE instances. This automation consists of:

-A small Python script, PushUpdates.py, responsible for reading changes and issuing requests to the SLATE API

-A GitHub Actions workflow for detecting changes and running the Python updater

The workflow looks for files that match `values.yaml` and `instance.yaml`. When a file associated with an instance is modified the workflow will update that instance. If a file is added, it will be deployed as a new instance.

## Setup

Place the Values file `values.yaml` into a directory that represents the instance. The directory can have any name, and can be nested. The values file must be called exactly `values.yaml`.

### instance.yaml

You must also have a file called `instance.yaml` that contains some details about the instance. For existing instances only the `instance` field is needed. Files at the repository root will be ignored.

Optionally you can specify and update the version of the SLATE application with the `version` field in `instance.yaml`. If `version` is unspecified the latest version is the default.

Example 

        cluster: uutah-prod
        group: slate-dev
        app: nginx
        instance: instance_BrX9HtpP1L0
        version: 1.2.0

## Git force pushes

Force pushes rewrite history in git, and can corrupt the state of your instances. Force pushing should be avoided.

## Other issues

If instance deletion is desired, it must currently be performed manually. 

The automation will writeback the instance ID for instances that get deployed, this should be refactored to happen on a branch.
