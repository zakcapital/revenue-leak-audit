# Stripe Integration Plan — Revenue Leak Audit

Status: Planning only; no Stripe resources created
Prepared for: ByQuill / Revenue Leak Audit
Site: https://zakcapital.github.io/revenue-leak-audit/
Business contact: cole@byquill.co
Planner guide: `iguide_61V3PbEX5RnBx0tdU41P74eEIlukT` (`accepted`)
Planner use cases: Payments conversion and Invoicing / accounts receivable

## 1. Recommendation

Launch the $49 Revenue Leak Audit with one Stripe-hosted Payment Link linked from the existing static GitHub Pages call-to-action. Keep fulfillment manual at first. This is the smallest integration that can accept payment without adding a backend, exposing API keys, or creating webhook infrastructure before demand is demonstrated.

Use Stripe-hosted Checkout Sessions instead when ByQuill needs server-created transactions, richer intake, first-party order records, reliable automated fulfillment, discounts tied to business logic, or custom post-payment behavior. Payment Links use Stripe's hosted checkout surface, but Checkout Sessions give the application control over creating each checkout.

Keep the three commercial models separate:

1. Payments: one-time $49 Revenue Leak Audit.
2. Billing: a future recurring monitoring service, only after recurring demand is validated.
3. Invoicing: manually scoped custom implementation work, created in the Stripe Dashboard and paid through the Hosted Invoice Page.

## 2. Current constraints and assumptions

- The site is static GitHub Pages and currently routes purchase intent to a prefilled email at `index.html:193`.
- The advertised offer is $49 once, delivered within 48 hours, with no subscription.
- The current sales workflow collects the website URL, primary service, and desired customer action.
- Stripe is assumed to be the sole online processor for this plan. Revisit if another processor is introduced.
- The audit is treated as a human-delivered professional service, not a pure digital-good flow for Stripe Managed Payments.
- Fulfillment volume is initially low enough for a human-reviewed queue.
- No tax obligation, registration, tax treatment, refund policy, or accounting integration has yet been established by the supplied evidence.

## 3. MVP architecture

```text
GitHub Pages CTA
    -> Stripe Payment Link
        -> Stripe-hosted payment page
            -> successful-payment confirmation / configured redirect

Stripe Dashboard + payment email notification
    -> Cole verifies payment status is paid
        -> intake is matched or requested
            -> audit performed
                -> report delivered from cole@byquill.co within 48 hours
```

The success page is not proof of payment and must not independently trigger fulfillment. For the manual MVP, verify the payment in Stripe before beginning work. If delayed payment methods are enabled, fulfillment waits until Stripe reports the payment as paid, not merely that checkout was submitted.

GitHub Pages cannot securely create Checkout Sessions or receive Stripe webhooks by itself. Any later automation requires a separate server-side or serverless component.

## 4. Stripe data model

The following objects are proposed definitions, not resources to create during planning.

### 4.1 One-time audit

Product:

- Name: `Website Revenue Leak Audit`
- Description: focused conversion, trust, mobile, and search audit delivered within 48 hours
- Internal metadata candidates: `offer=website_revenue_leak_audit`, `offer_version=1`, `delivery_sla_hours=48`
- Tax code: undecided; select only from Stripe's current Tax Codes catalog after tax review

Price:

- Currency: USD
- Unit amount: 4900 cents
- Type: one-time
- Suggested lookup key if an API integration is later added: `revenue_leak_audit_one_time_v1`
- Tax behavior: undecided until ByQuill chooses whether the advertised $49 is tax-inclusive or tax-exclusive and receives tax guidance

Do not edit an amount in place after sales begin. Create a new Price for a changed amount and archive the old Price so historical transactions retain their original commercial terms.

### 4.2 Future recurring monitoring

Use a separate Product, such as `Revenue Leak Monitoring`, because it represents a different ongoing obligation from the one-time audit. Create recurring Prices only after the service cadence, included work, cancellation policy, and support boundaries have been tested with customers.

Potential future dimensions:

- monthly or quarterly cadence;
- fixed recurring fee rather than usage billing for the first version;
- clearly defined number of monitored pages or sites;
- report and alert frequency;
- response and remediation boundaries.

Do not reuse the one-time $49 Price for subscriptions. Do not build manual recurring PaymentIntent loops.

### 4.3 Custom implementation work

For bespoke implementation engagements:

- Create or reuse a Stripe Customer after confirming the customer's billing identity and email.
- Create a Dashboard invoice with customer-visible line-item descriptions for agreed scope or milestones.
- Use invoice metadata for internal references such as a project or proposal identifier; metadata is not customer-visible by default.
- Use memo/footer fields for customer-visible terms as appropriate.
- Avoid a fixed reusable Price while scope and amounts remain genuinely custom. Add Products, Prices, or invoice templates later only for repeated packages.

## 5. Payment Links versus Checkout Sessions

### Payment Link — recommended MVP

Advantages:

- no backend and no API key on the static site;
- fastest route from the current email CTA to paid demand;
- Stripe-hosted payment UI and authentication;
- Dashboard-managed payment methods;
- easy to disable if the offer changes or capacity is unavailable.

Limits:

- one shared link rather than a server-created transaction for each order;
- less control over business metadata and first-party order creation;
- intake and fulfillment orchestration remain mostly manual;
- automated capacity controls, eligibility checks, and bespoke pricing are harder;
- a static success redirect cannot securely verify payment.

### Hosted Checkout Sessions — migration target

Adopt Checkout Sessions when one or more of these are demonstrated needs:

- create a unique order record before redirecting to Stripe;
- attach an internal audit-request ID to each transaction;
- validate or enrich intake server-side;
- automate fulfillment from signed webhooks;
- support controlled promotion codes, capacity rules, or multiple audit variants;
- reliably retrieve session details on a server-rendered success page;
- support subscriptions from an application-controlled flow.

Use the Checkout Sessions API rather than the legacy Charges API. Omit `payment_method_types` so Stripe can use eligible dynamic payment methods configured in the Dashboard. On Stripe API version `2026-03-25.dahlia` or later, include an `integration_identifier` with an eight-random-letter suffix when creating Checkout Sessions. Pin and test the account/API version used by the integration; the current Stripe best-practices reference identifies `2026-06-24.dahlia` as the latest version at plan creation.

## 6. Checkout and intake flow

Before a Payment Link is published, decide how required fulfillment information will be collected:

- website URL;
- primary service or offer;
- desired visitor action, such as call, form, or booking;
- purchaser email;
- optional context needed to access or interpret the public website.

Preferred MVP sequence:

1. Payment Link collects customer email and only the minimum practical checkout fields.
2. After payment, direct the buyer to a clear confirmation page or intake mechanism.
3. Match the intake to the Stripe payment using purchaser email and, if available, an order/reference identifier.
4. If intake is missing, send a request from `cole@byquill.co` before starting the 48-hour delivery clock; make the clock's start condition explicit to the customer.
5. Do not request credentials or private customer data through Stripe custom fields or ordinary email.

Before launch, decide whether delivery is promised within 48 hours of payment or within 48 hours of receiving complete intake. The website and receipt/confirmation language should state the same rule.

## 7. Fulfillment controls

For the manual MVP, maintain a small order register outside Stripe with:

- Stripe payment or Checkout Session identifier;
- purchaser email;
- website URL;
- paid timestamp;
- intake-complete timestamp;
- delivery deadline;
- status: paid, intake pending, in progress, delivered, refunded, or disputed;
- delivery timestamp and report location.

Treat Stripe as the payment record, not the complete fulfillment system. Never fulfill from a client-side redirect alone. Confirm the transaction is paid in the Dashboard and record enough provenance to reconcile the delivered report to its payment.

Define before launch:

- refund and cancellation policy;
- what happens if the submitted site is inaccessible or outside scope;
- capacity limit and how the Payment Link is disabled when capacity is reached;
- handling for duplicate purchases;
- who can authorize refunds.

## 8. Receipts and customer email

MVP settings and content decisions:

- Enable Stripe's successful-payment customer emails in the Dashboard if they are not already enabled.
- Configure the public business name, support email, statement descriptor, branding, and relevant policy links before live sales.
- Ensure the Payment Link collects the customer's email for receipt delivery and fulfillment matching.
- Use `cole@byquill.co` consistently as the support contact unless ByQuill establishes a dedicated support address.
- Keep Stripe's payment receipt distinct from ByQuill's fulfillment confirmation. The latter should acknowledge the submitted site, state the delivery deadline, and explain what happens next.
- Test the exact customer-visible receipt, card statement text, confirmation page, and support path.

Do not put confidential audit findings or access credentials in Stripe metadata, receipt descriptions, or webhook logs.

## 9. Webhook and event strategy

### MVP

No webhook is required for a deliberately manual Payment Link fulfillment process. Use Stripe Dashboard status and account notifications as the payment witness. This avoids creating an unreliable webhook endpoint solely to appear automated.

### Automation stage

When order volume justifies automation, deploy a server-side webhook endpoint and:

- verify every event using the raw request body and Stripe endpoint signing secret;
- return a quick success response, then perform work asynchronously;
- store processed Stripe event IDs and make handlers idempotent;
- tolerate duplicate and out-of-order delivery;
- retrieve current Stripe object state when the event payload alone is insufficient;
- log object IDs and outcomes, but never keys, signing secrets, full payloads containing unnecessary personal data, or environment dumps;
- provide replay and manual-reconciliation procedures.

Minimum events for an automated one-time Checkout flow:

- `checkout.session.completed`: create or update the internal order, but fulfill only when payment status is paid;
- `checkout.session.async_payment_succeeded`: release fulfillment for a delayed payment that later succeeds;
- `checkout.session.async_payment_failed`: mark the order unpaid and request another payment path if appropriate;
- `charge.refunded`: reconcile refunds;
- relevant dispute events if card disputes need an internal response workflow.

Minimum events for future subscriptions:

- `invoice.paid`: continue recurring service for the paid period;
- `invoice.payment_failed`: pause/escalate according to the written service policy;
- subscription lifecycle updates/deletions needed to synchronize entitlement state.

Minimum events for later invoice synchronization:

- `invoice.paid`;
- `invoice.payment_failed`;
- `charge.refunded`;
- `credit_note.created`.

Subscribe only to events the system actually handles. Webhooks notify ByQuill about Stripe state; they do not themselves create invoices. Business code or a human initiates invoice creation.

## 10. Billing evolution

Do not add Billing merely because recurring capability may be useful later. Validate that customers want ongoing monitoring and define the recurring obligation first.

When validated:

1. Create the separate monitoring Product and versioned recurring Price.
2. Use Checkout in `subscription` mode for enrollment.
3. Omit `payment_method_types` and use Dashboard-configured dynamic payment methods.
4. Use Stripe Billing for renewals, retries, and dunning rather than custom PaymentIntent renewal jobs.
5. Enable the Stripe Customer Portal for payment-method updates, invoice history, cancellation, and only those plan changes ByQuill is prepared to honor.
6. Define cancellation timing, proration, failed-payment grace period, report cadence, and service access before launch.
7. Add signed, idempotent webhooks and a durable customer/subscription-to-service mapping.
8. Test first payment, renewal, failed renewal, recovery, cancellation, refund/credit, and portal changes using test clocks where applicable.

Start with fixed recurring pricing. Usage-based pricing and Metronome are unnecessary unless the commercial model later becomes genuinely usage-based.

## 11. Invoicing workflow for custom implementation

Recommended initial workflow:

1. Agree scope, amount, milestones, payment terms, and refund/cancellation terms outside Stripe.
2. Create or select the correct Customer in the Dashboard.
3. Create a draft invoice manually with specific customer-visible line items.
4. Review recipient, amount, currency, due date, tax treatment, terms, and branding before sending.
5. Send the invoice through Stripe and let the customer pay on the Hosted Invoice Page, which handles authentication.
6. Track open, paid, overdue, void, refund, and credit-note state in the Dashboard.
7. Begin implementation only at the agreed payment milestone.
8. Export records for bookkeeping until an actual accounting-system integration is selected.

Use Dashboard branding once for all invoices. If repeated packages emerge, add invoice rendering templates. If invoice creation becomes event-driven or high-volume, then use the Invoicing API with idempotency keys; do not automate it prematurely.

Do not enable ACH or bank transfer until customer procurement needs justify it and ByQuill has documented settlement timing, partial-payment, cash-balance, and reconciliation handling. If enabled later, do not equate `invoice.paid` with immediately available cash.

## 12. Tax decision gates

Tax treatment is unresolved and requires accountable human review, with a qualified tax advisor where appropriate. Stripe Tax is a calculation and collection tool, not a determination of where ByQuill must register.

Before enabling tax collection on any Payment Link, Checkout Session, subscription, or invoice:

1. Identify ByQuill's legal entity, business location, customer locations, and the legal classification of the audit and implementation services.
2. Ask a qualified advisor where ByQuill is obligated to register and collect sales tax, VAT, or GST.
3. Complete registration with the relevant authority where required.
4. Record each already-established registration in Stripe and verify it shows as active/Collecting.
5. Select the Product tax code from Stripe's current canonical Tax Codes API or guide; do not guess a `txcd_` value.
6. Decide whether the advertised $49 is tax-inclusive or tax-exclusive and set Price tax behavior consistently.
7. Confirm Stripe has the business origin and sufficient customer location data.
8. Only then enable automatic tax on the applicable Payment Link, Checkout Session, subscription, or invoice.
9. Run jurisdiction-specific tests and verify the resulting tax and `taxability_reason` before launch.

Critical boundary: enabling `automatic_tax` without an active registration does not cause Stripe to collect tax and may not produce an error. Do not present automatic tax as operational until registrations and test transactions confirm it. Do not mix automatic tax and manual tax rates on the same object.

If ByQuill has no established collection obligation or registration, leave tax collection disabled while the decision is examined; do not silently assume the $49 offer is tax-free.

## 13. Security and key handling

### Payment Link MVP

- No Stripe secret or restricted key belongs in `index.html`, JavaScript, the repository, GitHub Pages configuration, query parameters, analytics, or logs.
- The site needs only the public Payment Link URL after a human creates and verifies it.
- Require strong Dashboard authentication, preferably passkeys or an authenticator app rather than SMS.
- Limit Dashboard team access and review access when roles change.
- Configure Stripe branding and customer-facing business details directly in the Dashboard.

### Later backend

- Prefer a separate least-privilege restricted API key (`rk_`) for each service and environment over a broad secret key (`sk_`).
- Store keys and webhook signing secrets in the deployment platform's secret manager; never commit them.
- Use separate test and live keys, webhook endpoints, and signing secrets.
- Add repository secret scanning or a pre-commit check for `sk_`, `rk_`, and webhook-secret patterns.
- Apply key access policies or IP restrictions where the hosting model supports stable egress.
- Never log keys, raw secrets, or environment variables.
- Practice key rotation and inspect Stripe Workbench request logs when validating restricted-key permissions.
- Verify webhook signatures; optionally allowlist Stripe webhook IPs as defense in depth.

If any key is exposed, rotate it immediately, review Workbench activity, and contact Stripe Support for unrecognized activity.

## 14. Test plan

Perform all integration testing in Stripe test mode or a Stripe Sandbox before live mode.

### Payment Link acceptance

- Payment Link displays the correct Product, USD $49 one-time Price, description, branding, and support contact.
- Customer email is collected and a successful-payment email is received.
- Successful card payment reaches the expected confirmation/intake path.
- Declined card and authentication-required scenarios show recoverable customer messaging.
- Refreshing or revisiting the success destination does not create a fulfillment record or duplicate work.
- A paid transaction can be matched to the submitted website and customer email.
- Delayed payment methods, if enabled, do not cause work to start before paid status.
- Refunds appear correctly in Stripe and in the manual order register.
- Mobile, keyboard, and screen-reader basics are checked through the landing-page-to-Stripe transition.
- The Payment Link can be disabled promptly when capacity or offer terms change.

### Checkout/webhook stage

- Signed valid events are accepted; invalid signatures are rejected.
- Duplicate events are idempotent.
- Out-of-order events converge to current Stripe state.
- Handler retries do not create duplicate orders, messages, invoices, or fulfillment jobs.
- Async success and failure paths are exercised.
- Refund and dispute updates reconcile correctly.
- Test and live objects, keys, and webhook secrets cannot cross environments.

### Billing stage

- Initial subscription payment and entitlement activation.
- Renewal, failed renewal, retry/recovery, cancellation, and end-of-period behavior.
- Customer Portal payment-method and cancellation flows.
- Proration behavior if plan changes are permitted.
- Tax results in each registered test jurisdiction.

### Invoicing stage

- Draft review, send, Hosted Invoice Page payment, overdue status, void, refund, and credit note.
- Customer-visible PDF/hosted page shows correct scope, terms, branding, and contact details.
- No internal-only metadata is mistaken for customer-visible terms.

## 15. Launch checklist

### Business and customer experience

- [ ] Human approval to create test resources, followed later by separate approval for live resources.
- [ ] Offer name, $49 amount, currency, scope, capacity, and 48-hour clock are explicitly confirmed.
- [ ] Refund, cancellation, inaccessible-site, duplicate-purchase, and out-of-scope policies are written.
- [ ] Privacy policy, terms, support contact, and any required business disclosures are available and linked where appropriate.
- [ ] Intake captures only information necessary to perform the audit.
- [ ] Fulfillment owner and backup procedure are named.

### Stripe Dashboard

- [ ] Public business details, support email, statement descriptor, branding, and receipt settings are verified.
- [ ] Strong authentication and least-privilege team access are enabled.
- [ ] Test Product, Price, and Payment Link have been reviewed before any live equivalents are created.
- [ ] Eligible payment methods are deliberately reviewed in Dashboard settings; API integrations do not hardcode `payment_method_types`.
- [ ] Tax decision is documented; active registrations and test results exist before automatic tax is enabled.
- [ ] Customer-facing receipt and Hosted Invoice Page are previewed.

### Site and operations

- [ ] CTA points to the reviewed live Payment Link only after live-resource approval.
- [ ] Existing no-subscription language remains accurate.
- [ ] Confirmation/intake path works without exposing secrets.
- [ ] Manual order register and payment-verification procedure are ready.
- [ ] Capacity shutdown procedure is tested.
- [ ] A complete low-value live purchase and refund are performed with human approval before broader promotion.
- [ ] Stripe Dashboard, bank payout, receipt, intake, fulfillment, and refund records reconcile.

## 16. Staged implementation

### Stage 0 — Decisions before configuration

Accountable human: Cole / designated ByQuill steward.

- settle fulfillment clock, intake, refund/cancellation, capacity, terms/privacy, tax review, and statement descriptor;
- configure secure Dashboard access and business identity;
- approve creation of test-mode resources only.

Exit criterion: the customer promise and operating procedure are coherent before money is accepted.

### Stage 1 — No-code test MVP

- create one test Product, one test one-time Price, and one test Payment Link;
- configure email collection, branding, confirmation/intake destination, and receipt behavior;
- execute the Payment Link acceptance tests;
- review the full customer and operator journey.

Exit criterion: a test payment can be securely matched, fulfilled, refunded, and reconciled without ambiguity.

### Stage 2 — Controlled live MVP

Requires separate action-specific approval.

- create live equivalents after test sign-off;
- replace the existing email CTA with the verified live Payment Link while retaining a support contact;
- perform one controlled live purchase/refund test;
- launch at bounded volume and review each order manually.

Exit criterion: real payments and deliveries reconcile, and observed demand justifies continued operation.

### Stage 3 — Fulfillment automation

Trigger: manual processing produces a demonstrated bottleneck or unacceptable error risk.

- add a minimal serverless backend for Checkout Session creation, signed webhooks, and durable order state;
- migrate the CTA from a shared Payment Link to hosted Checkout Sessions;
- add idempotent async fulfillment and reconciliation;
- preserve a manual recovery path.

Exit criterion: duplicate, delayed, failed, refunded, and disputed payments are handled correctly under test.

### Stage 4 — Recurring monitoring pilot

Trigger: customers repeatedly request ongoing monitoring and the service obligation is defined.

- create a separate recurring Product and Price in test mode;
- add subscription Checkout, Customer Portal, Billing webhooks, and service-state mapping;
- pilot with bounded customers before broad availability.

Exit criterion: recurring service delivery, failed payment, cancellation, and tax behavior are verified.

### Stage 5 — Invoicing automation, only if warranted

Trigger: manual custom invoices become repetitive or need accounting-system synchronization.

- introduce invoice templates for repeated presentation first;
- add API creation with idempotency only for a real business trigger;
- add webhook-driven accounting synchronization only after choosing the destination system;
- evaluate bank transfer only with a documented reconciliation need.

Exit criterion: automated invoice creation and reconciliation reduce verified work without weakening review controls.

## 17. Planner decision record

The Stripe implementation planner was finalized with these tailored decisions:

- Custom implementation invoices: manual Dashboard creation; unique invoices initially; ByQuill branding; Hosted Invoice Page; no saved-payment auto-charge; no ACH/bank transfer for MVP; Dashboard reconciliation.
- Standard $49 audit: Stripe-only browser payment; not treated as Managed Payments digital goods; Payment Link for the fixed-price MVP rather than a custom checkout integration.
- Recurring service: no subscription resource now; evolve to Billing plus subscription Checkout and Customer Portal only after demand validation.
- No Products, Prices, Payment Links, invoices, tax registrations, webhooks, or other Stripe resources were created while producing this plan.

## 18. Primary Stripe references returned or used

- Payment Links: https://docs.stripe.com/payment-links/create?pricing-model=standard#get-started
- Hosted Checkout: https://docs.stripe.com/payments/accept-a-payment?payment-ui=checkout&ui=stripe-hosted
- Create invoices in Dashboard: https://docs.stripe.com/invoicing/dashboard#create-invoice
- Invoice branding: https://docs.stripe.com/invoicing/customize#brand-customization
- Hosted Invoice Page: https://docs.stripe.com/invoicing/hosted-invoice-page
- Invoice Dashboard: https://docs.stripe.com/invoicing/dashboard
- Billing integration design: https://docs.stripe.com/billing/subscriptions/design-an-integration
- Customer Portal: https://docs.stripe.com/customer-management/integrate-customer-portal
- Stripe Tax setup: https://docs.stripe.com/tax/set-up
- Restricted API keys: https://docs.stripe.com/keys/restricted-api-keys
- Webhook signatures: https://docs.stripe.com/webhooks#verify-events
- Go-live checklist: https://docs.stripe.com/get-started/checklist/go-live
