#PTG Management JSON Guideline
subclass of Business
######version 0.1
##Structure

```json
{
  "name": "The Name",
  "required_structures": [
    {
      "structure_id": "structure_field",
      "bonus": 1
    },
    {
      "structure_id": null,
      "bonus": 0.5
    }
  ],
  "workforce": {
    "positions": [
      {
        "title": "Farmer",
        "required": true,
        "contracts": [],
        "count": 1,
        "experience_efficiency": [
          {
            "experience_id": "experience_field",
            "curve": 260,
            "stages": [
              {
                "stage": 10,
                "workforce": 0
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
        "count": 10,
        "experience_efficiency": [
          {
            "experience_id": "experience_1",
            "curve": 260,
            "stages": [
              {
                "stage": 0,
                "workforce": 1
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
    "bonus_package": {}
  }
}
```
##Explanation
### required_structure_id (Optional)
Apply when this production requires a structure.
