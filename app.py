from flask import Flask, request, jsonify, abort
import sqlite3
import urllib

app = Flask(__name__)


def get_paginated_list(results, url, start, limit):
    start = int(start)
    limit = int(limit)
    count = len(results)
    # make response
    obj = {}
    obj['start'] = start
    obj['limit'] = limit
    obj['count'] = count
    if count < start or limit < 0:
        if count == 0:
            obj['start'] = ''
            obj['limit'] = limit
            obj['count'] = count
            obj['previous'] = ''
            obj['next'] = ''
            obj['results'] = []
            return obj
        else:
            abort(404)
    # make URLs
    # make previous url
    if start == 1:
        obj['previous'] = ''
    else:
        start_copy = max(1, start - limit)
        # limit_copy = start - 1
        obj['previous'] = url + '&start=%d&limit=%d' % (start_copy, limit)
    # make next url
    if start + limit > count:
        obj['next'] = ''
    else:
        start_copy = start + limit
        obj['next'] = url + '&start=%d&limit=%d' % (start_copy, limit)
    # finally extract result according to bounds
    obj['results'] = results[(start - 1):(start - 1 + limit)]
    return obj


def dictionary_factory(db, row):
    return {
        "first_name": row[0],
        "last_name": row[1],
        "state": row[2],
        "phonenumber": row[3],
        "email": row[4]
    }


def search_phone_book(**kwargs):
    db = sqlite3.connect("phonebook.db")
    cur = db.cursor()

    search_first_name = kwargs.get("first_name")
    search_last_name = kwargs.get("last_name")
    search_state = kwargs.get("state")
    search_phone_number = kwargs.get("phone_number")

    if not any([search_first_name, search_last_name, search_state, search_phone_number]):
        return []

    query = "SELECT * FROM people WHERE "

    query_arguments = []

    if search_first_name:
        query_arguments.append(f"first_name LIKE '%{search_first_name}%'")

    if search_last_name:
        query_arguments.append(f"last_name LIKE '%{search_last_name}%'")

    if search_state:
        query_arguments.append(f"state LIKE '%{search_state}%'")

    if search_phone_number:
        query_arguments.append(f"phonenumber LIKE '%{search_phone_number}%'")

    query += " AND ".join(query_arguments)

    cur.row_factory = dictionary_factory
    result_list = list(cur.execute(query))
    db.close()
    return result_list


@app.route("/search/", methods=['GET'])
def search_phonebook():
    first_name = request.args.get("firstName")
    last_name = request.args.get("lastName")
    state = request.args.get("state")
    query_dict = {'firstName': first_name, 'lastName': last_name, 'state': state}
    final_dict = {key: value for key, value in query_dict.items() if value is not None}
    qstr = urllib.parse.urlencode(final_dict)
    base_url = "http://127.0.0.1:8080/search/?" + qstr

    if not any([first_name, last_name, state]):
        return jsonify({"error": "At least one of the three fields must be filled."}), 400

    search_results = search_phone_book(
        first_name=first_name,
        last_name=last_name,
        state=state
    )

    return jsonify(get_paginated_list(
        search_results,
        base_url,
        start=request.args.get('start', 1),
        limit=request.args.get('limit', 5)
    ))


@app.route("/find/", methods=['GET'])
def search_phone():
    phone_number = request.args.get("phoneNumber")

    if not phone_number:
        return jsonify({"error": "PhoneNumber field must be filled."}), 400
    query_dict = {'phoneNumber': phone_number}
    qstr = urllib.parse.urlencode(query_dict)
    base_url = "http://127.0.0.1:8080/search/?" + qstr

    search_results = search_phone_book(
        phone_number=phone_number
    )
    return jsonify(get_paginated_list(
        search_results,
        base_url,
        start=request.args.get('start', 1),
        limit=request.args.get('limit', 5)
    ))


if __name__ == "__main__":
    app.run(debug=True, port=8080, threaded=True)
