# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 17:20:47 2022

@author: artim
"""

import os
import pandas as pd
from pybatfish.client.commands import *
from pybatfish.question import load_questions
from pybatfish.question import bfq
from pybatfish.client.asserts import (
    assert_no_duplicate_router_ids,
    assert_no_incompatible_bgp_sessions,
    assert_no_incompatible_ospf_sessions,
    assert_no_unestablished_bgp_sessions,
    assert_no_undefined_references,
    assert_num_results,
    assert_zero_results,
)


# Get environment variables
BATFISH_SERVER = os.getenv('BATFISH_SERVER')


# from rich import print as rprint

pd.set_option('display.max_columns', None)
pd.set_option('expand_frame_repr', False)


# Snap info
num = 5
routers = ['r11', 'r12', 'r21', 'r22', 'r23']
domain_name = "inwk.local"


def test_num_routers():
    """Testing for number of devices"""
    file_status = bfq.fileParseStatus().answer().frame()
    assert_num_results(file_status, num, soft=True)


def test_init_issues():
    """Testing for parsing violations"""
    inissue = bfq.initIssues().answer().frame()
    assert_zero_results(inissue, soft=True)


def test_clean_parsing():
    """Testing for parsing violations"""
    file_status = bfq.fileParseStatus().answer().frame()
    status_violations = file_status[file_status["Status"] != "PASSED"]
    assert_zero_results(status_violations, soft=True)


def test_hostnames():
    """Testing correct hostnames"""
    node_props = bfq.nodeProperties(
        nodes="", properties="Hostname, Domain_Name").answer().frame()
    name_violators = node_props[node_props['Hostname'].apply(
        lambda x: x not in routers)]
    assert_zero_results(name_violators, soft=True)

    domain_violators = node_props[node_props['Domain_Name'].apply(
        lambda x: x != domain_name)]
    assert_zero_results(domain_violators, soft=True)


def test_undefined_references(snap):
    assert_no_undefined_references(snapshot=snap, soft=True)


def test_duplicate_rtr_ids(snap):
    """Testing for duplicate router IDs"""
    assert_no_duplicate_router_ids(
        snapshot=snap,
        protocols={"ospf", "bgp"},
        soft=True
    )


def main():
    """init all the things"""
    NETWORK_NAME = "DESIGN_LAB1"
    SNAPSHOT_NAME = "lab1"
    SNAPSHOT_DIR = "lab1"
    bf_session.host = BATFISH_SERVER
    bf_set_network(NETWORK_NAME)
    init_snap = bf_init_snapshot(
        SNAPSHOT_DIR, name=SNAPSHOT_NAME, overwrite=True)
    load_questions()

    test_num_routers()
    test_init_issues()
    test_clean_parsing()
    test_hostnames()
    test_undefined_references(init_snap)
    # test_duplicate_rtr_ids(init_snap)
    # test_bgp_compatibility(init_snap)
    # test_ospf_compatibility(init_snap)
    # test_bgp_unestablished(init_snap)
    # test_undefined_references(init_snap)


if __name__ == "__main__":
    main()
