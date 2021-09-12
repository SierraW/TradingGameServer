#PTG Production JSON Guideline
subclass of Business
######version 0.1
##Structure

```json
{
  "name": "The Name",
  "product": [
    {
      "product_id": "product_wheat",
      "amount": 10
    }
  ],
  "consume": [
    {
      "product_id": "product_wheat_seed",
      "amount": 1000
    }
  ],
  "required_structures": {
    "structure_field": {
      "bonus": 1
    },
    "_none": {
      "bonus": 0.5
    }
  },
  "workforce": {
    "_reserved_workforce": 0,
    "_reserved_bonus": 0,
    "amount": -1000,
    "production_t_plus": 10,
    "positions": [
      {
        "title": "Farmer",
        "required": true,
        "contracts": [],
        "count": 10,
        "experience_efficiency": [
          {
            "experience_id": "experience_field",
            "curve": 260,
            "stages": [
              {
                "stage": 0,
                "workforce": 5,
                "charming": 1
              },
              {
                "stage": 1,
                "workforce": 10,
                "charming": 1
              },
              {
                "stage": 3,
                "workforce": 12,
                "charming": 1
              },
              {
                "stage": 9,
                "workforce": 15,
                "charming": 1
              }
            ]
          }
        ],
        "experience_acquire": [
          {
            "id": "experience_id",
            "chance": 1
          }
        ]
      },
      {
        "title": "Land Manager",
        "required": false,
        "contracts": [],
        "count": 1,
        "experience_efficiency": [
          {
            "experience_id": "experience_1",
            "curve": 260,
            "stages": [
              {
                "stage": 0,
                "bonus": 1.2,
                "charming": 2
              }
            ]
          }
        ],
        "experience_acquire": [
          {
            "id": "experience_id",
            "chance": 1
          }
        ]
      }
    ],
    "bonus": [
      {
        "type": "quality",
        "curve": 100,
        "stages": [
          {
            "stage": 1,
            "bonus": 20
          },
          {
            "stage": 3,
            "bonus": 30
          },
          {
            "stage": 9,
            "bonus": 40
          }
        ]
      }
    ],
    "base_charming": 0,
    "bonus_package": {}
  }
}
```
##Explanation
### bonus_package (Optional)
Apply when the production is effect by bonus content.

multiplier name | explanation
----------------|---------------
employee_experience_multiplier|All experience (days) from employees (only required experience count) added up, then multiplied by this multiplier.
### required_structures (Optional)
Apply when this production requires a structure.
### consume_amount (Optional)
Apply when the production require raw material.
### consume_charming_filter (Optional)
Should only apply when the charming level of the raw material is static.
### maximum_production_t_plus (Optional)
Production will be terminated upon the time exceed.
