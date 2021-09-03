
import unittest
from wpaudit.core.conditions import pass_condition
from wpaudit.core.cli_parser import *
from wpaudit.core.console import prompt, prompt_overwrite, prompt_value

#
# Test methods for wpaudit/core
#
class TestScoutCore(unittest.TestCase):

    ########################################
    # cli_parser.py
    ########################################

    def test_argument_parser(self):
        test_arguments = wpauditArgumentParser()
        assert (test_arguments.parser._subparsers.title == 'The provider you want to run scout against')
        assert (test_arguments.subparsers._choices_actions[0].help == 'Run Scout against an Amazon Web Services account')
        assert (test_arguments.subparsers._choices_actions[1].help == 'Run Scout against a Google Cloud Platform account')
        assert (test_arguments.subparsers._choices_actions[2].help == 'Run Scout against a Microsoft Azure account')
        assert (test_arguments.subparsers._choices_actions[3].help == 'Run Scout against an Alibaba Cloud account')
        assert (test_arguments.subparsers._choices_actions[4].help == 'Run Scout against an Oracle Cloud Infrastructure account')

    ########################################
    # console.py
    ########################################

    def test_prompt(self):
        assert (prompt('test') == 'test')
        assert (prompt(['test']) == 'test')

    def test_prompt_overwrite(self):
        assert (prompt_overwrite('', True, None))

    def test_prompt_value(self):
        assert (prompt_value(question='', max_laps=1, test_input='test', is_question=True, choices=['test']) is None)
        assert (prompt_value(question='', max_laps=1, test_input='test', is_question=True, choices=['test'], no_confirm=True) == 'test')
