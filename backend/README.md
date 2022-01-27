**Run MongoDB**

```Bash
mongod --dbpath <change-directory>
```
Make sure that fold exist. Example create a folder data under the ECSE458DP_Project folder if using mongod --dbpath ./data

**Run Flask**
```Bash

pip install Flask
pip install pymongo
pip install PyGithub

export FLASK_APP=./backend/app
flask run
```
