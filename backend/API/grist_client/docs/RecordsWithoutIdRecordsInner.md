# RecordsWithoutIdRecordsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**fields** | **object** | A JSON object mapping column names to [cell values](https://support.getgrist.com/code/modules/GristData/#cellvalue). | 

## Example

```python
from grist_client.models.records_without_id_records_inner import RecordsWithoutIdRecordsInner

# TODO update the JSON string below
json = "{}"
# create an instance of RecordsWithoutIdRecordsInner from a JSON string
records_without_id_records_inner_instance = RecordsWithoutIdRecordsInner.from_json(json)
# print the JSON string representation of the object
print(RecordsWithoutIdRecordsInner.to_json())

# convert the object into a dict
records_without_id_records_inner_dict = records_without_id_records_inner_instance.to_dict()
# create an instance of RecordsWithoutIdRecordsInner from a dict
records_without_id_records_inner_from_dict = RecordsWithoutIdRecordsInner.from_dict(records_without_id_records_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


