import unittest

from audit import analyze_html, score_findings


GOOD_HTML = """<!doctype html>
<html lang="en"><head>
<title>Clear Plumbing | Emergency Service</title>
<meta name="description" content="Fast local plumbing service.">
<meta name="viewport" content="width=device-width, initial-scale=1">
</head><body>
<h1>Emergency plumbing without the wait</h1>
<a href="tel:+15551234567">Call now</a>
<form><label for="email">Email</label><input id="email" name="email"></form>
<img src="team.jpg" alt="Clear Plumbing service team">
</body></html>"""


class AuditTests(unittest.TestCase):
    def test_good_page_has_no_critical_findings(self):
        findings = analyze_html(GOOD_HTML, "https://example.com")
        critical = [item for item in findings if item["severity"] == "critical"]
        self.assertEqual(critical, [])

    def test_missing_conversion_and_search_elements_are_detected(self):
        findings = analyze_html("<html><body><img src='x.jpg'></body></html>", "http://example.com")
        codes = {item["code"] for item in findings}
        self.assertTrue({"no_https", "missing_title", "missing_description", "missing_h1", "missing_cta", "missing_alt"}.issubset(codes))

    def test_score_is_bounded_and_decreases_with_findings(self):
        clean_score = score_findings([])
        weak_score = score_findings(analyze_html("<html></html>", "http://example.com"))
        self.assertEqual(clean_score, 100)
        self.assertGreaterEqual(weak_score, 0)
        self.assertLess(weak_score, clean_score)


if __name__ == "__main__":
    unittest.main()
