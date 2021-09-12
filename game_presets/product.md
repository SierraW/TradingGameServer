#PTG Product JSON Guideline
######version 0.1
##Structure

```json
{
  "name": "The Name",
  "category": 0,
  "items_per_stack": 99,
  "charming": {
    "material": 0.1,
    "designo": 0.2,
    "software_solution": 0.3
  }
}
```
##Explanation
The type of product. Name should be unique.

###category (int)
* 0 Food
* 1 Raw Materials (used by light industry)
* 2 Light Industry Products
* 3 Heavy Industry Products
* 4 Artisan Industry Products
* 5 Virtual Products (Work Force etc.)