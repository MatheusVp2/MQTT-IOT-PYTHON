from flask import Flask, render_template, jsonify, request
from flask_bootstrap import Bootstrap
from flask_cors import CORS

app       = Flask(__name__)
bootstrap = Bootstrap(app)

CORS(app)
cors = CORS(app, resources={
	r"/*": {
		"origins" : "*"
	}
})

@app.route( '/', methods = ['POST', 'GET'] )
def home():
	return render_template('index_gps.html')

@app.route( '/device/<string:device>/attr/<string:attrs>', methods = ['GET'] )
def device_attr_info(device, attrs):
	# URL TESTE => http://127.0.0.1:5000/device/deb8e7/attr/latitude,longitude
    return jsonify( getDataDivce( device, attrs ) )

if __name__ == '__main__':
    app.run( host="127.0.0.1", port=5000 , debug=True )