# Definition
The currency used to list amounts and totals.

# Where to find it
The currency is usually not stated as a header field (although it does occasionally happen), but rather the currency can be found next to the prices.

There are rare cases where the currency is not stated explicitly anywhere in the document. You should try to infer the currency if possible in those cases. For example, say that a Spanish store gives you a receipt, but does not state the currency. We know that Spain uses euros, so we can infer that the currency must be euro.

It might not be possible to infer the currency in some cases: That could be for invoices where a supplier and customer reside in countries with different currencies and the supplier has not written what the currency is. Leave the currency empty in those cases.

# Which to pick
Sometimes a supplier may list the prices using several currencies. This usually happens when they list the prices in a local currency as well as in euros or in US dollars. For example, a Danish supplier might list prices in Danish kroner and euros. You should pick the currency that appears to be the most common in the document. For example, it might say something like this:

```
Total VAT: 20 DKK
Total excluding VAT: 80 DKK
Total including VAT: 100 DKK
Amount due: 100 DKK
Amount due in EUR: 13.44 EUR
```

The most common currency is DKK in this example.

Make sure that the currency you pick also matches the values that you annotate the amounts and totals with. E.g. we do not support annotating the total VAT in DKK, but the amount due in EUR - both should be annotated using the same currency.
