# Drive API tutorial

## Step 1 : Generate the key

generate the django admin key : 

First edit the METRIC_ENABLE to true at : **drive/src/backend/drive/settings.py**

Then you need to generate a superuser account to loggin with django just do : **make superuser** 

the superuser credential will be : 
- login : admin@example.com
- password : admin

Then login to http://localhost:8071/admin, with the superuser account, and you can now generate a key. It will be show in a notification popup, you have to copy it right after, it wont be shown again.

## Step 2 : Use the api

Add this line : @extend_schema_view(list=extend_schema(exclude=True)) , to this file : drive/src/backend/core/api/viewsets.py line 2539 (dont forget to rebuild)

now you can view all the routes!