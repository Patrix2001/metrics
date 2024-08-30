# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import os
import sys

from typing import List
from datetime import datetime, timedelta, timezone
import json

from alibabacloud_ecs20140526.client import Client as Ecs20140526Client
from alibabacloud_ecs20140526 import models as ecs_20140526_models
from alibabacloud_cms20190101.client import Client as Cms20190101Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_cms20190101 import models as cms_20190101_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_console.client import Client as ConsoleClient
from alibabacloud_tea_util.client import Client as UtilClient

access_key=''
secret_key=''
region_id='ap-southeast-1'

def export_csv(lst_instances, metric_collection):
    with open("ecs.csv", "w") as resource_file:
        resource_file.write("instanceId,CPU Utilization (AVG),CPU Utilization (MAX),Memory Utilization(AVG),Memory Utilization(MAX),IOPS AVG (read Times/s),IOPS MAX (read Times/s),IOPS AVG (write Times/s),IOPS MAX (write Times/s)\n")
        for instance in lst_instances:
            data = []
            for metric in metric_collection:
                data.append(Monitoring.main(sys.argv[1:], present, past, instance, metric["metricName"], metric["namespace"]))
            resource_file.write(f"{instance},{data[0][0]},{data[0][1]},{data[1][0]},{data[1][1]},{data[2][0]},{data[2][1]},{data[3][0]},{data[3][1]}\n")

def convert_str_dict(data):
    return json.loads(data)

def average(data):
    return sum(data) / len(data)

def minimum(data):
    return min(data)

def maximum(data):
    return max(data)


class ListInstances:
    def __init__(self):
        pass

    @staticmethod
    def create_client() -> Ecs20140526Client:
        """
        Initialize the Client with the AccessKey of the account
        @return: Client
        @throws Exception
        """
        # The project code leakage may result in the leakage of AccessKey, posing a threat to the security of all resources under the account. The following code examples are for reference only.
        # It is recommended to use the more secure STS credential. For more credentials, please refer to: https://www.alibabacloud.com/help/en/alibaba-cloud-sdk-262060/latest/configure-credentials-378659.
        config = open_api_models.Config(
            # Required, please ensure that the environment variables ALIBABA_CLOUD_ACCESS_KEY_ID is set.,
            access_key_id=access_key,
            # Required, please ensure that the environment variables ALIBABA_CLOUD_ACCESS_KEY_SECRET is set.,
            access_key_secret=secret_key
        )
        # See https://api.alibabacloud.com/product/Ecs.
        config.endpoint = f'ecs.{region_id}.aliyuncs.com'
        return Ecs20140526Client(config)

    @staticmethod
    def main(
        args: List[str],
    ) -> None:
        client = ListInstances.create_client()
        describe_instances_request = ecs_20140526_models.DescribeInstancesRequest(
            region_id=region_id
        )
        runtime = util_models.RuntimeOptions()
        try:
            resp = client.describe_instances_with_options(describe_instances_request, runtime)
            instances_id = [i.instance_id for i in resp.body.instances.instance]
            return instances_id
        
        except Exception as error:
            # Only a printing example. Please be careful about exception handling and do not ignore exceptions directly in engineering projects.
            # print error message
            print(error.message)
            # Please click on the link below for diagnosis.
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)


class Monitoring:
    def __init__(self):
        pass

    @staticmethod
    def create_client() -> Cms20190101Client:
        """
        Initialize the Client with the AccessKey of the account
        @return: Client
        @throws Exception
        """
        # The project code leakage may result in the leakage of AccessKey, posing a threat to the security of all resources under the account. The following code examples are for reference only.
        # It is recommended to use the more secure STS credential. For more credentials, please refer to: https://help.aliyun.com/document_detail/378659.html.
        config = open_api_models.Config(
            # Required, please ensure that the environment variables ALIBABA_CLOUD_ACCESS_KEY_ID is set.,
            access_key_id=access_key,
            # Required, please ensure that the environment variables ALIBABA_CLOUD_ACCESS_KEY_SECRET is set.,
            access_key_secret=secret_key
        )
        # See https://api.alibabacloud.com/product/Cms.
        config.endpoint = f'metrics.{region_id}.aliyuncs.com'
        return Cms20190101Client(config)

    @staticmethod
    def main(
        args: List[str],
        present,
        past,
        instanceid,
        metric_name,
        namespace
    ) -> None:
        client = Monitoring.create_client()
        describe_metric_list_request = cms_20190101_models.DescribeMetricListRequest(
            namespace=namespace,
            metric_name=metric_name,
            dimensions=f'[{{"instanceId":"{instanceid}"}}]',
            start_time= past.strftime("%Y-%m-%d %H:%M:%SZ"),
            end_time= present.strftime("%Y-%m-%d %H:%M:%SZ"),
            period='2592000'
        )
        runtime = util_models.RuntimeOptions()
        try:
            resp = client.describe_metric_list_with_options(describe_metric_list_request, runtime)

            lst_average = [monitor['Average'] for monitor in convert_str_dict(resp.body.datapoints)]
            lst_minimum = [monitor['Minimum'] for monitor in convert_str_dict(resp.body.datapoints)]
            lst_maximum = [monitor['Maximum'] for monitor in convert_str_dict(resp.body.datapoints)]
            
            return [average(lst_average), maximum(lst_maximum)]
        except Exception as error:
            print(error.message)
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)


if __name__ == '__main__':
    present = datetime.now(tz=timezone.utc).replace(microsecond=0)
    past = present.replace(day=1) - timedelta(1)
    metric_collection = [
        {"metricName": "CPUUtilization", "namespace": "acs_ecs_dashboard"},
        {"metricName": "memory_usedutilization", "namespace": "acs_ecs_dashboard"},
        {"metricName": "DiskReadIOPS", "namespace": "acs_ecs_dashboard"},
        {"metricName": "DiskWriteIOPS", "namespace": "acs_ecs_dashboard"},
    ]
    lst_instances = ListInstances.main(sys.argv[1:])

    export_csv(lst_instances, metric_collection)
