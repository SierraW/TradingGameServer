#PTG Company Type JSON Guideline
######version 0.1
##Structure

```json
{
  "name": "Name of the type",
  "company_scope_id": "scope_1",
  "stock_market": {
    "allow_register": true,
    "access_register": 0,
    "allow_trade": true,
    "access_level_trade": 0
  }
}
```
##Explanation
### ~~company_type~~
Specify the type of the company.

Numeric Level | Type of the Company | Property Access | Stock Market Access
----------------|---------------|-------------|--------
0|Investment Company|No|Full
1|Area Management Company|No|Home Country
2|Management Company|No|Home City
3|Manufacture Company|Limited by scope|No
### stock_market
####access_level

Numeric Level | Explain
----------------|---------------
0|Invitation Only
1|City
2|Country
3|International
