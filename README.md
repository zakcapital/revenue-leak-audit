# Revenue Leak Audit

A small, productized service for finding conversion, trust, mobile, and search problems on service-business websites.

## Offer

- Introductory price: **$49**
- Turnaround: **48 hours**
- Deliverable: prioritized Markdown/PDF-ready report
- No recurring subscription
- Contact: **cole@byquill.co**

## Audit tool

The audit CLI uses only Python’s standard library.

```bash
python3 audit.py https://example.com --output reports/example.md
```

Run the tests:

```bash
python3 -m unittest discover -s tests -v
```

## Stripe

The Stripe sandbox foundation includes a one-time $49 Product, Price, and Payment Link. The public site remains email-first until a separately approved live launch.

- Tailored plan: [`STRIPE_PLAN.md`](STRIPE_PLAN.md)
- Account review: [`STRIPE_ACCOUNT_REVIEW.md`](STRIPE_ACCOUNT_REVIEW.md)
- Setup and operating procedure: [`STRIPE_SETUP.md`](STRIPE_SETUP.md)

Verify the sandbox configuration with:

```bash
scripts/verify_stripe_test_setup.sh
```

## Sales workflow

1. Find a service business with a clear, observable website problem.
2. Send one personalized observation—never a mass generic pitch.
3. Link to the landing page.
4. On interest, collect the URL, primary service, and desired customer action.
5. Run the automated scan, manually inspect the journey, and deliver the highest-impact fixes first.

## Spending rule

Do not spend the project’s $50 until outreach produces a qualified reply or sale. The first expense should remove a demonstrated bottleneck, not create speculative infrastructure.
