# Definition
The customer number is the ID assigned to the customer by the supplier.

Format: alpha-numeric, e.g. abcd1234. The customer number will typically not resemble a dictionary word, but it does sometimes contain something that looks like a date.

Documents will sometimes state something like "customer VAT number". This is __not__ what we are interested in as this is the VAT number of the customer, which is not the same as the identifier assigned by the supplier to the customer.

Some documents may state *account number* as the customer number. This is particularly true for subscription based services. We accept those cases as customer numbers, but take care not to confuse it for bank account numbers. It should be clear from the context of the document whether it is a customer number or a bank account number. Ask in Slack if you are in doubt.

Similar to *account number*, some documents will state a member or user ID. These are also acceptable as customer numbers.

# Where to find it
The customer number will frequently be found in a table of document information similar to this:

|                     |           |
| ------------------- | --------- |
| Invoice number      | 123456789 |
| Your reference      | John Doe  |
| __Customer number__ | xyz       |
| Order number        | AB1234    |

It will most often be found in the beggining of a document before the product table.

Receipts do typically not contain customer numbers, but there are exceptions to this.
