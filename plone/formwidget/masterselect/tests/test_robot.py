# -*- coding: utf-8 -*-
from plone.testing import layered
from plone.formwidget.masterselect.testing import \
    PLONE_FORMWIDGET_MASTERSELECT_ROBOT

import os
import robotsuite
import unittest


def test_suite():
    suite = unittest.TestSuite()
    current_dir = os.path.abspath(os.path.dirname(__file__))

    robot_dir = os.path.join(current_dir, 'robot')
    robot_tests = [
        os.path.join('robot', doc) for doc in os.listdir(robot_dir)
        if doc.endswith('.robot') and doc.startswith('test_')
    ]

    for test in robot_tests:
        suite.addTests([
            layered(
                robotsuite.RobotTestSuite(test),
                layer=PLONE_FORMWIDGET_MASTERSELECT_ROBOT),
        ])
    return suite
