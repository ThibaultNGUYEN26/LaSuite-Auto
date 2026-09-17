# UpdateColumns


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**columns** | [**List[UpdateColumnsColumnsInner]**](UpdateColumnsColumnsInner.md) |  | 

## Example

```python
from grist_client.models.update_columns import UpdateColumns

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateColumns from a JSON string
update_columns_instance = UpdateColumns.from_json(json)
# print the JSON string representation of the object
print(UpdateColumns.to_json())

# convert the object into a dict
update_columns_dict = update_columns_instance.to_dict()
# create an instance of UpdateColumns from a dict
update_columns_from_dict = UpdateColumns.from_dict(update_columns_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


