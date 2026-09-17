# ColumnsWithoutFields


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**columns** | [**List[ColumnsWithoutFieldsColumnsInner]**](ColumnsWithoutFieldsColumnsInner.md) |  | 

## Example

```python
from grist_client.models.columns_without_fields import ColumnsWithoutFields

# TODO update the JSON string below
json = "{}"
# create an instance of ColumnsWithoutFields from a JSON string
columns_without_fields_instance = ColumnsWithoutFields.from_json(json)
# print the JSON string representation of the object
print(ColumnsWithoutFields.to_json())

# convert the object into a dict
columns_without_fields_dict = columns_without_fields_instance.to_dict()
# create an instance of ColumnsWithoutFields from a dict
columns_without_fields_from_dict = ColumnsWithoutFields.from_dict(columns_without_fields_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


