# home-aid-api

## Setup the env 
### Create a virtual environment
```
    python3 -m venv .homeaid
```

### Active the environment
```
    source .homeaid/bin/activate
```

### Install the dependencies
```
    pip install -r requirements.txt
```


## Start app
```
uvicorn src.app.main:app --host 0.0.0.0 --port 8080 --reload
```