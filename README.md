# Blake

# Setup
Update config... I have hardcoded paths...

BLAKE_JOB_DIR -- When a job executes it creates a working dir (currently on a dir gets made...)

BLAKE_SCRIPT_DIR -- Should point to repo: app/scripts/Scripts_Dir. This just dynamically imports the "scripts" from this dir currently...

## Environment (virtualenv, bower, redis)
```
./setup.sh
```
## Database (flask_migrate)
Name: blake/blake-stage (see config)
```
source venv/bin/active
flask db init
flask db migrate
flask db
```

## DatabaseScheduler -- (celery crontab)
It crashes if nothing exists in the db table (ah eh eh)... so this adds a task which runs every 5 min "checking" audiostores
```
source venv/bin/active
flask init
```
## Add a test_store
Note: can also be added through ui... this creates a folder at "cwd + test_store"
```
source venv/bin/active
flask fill
```


# Starting misc
## Flask App
```
source venv/bin/active
flask run
```
## Redis Server
```
redis-stable/src/redis-server
```
## Celery
### Celery Beat
```
source venv/bin/active
celery -A celery_worker.celery beat
```

### Celery Worker
#### Queue: normal (avaiable queues: high, normal, low)
Everything defaults to normal (no tasks setup for queues)
```
source venv/bin/active
celery -A celery_worker.celery  worker -E -n worker.normal -Q low
celery -A celery_worker.celery  worker -E -n worker.normal -Q normal
celery -A celery_worker.celery  worker -E -n worker.normal -Q high
```
