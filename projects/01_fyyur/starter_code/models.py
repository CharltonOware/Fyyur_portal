from datetime import datetime
from sqlalchemy import ForeignKey
from app import db


#Define model Venue
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


#Define model Artist
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

#Define model Show
class Show(db.Model):
  __tablename__ = 'shows'

  id = db.Column(db.Integer, primary_key=True)
  start_time = db.Column(db.DateTime, default=datetime.utcnow)
  artist_id = db.Column(db.Integer,ForeignKey('Artist.id', ondelete='CASCADE'),nullable=False)
  venue_id = db.Column(db.Integer,ForeignKey('Venue.id', ondelete='CASCADE'), nullable=False)

  def __repr__(self):
    return f'<Show ID: {self.id}, name: {self.name}>'