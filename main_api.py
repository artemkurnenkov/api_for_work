import json
import main

from flask import Flask, request

app = Flask(__name__)


@app.route('/recommended', methods=["GET"])
def recommended():
    user_ids = request.args.getlist("user_ids")
    if not user_ids:
        return json.dumps({"error": {"error_code": 1, "error_msg": "Empty users list"}}), 400
    try:
        user_ids = [int(i) for i in set(user_ids)]
    except (ValueError, TypeError) as error_message:
        return json.dumps({"error": {"error_code": 2, "error_msg": str(error_message)}}), 400
    result_dict = main.method_of_recommendation(user_ids)
    result = []
    for user_id, products in result_dict.items():
        result.append({"user_id": user_id, "products": products})
        user_ids.remove(int(user_id))
    for user_id in user_ids:
        result.append({"user_id": user_id, "error": "Not found"})
    result_1 = json.dumps({"users": result}, indent=4)
    return result_1, 200


if __name__ == "__main__":
    app.run()
