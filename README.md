# Blake

# Setup
Update config... I have hardcoded paths...

BLAKE_JOB_DIR -- When a job executes it creates a working dir (currently on a dir gets made...)

BLAKE_SCRIPT_DIR -- Should point to repo: app/scripts/Scripts_Dir. This just dynamically imports the "scripts" from this dir currently...

BALKE_SCRIPT_VERSIONS -- Script versioning directory...

## Environment (virtualenv, bower, redis)
This will also install redis inside the application. This might fail if you have compilation errors - ignore these if you have your own version of redis already installed.

```
./setup.sh
```
## Database (flask_migrate)
Name: blake/blake-stage (see config)
```
source venv/bin/activate
flask db init
flask db migrate
flask db
```

## DatabaseScheduler -- (celery crontab)
It crashes if nothing exists in the db table (ah eh eh)... so this adds a task which runs every 5 min "checking" audiostores
```
source venv/bin/activate
flask init
```
## Add a test_store
Note: can also be added through ui... this creates a folder at "cwd + test_store"
```
source venv/bin/activate
flask fill
```


# Starting misc
## Flask App
```
source venv/bin/activate
flask run
```
## Redis Server
Start up an existing redis installation, or run the one built into the app:

```
redis-stable/src/redis-server
```
## Celery
### Celery Beat
```
source venv/bin/activate
celery -A celery_worker.celery beat
```

### Celery Worker
#### Queue: normal (avaiable queues: high, normal, low)
Everything defaults to normal (no tasks setup for queues)
```
source venv/bin/activate
celery -A celery_worker.celery  worker -E -n worker.normal -Q low
celery -A celery_worker.celery  worker -E -n worker.normal -Q normal
celery -A celery_worker.celery  worker -E -n worker.normal -Q high
```
