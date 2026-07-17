import unittest
from pathlib import Path


class StripeReadinessTests(unittest.TestCase):
    def test_success_page_collects_intake_without_treating_redirect_as_payment_proof(self):
        page = Path("success.html").read_text(encoding="utf-8")
        self.assertIn("cole@byquill.co", page)
        self.assertIn("payment confirmation", page.lower())
        self.assertIn("Website URL", page)

    def test_customer_policy_pages_cover_service_and_privacy_basics(self):
        terms = Path("terms.html").read_text(encoding="utf-8")
        privacy = Path("privacy.html").read_text(encoding="utf-8")
        self.assertIn("48 hours", terms)
        self.assertIn("Refund", terms)
        self.assertIn("Stripe", privacy)
        self.assertIn("card details", privacy)

    def test_landing_page_links_customer_policies(self):
        page = Path("index.html").read_text(encoding="utf-8")
        self.assertIn('href="terms.html"', page)
        self.assertIn('href="privacy.html"', page)

    def test_landing_page_uses_live_checkout_and_retains_support_contact(self):
        page = Path("index.html").read_text(encoding="utf-8")
        self.assertIn("https://buy.stripe.com/28E9AV6EU0Ckd6t0CS24000", page)
        self.assertIn('href="mailto:cole@byquill.co"', page)


if __name__ == "__main__":
    unittest.main()
