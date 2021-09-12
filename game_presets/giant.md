#PTG Giant JSON Guideline
######version 0.1
##Structure

```json
{
  "name": "The Name",
  "city_id": "city_id",
  "company_type": "company_type_international_investment_company",
  "property": {
    "count": 1,
    "structures": [""]
  },
  "stock_distribution": [
    {
      "type": "individual",
      "family": true,
      "minimum_age": 18,
      "amount": 500
    },
    {
      "type": "city",
      "id": "city_id",
      "amount": 49500,
      "investment": 500000
    }
  ],
  "subsidiaries": [
    {
      "name": "The Sub Name",
      "city_id": "city_id",
      "company_type": "company_type_investment_company",
      "subsidiaries": [
        {
          "name": "The Sub Sub Name",
          "city_id": "city_id",
          "company_type": "company_type_agriculture_company"
          "property": {
          }
        }
      ],
      "investment": 100000
    }
  ]
}
```
##Explanation
### obj
