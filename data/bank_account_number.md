# Definition

Number that uniquely identifies an account in a given bank. The bank in question is specified by the bank registration number.

# When to annotate

You should always annotate the bank account number if it is present in a document. Bank account numbers are mostly present in invoices, credit notes, and debit notes, but rarely in receipts.

Note that this field is only meant for domestic formats. So even though IBAN is technically an account number, that should never go into this field. Generally speaking, separate bank account and registration number even if they appear in a "bank line". See the country specific instructions for how to make the split.

Note that it is very common almost everywhere to ommit leading zeros from account numbers. So always assume that the specified formats could be shorter than stated.

# Where to find it

Bank account numbers are usually found together with payment terms in the vicinity of the amount due, or in the footer of the document.
