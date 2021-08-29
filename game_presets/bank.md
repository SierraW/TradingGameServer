#PTG Bank JSON Guideline
######version 0.1
##Structure

```json
{
  "name": "The Name",
  "financial_entity_id": null,
  "main_currency_id": "currency_cad",
  "reserve_ratio": 0.054,
  "deposit_products": [
    {
      "name": "Flexible Deposit",
      "limit": null,
      "rate": 0.005,
      "expiry_days": null,
      "owner_permissions": "io"
    },
    {
      "name": "One Year Deposit",
      "limit": null,
      "rate": 0.009,
      "expiry_days": 365,
      "owner_permissions": ""
    }
  ],
  "loan_product": {
  },
  "accounts": {
  }
}
```
##Explanation
### bank
