#PTG Experience JSON Guideline
######version 0.1
##Structure
```json
{
  "name": "The Name",
  "description": "The description",
  "formation_time": -360
}
```
##Explanation
### formation_time
The formation time should have a negative amount initially.
* value < 0 means the skill is not yet learned.
* value = n (n >= 0) means the skill is learned and has n days of experience.
