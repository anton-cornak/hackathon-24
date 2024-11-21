# Definition
IBAN is short for International Bank Account Number. It is used to identify bank accounts across countries.

# Format
The exact format of an IBAN depends on the country, but there are a few general rules that each country has to comply with:

* Consists of up to 34 alphanumeric characters.
* Must start with a 2-letter country code.
* The next 2 digits must be check digits (used to ensure that the IBAN is valid and has not been tampered with).
* The remaining up to 30 alphanumeric characters are country specific. This part is also called the Basic Bank Account Number (BBAN).

IBANs are traditionally written in groups of four characters, but this is not a requirement. Both of the following formats are acceptable:

* FR76 3000 6000 0112 3456 7890 189
* FR7630006000011234567890189

You should annotate the IBAN using the same format that it is written as in the document.

[Wikipedia has a thorough list](https://en.wikipedia.org/wiki/International_Bank_Account_Number#IBAN_formats_by_country) of what an IBAN looks like for many countries. We see, for example, that Danish IBANs look like *DKkk bbbb cccc cccc cx* where k = check digit, b = bank registration number, c = bank account number, and x = national check digit.

# Which to pick
Suppliers do sometimes list more than one IBAN. This usually happens when they have bank accounts in multiple countries.

You should pick the IBAN that matches the supplier country. E.g., if the supplier country is Denmark, then you should pick the IBAN starting with DK.

There might be multiple IBANs matching the supplier country. Pick the top-left most of these in that case.

It might also be that none of the IBANs match the supplier country. Pick the top-left most IBAN in the document in that case.

# Be aware of this
Some countries have bank account numbers that look a lot like IBANs without actually being IBANs. If you see a document saying "account number" followed by something that looks like an IBAN, then check that it is actually an IBAN before annotating the IBAN field. [This tool](https://www.iban.com/iban-checker) can help you validate that the number is actually an IBAN. Otherwise the Wikipedia list linked above can be useful.

We know that at least Spain have domestic bank account numbers that look like IBANs. We also know that Finland uses IBANs as the domestic bank account number.
