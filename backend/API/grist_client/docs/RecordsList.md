# RecordsList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**records** | [**List[RecordsListRecordsInner]**](RecordsListRecordsInner.md) |  | 

## Example

```python
from grist_client.models.records_list import RecordsList

# TODO update the JSON string below
json = "{}"
# create an instance of RecordsList from a JSON string
records_list_instance = RecordsList.from_json(json)
# print the JSON string representation of the object
print(RecordsList.to_json())

# convert the object into a dict
records_list_dict = records_list_instance.to_dict()
# create an instance of RecordsList from a dict
records_list_from_dict = RecordsList.from_dict(records_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


