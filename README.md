# lion-parcel-assesment
## Description
This project contain 2 pipelines, pipeline_task and pipeline bonus as solution for problem given at this link https://docs.google.com/document/d/1JYjrKxhkYDNUd6X_VVv4rbS5m0CCyYk5-ijQNaHvUec/edit?tab=t.0

The general process of the pipelines are init databases >> process data >> data warehouse
### Tech Stack
- MySQL
- Clickhouse
- Dagster

## How To Run
1. Clone project using `git clone https://github.com/technisekai/lion-parcel-assesment.git`
2. Change to root directory `cd lion-parcel-assesment`
3. Run command `docker-compose up --build`
4. Visit `localhost:3000` in web browser you will see dagster UI, click `Jobs` tab then click `Launchpad` then click `Launch Run` button at the corne right bottom or you can activate the scheduler with toggle on pipelines in `Jobs` tab 