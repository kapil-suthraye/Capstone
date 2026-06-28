def get_discrepancies():

    return [

        {
            "Title":"MRI Procedure",

            "Claim":"MRI billed",

            "Record":"No MRI found",

            "Risk":"High",

            "Confidence":"98%",

            "Recommendation":"Manual Review"
        },

        {
            "Title":"Length of Stay",

            "Claim":"5 Days",

            "Record":"4 Days",

            "Risk":"Medium",

            "Confidence":"95%",

            "Recommendation":"Verify Billing"
        }

    ]