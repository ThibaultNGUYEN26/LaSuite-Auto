# GroupInResponseMeta


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**resource_type** | **str** |  | [optional] 
**location** | **str** |  | [optional] 

## Example

```python
from grist_client.models.group_in_response_meta import GroupInResponseMeta

# TODO update the JSON string below
json = "{}"
# create an instance of GroupInResponseMeta from a JSON string
group_in_response_meta_instance = GroupInResponseMeta.from_json(json)
# print the JSON string representation of the object
print(GroupInResponseMeta.to_json())

# convert the object into a dict
group_in_response_meta_dict = group_in_response_meta_instance.to_dict()
# create an instance of GroupInResponseMeta from a dict
group_in_response_meta_from_dict = GroupInResponseMeta.from_dict(group_in_response_meta_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


