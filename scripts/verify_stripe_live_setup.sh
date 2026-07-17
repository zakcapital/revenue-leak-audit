#!/usr/bin/env bash
set -euo pipefail

command -v stripe >/dev/null || { echo "Stripe CLI is required" >&2; exit 1; }
command -v jq >/dev/null || { echo "jq is required" >&2; exit 1; }

product_id="prod_UtpkcDtJ6HQ1au"
price_id="price_1Tu2QbP74eEIlukTjXIY3TBy"
link_id="plink_1Tu2QdP74eEIlukT3hSk1YLV"
expected_url="https://buy.stripe.com/28E9AV6EU0Ckd6t0CS24000"
expected_redirect="https://zakcapital.github.io/revenue-leak-audit/success.html"

tmpdir="$(mktemp -d "${TMPDIR:-/tmp}/revenue-leak-stripe-live-verify.XXXXXX")"
trap 'rm -rf "$tmpdir"' EXIT

stripe products retrieve --live "$product_id" > "$tmpdir/product.json"
stripe prices retrieve --live "$price_id" > "$tmpdir/price.json"
stripe payment_links retrieve --live "$link_id" > "$tmpdir/link.json"
stripe get --live "/v1/payment_links/$link_id/line_items" > "$tmpdir/line-items.json"

jq -e --arg id "$product_id" '
  .id == $id and
  .livemode == true and
  .active == true and
  .name == "Website Revenue Leak Audit"
' "$tmpdir/product.json" >/dev/null

jq -e --arg id "$price_id" --arg product "$product_id" '
  .id == $id and
  .livemode == true and
  .active == true and
  .currency == "usd" and
  .unit_amount == 4900 and
  .type == "one_time" and
  .product == $product
' "$tmpdir/price.json" >/dev/null

jq -e --arg id "$link_id" --arg url "$expected_url" --arg redirect "$expected_redirect" '
  .id == $id and
  .livemode == true and
  .active == true and
  .url == $url and
  .after_completion.type == "redirect" and
  .after_completion.redirect.url == $redirect and
  .customer_creation == "always" and
  .automatic_tax.enabled == false and
  .payment_intent_data.statement_descriptor_suffix == "AUDIT"
' "$tmpdir/link.json" >/dev/null

jq -e --arg price "$price_id" '
  .data | length == 1 and
  .[0].price.id == $price and
  .[0].quantity == 1
' "$tmpdir/line-items.json" >/dev/null

printf 'Verified live Stripe Product, $49 Price, active Payment Link, and success redirect.\n'
