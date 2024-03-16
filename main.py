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
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024 * 1024
nb_files = 0

def delete_folder(folder_name):
	for root, dirs, files in os.walk(folder_name, topdown=False):
		for name in files:
			os.remove(os.path.join(root, name))
		for name in dirs:
			os.rmdir(os.path.join(root, name))

delete_folder(app.config['UPLOAD_FOLDER'])

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
			return render_template('hello.html', notif='No file part')
		
		file = request.files['file']
		
		# Check if the file is allowed
		if file and allowed_file(file.filename):
			# Save the file to a secure location
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			if not zipfile.is_zipfile(file_path):
				flash('Invalid file type. Only .zip files are allowed.')
				return render_template('hello.html', notif='Invalid file type. Only .zip files are allowed.')
			with zipfile.ZipFile(file_path, 'r') as zip_ref:
				zip_ref.extractall(app.config['UPLOAD_FOLDER']+ '/up_' + str(nb_files))
			nb_files += 1
			os.remove(file_path)
			if not os.path.exists(app.config['UPLOAD_FOLDER'] + '/up_' + str(nb_files-1) + '/stats/'):
				delete_folder(app.config['UPLOAD_FOLDER'] + '/up_' + str(nb_files-1))
				os.rmdir(app.config['UPLOAD_FOLDER'] + '/up_' + str(nb_files-1))
				flash('Invalid file. No stats/ folder found')
				return render_template('hello.html', notif='Invalid file. No stats/ folder found')
			files = os.listdir(app.config['UPLOAD_FOLDER'] + '/up_' + str(nb_files-1) + '/stats/')
			players = {}
			count = 0
			for f in files:
				if f.endswith('.json'):
					pseudo = uuid_pseudo(f.replace('.json', '').replace('-', ''))
					if pseudo:
						players[pseudo] = f
						count += 1
			if count == 0:
				flash('Invalid file. No .json files found in stats/ folder')
				return render_template('hello.html', notif='Invalid file. No .json files found in stats/ folder')
			return render_template('choose_player.html', players=players, nb_files=nb_files-1)
		
		else:
			flash('Invalid file type. Only .zip files are allowed.')
			return render_template('hello.html', notif='Invalid file type. Only .zip files are allowed.')
	
	# If the request method is GET, render the hello.html template
	return render_template('hello.html', notif='')

@app.route('/show', methods=['POST'])
def loading():
	player_id = request.form.get('player')
	nb_files = request.form.get('nb_files')
	with open(app.config['UPLOAD_FOLDER'] + '/up_' + nb_files + '/stats/' + player_id, 'r') as file:
		try:
			datas = json.load(file)
		except:
			delete_folder(app.config['UPLOAD_FOLDER'] + '/up_' + nb_files)
			flash('Invalid file. The .json file is not valid.')
			return render_template('hello.html', notif='Invalid file. The .json file is not valid.')
	stats = getstats(datas)
	stats['pseudo'] = uuid_pseudo(player_id.replace('.json', '').replace('-', ''))
	stats['player_id'] = player_id.replace('.json', '').replace('-', '')
	return render_template('show.html', stats=stats)