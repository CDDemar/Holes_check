import xml.etree.ElementTree as ET
import math
class Point:
	def __init__(self, Lat, Lng, Alt, Ace, ID=None, Trip_ID=None, TimeStamp=None, Speed=None):
		self.ID = ID if ID is not None else ''
		self.Trip_ID = Trip_ID if Trip_ID is not None else ''
		self.TimeStamp = TimeStamp if TimeStamp is not None else '' 
		self.Lat = Lat
		self.Lng = Lng
		self.Alt = Alt
		self.Speed = Speed if Speed is not None else -1 
		self.Ace = Ace
		self.processed = False		
	def haversine(self, candidate):
		R = 6371000
		dLat = math.radians(abs(candidate.Lat -self.Lat))
		dLng = math.radians(abs(candidate.Lng -self.Lng))
		a = (math.sin(dLat/2) *math.sin(dLat/2)) +(math.cos(math.radians(candidate.Lat)) *math.cos(math.radians(self.Lat)) *math.sin(dLng/2) *math.sin(dLng/2))
		c = 2 *math.atan2(math.sqrt(a), math.sqrt(1-a))
		d = R *c
		return d
class Trip:
	def __init__(self, ID):
		self.ID = ID
		self.points = []
		self.a_max = -1000000
		self.a_min = 1000000
		self.distance = 0
	def normalize(self):
		a_min = 1000000
		a_max = -1000000
		for point in self.points:
			if(a_min > point.Ace):
				a_min = point.Ace
			if(a_max < point.Ace):
				a_max = point.Ace

		for i, point in enumerate(self.points):
			self.points[i].Ace = (self.points[i].Ace -a_min)/(a_max -a_min)
go = True
try:
	R = input('R: ')
	try:
		R = int(R)
	except ValueError:
		go = False
except SyntaxError:
	R = 30
try:
	S = input('S: ')
	try:
		S = float(S)
	except ValueError:
		go = False
except SyntaxError:
	S = 0.8
if(go):
	print('Loading data!')
	tree = ET.parse('raw.xml')
	root = tree.getroot()
	trips = []
	bookmark = 0
	index = 0
	print('Data loaded, processing begins!')
	raw_input('Hit ENTER to continue')
	# Creando los viajes y asignandoles sus respectivos puntos:
	for database in root.findall('database'):
		for child in database:
			if(bookmark != int(child[1].text)):
				bookmark = int(child[1].text)
				if(len(trips) <= 1):
					trip = Trip(bookmark)
					if(len(trips) == 0):
						index = 0
					else: 
						index = 1
					trips.append(trip)
				else:
					exist = False
					for i, trip in enumerate(trips):
						if(trip.ID == bookmark):
							exist = True
							index = i
							break
					if(not exist):
						trip = Trip(bookmark)
						trips.append(trip)
						index = len(trips) -1
			ID = int(child[0].text)
			Trip_ID = int(child[1].text)
			TimeStamp = int(child[2].text)
			Lat = float(child[3].text)
			Lng = float(child[4].text)
			Alt = float(child[5].text)
			Speed = float(child[6].text)
			Ace = float(child[7].text)
			x = Point(Lat, Lng, Alt, Ace, ID, Trip_ID, TimeStamp, Speed)
			trips[index].points.append(x)
	# Normalizando los puntos por viaje:
	print('Normalizing all the points per trips!')
	for trip in trips:
		trip.normalize()
	# Creando un vector de puntos y ordenandolo:
	print('Sorting all the points!')
	sPoints = []
	for trip in trips:
		for point in trip.points:
			sPoints.append(point)
	sPoints.sort(key = lambda x: x.Ace, reverse=True)
	print('Finding neighborhoods!')
	neighborhoods = []
	neighborhood = []
	# P >= S y dist(cand, P) <= R!
	for point in sPoints:
		if(point.Ace >= S and not point.processed):
			neighborhood = []
			neighborhood.append(point)
			point.processed = True
			for candidate in sPoints:
				d = point.haversine(candidate)
				if(d <= R and not candidate.processed):
					neighborhood.append(candidate)
					candidate.processed = True
			# Marcar puntos de la misma ruta:
			for candidate in sPoints:
				if(point.Trip_ID == candidate.Trip_ID):
					candidate.processed = True
			neighborhoods.append(neighborhood)
	print('Finding holes!')
	holes = []
	prom_Lat = 0
	prom_Lng = 0
	prom_Alt = 0
	prom_Ace = 0
	for neighborhood in neighborhoods:
		for point in neighborhood:
			prom_Lat = prom_Lat +point.Lat
			prom_Lng = prom_Lng +point.Lng
			prom_Alt = prom_Alt +point.Alt
			prom_Ace = prom_Ace +point.Ace
		prom_Lat = prom_Lat/len(neighborhood)
		prom_Lng = prom_Lng/len(neighborhood)
		prom_Alt = prom_Alt/len(neighborhood)
		prom_Ace = prom_Ace/len(neighborhood)
		if(prom_Ace >= S):
			h = Point(prom_Lat, prom_Lng, prom_Alt, prom_Ace)
			print(h.Lat, h.Lng, h.Alt, h.Ace)
			holes.append(h)
	print('there are %d holes', len(holes))
else:
	print('Syntax error, R must be an int and S must be a float!')

raw_input('Press ENTER to exit')