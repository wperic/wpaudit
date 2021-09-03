import unittest
from wpaudit.output.html import *
from wpaudit.output.utils import *

#
# Test methods for wpaudit/output
#
class TestScoutOutput(unittest.TestCase):

    ########################################
    # html.py
    ########################################

    def test_html_report(self):
        test_html = HTMLReport(report_name='test')
        assert (test_html.report_name == 'test')
        assert ('json' in test_html.get_content_from_folder(templates_type='conditionals'))
        assert ('json' in test_html.get_content_from_file(filename='/json_format.html'))

    def test_get_filename(self):
        assert ('wpaudit-report/report.html' in get_filename("REPORT"))
        assert ('wpaudit-report/wpaudit-results/wpaudit_results.js' in get_filename("RESULTS"))
        assert ('wpaudit-results/wpaudit_results.js' in get_filename("RESULTS", relative_path=True))
        assert ('wpaudit-report/wpaudit-results/wpaudit_exceptions.js' in get_filename("EXCEPTIONS"))
        assert ('wpaudit-results/wpaudit_exceptions.js' in get_filename("EXCEPTIONS", relative_path=True))
        assert ('wpaudit-report/wpaudit-results/wpaudit_errors.json' in get_filename("ERRORS"))
        assert ('wpaudit-results/wpaudit_errors.json' in get_filename("ERRORS", relative_path=True))
