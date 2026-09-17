# DocumentStoreSetting


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | [optional] 

## Example

```python
from grist_client.models.document_store_setting import DocumentStoreSetting

# TODO update the JSON string below
json = "{}"
# create an instance of DocumentStoreSetting from a JSON string
document_store_setting_instance = DocumentStoreSetting.from_json(json)
# print the JSON string representation of the object
print(DocumentStoreSetting.to_json())

# convert the object into a dict
document_store_setting_dict = document_store_setting_instance.to_dict()
# create an instance of DocumentStoreSetting from a dict
document_store_setting_from_dict = DocumentStoreSetting.from_dict(document_store_setting_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


