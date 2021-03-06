# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
import requests
import unittest
import boto3
from botocore.exceptions import ClientError
from EmailBot import EmailBot
# some version issue
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch


class TestEmailBot(unittest.TestCase):
  """
  Unittest of EmailBot.py, coverage:91%
  """

    def setUp(self):
        self.eb = EmailBot(img_file="./test_img.png",
                           elastic_beanstalk_url = "http://fakedocker.us-west-2.elasticbeanstalk.com",
                           repo = "apache/incubator-mxnet",
                           sender = "a@email.com",
                           recipients = "a@gmail.com",
                           aws_region = "us-east-1")

    def test_read_repo(self):
        with patch('EmailBot.requests.get') as mocked_get:
            mocked_get.return_value.status_code = 200
            mocked_get.return_value.json.return_value = [{"body": "issue's body",
                                                          "created_at": "2018-08-04T18:27:17Z",
                                                          "comments": "0",
                                                          "number": 11925,
                                                          "labels": [{'name': 'Doc'}],
                                                          "state": "open",
                                                          "title": "issue's title",
                                                          "html_url": "https://github.com/apache/incubator-mxnet/issues/11925",
                                                          },
                                                         {"body": "issue's body",
                                                          "created_at": "2018-08-04T18:27:17Z",
                                                          "comments": "0",
                                                          "number": 11924,
                                                          "labels": [],
                                                          "state": "closed",
                                                          "title": "issue's title",
                                                          "html_url":"https://github.com/apache/incubator-mxnet/issues/11925",
                                                          }]
            self.eb.read_repo(True)

    def test_sendemail(self):
        with patch('EmailBot.requests.get') as mocked_get, patch('EmailBot.requests.post') as mocked_post:
            mocked_get.return_value.status_code = 200
            mocked_get.return_value.json.return_value = [{"body": "issue's body",
                                                          "created_at": "2018-08-04T18:27:17Z",
                                                          "comments": 0,
                                                          "number": 11925,
                                                          "labels": [{'name': 'Doc'}],
                                                          "state": "open",
                                                          "title": "issue's title",
                                                          "html_url": "https://github.com/apache/incubator-mxnet/issues/11925",
                                                          },
                                                         {"body": "issue's body",
                                                          "created_at": "2018-08-04T18:27:17Z",
                                                          "comments": 1,
                                                          "comments_url": "https://api.github.com/repos/apache/incubator-mxnet/issues/11918/comments",
                                                          "number": 11918,
                                                          "labels": [],
                                                          "state":"open",
                                                          "title":"issue's title",
                                                          "html_url":"https://github.com/apache/incubator-mxnet/issues/11918",
                                                          }]
            mocked_post.return_value.json.return_value = [{'number': 11919, 'predictions': ['Performance']}, 
                                                          {'number': 11924, 'predictions': ['Build']}]                                             
            self.assertRaises(ClientError, self.eb.sendemail())


if __name__ == "__main__":
    unittest.main()
