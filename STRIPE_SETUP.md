# Stripe setup — Revenue Leak Audit by ByQuill

Status: test-mode foundation complete; live sales are not enabled.

## Test resources

- Stripe account: ByQuill (`acct_1TtzLiP74eEIlukT`)
- Product: `prod_UtpWpNtf0R4cdG` — Website Revenue Leak Audit
- One-time price: `price_1Tu1rAP74eEIlukT81MdB8gC` — USD $49.00
- Payment Link: `plink_1Tu1riP74eEIlukTvR8u0dZb`
- Sandbox checkout: https://buy.stripe.com/test_28E9AV6EU0Ckd6t0CS24000
- Completion redirect: https://zakcapital.github.io/revenue-leak-audit/success.html

These IDs are non-secret test resource identifiers. API credentials are not stored in this repository.

## Payments MVP

The public site remains email-first until live launch approval. The test Payment Link:

- collects the customer email;
- creates a Stripe Customer;
- charges the fixed one-time $49 price;
- leaves eligible payment methods controlled by Stripe Dashboard settings;
- keeps automatic tax disabled pending a tax decision;
- uses `AUDIT` as the card statement-descriptor suffix;
- redirects to the intake page after checkout;
- requires manual payment verification before fulfillment.

A test-mode $49 PaymentIntent succeeded and a full test refund succeeded. The hosted sandbox checkout was also verified to load the ByQuill product, description, and price. No real money moved.

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

## Live launch gates

Before creating live resources or replacing the public CTA:

- verify Stripe business identity, support details, payout account, branding, receipt settings, and the `BYQUILL` statement descriptor;
- document the sales-tax decision; do not enable Stripe Tax without relevant registrations and review;
- review eligible payment methods in Dashboard;
- preview customer receipts and the Hosted Invoice Page;
- approve creation of one live Product, Price, and Payment Link;
- perform one controlled low-value live purchase and refund with explicit human approval;
- confirm the payment, receipt, payout, intake, and refund records reconcile.

## Verification

Run:

```sh
scripts/verify_stripe_test_setup.sh
python3 -m unittest discover -s tests -v
```

The Stripe CLI uses its secure local login. Never place `sk_`, `rk_`, or webhook secrets in this repository or in browser-delivered code.
