from datetime import datetime
from sqlalchemy import ForeignKey, Enum
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#Define Genres class for Enum restriction
# class Genres(Enum):
#   ALTERNATIVE = 'Alternative'
#   BLUES = 'Blues'
#   CLASSICAL = 'Classical'
#   COUNTRY = 'Country'
#   ELECTRONIC = 'Electronic'
#   FOLK = 'Folk'
#   FUNK = 'Funk'
#   JAZZ = 'Jazz'
#   REGGAE = 'Reggae'
#   HIP_HOP = 'Hip-hop'
#   HEAVY_METAL = 'Heavy metal'
#   INSTRUMENTAL = 'Instrumental'
#   MUSICAL_THEATRE = 'Musical theatre'
#   ROCK_N_ROLL = 'Rock n roll'
#   POP = 'Pop'
#   PUNK = 'Punk'
#   RNB = 'R&B'
#   SOUL = 'Soul'
#   OTHER = 'Other'

#   @staticmethod
#   def fetch_genres():
#     for genre in Genres:
#       return genre.value


#Define model Venue
class Venue(db.Model):

  __tablename__ = 'Venue'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(),nullable=False)
  city = db.Column(db.String(120),nullable=False)
  state = db.Column(db.String(120),nullable=False)
  address = db.Column(db.String(120),nullable=False)
  phone = db.Column(db.String(120))
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120), nullable=False)
  seeking_talent = db.Column(db.Boolean, default=False, nullable=False)
  seeking_description = db.Column(db.String(),nullable=True)
  genres = db.Column(db.ARRAY(db.String()),nullable=False)
  #genres = db.Column(db.Enum(Genres, values_callable=lambda x: [genre.value for genre in Genres]))
  website_link = db.Column(db.String(120), nullable=False)
  shows = db.relationship('Show',backref='venue', passive_deletes=True, lazy=True)

  #Add __repr__
  def __repr__(self):
    return f'<Venue ID: {self.id}, name: {self.name}>'


#Define model Artist
class Artist(db.Model):
  __tablename__ = 'Artist'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(), nullable=False)
  city = db.Column(db.String(120),nullable=False)
  state = db.Column(db.String(120),nullable=False)
  phone = db.Column(db.String(120), nullable=False)
  genres = db.Column(db.ARRAY(db.String()), nullable=False)
  # genres = db.Column(db.Enum(Genres, 
  #   values_callable=lambda x: [genre.value for genre in Genres]))
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120), nullable=False)
  website_link = db.Column(db.String(120), nullable=False)
  seeking_venue = db.Column(db.Boolean, default=False, nullable=False)
  shows = db.relationship('Show',backref='artist', passive_deletes=True, lazy=True)


  def __repr__(self):
    return f'< Artist ID: {self.id}, name: {self.name}>'

#Define model Show
class Show(db.Model):
  __tablename__ = 'shows'

  id = db.Column(db.Integer, primary_key=True)
  start_time = db.Column(db.DateTime, default=datetime.utcnow)
  artist_id = db.Column(db.Integer,ForeignKey('Artist.id', ondelete='CASCADE'),nullable=False)
  venue_id = db.Column(db.Integer,ForeignKey('Venue.id', ondelete='CASCADE'), nullable=False)

  def __repr__(self):
    return f'<Show ID: {self.id}, name: {self.name}>'