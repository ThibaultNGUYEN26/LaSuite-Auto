# UpdateColumnsColumnsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Column identifier | 
**fields** | [**UpdateColumnsColumnsInnerFields**](UpdateColumnsColumnsInnerFields.md) |  | 

## Example

```python
from grist_client.models.update_columns_columns_inner import UpdateColumnsColumnsInner

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateColumnsColumnsInner from a JSON string
update_columns_columns_inner_instance = UpdateColumnsColumnsInner.from_json(json)
# print the JSON string representation of the object
print(UpdateColumnsColumnsInner.to_json())

# convert the object into a dict
update_columns_columns_inner_dict = update_columns_columns_inner_instance.to_dict()
# create an instance of UpdateColumnsColumnsInner from a dict
update_columns_columns_inner_from_dict = UpdateColumnsColumnsInner.from_dict(update_columns_columns_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


