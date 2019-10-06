import json
import logging
import os
from pathlib import Path

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/", methods=['OPTIONS'])
def serve_options():
    """
    Deals with OPTIONS requests - returns legal CORS header
    """
    return "", 200, {
        'Access-Control-Allow-Origin': "*",
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS, PUT, DELETE',
        'Access-Control-Allow-Credentials': 'true',
        'Access-Control-Allow-Headers': request.headers.get('Access-Control-Allow-Headers', '*')
    }


@app.route("/", methods=['POST'])
def serve_completions():
    # Get the context data from the request
    data = json.loads(request.data)
    if data is None:
        return jsonify({}), 200

    context = data.get('context', '')
    value = data.get('value', '')
    sn = data.get('sn', -1)

    logging.info("POST: context='%s' value='%s'", context, value)

    # Get the prediction
    completions = model.predict(context, value)

    logging.info("POST: completions='%s'", completions)

    return jsonify({
        "completions": completions,
        'sn': sn
    }), 200, HEADERS


@app.route("/", methods=['PUT'])
def collect_telemetry():
    # Get the context data from the request
    data = json.loads(request.data)
    logging.debug("PUT json: {}".format(data))
    if data is None:
        return jsonify({}), 200

    # Process the telemetry request
    try:
        logging.info("TELE: data='%s'", data)

        session_id = data.pop('session_id')
        context = data.pop('context', None)
        TELEMETRY.add(session_id=session_id, context=context, telemetry=data)
    except Exception:
        logging.exception('Problem with telemetry')

    return jsonify({
    }), 200, HEADERS


def gunicorn_run(**kwargs):
    app.run(debug=False, port=5000)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    app.run(debug=False, port=5000)

