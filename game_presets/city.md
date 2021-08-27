#PTG City JSON Guideline
######version 0.1
##Structure
```json
{
  "country_id": "country_id_0",
  "name": "The Name",
  "financial_id": {
    "name": "The Financial Name",
    "initial_fund_map": {
      "currency_cad": 1000
    }
  },
  "currency_id": "currency_cad",
  "structures": [
    "structure_0",
    "structure_1",
    "structure_2"
  ],
  "population_count": 0,
  "population": {
    "first_name_pool": ["Nelson", "Cherie"],
    "last_name_pool": ["Zhang", "Chen"],
    "experience_chance_dict": {
      "experience_id_0": [18, 0.02],
      "experience_id_1": [23, 0.17]
    },
    "age_distribution": [
      [[18, 29], 3000, 0.03, [10000, 250000]],
      [[30, 49], 5000, 0.3, [200000, 500000], [[[0, 6], 0.3], [[0, 6], 0.04],  [[7, 17], 0.01]], [200000, 360000]],
      [[50, 64], 6000, 0.45, [300000, 800000], [[[0, 6], 0.01], [[7, 17], 0.4], [[7, 17], 0.1]], [150000, 250000]],
      [[65, 79], 3000, 0.14, [500000, 900000]],
      [[80, 120], 2400, 0.08, [400000, 700000]]
    ]
  },
  "market": {
    "name": "The market name",
    "financial_id": {
      "name": "The Financial Name",
      "initial_fund_map": {
        "currency_cad": 1000
      }
    },
    "property_name": "name of the property",
    "handling_fee_rate": 0.05
  },
  "property": {
    "property_name_pool": [["Windsor", 500], ["Winston", 500]],
    "build_properties": {
      
    }
  },
  "company": {
    
  },
  "land_tax_per_year": 1000,
  "human_model": [
    {
      "requirements": {
        "all_time": {
          "product_clothes": [1, 2, 0.01]
        },
        "life_goal": {
          
        }
      }
    }
  ]
}
```
##Explanation
### population
####experience_chance_dict
#####key
The ID of experience.
#####value(list)
position 0: minimum_achieve_age

position 1:achieve_chance
####age_distribution (list)
position | prop | leave blank
---|---|---
0|age range|Mandatory
1|total population|Mandatory
2|marriage rate|Mandatory
3|saving range|Mandatory
4|child age range{3}|This age group should not have a baby
5|addition saving (per child) range|~

{1}: This age group will only be arranged to position 3 family

{2}: This age group will only be arranged to position 4 family

{3}: Child Age Range: 2D list [[child_age_range_list, n_children_combined_possibility], ...]

###human_model
####requirements
all_time: all time requirement

life_goal: try to achieve after age 26

field | explanation | extra
---|---|---
key | product_id
value pos 0|frequency (months)
value pos 1|budget type|0 = all saving, 1 = yearly salary, 2 = monthly salary
value pos 2|budget rate| based on budget type above