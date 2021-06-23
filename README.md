# GitOps automation for SLATE instances

This repository provides a reference implementation of GitOps style automation for SLATE instances. This automation consists of:

-A small Python script, PushUpdates.py, responsible for reading changes and issuing requests to the SLATE API

-A GitHub Actions workflow for detecting changes and running the Python updater

The workflow looks for files that match `values.yaml` and `instance.yaml`. When a file associated with an instance is modified the workflow will update that instance. If a file is added, it will be deployed as a new instance.

## Setup

Place the Values file `values.yaml` into a directory that represents the instance for each instance you want to manage. The directory can have any name, and can be nested. The values file must be called exactly `values.yaml`. Files at the repository root will be ignored. You will also need an `instance.yaml` for each instance.

Example:

        MY_INSTANCE/values.yaml
        MY_INSTANCE/instance.yaml
        

### SLATE Token

You will need to add your SLATE user token (obtained from portal.slateci.io/cli) as a repository secret on your GitHub repository. To do this:

1. Navigate to `Settings` on the top bar of the GitHub repository interface
2. Choose `Secrets` from the left-hand side bar menu
3. Click the button that says `New repository secret` upper right
4. Name the secret `SLATE_API_TOKEN`

### instance.yaml

For each instance, you must also have a file called `instance.yaml` that contains some details about the instance. For existing instances, only the `instance` field is needed to provide the ID. Info about the cluster, group, and app can be used to automatically deploy new instances too.

Optionally you can specify and update the version of the SLATE application with the `version` field in `instance.yaml`. If `version` is unspecified the latest version is the default.

**New Instances**

To deploy new instances you must include the cluster, group, and app. Version is optional.

        cluster: uutah-prod
        group: slate-dev
        app: nginx
        version: 1.2.0
        
 **Existing instances**
 
 To manage existing instances you only need to specify a SLATE instanceID.
 
        instance: instance_BrX9HtpP1L0
        
### Copy the workflow

Once everything is setup, copy `PushUpdates.py` and `.github/workflows/slate-deployment.yml` into your repository.

### Enable Actions in the GitHub UI

Once the workflow is added to the repository, you must allow it to run by navigating to the Actions tab in GitHub's interface.

## Git force pushes

Force pushes rewrite history in git, and can corrupt the state of your instances. Force pushing should be avoided.

## Other issues

If instance deletion is desired, it must currently be performed manually. 

The automation will writeback the instance ID for instances that get deployed, this should be refactored to happen on a branch.
