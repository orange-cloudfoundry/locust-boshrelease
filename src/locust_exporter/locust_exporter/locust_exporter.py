#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Requires prometheus_client library:
# sudo pip install prometheus_client
import json
import sys
from http.server import HTTPServer
from urllib.parse import urlparse

import requests
from prometheus_client import Metric, REGISTRY, MetricsHandler


class LocustCollector(object):
    def __init__(self, ep, host):
        self._ep = ep
        if host is None:
            self._host = 'none'
        else:
            self._host = host

    def collect(self):
        # Fetch the JSON
        url = self._ep + '/stats/requests'
        parsed_url = urlparse(self._ep)
        auth_value = None
        if parsed_url.username is not None:
            auth_value = (parsed_url.username, parsed_url.password)
        try:
            response = requests.request("GET", url, auth=auth_value, verify=False).content.decode('Utf-8')
        except requests.exceptions.ConnectionError:
            print("Failed to connect to Locust:", url)
            exit(2)

        response = json.loads(response)

        stats_metrics = ['avg_content_length', 'avg_response_time', 'current_rps', 'max_response_time',
                         'median_response_time', 'min_response_time', 'num_failures', 'num_requests']

        metric = Metric('locust_user_count', 'Swarmed users', 'gauge')
        metric.add_sample('locust_user_count', value=response['user_count'], labels={})
        yield metric

        metric = Metric('locust_errors', 'Locust requests errors', 'gauge')
        for err in response['errors']:
            metric.add_sample('locust_errors', value=err['occurences'],
                              labels={'host': self._host, 'path': err['name'], 'method': err['method']})
        yield metric

        if 'slave_count' in response:
            metric = Metric('locust_slave_count', 'Locust number of slaves', 'gauge')
            metric.add_sample('locust_slave_count', value=len(response['slaves']), labels={})
            yield metric

        metric = Metric('locust_fail_ratio', 'Locust failure ratio', 'gauge')
        metric.add_sample('locust_fail_ratio', value=response['fail_ratio'], labels={})
        yield metric

        metric = Metric('locust_state', 'State of the locust swarm', 'gauge')
        metric.add_sample('locust_state', value=1, labels={'state': response['state']})
        yield metric

        for mtr in stats_metrics:
            mtype = 'gauge'
            if mtr in ['num_requests', 'num_failures']:
                mtype = 'counter'
            metric = Metric('locust_requests_' + mtr, 'Locust requests ' + mtr, mtype)
            for stat in response['stats']:
                if not 'Total' in stat['name']:
                    metric.add_sample('locust_requests_' + mtr, value=stat[mtr],
                                      labels={'host': self._host, 'path': stat['name'], 'method': stat['method']})
            yield metric


def main():
    # Usage: locust_exporter.py <port> <locust_host:port>
    if len(sys.argv) < 3:
        print('Usage: locust_exporter.py <port> <locust_url> <target-host>')
        exit(1)
    else:
        try:
            host = None
            if len(sys.argv) == 4:
                host = str(sys.argv[3])
            REGISTRY.register(LocustCollector(str(sys.argv[2]), host))
            CustomMetricsHandler = MetricsHandler.factory(REGISTRY)
            server = HTTPServer(('', int(sys.argv[1])), CustomMetricsHandler)
            print("Connecting to locust on: " + sys.argv[2])
            server.serve_forever()
        except KeyboardInterrupt:
            exit(0)
