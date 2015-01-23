from queue import Queue
import sys

sys.path.insert(0, ".")
import unittest
from coalib.results.LineResult import LineResult
from coalib.settings.Setting import Setting
from bears.tests.LocalBearTestHelper import LocalBearTestHelper
from bears.spacing.SpaceConsistencyBear import SpaceConsistencyBear, SpacingHelper
from coalib.settings.Section import Section
from coalib.misc.i18n import _


class SpaceConsistencyBearTest(LocalBearTestHelper):
    def setUp(self):
        self.section = Section("test section")
        self.section.append(Setting("use_spaces", "true"))
        self.uut = SpaceConsistencyBear(self.section, Queue())

    def test_needed_settings(self):
        needed_settings = self.uut.get_non_optional_settings()
        self.assertEqual(len(needed_settings), 1 + len(SpacingHelper.get_non_optional_settings()))
        self.assertIn("use_spaces", needed_settings)

    def test_data_sets_spaces(self):
        self.assertLineValid(self.uut, "    t")

        self.assertLineYieldsResult(self.uut,
                                    "t \n",
                                    LineResult("SpaceConsistencyBear",
                                               1,
                                               "t \n",
                                               _("Line has trailing whitespace characters"),
                                               "file"),
                                    "file")

        self.assertLineYieldsResult(self.uut,
                                    "\tt\n",
                                    LineResult("SpaceConsistencyBear",
                                               1,
                                               "\tt\n",
                                               _("Line contains one or more tabs"),
                                               "file"),
                                    "file")

    def test_data_sets_tabs(self):
        self.section = Section("test section")
        self.section.append(Setting("use_spaces", "false"))
        self.section.append(Setting("allow_trailing_whitespace", "true"))
        self.uut = SpaceConsistencyBear(self.section, Queue())

        self.assertLineYieldsResult(self.uut,
                                    "    t",
                                    LineResult("SpaceConsistencyBear",
                                               1,
                                               "    t\n",
                                               _("Line contains with tab replaceable spaces"),
                                               "file"),
                                    "file")

        self.assertLineValid(self.uut, "t \n")

        self.assertLineValid(self.uut, "\tt\n")


if __name__ == '__main__':
    unittest.main(verbosity=2)
