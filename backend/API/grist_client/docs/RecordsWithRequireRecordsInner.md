# RecordsWithRequireRecordsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**require** | **object** | keys are column identifiers, and values are [cell values](https://support.getgrist.com/code/modules/GristData/#cellvalue) we want to have in those columns (either by matching with an existing record, or creating a new record)  | 
**fields** | **object** | keys are column identifiers, and values are [cell values](https://support.getgrist.com/code/modules/GristData/#cellvalue) to place in those columns (either overwriting values in an existing record, or in a new record)  | [optional] 

## Example

```python
from grist_client.models.records_with_require_records_inner import RecordsWithRequireRecordsInner

# TODO update the JSON string below
json = "{}"
# create an instance of RecordsWithRequireRecordsInner from a JSON string
records_with_require_records_inner_instance = RecordsWithRequireRecordsInner.from_json(json)
# print the JSON string representation of the object
print(RecordsWithRequireRecordsInner.to_json())

# convert the object into a dict
records_with_require_records_inner_dict = records_with_require_records_inner_instance.to_dict()
# create an instance of RecordsWithRequireRecordsInner from a dict
records_with_require_records_inner_from_dict = RecordsWithRequireRecordsInner.from_dict(records_with_require_records_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


