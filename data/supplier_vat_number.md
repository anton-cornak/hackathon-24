# Definition
The supplier VAT number is a (mostly) international unique identifier of an organisation with VAT liabilities. Within the EU these are prefixed with a two-character country code specifying the country of the supplier. Organizations in non-EU countries can register for a EU vat number with the format "EU + 9 digits". This vat number can be used when trading cross EU borders.

# Instructions
You should mostly see it specified in the per-country instructions if you can come across "EU numbers". But we might have missed this for some countries. So it is _always_ ok to put an EU number in the annotation. However, you should _always_ choose the domestic VAT number over the EU vat number if both are stated.

In many countries the organisation and VAT numbers are closely connected in some way. For instance, in Denmark the "CVR" number functions as both the VAT and organisation number. The per-country instructions will specify when such a connection exists. If the organisation and VAT numbers are stated separately, despite them being almost equal, please annotate both.

    -- Norwegian Invoice --

    The document states:

    Foretaksregisteret: NO 123 456 789 MVA      <-- This is a VAT number
    Organisasjonsnummer: 123.456.789            <-- This is an organisation number

    So you should annotate:

    supplier vat number: NO 123 456 789 MVA
    supplier organisation number: 123.456.789

Note that you should enter the text as it is stated in the document. So as you can see in the example above, we also included the spaces/periods.

# Where to find it
You will mostly find the supplier VAT number near the supplier information (address and so on) in the document header, or in the footer of the document.
