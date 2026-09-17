# RecordsWithoutId


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**records** | [**List[RecordsWithoutIdRecordsInner]**](RecordsWithoutIdRecordsInner.md) |  | 

## Example

```python
from grist_client.models.records_without_id import RecordsWithoutId

# TODO update the JSON string below
json = "{}"
# create an instance of RecordsWithoutId from a JSON string
records_without_id_instance = RecordsWithoutId.from_json(json)
# print the JSON string representation of the object
print(RecordsWithoutId.to_json())

# convert the object into a dict
records_without_id_dict = records_without_id_instance.to_dict()
# create an instance of RecordsWithoutId from a dict
records_without_id_from_dict = RecordsWithoutId.from_dict(records_without_id_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


