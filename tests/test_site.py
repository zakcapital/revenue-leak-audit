import unittest
from pathlib import Path


class LandingPageTests(unittest.TestCase):
    def setUp(self):
        self.page = Path("index.html").read_text(encoding="utf-8")

    def test_page_states_offer_price_and_turnaround(self):
        self.assertIn("Website Revenue Leak Audit", self.page)
        self.assertIn("$49", self.page)
        self.assertIn("48 hours", self.page)

    def test_page_has_no_unsubstantiated_testimonials(self):
        lowered = self.page.lower()
        self.assertNotIn("testimonial", lowered)
        self.assertNotIn("trusted by", lowered)

    def test_page_includes_accessible_basics(self):
        self.assertIn('name="viewport"', self.page)
        self.assertIn("prefers-reduced-motion", self.page)
        self.assertIn("Skip to content", self.page)


if __name__ == "__main__":
    unittest.main()
