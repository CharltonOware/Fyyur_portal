#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import sys
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_migrate import Migrate
from sqlalchemy import ForeignKey
from forms import *
from config import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database - DONE

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):

  __tablename__ = 'Venue'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  address = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))
  seeking_talent = db.Column(db.Boolean, default=False, nullable=False)
  seeking_description = db.Column(db.String(),nullable=True)
  genres = db.Column(db.ARRAY(db.String()))
  website_link = db.Column(db.String(120))
  shows = db.relationship('Show',backref='venue', lazy=True)

  #Add __repr__
  def __repr__(self):
    return f'<Venue ID: {self.id}, name: {self.name}>'

class Artist(db.Model):
  __tablename__ = 'Artist'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  genres = db.Column(db.String(120))
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))
  seeking_venue = db.Column(db.Boolean, default=False, nullable=False)
  shows = db.relationship('Show',backref='artist',lazy=True)


  def __repr__(self):
    return f'< Artist ID: {self.id}, name: {self.name}>'

#db.create_all()

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Show(db.Model):
  __tablename__ = 'shows'

  id = db.Column(db.Integer, primary_key=True)
  start_time = db.Column(db.DateTime, default=datetime.utcnow)
  artist_id = db.Column(db.Integer,ForeignKey('Artist.id', ondelete='CASCADE'),nullable=False)
  venue_id = db.Column(db.Integer,ForeignKey('Venue.id', ondelete='CASCADE'), nullable=False)

  def __repr__(self):
    return f'<Show ID: {self.id}, name: {self.name}>'


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  #Ensure formatting filter accepts datetime values too to avoid the error
  #TypeError: Parser must be a string or character stream, not datetime
  if isinstance(value, str):
    date = dateutil.parser.parse(value)
  else:
    date = value
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  areas = Venue.query.distinct(Venue.city, Venue.state).all()
  data = []
  for area in areas:
    area_data = {
      'city': area.city,
      'state': area.state
    }
    venues = Venue.query.filter_by(city=area.city, state=area.state).all()
    new_venues = []
    for venue in venues:
      #count the rows having venue_id matching this venue's id and the start_time is a time greater than this insant
      upcoming_shows = Show.query.filter_by(venue_id=venue.id).filter(Show.start_time > datetime.now()).all()
      num_upcoming_shows = len(upcoming_shows)
      new_venues.append({
        'id': venue.id,
        'name': venue.name,
        'num_upcoming_shows': num_upcoming_shows
      })
      #insert new venues into the area_data dictionary object
      area_data['venues'] = new_venues
    data.append(area_data)
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  response={
    "count": 1,
    "data": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  venue = Venue.query.filter_by(id=venue_id).first()
  shows = Show.query.filter_by(venue_id=venue.id).all()
  upcoming_shows = []
  past_shows = []
  for show in shows:
    if show.start_time > datetime.now():
      upcoming_shows.append({
        #object.backref.attribute
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": show.start_time
      })
    if show.start_time < datetime.now():
      past_shows.append({
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": show.start_time
      })
  upcoming_shows_count = len(upcoming_shows)
  past_shows_count = len(past_shows)

  venue={
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website_link,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "image_link": venue.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": past_shows_count,
    "upcoming_shows_count": upcoming_shows_count,
  }
  
  return render_template('pages/show_venue.html', venue=venue)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm()
  #if form.validate_on_submit():
  try:
    venue = Venue(name=form.name.data, 
      city=form.city.data, 
      state=form.state.data, 
      address=form.address.data,
      phone=form.phone.data, 
      image_link=form.image_link.data, 
      genres=form.genres.data, 
      facebook_link=form.facebook_link.data, 
      website_link=form.website_link.data,
      seeking_talent=form.seeking_talent.data, 
      seeking_description=form.seeking_description.data
      )
      
    db.session.add(venue)
    db.session.commit()
    # on successful db insert, flash success
    flash('Venue ' + str(form['name']) + ' was successfully listed!')
  except:
    db.session.rollback()
    flash('An error occurred.Venue '+ str(form['name']) + ' could not be listed.')
    print(sys.exc_info())
  finally:
    db.session.close()
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  venue = Venue.query.get(venue_id)
  try:
    db.session.delete(venue)
    db.session.commit()
    flash('Venue ' + venue.name + ' successfully deleted.')
  except:
    db.session.rollback()
    flash('Delete action unsuccessful!')
    print(sys.exc_info())
  finally:
    db.session.close()

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  artists = Artist.query.all()
  return render_template('pages/artists.html', artists=artists)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  response={
    "count": 1,
    "data": [{
      "id": 4,
      "name": "Guns N Petals",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  artist = Artist.query.filter_by(id=artist_id).first()
  #data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  return render_template('pages/show_artist.html', artist=artist)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  form = ArtistForm(request.form)
  artist = Artist.query.get(artist_id)
  
  try:
    artist.name = form.name.data
    artist.city = form.city.data
    artist.state = form.state.data
    artist.phone = form.phone.data
    artist.genres = form.genres.data
    artist.seeking_venue = form.seeking_venue.data
    artist.website_link = form.website_link.data
    artist.facebook_link = form.facebook_link.data
    artist.image_link = form.image_link.data
    artist.seeking_description = form.seeking_description.data

    db.session.add(artist)
    db.session.commit()
    flash('Artist' + str(form['name']) + ' successfully edited.')
  except:
    db.session.rollback()
    flash('Sorry, artist' + str(form['name']) + 'could not be updated.')
    print(sys.exc_info())
  finally:
    db.session.close()
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  # venue={
  #   "id": 1,
  #   "name": "The Musical Hop",
  #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
  #   "address": "1015 Folsom Street",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "123-123-1234",
  #   "website": "https://www.themusicalhop.com",
  #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
  #   "seeking_talent": True,
  #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
  #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  # }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  try:
    venue.name = form.name.data
    venue.genres = form.genres.data
    venue.address = form.address.data
    venue.city = form.city.data
    venue.state = form.state.data
    venue.phone = form.phone.data
    venue.website_link = form.website_link.data
    venue.facebook_link = form.facebook_link.data
    venue.image_link = form.image_link.data
    venue.seeking_talent = form.seeking_talent.data
    venue.seeking_description = form.seeking_description.data

    db.session.add(venue)
    db.session.commit()
    flash('Venue ' + str(form['name']) + ' updated successfully.')
  except:
    db.session.rollback()
    flash('Venue' + str(form['name']) + 'could not be updated.')
    print(sys.exc_info())
  finally:
    db.session.close()
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  form = ArtistForm()
  try:
    artist = Artist(name=form.name.data, 
        city=form.city.data, 
        state=form.state.data, 
        phone=form.phone.data,
        genres=form.genres.data, 
        seeking_venue=form.seeking_venue.data)

    db.session.add(artist)
    db.session.commit()
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
    db.session.rollback()
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
    print(sys.exc_info())
  finally:
    db.session.close() 
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  show_data = []
  shows = Show.query.all()
  for show in shows:
    artist = Artist.query.get(show.artist_id)
    venue = Venue.query.get(show.venue_id)
    show_data.append({
      "venue_id": show.venue_id,
      "venue_name": venue.name,
      "artist_id": show.artist_id,
      "artist_name": artist.name,
      "artist_image_link": artist.image_link,
      "start_time": show.start_time
    })
  
  return render_template('pages/shows.html', shows=show_data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  form = ShowForm()
  try:
    show = Show(
      start_time=form.start_time.data,
      artist_id=form.artist_id.data,
      venue_id=form.venue_id.data
    )
    db.session.add(show)
    db.session.commit()
    flash('Show was successfully listed!')
  except:
    db.session.rollback()
    flash('Sorry, the show listing was not successful.')
    print(sys.exc_info())
  finally:
    db.session.close()

  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
