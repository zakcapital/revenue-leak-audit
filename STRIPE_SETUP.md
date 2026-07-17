# Stripe setup — Revenue Leak Audit by ByQuill

Status: live $49 checkout launched after successful sandbox purchase and refund verification.

## Test resources

- Stripe account: ByQuill (`acct_1TtzLiP74eEIlukT`)
- Product: `prod_UtpWpNtf0R4cdG` — Website Revenue Leak Audit
- One-time price: `price_1Tu1rAP74eEIlukT81MdB8gC` — USD $49.00
- Payment Link: `plink_1Tu1riP74eEIlukTvR8u0dZb`
- Sandbox checkout: https://buy.stripe.com/test_28E9AV6EU0Ckd6t0CS24000
- Completion redirect: https://zakcapital.github.io/revenue-leak-audit/success.html

These IDs are non-secret test resource identifiers. API credentials are not stored in this repository.

## Live resources

- Product: `prod_UtpkcDtJ6HQ1au` — Website Revenue Leak Audit
- One-time price: `price_1Tu2QbP74eEIlukTjXIY3TBy` — USD $49.00
- Payment Link: `plink_1Tu2QdP74eEIlukT3hSk1YLV`
- Checkout: https://buy.stripe.com/28E9AV6EU0Ckd6t0CS24000
- Completion redirect: https://zakcapital.github.io/revenue-leak-audit/success.html

## Payments MVP

The public site links to the live Stripe-hosted checkout and retains `cole@byquill.co` for support. The checkout:

- collects the customer email;
- creates a Stripe Customer;
- charges the fixed one-time $49 price;
- leaves eligible payment methods controlled by Stripe Dashboard settings;
- keeps automatic tax disabled pending a tax decision;
- uses `AUDIT` as the card statement-descriptor suffix;
- redirects to the intake page after checkout;
- requires manual payment verification before fulfillment.

A sandbox $49 purchase and full refund succeeded through the hosted checkout. No real money moved during verification.

## Fulfillment procedure

1. Verify the Stripe payment is `paid` or the PaymentIntent is `succeeded`.
2. Match the payment email to the intake received at `cole@byquill.co`.
3. Start the 48-hour delivery clock only after payment and complete intake are both present.
4. Record the order, due time, delivery, and any refund in a bounded order register.
5. Deactivate the Payment Link if capacity cannot support the promise.

The success-page redirect is not proof of payment.

## Billing foundation

Do not create a subscription yet. A recurring product should be introduced only after customers repeatedly request ongoing monitoring and the cadence, included work, cancellation policy, failed-payment handling, and support boundaries are defined.

When validated:

1. Create a separate `Revenue Leak Monitoring` Product and recurring Price in test mode.
2. Use Stripe Checkout in subscription mode.
3. Enable Customer Portal cancellation and payment-method management.
4. Add a server-side webhook endpoint with signature verification and idempotent handling.
5. Map `invoice.paid`, `invoice.payment_failed`, and subscription status changes to service access.

## Invoicing foundation

Use Stripe Dashboard invoices for custom implementation work. Each engagement requires a separately approved written scope and price.

1. Create or select the Customer.
2. Add the scoped implementation line item.
3. Use Stripe's Hosted Invoice Page and ByQuill branding.
4. Review recipient, amount, due date, memo, and payment methods before sending.
5. Mark work ready only after payment status is verified.
6. Reconcile payment, delivery, refunds, and credits in Stripe Dashboard.

Do not automate invoice creation until recurring manual work demonstrates a need.

## Launch record and controls

Completed before launch:

- Stripe business details, card payments, charges, payouts, and transfers were verified active;
- the Product, $49 one-time Price, Payment Link, checkout messaging, and success redirect were verified in live mode;
- automatic tax remains disabled pending tax review;
- the sandbox hosted checkout purchase and refund were verified;
- the user explicitly approved activating the live resources and publishing the checkout CTA.

No live test purchase was made because the project cannot justify spending money solely for testing. Treat the first genuine customer payment as the controlled live verification: manually confirm payment, receipt, intake, payout, and delivery before accepting additional orders.

## Verification

Run:

```sh
scripts/verify_stripe_test_setup.sh
scripts/verify_stripe_live_setup.sh
python3 -m unittest discover -s tests -v
```

The Stripe CLI uses its secure local login. Never place `sk_`, `rk_`, or webhook secrets in this repository or in browser-delivered code.
