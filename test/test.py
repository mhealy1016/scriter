"""
A test suite script for assessing basic functionality and use cases.

Should be run after setup is complete and as the 'scriter' user.
"""

import os
import shutil
import unittest
import subprocess
import json
import logging
import argparse
import numpy as np
import pandas as pd
from sqlalchemy import create_engine

LOG_FORMAT = '%(asctime)s: %(filename)s [%(funcName)s]- %(message)s'
logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)
LOGGER = logging.getLogger()
TECH_LISTING = 'tech.json'
DB_USER = os.environ['DB_USER']
DB_PASS = os.environ['DB_PASS']
INGEST_DB_CONN_STR = 'postgresql://{0}:{1}@localhost/scriter_ingest'.format(DB_USER, DB_PASS)
MODEL_DB_CONN_STR = 'postgresql://{0}:{1}@localhost/scriter_web'.format(DB_USER, DB_PASS)


class TestWebScrape(unittest.TestCase):
    def test_run(self):
        """
        Basic Functional Test
        :return:
        """
        # Prior setup
        target_dir = '../web_scraper'

        # Execute and store any output
        cmd = "scrapy runspider web_scrape.py -o test_links.csv -s CLOSESPIDER_PAGECOUNT=50 -a job_title='software+engineer'  >> ../test/test_log.txt 2>&1"
        output = subprocess.check_output(cmd, cwd=target_dir, shell=True)

        # Assert results match expectations
        self.assertTrue(os.path.exists('../web_scraper/test_links.csv'))
        ## TODO: CLOSESPIDER_PAGECOUNT ~ Output Count

        # Cleanup
        os.remove('../web_scraper/test_links.csv')


class TestDataLoad(unittest.TestCase):
    def test_run(self):
        """
        Basic Functional Test
        :return:
        """
        # Prior setup
        target_dir = '../web_scraper'
        shutil.copy('test_links.csv', '../web_scraper')
        self.assertTrue(os.path.exists('../web_scraper/test_links.csv'))

        # Drop test table if it already exists
        tbl_drop_cmd = "psql -d scriter_ingest -c 'DROP TABLE IF EXISTS test_title'"
        output = subprocess.check_output(tbl_drop_cmd, cwd=target_dir, shell=True)

        # Execute and store any output
        cmd = "python data_load.py test_links.csv test_title >> ../test/test_log.txt 2>&1"
        output = subprocess.check_output(cmd, cwd=target_dir, shell=True)

        # Assert results match expectations
        ## TODO: Input Shape ~ Output Shape
        ## TODO: Duplicate Detection

        # Cleanup
        output = subprocess.check_output(tbl_drop_cmd, cwd=target_dir, shell=True)
        os.remove('../web_scraper/test_links.csv')


class TestModelBuild(unittest.TestCase):
    def test_run(self):
        """
        Basic Functional Test
        :return:
        """
        pass

    # def test_expected_metrics(self):
    #     """
    #     Sample Metrics ~ Expected Metrics
    #     :return:
    #     """
    #     pass


class TestWebServer(unittest.TestCase):
    def test_run(self):
        """
        Basic Functional Test
        :return:
        """
        pass

    # def test_ui(self):
    #     """
    #     Basic UI Functionality
    #     :return:
    #     """
    #     pass


if __name__ == '__main__':
    unittest.main()
