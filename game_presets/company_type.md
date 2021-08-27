#PTG Company Type JSON Guideline
######version 0.1
##Structure
```json
{
  "name": "Name of the type",
  "company_scope_id": "scope_1",
  "designated_structures": [
    "structure_id_0",
    "structure_id_1",
    "structure_id_2"
  ],
  "stock_market_visibility": 0,
  "stock_market_access_type": 1
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
### stock_market_visibility
Specify the stock can be owned by which type of company.

Numeric Level | Visibility for company | Visibility for individuals
----------------|---------------|-------------
0|All|All
1|Within the country|All
2|Within the city|All
3|Within the city|No

### stock_market_access_type
Specify what types of company stocks it can own.

Numeric Level | Detail
----------------|---------------
0|All types of company
1|Reserved
2|Management Company
3|Manufacture Company
4|No access

##Idea
The whole design of different access levels was to maintain a good-looking company tree.

**Investment Company**
- Designed to hold stocks both within country or aboard
- Designed to use as the top level of the company group.
- Or can use as an international foundation.
- Has almost no limit to purchase stocks.

**Area Management Company**
- Designed to be a country-level management company.
- Designed to be a bridge for international company to purchase any lower level companies.

**Management Company**
- Designed to be a city-level management company.
- It should not be purchase by any company from aboard.

**Advanced Management Company**
- Not visible by individuals.
- This type of company required higher level operators. So it should be directly own by Management Company

**Manufacture Company**
- A company that actual manufacturing product.
