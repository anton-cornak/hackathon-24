# Definition
The total price of services and goods provided by the supplier.

We express the totals using three fields:

|                     |                                                                           |
| ------------------- | ------------------------------------------------------------------------- |
| Total VAT           | Amount of VAT to be paid for the goods/services.                          |
| Total excluding VAT | The value of the goods/services.                                          |
| Total including VAT | The value of goods/services after VAT, discounts, shipping, and rounding. |

We seek to annotate each field as much as possible. We encourage to infer these fields for that reason. For example, say that the document states the total excluding VAT and the total including VAT, but does not say what the total VAT is. We encourage inferring the total VAT as total including VAT - total excluding VAT in that case. However, remember to take care to follow the guidelines further below.

# What is VAT?
Value added tax (VAT) is a tax on products in most industries. See [this page](https://www.investopedia.com/terms/v/valueaddedtax.asp) for a more thorough explanation of what VAT is.

A few countries do not use VAT, but it is common within most countries and particularly within the EU.

The percentage of the price that you have to pay as VAT differs between countries.

VAT is most often paid by the supplier by adding the VAT to the price in the invoice. However, some countries implement reverse VAT charges where it is the responsibility of the customer to pay the VAT to the government. Documents will not specify the VAT when reverse VAT charge is in place. The document will say if reverse VAT charges are to be applied.

# Be aware of this
There are several pitfalls with totals that you should take special care about.

## The total VAT is only stated implicitly
It is common that some documents only state the total VAT as a percentage of the price or as a breakdown of different VAT levels.

The first case would be something like *"VAT is 20% of 50 EUR"* in which case you should fill in the total VAT as *10*.

The second case would look something like the following table:

| VAT level | Amount | VAT   |
| --------- | ------ | ----- |
| 5%        | 200.00 | 10.00 |
| 10%       | 300.00 | 30.00 |
| 21%       | 50.00  | 10.50 |

You should sum the VAT column in this case to get the total VAT of *50.50*.

## The document does not say what the VAT is
There can be several reasons for why a document does not say what the VAT is and we deal with the cases a bit differently:

1. __Reverse VAT charge is applied__: We cannot know what total VAT and total including VAT is in this case, so you should only annotate total excluding VAT.
2. __Total VAT is obscured__: It might happen that the total VAT is probably there, but it is obscured. That might happen in a cropped receipt. Do not annotate the total VAT in this case.
3. __VAT does not apply__: Some documents may not be applicable to VAT. For example, when a supplier from a VAT-exempt country trades within its own borders. Do not fill in VAT in those cases. Ask in Slack if you are doubt about whether VAT is applicable to a document.
4. __Otherwise__: Assume that the total VAT is 0. This also means that you should annotate with the same value for total excluding VAT and total including VAT.
