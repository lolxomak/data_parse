from flask import Flask, request
import json
import parse
import data_clean

app = Flask(__name__)

def readFileHandler(path, request=None):
	try:
		with open(path, 'r') as f:
			text = f.read()
			return json.dumps({'status': 'ok', 'text': text})
	except Exception as e:
		return json.dumps({'status': 'error', 'type': str(e), 'method': request.method})

def writeFileHandler(path, text, request):
	try:
		with open(path, 'w') as f:
			f.write(text)
			return json.dumps({'status': 'ok', 'method': request.method})
	except Exception as e:
		return json.dumps({'status': 'error', 'type': str(e), 'method': request.method})



@app.route('/api/file_handler', methods = ['POST', 'GET'])
def file_handler():
	if request.method == 'GET':
		pages = request.args.get('pages', default=10, type=int)
		parse.parser(pages)
		rooms = request.args.get('rooms', default=2, type=int)
		data_clean.clean_data(rooms)
		return readFileHandler('clean_data.csv', request)
	else:
		text = request.form['text']
		return writeFileHandler('clean_data.csv', text, request)






if __name__ == '__main__':
	app.debug = True
	app.run()