#PTG Production JSON Guideline
######version 0.1
##Structure

```json
{
  "name": "The Name",
  "product_amount": {
    "product_id_0": 1,
    "product_id_1": 2
  },
  "consume_amount": {
    "product_id_2": 2
  },
  "consume_charming_filter": {
    "product_id_2": 56
  },
  "base_charming": 0,
  "experience_acquire": [
    "experience_id_1",
    "experience_id_2"
  ],
  "experience_acquire_chance": [
    0.2,
    1.0
  ],
  "required_structure_id": "structure_id",
  "workforce": [
    {
      "title": "Farmer",
      "required": true,
      "contracts": [],
      "position": 10,
      "experience_efficiency": [
        {
          "experience_id": "experience_1",
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
      ]
    },
    {
      "title": "Land Manager",
      "required": false,
      "contracts": [],
      "position": 1,
      "experience_efficiency": [
        {
          "experience_id": "experience_1",
          "curve": 260,
          "stages": [
            {
              "stage": 0,
              "bonus": 0.2,
              "charming": 2
            }
          ]
        }
      ]
    }
  ],
  "production_t_plus": 10,
  "workforce_bonus": [
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
  ]
}
```
##Explanation
### bonus_package (Optional)
Apply when the production is effect by bonus content.

multiplier name | explanation
----------------|---------------
employee_experience_multiplier|All experience (days) from employees (only required experience count) added up, then multiplied by this multiplier.
### required_structure_id (Optional)
Apply when this production requires a structure.
### consume_amount (Optional)
Apply when the production require raw material.
### consume_charming_filter (Optional)
Should only apply when the charming level of the raw material is static.
### maximum_production_t_plus (Optional)
Production will be terminated upon the time exceed.
