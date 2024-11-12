# Definition
The method that is used to pay or expected to be used for payment.

The payment method should be inferred when not stated explicitly.

## Invoices, credit notes, and debit notes
Invoices will often have a bank account number, an IBAN number, or a SWIFT number. If any of these can be found - and nothing else is stated - then *bank transfer* should be inferred.

## Receipt
You should pick *credit card* as the payment method if there is any mention of a credit card.

Here are some examples of credit card mentions:

* Credit card
* VISA
* MasterCard
* Last four digits
* `********* 2352`
* Card
* Contactless

*Cash* should be inferred when there is no mention of a credit card. However, this rule only applies to receipts from physical stores. It does not apply to receipts from web shops. Receipts from web shops should instead be inferred as *credit card* unless something else is specified.
