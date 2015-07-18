from unittest import TestCase

from foodsite.core.util import prettyprint as pp
from decimal import Decimal


class TestPhoto(TestCase):
    """
    Util functions
    """

    def test_prettyprint(self):
        """
        see if the convertion to nicer units is working
        """
        self.assertEqual(pp(Decimal("1.5")), "1 + 1/2")
        self.assertEqual(pp(Decimal("2.4")), "2 + 2/5")
        self.assertEqual(pp(Decimal("2.2")), "2 + 1/5")
        self.assertEqual(pp(Decimal("2.25")), "2 + 1/4")
        self.assertEqual(pp(Decimal("1")), "1")
        self.assertEqual(pp(Decimal("1.01")), "1")
        # the limit for my conversion is 1/5 anything less than that is round up
        self.assertEqual(pp(Decimal("1.1")), "1")
        self.assertEqual(pp(Decimal("1.001")), "1")
        self.assertEqual(pp(Decimal("0.2")), "1/5")
