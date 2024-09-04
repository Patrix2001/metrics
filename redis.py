# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import os
import sys
from typing import List
from datetime import datetime, timedelta, timezone
import json

from alibabacloud_r_kvstore20150101.client import Client as R_kvstore20150101Client
from alibabacloud_r_kvstore20150101 import models as r_kvstore_20150101_models
from alibabacloud_cms20190101.client import Client as Cms20190101Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_cms20190101 import models as cms_20190101_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_console.client import Client as ConsoleClient
from alibabacloud_tea_util.client import Client as UtilClient

from metrics import REDIS_STANDARD, REDIS_CLUSTER, REDIS_RW
from regions import REGIONS_OUT_CHINA

access_key=''
secret_key=''

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
    def create_client(region_id) -> R_kvstore20150101Client:
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
        # See https://api.alibabacloud.com/product/R-kvstore.
        config.endpoint = f'r-kvstore.{region_id}.aliyuncs.com'
        return R_kvstore20150101Client(config)

    @staticmethod
    def main(
        args: List[str],
        region_id
    ) -> None:
        client = ListInstances.create_client(region_id)
        describe_instances_request = r_kvstore_20150101_models.DescribeInstancesRequest(
            region_id=region_id
        )
        runtime = util_models.RuntimeOptions()
        try:
            # Copy the code to run, please print the return value of the API by yourself.
            resp = client.describe_instances_with_options(describe_instances_request, runtime)
            instances_id = [i.instance_id for i in resp.body.instances.kvstore_instance]
            architecture_type = [i.architecture_type for i in resp.body.instances.kvstore_instance]
            
            return (instances_id, architecture_type)
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
    def create_client(region_id) -> Cms20190101Client:
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
        region_id,
        present,
        past,
        instanceid,
        metric_name,
        namespace
    ) -> None:
        client = Monitoring.create_client(region_id)
        describe_metric_list_request = cms_20190101_models.DescribeMetricListRequest(
            namespace=namespace,
            metric_name=metric_name,
            dimensions=f'[{{"instanceId":"{instanceid}"}}]',
            start_time= past.strftime("%Y-%m-%d %H:%M:%SZ"),
            end_time= present.strftime("%Y-%m-%d %H:%M:%SZ"),
            period='2592000',
            region_id=region_id
        )
        runtime = util_models.RuntimeOptions()
        try:
            resp = client.describe_metric_list_with_options(describe_metric_list_request, runtime)

            if len(convert_str_dict(resp.body.datapoints)) == 0:
                return ['', '']
            lst_average = [monitor['Average'] for monitor in convert_str_dict(resp.body.datapoints)]
            lst_minimum = [monitor.get('Minimum', '') for monitor in convert_str_dict(resp.body.datapoints)]
            lst_maximum = [monitor.get('Maximum', '') for monitor in convert_str_dict(resp.body.datapoints)]
            
            return [average(lst_average), maximum(lst_maximum)]
        except Exception as error:
            print(error.message)
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)

if __name__ == '__main__':
    present = datetime.now(tz=timezone.utc).replace(microsecond=0)
    past = present.replace(day=1) - timedelta(1)

    lst_instances = []
    lst_archictectures = []
    for region_id in REGIONS_OUT_CHINA:
        data = ListInstances.main(sys.argv[1:], region_id)
        lst_instances.append(data[0])
        lst_archictectures.append(data[1])

    with open("redis.csv", "w") as resource_file:
        resource_file.write("instanceId,Region,Archictectures,CPU Utilization (AVG),CPU Utilization (MAX),Memory Utilization(AVG),Memory Utilization(MAX),IOPS AVG,IOPS MAX,Disk AVG ,Disk MAX\n")
        for region, instances, archictectures in zip(REGIONS_OUT_CHINA, lst_instances, lst_archictectures):
            if instances and archictectures:
                for index in range(len(instances)):
                    data = []  
                    if archictectures[index] == "standard":
                        metric_collection = REDIS_STANDARD
                    elif archictectures[index] == "rwsplit":
                        metric_collection = REDIS_RW
                    else:
                        metric_collection = REDIS_CLUSTER
                    for metric in metric_collection:
                        data.append(Monitoring.main(sys.argv[1:], region, present, past, instances[index], metric.metricName, metric.namespace))
                    resource_file.write(f"{instances[index]},{region},{archictectures[index]},{data[0][0]},{data[0][1]},{data[1][0]},{data[1][1]},{data[2][0]},{data[2][1]},{data[3][0]},{data[3][1]}\n")
            else:
                print(f"{region} No Deployed Instances")
                
