from flask import render_template, Flask, flash, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
import zipfile
from mcstats import *

app = Flask(__name__)

# Define the allowed file extensions
ALLOWED_EXTENSIONS = {'zip'}
app.secret_key = 'caca'
app.config['UPLOAD_FOLDER'] = './uploads'
nb_files = 0

def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def test():
	global nb_files
	if request.method == 'POST':
		# Check if the file is present in the request
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		
		file = request.files['file']
		
		# Check if the file is allowed
		if file and allowed_file(file.filename):
			# Save the file to a secure location
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			with zipfile.ZipFile(file_path, 'r') as zip_ref:
				zip_ref.extractall(app.config['UPLOAD_FOLDER']+ '/up_' + str(nb_files))
			nb_files += 1
			os.remove(file_path)
			files = os.listdir(app.config['UPLOAD_FOLDER'] + '/up_' + str(nb_files-1) + '/stats/')
			players = {}
			for f in files:
				if f.endswith('.json'):
					players[uuid_pseudo(f.replace('.json', '').replace('-', ''))] = f
			return render_template('choose_player.html', players=players, nb_files=nb_files-1)
		
		else:
			flash('Invalid file type. Only .zip files are allowed.')
			return redirect(request.url)
	
	# If the request method is GET, render the hello.html template
	return render_template('hello.html')

@app.route('/show', methods=['POST'])
def loading():
	player_id = request.form.get('player')
	nb_files = request.form.get('nb_files')
	with open(app.config['UPLOAD_FOLDER'] + '/up_' + nb_files + '/stats/' + player_id, 'r') as file:
		datas = json.load(file)
	stats = getstats(datas)
	stats['pseudo'] = uuid_pseudo(player_id.replace('.json', '').replace('-', ''))
	stats['player_id'] = player_id.replace('.json', '').replace('-', '')
	return render_template('show.html', stats=stats)