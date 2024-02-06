# HIRO - PyRunner

This is a simple module for remote script execution using Python,
suitable for use as a service in other projects

## Build

```
git clone git@github.com:Galzuris/PyRunner.git hiro
cd hiro
docker build -t hiro:latest -f ./docker/Dockerfile .
```

## Run

```
docker run --rm -p 12001:8080 hiro:latest
```

## Example request

```
POST http://localhost:12001/run
```

```json
{
    "vars": "a=2",
    "code": "return math.pow(4, a)",
    "timeout": 4,
    "safe": false
}
```

```json
{
    "execution_error": null,
    "execution_time": 0.0000123,
    "result": 16.0,
    "success": true
}
```