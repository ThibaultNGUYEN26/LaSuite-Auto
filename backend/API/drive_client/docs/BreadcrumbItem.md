# BreadcrumbItem

Serialize breadcrumb items.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **UUID** | primary key for the record as UUID | [readonly] 
**title** | **str** |  | [readonly] 
**path** | **str** |  | [readonly] 
**depth** | **str** |  | [readonly] 
**main_workspace** | **bool** |  | [readonly] 

## Example

```python
from openapi_client.models.breadcrumb_item import BreadcrumbItem

# TODO update the JSON string below
json = "{}"
# create an instance of BreadcrumbItem from a JSON string
breadcrumb_item_instance = BreadcrumbItem.from_json(json)
# print the JSON string representation of the object
print(BreadcrumbItem.to_json())

# convert the object into a dict
breadcrumb_item_dict = breadcrumb_item_instance.to_dict()
# create an instance of BreadcrumbItem from a dict
breadcrumb_item_from_dict = BreadcrumbItem.from_dict(breadcrumb_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


