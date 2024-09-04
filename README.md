# Alibaba Cloud Monitoring and Export Tool

This project provides a Python script for fetching instance monitoring data from Alibaba Cloud (AliCloud) and exporting it to a CSV file. This tool can help you better understand and manage the performance.

Scope of service:
* ECS, 
* RDS,
* Redis

Some of the metrics collected include: 
* CPU utilization, 
* memory utilization,
* disk I/O utilization

## Introduction

This tool collects the basic information and monitoring metrics (such as CPU utilization, memory utilization, etc.) of all ECS instances in a specified region by calling Alibaba Cloud API, and outputs the data into a file named `<service>.csv` after organizing it.

## Installation

Since this project depends on the Alibaba Cloud SDK, you need to install the relevant libraries first:

```bash
pip install -r requirements.txt
```

Make sure that the ACCESS_KEY and SECRET_KEY environment variables are set in your ``cred.py``.

## Usage

Before running this script, make sure that the access key ID and secret are correctly configured. You can either edit the ``cred.py`` file directly or set the environment variables.

### Run the script

```bash
python ecs.py
```

This will iterate through all instances defined in the loop call of region (Outside of China) and collect their monitoring data.

## Function Description

Below is an overview of the main functional modules and the interfaces they provide:

| Property | Type | Description | Required | Default Value |
| --- | --- | --- | --- | --- |
| `create_client` | Method | Creates a client object for subsequent requests | Yes | N/A |
| `describe_instances_request` | Object | Constructs parameters for querying instance lists | No | Region ID as required parameter |
| `describe_metric_list_request` | Object | Builds parameters for querying monitoring data | No | Includes necessary parameters such as Instance ID, time range, etc. |

## Sample Usage

Executing the following command will start the script and begin collecting data:
```bash
python ecs.py
```
Upon completion, a file named `ecs.csv` will be generated in the current directory containing detailed monitoring information for each instance.

Please note that when deploying in practice, security issues should be considered to avoid storing sensitive information like Access Key ID and Secret Key in plain text. It's recommended to handle authentication information in a more secure manner. For Example, you can set policy to limit, `ReadOnlyAccess` to the Access Key ID and Secret Key.