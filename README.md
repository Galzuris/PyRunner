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

* **vars** (string) - source of unsafe code, any checks are skipped
* **code** (string) - main script source
* **safe** (bool) - safe-run mode, limit execution time by timeout
* **timeout** (float) - timeout for safe-run mode in seconds

```json
{
    "vars": "a=2",
    "code": "return math.pow(4, a)",
    "safe": false,
    "timeout": 4
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

**Error response example**

```json
{
    "execution_error": "invalid syntax",
    "execution_time": 9.965896606445312e-05,
    "result": null,
    "success": false
}
```

## Stop rules

To ensure the safety of script execution, you can block certain expressions through rules in `/app/disabled.txt`. 

**Default rules list**

```
(open\s+["'`\(])|(open["'`\(])
(close\s+["'`\(])|(close["'`\(])
(exit\s+["'`\(])|(exit["'`\(])
(import\s+["'`\(])|(import["'`\(])
(eval\s+["'`\(])|(eval["'`\(])
(exec\s+["'`\(])|(exec["'`\(])
(from.+import)
```

**Error response example**

```json
{
    "execution_error": "unsafe code",
    "execution_time": null,
    "result": null,
    "success": false
}
```

## Template

To run the script, it is built using the `/app/template.py` template.
Stop rules (disabled.txt) for the `#CODE#` block are checked before execution. For the `#VARS#` block any checks are skipped.

```python
import math

#VARS#

def run():
#CODE#
    pass
```
