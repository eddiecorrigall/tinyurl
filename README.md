# tinyurl
A tinyurl clone service

## Features
- [todo] App configuration
- [todo] Python linter
- [todo] Doc strings
- [done] Test environment
- [done] Deployment environment
- [todo] Production environment (AWS Lambda, AWS ElastiCache: Redis)
- [todo] Continuous Integration (Circle CI or Travis CI)
- [todo] Internationalization (i18n)
- [todo] Test app error handlers
- [todo] Integration tests: local redis server and read-only
- [todo] Rename serverless function in template

## References
- https://stackoverflow.com/questions/742013/how-do-i-create-a-url-shortener
- https://serverless.com/blog/flask-python-rest-api-serverless-lambda-dynamodb/
- https://pypi.org/project/redis/
- https://stackoverflow.com/questions/1119722/base-62-conversion
- https://stackoverflow.com/questions/22340676/find-or-create-idiom-in-rest-api-design
- https://flask.palletsprojects.com/en/1.1.x/patterns/apierrors/
- http://werkzeug.palletsprojects.com/en/0.16.x/exceptions/
- https://flask.palletsprojects.com/en/1.1.x/appcontext/
- https://flask.palletsprojects.com/en/1.1.x/logging/
- https://flask.palletsprojects.com/en/1.1.x/testing/

## Technique

### Long to short

Given an url: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ', insert into table.

|id|long|short|
|---|---|---|
|125|'https://www.youtube.com/watch?v=dQw4w9WgXcQ'|???|

Get an id (125) which is a auto incremented unique identifier.
Convert id into a base-62 string ('cb') which will be the short form url.
Update table at the id, and update the short form url.

|id|long|short|
|---|---|---|
|125|'https://www.youtube.com/watch?v=dQw4w9WgXcQ'|'cb'|

### Short to long

Convert short base-62 string ('cb') into a base-10 integer which will be the table id (125).
Select from table at id, and return long form url: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'.

|id|long|short|
|---|---|---|
|125|'https://www.youtube.com/watch?v=dQw4w9WgXcQ'|'cb'|

## Design decision

### Database
URLs can be viral, meaning there is no even traffic distribution between unique urls.

#### DynamoDB
DynamoDB is not suitable since the partition key, which uniquely identifies the URL, will be quickly reach provisioned thoroughput and the application will no longer service requests.

#### ElastiCache: Redis
Redis supports HSET and HGET which does not suffer from hot partitions and will consistently perform at O(1) time complexity.

### Service

#### Lambda
- Pro: pay per usage
- Pro: light-weight infrastructure
- Pro: scalable

## Setup Project
```bash
# Setup project
sh bin/setup.sh

# Run all tests
sh bin/tests.sh

# Run locally
serverless wsgi serve
```

## Example

### Set Endpoint
```bash
# Local development: `serverless wsgi serve`
export TINYURL_ENDPOINT=http://localhost:5000

# OR, deployed: `serverless deploy`
export TINYURL_ENDPOINT=https://xg8hjfwp7d.execute-api.us-east-1.amazonaws.com/development
```

### Make TinyURL
```bash
curl \
    --write-out '%{http_code}\n' \
    --request POST "${TINYURL_ENDPOINT}/tinyurl" \
    --header 'Content-Type: application/json' \
    --data '{"url": "http://example.com"}'
```

### Get TinyURL
```bash
curl \
    --write-out '%{http_code}\n' \
    --request GET "${TINYURL_ENDPOINT}/tinyurl?url=http://example.com"
```

### Redirect from TinyURL
```bash
curl \
    --write-out '%{http_code}\n' \
    --request GET "${TINYURL_ENDPOINT}/a"
```

## Commands

|Command|Description|
|---|---|
|`sh bin/setup.sh`|Setup project|
|`sh bin/test.sh`|Run tests|
|`sh bin/run.sh`|Run locally|
|`sh bin/deploy.sh`|Deploy to cloud|
|`sh bin/logs.sh`|Get logs from cloud|
