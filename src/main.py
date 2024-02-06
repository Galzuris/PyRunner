import time
import os
from libs import code
from flask import Flask, jsonify, request
from waitress import serve

app = Flask(__name__)
app.config['RATELIMIT_ENABLED'] = False
app.config['CACHE_ENABLED'] = False

@app.route("/run", methods=['POST'])
def runner_unsafe():
    data = request.form or request.json
    src = data['code']
    vars = str(data['vars'] if 'vars' in data else '')
    safe = bool(data['safe'] if 'safe' in data else True)
    timeout = float(data['timeout'] if 'timeout' in data else 1)

    if not code.is_safe(src):
        return jsonify({
            "success": False,
            "result": None,
            "execution_error": "unsafe code",
            "execution_time": None,
        })
    else:
        start = time.time()
        source = code.render(vars, src)
        if safe:
            res, val = code.run_safe(source, timeout=timeout)
        else:
            res, val = code.run(source)            
        end = time.time()

        return jsonify({
            "success": res,
            "result": val if res else None,
            "execution_error": val if not res else None,
            "execution_time": end-start,
        })        


if __name__ == '__main__':  
    debug = os.environ['DEBUG'] if 'DEBUG' in os.environ else False
    if debug:
        print('run in debug mode')
        app.run(debug=True, host='0.0.0.0', port=8080)
    else:
        print('run in production mode')
        serve(app, host='0.0.0.0', port=8080)    
