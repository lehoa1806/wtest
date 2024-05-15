from functools import cached_property
from typing import Any, Dict

import s3fs
import yaml

from configs.setting import Setting
from utils.singleton import Singleton


class TestData(metaclass=Singleton):
    S3LOCATION = Setting().s3_location

    @classmethod
    def read_data_from_s3_yaml(cls, s3path: str) -> Any:
        fs = s3fs.S3FileSystem(client_kwargs={'region_name': 'us-west-2'},
                               endpoint_url=Setting().s3_endpoint_url,
                               key=Setting().s3_access_key,
                               secret=Setting().s3_secret_key)
        with fs.open(s3path, 'rb') as f:
            return yaml.safe_load(f)

    @cached_property
    def users(self) -> Dict:
        return self.read_data_from_s3_yaml(f'{self.S3LOCATION}/test_users.yaml')
