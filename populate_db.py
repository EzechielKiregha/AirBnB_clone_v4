#!/usr/bin/python3
"""Populate database with sample data"""
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User
from models.amenity import Amenity

# Helper function to check if a record exists
def record_exists(cls, **kwargs):
    """Check if a record exists in the storage."""
    all_records = storage.all(cls).values()
    for record in all_records:
        if all(getattr(record, k) == v for k, v in kwargs.items()):
            return True
    return False

# Create 5 states with example names if not already present
states = []
state_names = ['California', 'Texas', 'New York', 'Florida', 'Illinois']
for name in state_names:
    if not record_exists(State, name=name):
        state = State(name=name)
        storage.new(state)
        storage.save()
        states.append(state)
    else:
        states.append([s for s in storage.all(State).values() if s.name == name][0])

# Create 5 cities for each state with example names if not already present
city_names = {
    'California': ['Los Angeles', 'San Francisco', 'San Diego', 'Sacramento', 'Fresno'],
    'Texas': ['Houston', 'Dallas', 'Austin', 'San Antonio', 'Fort Worth'],
    'New York': ['New York City', 'Buffalo', 'Rochester', 'Albany', 'Syracuse'],
    'Florida': ['Miami', 'Orlando', 'Tampa', 'Jacksonville', 'Tallahassee'],
    'Illinois': ['Chicago', 'Aurora', 'Naperville', 'Springfield', 'Peoria']
}

for state in states:
    for city_name in city_names[state.name]:
        if not record_exists(City, name=city_name, state_id=state.id):
            city = City(name=city_name, state_id=state.id)
            storage.new(city)
            storage.save()

# Create 5 users with example data if not already present
users = []
user_data = [
    ('user1@example.com', 'password', 'John', 'Doe'),
    ('user2@example.com', 'password', 'Jane', 'Smith'),
    ('user3@example.com', 'password', 'Alice', 'Johnson'),
    ('user4@example.com', 'password', 'Bob', 'Brown'),
    ('user5@example.com', 'password', 'Charlie', 'Davis')
]

for email, password, first_name, last_name in user_data:
    if not record_exists(User, email=email):
        user = User(email=email, password=password, first_name=first_name, last_name=last_name)
        storage.new(user)
        storage.save()
        users.append(user)
    else:
        users.append([u for u in storage.all(User).values() if u.email == email][0])

# Create one place for each city with example data if not already present
cities = storage.all(City).values()
place_data = ['Sample Place']
for city in cities:
    if not record_exists(Place, name=place_data[0], city_id=city.id, user_id=users[0].id):
        place = Place(name=place_data[0], city_id=city.id, user_id=users[0].id)  # Assigning all places to the first user for simplicity
        storage.new(place)
        storage.save()

# Create 5 amenities with example names if not already present
amenities = []
amenity_names = ['WiFi', 'Pool', 'Air Conditioning', 'Free Parking', 'Pet Friendly']
for name in amenity_names:
    if not record_exists(Amenity, name=name):
        amenity = Amenity(name=name)
        storage.new(amenity)
        storage.save()
        amenities.append(amenity)
    else:
        amenities.append([a for a in storage.all(Amenity).values() if a.name == name][0])

# Assign amenities to places
places = storage.all(Place).values()
for place in places:
    for amenity in amenities:
        if amenity not in place.amenities:
            place.amenities.append(amenity)
    storage.save()

# Create 5 reviews for each place with example data if not already present
review_texts = [
    'Great place to stay!',
    'Had an amazing time!',
    'Would definitely come back.',
    'The host was very accommodating.',
    'Clean and comfortable.'
]
for place in places:
    for text in review_texts:
        if not record_exists(Review, place_id=place.id, user_id=users[0].id, text=text):
            review = Review(place_id=place.id, user_id=users[0].id, text=text)  # Assigning all reviews to the first user for simplicity
            storage.new(review)
            storage.save()

print("Database populated with sample data.")
