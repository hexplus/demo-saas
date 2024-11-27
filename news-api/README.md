## API project

### Installing pip (dependency manager)

1. Have python installed
2. ```curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py```
3. ```python get-pip.py```

### Installing dependencies

```pip install -r requirements.txt```


### If some dependency is missing


```pip install <name-of-dependency>```

Look for the name and version in: [https://pypi.org](https://pypi.org), add the name and version of the dependency in the requirements.txt file in the root of this project.

### Cloning repository

```git@github.com:hexplus/limbic-api.git```

### Create a new branch

```git checkout -b kratsaira```

### Process to create a Pull Request

1. Add all the files that you want to commit:
```git add <name-of-files>```

2. Commit those files ```git commit -m "Describe the changes you did"```
3. Push your changes ```git push origin kratsaira```
4. Go to Github and create the Pull Request from your branch to main

**NEVER PUSH TO MAIN**

### Testing your adapter

Go to the http-request folder and add your test, for example, this GET request to CNNE (CNN en Español):

```
###
GET http://127.0.0.1:5000/categories/CNNE
Content-Type: application/json
```

### Adding the adapter to the API

The adapters data once created should not be change, so, there is a plain json file where the information of the adapter should be added, it is in the `data` folder.

