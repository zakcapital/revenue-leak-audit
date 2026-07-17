#!/usr/bin/env bash
set -euo pipefail

command -v stripe >/dev/null || { echo "Stripe CLI is required" >&2; exit 1; }
command -v jq >/dev/null || { echo "jq is required" >&2; exit 1; }

product_id="prod_UtpWpNtf0R4cdG"
price_id="price_1Tu1rAP74eEIlukT81MdB8gC"
link_id="plink_1Tu1riP74eEIlukTvR8u0dZb"
expected_redirect="https://zakcapital.github.io/revenue-leak-audit/success.html"

tmpdir="$(mktemp -d "${TMPDIR:-/tmp}/revenue-leak-stripe-verify.XXXXXX")"
trap 'rm -rf "$tmpdir"' EXIT

stripe products retrieve "$product_id" > "$tmpdir/product.json"
stripe prices retrieve "$price_id" > "$tmpdir/price.json"
stripe payment_links retrieve "$link_id" > "$tmpdir/link.json"
stripe get "/v1/payment_links/$link_id/line_items" > "$tmpdir/line-items.json"

jq -e --arg id "$product_id" '
  .id == $id and
  .livemode == false and
  .active == true and
  .name == "Website Revenue Leak Audit"
' "$tmpdir/product.json" >/dev/null

jq -e --arg id "$price_id" --arg product "$product_id" '
  .id == $id and
  .livemode == false and
  .active == true and
  .currency == "usd" and
  .unit_amount == 4900 and
  .type == "one_time" and
  .product == $product
' "$tmpdir/price.json" >/dev/null

jq -e --arg id "$link_id" --arg redirect "$expected_redirect" '
  .id == $id and
  .livemode == false and
  .active == true and
  .after_completion.type == "redirect" and
  .after_completion.redirect.url == $redirect
' "$tmpdir/link.json" >/dev/null

jq -e --arg price "$price_id" '
  .data | length == 1 and
  .[0].price.id == $price and
  .[0].quantity == 1
' "$tmpdir/line-items.json" >/dev/null

printf 'Verified Stripe sandbox Product, $49 Price, Payment Link, and success redirect.\n'
