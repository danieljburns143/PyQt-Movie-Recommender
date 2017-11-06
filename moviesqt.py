import sys
import requests
import json
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class MoviesQT(QMainWindow):
	def __init__(self):
		super(MoviesQT, self).__init__()
		self.setWindowTitle('Movie Recommender')

		self.filemenu = self.menuBar().addMenu('&File')
		self.usermenu = self.menuBar().addMenu('&User')
		fileExitAction = QAction('Exit', self)
		userProfileAction = QAction('View Profile', self)
		userSetAction = QAction('Set User', self)
		self.filemenu.addAction(fileExitAction)
		self.usermenu.addAction(userProfileAction)
		self.usermenu.addAction(userSetAction)

		self.connect(fileExitAction, SIGNAL('triggered()'), self.exit_program)
		self.connect(userProfileAction, SIGNAL('triggered()'), self.view_profile)
		self.connect(userSetAction, SIGNAL('triggered()'), self.set_user)
		
		class MoviesCentral(QWidget):
			def __init__(self, parent=None):
				super(MoviesCentral, self).__init__(parent)
				self.uid = 5
				self.SITE_URL = 'http://student04.cse.nd.edu:51001'
				self.RECOMMENDATIONS_URL = self.SITE_URL + '/recommendations/'
				r = requests.get(self.RECOMMENDATIONS_URL + str(self.uid))
				resp = json.loads(r.content.decode())
				self.mid = resp['movie_id']

				self.MOVIES_URL = self.SITE_URL + '/movies/'
				r = requests.get(self.MOVIES_URL + str(self.mid))
				resp = json.loads(r.content.decode())

				self.imagesDirectory = '/home/paradigms/images/' + resp['img']
				self.image = QImage(self.imagesDirectory)

				self.imageLabel = QLabel('no image available')
				self.imageLabel.setAlignment(Qt.AlignCenter)
				self.imageLabel.setPixmap(QPixmap.fromImage(self.image))
				self.movieTitle = resp['title']
				self.movieGenres = resp['genres']

				self.RATINGS_URL = self.SITE_URL + '/ratings/'
				r = requests.get(self.RATINGS_URL + str(self.mid))
				resp = json.loads(r.content.decode())
				self.rating = resp['rating']

				self.sub_layout = QVBoxLayout()
				self.movieTitleLabel = QLabel(self.movieTitle)
				self.movieTitleLabel.setAlignment(Qt.AlignCenter)
				self.movieGenresLabel = QLabel(self.movieGenres)
				self.movieGenresLabel.setAlignment(Qt.AlignCenter)
				self.ratingLabel = QLabel(str('{0:.2f}'.format(self.rating)))
				self.ratingLabel.setAlignment(Qt.AlignCenter)
				self.sub_layout.addWidget(self.movieTitleLabel)
				self.sub_layout.addWidget(self.imageLabel)
				self.sub_layout.addWidget(self.movieGenresLabel)
				self.sub_layout.addWidget(self.ratingLabel)

				self.upbutton = QPushButton('UP')
				self.downbutton = QPushButton('DOWN')
				self.layout = QHBoxLayout()
				self.layout.addWidget(self.upbutton)
				self.layout.addLayout(self.sub_layout)
				self.layout.addWidget(self.downbutton)

				self.setLayout(self.layout)
				self.connect(self.upbutton, SIGNAL('clicked()'), self.up_movie)
				self.connect(self.downbutton, SIGNAL('clicked()'), self.down_movie)

			def up_movie(self):
				requests.put(self.RECOMMENDATIONS_URL + str(self.uid), \
				data=json.dumps({'movie_id': int(self.mid), 'rating': 5}))

				r = requests.get(self.RECOMMENDATIONS_URL + str(self.uid))
				resp = json.loads(r.content.decode())
				self.mid = resp['movie_id']
				r = requests.get(self.MOVIES_URL + str(self.mid))
				resp = json.loads(r.content.decode())
				self.movieTitle = resp['title']
				self.movieGenres = resp['genres']
				self.imagesDirectory = '/home/paradigms/images/' + resp['img']
				r = requests.get(self.RATINGS_URL + str(self.mid))
				resp = json.loads(r.content.decode())
				self.rating = resp['rating']
				self.updateGUI()

			def down_movie(self):
				requests.put(self.RECOMMENDATIONS_URL + str(self.uid), \
				data=json.dumps({'movie_id': int(self.mid), 'rating': 1}))

				r = requests.get(self.RECOMMENDATIONS_URL + str(self.uid))
				resp = json.loads(r.content.decode())
				self.mid = resp['movie_id']
				r = requests.get(self.MOVIES_URL + str(self.mid))
				resp = json.loads(r.content.decode())
				self.movieTitle = resp['title']
				self.movieGenres = resp['genres']
				self.imagesDirectory = '/home/paradigms/images/' + resp['img']
				r = requests.get(self.RATINGS_URL + str(self.mid))
				resp = json.loads(r.content.decode())
				self.rating = resp['rating']
				self.updateGUI()

			def updateGUI(self):
				self.image = QImage(self.imagesDirectory)
				self.imageLabel.setPixmap(QPixmap.fromImage(self.image))
				self.movieTitleLabel.setText(str(self.movieTitle))
				self.movieGenresLabel.setText(str(self.movieGenres))
				self.ratingLabel.setText('{0:.2f}'.format(self.rating))

		self.central = MoviesCentral(parent=self)
		self.setCentralWidget(self.central)
	
	def exit_program(self):
		app.quit()

	def view_profile(self):
		self.USER_URL = self.central.SITE_URL + '/users/'
		r = requests.get(self.USER_URL + str(self.central.uid))
		resp = json.loads(r.content.decode())
		msg = QMessageBox()
		msg.setWindowTitle('VP')
		msg.setText('Profile\nGender: {}\nZipcode: {}\nAge:   {}'.format(resp['gender'], \
		resp['zipcode'], resp['age']))
		msg.setStandardButtons(QMessageBox.Ok)
		msg.exec_()
	
	def set_user(self):
		userNumber, ok = QInputDialog.getInt(self, 'Set User', 'User ID:')
		if ok:
			self.central.uid = int(userNumber)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	gui = MoviesQT()
	gui.show()
	sys.exit(app.exec_())
