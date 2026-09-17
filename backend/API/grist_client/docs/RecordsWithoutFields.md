# RecordsWithoutFields


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**records** | [**List[RecordsWithoutFieldsRecordsInner]**](RecordsWithoutFieldsRecordsInner.md) |  | 

## Example

```python
from grist_client.models.records_without_fields import RecordsWithoutFields

# TODO update the JSON string below
json = "{}"
# create an instance of RecordsWithoutFields from a JSON string
records_without_fields_instance = RecordsWithoutFields.from_json(json)
# print the JSON string representation of the object
print(RecordsWithoutFields.to_json())

# convert the object into a dict
records_without_fields_dict = records_without_fields_instance.to_dict()
# create an instance of RecordsWithoutFields from a dict
records_without_fields_from_dict = RecordsWithoutFields.from_dict(records_without_fields_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


