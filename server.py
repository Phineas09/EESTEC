from flask import *

app = Flask(__name__)
''' 
        Sanity check, returns 200 and empty body, it proves that the server is 
    running
'''


@app.route("/sanity", methods=['GET'])
def sanityResponse():
    return Response("", status=200, mimetype='application/json')


'''
        Echo response test for path /test/echoEndpoint, it returns the sent 
    json, if none present must return error
'''


@app.route('/test/echoEndpoint', methods=['POST'])
def my_test_endpoint():
    data = request.get_json()
    if data is None:
        abort(400)
    return jsonify(data)


'''
        The bellow section is for errorhandlers
'''


@app.errorhandler(400)
def page_not_found():
    return Response('No data provided! It should be of type application/json',
                    status=400,
                    mimetype='application/json')


'''
        Main function for starting the app
'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)