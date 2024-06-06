Site Specific Search App API:
This API developed using FastAPi and Python enables programmatically searching Google by using Google’s Site Specific Search to find specific terms on a website. The base URL and search term are given as input to the API which returns a list of links in the website domain that contain the search term. The results are stored in an AWS DynamoDb table.

Requirements: The requirements are specified in the requirement.txt file.All the libraries can be installed using in python3. In addition, aws credentials need to be configured for the environment.
The api is run using the Uvicorn server and can be started using this command:

uvicorn shortener_app.main:app --reload

Testing: FastApi automatically creates swagger documentation that can be accessed and tested by going to:
http://127.0.0.1:8000/doc
