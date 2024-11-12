# Definition
The last date that a payment has to be made.

Documents may sometimes contain multiple payment due dates. This happens when a customer gets a discount when paying early. For example:
"Due date is in 5 days net for a 5% discount and 30 days net without a discount."

We have decided to pick the latest of the due dates, which would be the 30 days net in the example.

Receipts do not have a payment due date since they are a proof of payment. Exceptions may occur to this rule though since some receipts can be proof of a partial payment.

# How to annotate
We use two fields to specify the payment due date.

## Due date
This should always be filled in if the payment due date is either explicitly stated or if it can be inferred.

__How to infer__:
The payment due date will sometimes not be stated explicitly, so we need to fill in the __Due date__ field by inferring. Pay attention to the payment terms when inferring. Here are some examples:

* The invoice date is 2022/02/15 and the payment terms are "30 days NET". Payment due date = 2022/03/17 because there are 13 days left in February and 17 days goes into March.
* The invoice date is 2022/02/15 and the payment terms are "30 days EOM". Payment due date = 2022/03/30 because we calculate relative to the end of February.

Here are some examples of payment terms and what they mean.

| Terms       | Explanation                                                                                    |
| ----------- | ---------------------------------------------------------------------------------------------- |
| Net 30      | Pay in 30 days from the document date.                                                         |
| Net 30 EOM  | Pay in 30 days after the end of the document date month.                                       |
| 2/10 NET 30 | Pay in 10 days to get a 2% discount, otherwise pay in 30 days. We pick the latter.             |
| Net 30 ROG  | Pay in 30 days upon receipt of goods. The due date is based on the delivery date in this case. |

## Due in x days
This should only be filled in if the text contains "due in 30 days net" or a similar phrase to denote payment terms.

Note that the payment terms will say whether it is "net" or "EOM" (end of month). We are only interested in the cases where it is "x days net" from the document date. Note also that we do not fill in this field if the payment terms are relative to receipt of goods (ROG).
