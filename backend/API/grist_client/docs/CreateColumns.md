# CreateColumns


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**columns** | [**List[CreateColumnsColumnsInner]**](CreateColumnsColumnsInner.md) |  | 

## Example

```python
from grist_client.models.create_columns import CreateColumns

# TODO update the JSON string below
json = "{}"
# create an instance of CreateColumns from a JSON string
create_columns_instance = CreateColumns.from_json(json)
# print the JSON string representation of the object
print(CreateColumns.to_json())

# convert the object into a dict
create_columns_dict = create_columns_instance.to_dict()
# create an instance of CreateColumns from a dict
create_columns_from_dict = CreateColumns.from_dict(create_columns_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


