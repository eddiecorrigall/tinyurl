# tinyurl
A tinyurl clone service

## Features
- [done] Test environment
- [done] Deployment environment
- [done] Staging environment
- [done] Production environment (AWS Lambda, AWS ElastiCache: Redis)
- [done] Bootstrap frontend
- [todo] App configuration
- [todo] Python linter
- [todo] Doc strings
- [todo] Continuous Integration (Circle CI or Travis CI)
- [todo] Internationalization (i18n)
- [todo] Test app error handlers
- [todo] Integration tests: local redis server and read-only
- [todo] Solve lambda cold starts
- [todo] Solve duplicate logs in CloudWatch Logs
- [todo] Choose at least 2 subnets for Lambda to run your functions in high availability mode
- [todo] Automatically generate api docs

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
- https://serverless.com/blog/serverless-api-gateway-domain/
- https://serverless-stack.com/chapters/stages-in-serverless-framework.html
- https://serverless.com/framework/docs/dashboard/testing/
- https://serverless-stack.com/chapters/load-secrets-from-env.html

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

## Quick Start
```bash
# Setup project
./bin/setup.sh

# Run locally
./bin/local.sh
```

## Example

### Set Endpoint
```bash
# Local development: `./bin/local.sh`
export TINYURL_ENDPOINT=http://localhost:5000

# OR, in the cloud: `./bin/provision.sh --stage staging`
export TINYURL_ENDPOINT=https://tinyurl-staging.7okyo.com
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

|Command|Wrapper for|Description|
|---|---|---|
|`./bin/setup.sh`|N/A|Setup project|
|`./bin/test.sh`|pytest|Run tests|
|`./bin/local.sh`|serverless wsgi|Run locally|
|`./bin/provision.sh`|serverless deploy|Provision cloud|
|`./bin/deprovision.sh`|serverless remove|De-provision cloud|
|`./bin/logs.sh`|serverless logs|Get logs from cloud|

### Arguments

The pytest and serverless arguments are passed into the CLI tools. For example, to deploy to production use the `--stage production` argument to the `./bin/provision.sh` script.

# Troubleshooting

---
**AWS DNS is unable to resolve the S3 path for the deploy. To continue developing, try switching the `--region`.**

```Serverless: Recoverable error occurred (Inaccessible host: `*.s3.amazonaws.com'. This service may not be available in the `us-east-1' region.), sleeping for 5 seconds. Try 4 of 4```

---
**Lambda log collection is not supported in ca-central-1.**

```ServerlessError: No existing streams for the function```
