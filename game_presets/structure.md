#PTG Structure JSON Guideline
######version 0.1
##Structure
```json
{
  "name": "The Name",
  "storage_space": 50,
  "structure_build_contract": {
    "work_force": 1000,
    "experience_required": [
      "experience_1", "experience_2"
    ],
    "material_required_per_work_force": {
      "material_1": 1,
      "material_2": 2
    }
  },
  "bonus_package": {
    "designo_multiplier": 0.1,
    "software_solution_multiplier": 0.5,
    "raw_material_multiplier": 0.0,
    "employee_experience_multiplier": 0.02
  },
  "unit_name_and_property_id_dict": {
    "unit_generation_guideline": [
      {
        "number_of_area": 3,
        "number_of_unit_per_area": 1,
        "unit_size": 2,
        "structure_id": "structure_room_medium" 
      },
      {
        "number_of_area": 34,
        "number_of_unit_per_area": 12,
        "unit_size": 1,
        "structure_id": "structure_room_small" 
      }
    ]
  }
}
```
##Explanation
The blueprint of the building.
###product_required_type_list
Indicate types product needed for this structure to complete.
###product_required_amount_list
Indicate quantities required by this structure.
###product_required_quality_list
Indicates the minimum charming level acceptable for each product.