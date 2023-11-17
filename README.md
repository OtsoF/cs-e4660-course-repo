# cs-e4660 Course repo

## Dir Structure

Most of the project and course tasks are contained in folders, which contain their own documentation:

- `./data` The dataset used in the project
- `./data-fetch` Project mock data fetcher
- `./database` Config for database used in project
- `./model-api` Project model api serving predictions
- `./model-training` Project model training
- `./preprocessing` Project mock preprocessing
- `./project-plan` The inital project plan 
- `./study-logs` Study logs written during the course

## Project: Green e2e ML
Seen initial project plan in [project-plan](./project-plan/) folder

### Background

- At work we have an ML pipeline, which currently has no proper orchestration & no workflow engine used
- The pipeline is quite simple, however, there are more similar simple pipelines coming in the future
- Engineering challenge: how to support and maintain ML pipelines on existing (shared) infra with quite small DevOps team

#### Existing pipeline

- Financial management SaaS product
- Invoice field predictions (VAT %, amount, receiver, etc...) using Randomforest classifier
- Similar pipelines expected in the future to help predict financial management & accounting related
- ML pipelines run on a (shared) Kubernetes cluster (AKS)


![(image missing)](./project-plan/finago-pipeline.drawio.png)

### The mock env and story

The 

### Challenges to be solved

This project attempts to solve two main challenges:

1. Best solution for DevOps engineers to create and maintain ML pipelines on a shared (Azure) Kubernetes cluster
2. How to make the pipelines green (and by proxy cheap and efficient)

### Solution 1: Proper ochrestration and e2e workflow using workflow engine

#### Pipeline Ochestration tools Comparison

Here is a comparisons table based on the different requirements of the system described above.

|                                                | Argo Workflows | Kubeflow | Apache airflow |
|------------------------------------------------|----------------|----------|----------------|
| Kubernetes support                             |       yes      |     yes  | technically yes, could not get working |
| CasC                                           |       yaml (kubernetes)         |    pipeline sdk (python)/proprietary dsl      |      python sdk (not tested)          |
| Learning curve for DevOps <br> (personal estimate) |    medium(*)   |    high(**)      |       n/a     |
| Schduling                                      |        yes     |          |                |
| Event triggering                               |        yes     |          |                |
| Logging                                        |      kuberntes logs (native kubernetes jobs)       |          |                |
| Alerting                                       |      integrations to slack and opsgenie          |          |                |
| Good UI (usable by ML engineers)               |                |          |                |


(*) kubernetes like yaml syntax to configure worflows 

(**) Uses argo workflow under the hood, but confiured in python. This might be the best solution for ML engingeers, but since in this case the pipeline needs to be maintained by DevOps engineers it's not ideal


#### Mock pipeline parts

Based on the comparison Argo Workflows as chosen as the pipeline orchestration tool / workflow engine. This means the different pipline steps are contanerized, more info on these in their own folders (in order):

- `./data-fetch` Project mock data fetcher-
- `./preprosessing` Project mock preprosessing
- `./model-training` Project model training
- `./model-api` Project model api serving predictions

#### Argo workflows and the pipeline

The Argo workflow configuration and pipeline configuration will be #FIXME(are) in the `./pipeline` folder


#TODO:
- See how the pipeline solution supports and enables R3E + Monitoring, Observability & Experimenting
  - what restrictions come from existing ML pipeline, what restrictions (potentially) come from workflow pipeline solution being implemented
  - what areas of R3E + Monitoring, Observability & Experimenting can't be solved by orchestration & workflow engine (just figure out, supporting these out of scope)

### Solution 2: Making the pipeline green

#### Pipeline scheduling

Scheduling can help make the pipeline green in two ways: 
- scheduling frequency
  - the real pipeline is currently run nigthly, but by assesing model perfomance on incoming training data (or potentially by getting feedback on predictions) we can make determinations on when to re-train the model(s)
- scheduling timing
  - the *carbon intensity* of the electric grid changes based on certain factors (see [Planning document](./project-plan/plan.md) for more details)
  - the mock pipeline is run in a local kuberntes cluster, but we can pretend it's running in a specific Azure datacenter and use APIs to see when the datacenter has low carbon intensity

This table shows the plan to combine both scheduling factors into one solution:

| Accuracy of model on new training data | Action  |
|----------------------------------------|---------|
| Small decrease compared to inital training accuracy (to be quantified) | Retrain model once carbon intensity drops below set threshold |
| Big decrease ...                                                       | Retrain model immediately |

#### Metrics collection

#Fixme placehoder just copied from planning doc:

![(image missing)](./project-plan/sci.png)
*Green software foundation*

- See which parts of the pipeline contribute most to co2 emissions
- See trends over time, sudden increases etc.
- SCI: https://learn.greensoftware.foundation/measurement/#the-sci-equation


## (sort out)

- scaling
- what can be scaled
- customers vs 

https://www.kaggle.com/code/prashant111/random-forest-classifier-tutorial/notebook

https://archive.ics.uci.edu/dataset/19/car+evaluation