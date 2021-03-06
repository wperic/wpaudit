import subprocess
import unittest
from unittest import mock

import pytest
from wpaudit.__main__ import run_from_cli
from wpaudit.core.console import set_logger_configuration


class TestwpauditClass(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        set_logger_configuration(is_debug=True)
        cls.has_run_scout_suite = False

    @pytest.mark.xfail("only runs with AWS, cannot be used dynamically")
    @staticmethod
    def call_scout_suite(args):
        args = ['./scout.py'] + args

        args.append('aws')

        if TestwpauditClass.profile_name:
            args.append('--profile')
            args.append(TestwpauditClass.profile_name)
        # TODO: FIXME this only tests AWS

        args.append('--force')
        args.append('--debug')
        args.append('--no-browser')
        if TestwpauditClass.has_run_scout_suite:
            args.append('--local')
        TestwpauditClass.has_run_scout_suite = True

        sys = None
        with mock.patch.object(sys, 'argv', args):
            return run_from_cli()

    def test_scout_suite_help(self):
        """Make sure that wpaudit does not crash with --help"""
        command = './scout.py --help'
        process = subprocess.Popen(command, shell=True, stdout=None)
        process.wait()
        assert process.returncode == 0

    @pytest.mark.xfail
    def test_scout_suite_default_run(self):
        """Make sure that wpaudit's default run does not crash"""
        rc = self.call_scout_suite([])
        assert (rc == 0)
