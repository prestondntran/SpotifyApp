from django.http import HttpResponse
from django.template import loader
import recs.spotifyrec as spotifyrec

def main(request):
  template = loader.get_template('main.html')
  return HttpResponse(template.render())

def artistrec(request):
  template = loader.get_template('artistrec.html')
  return HttpResponse(template.render())

def trackrec(request):
  template = loader.get_template('trackrec.html')
  return HttpResponse(template.render())

def genrerec(request):
  template = loader.get_template('genrerec.html')
  genreSeeds = spotifyrec.getGenreSeeds()["genres"]
  context = {
    'genreSeeds': genreSeeds
  }
  return HttpResponse(template.render(context, request))

def searchArtist(request):
  if (request.method == 'POST'):
    searchQuery = request.POST['searchQuery']
    template = loader.get_template('artistrec.html')

    # if search bar is empty
    if (searchQuery == ""):
      return HttpResponse(template.render())

    results = spotifyrec.search(searchQuery, "artist")

    # store all metadata of artists in searchResults
    artists = []
    artistImages = []
    indices = [] # for which track the user selects
    i = 0
    for result in results:
      artists.append(result[0])
      artistImages.append(result[1])
      indices.append(i)
      i += 1
    searchResults = zip(artists, artistImages, indices)

    context = {
      'query': searchQuery,
      'searchResults': searchResults
    }
    return HttpResponse(template.render(context, request))

def searchTrack(request):
  if (request.method == 'POST'):
    searchQuery = request.POST['searchQuery']
    template = loader.get_template('trackrec.html')

    # if search bar is empty
    if (searchQuery == ""):
      return HttpResponse(template.render())

    results = spotifyrec.search(searchQuery, "track")

    # store all metadata of tracks in searchResults
    tracks = []
    artists = []
    trackArts = []
    indices = [] # for which track the user selects
    i = 0
    for result in results:
      tracks.append(result[0])
      artists.append(result[1])
      trackArts.append(result[2])
      indices.append(i)
      i += 1
    searchResults = zip(tracks, artists, trackArts, indices)

    context = {
      'query': searchQuery,
      'searchResults': searchResults
    }
    return HttpResponse(template.render(context, request))

def recResults(request):
  # if search type is artist or track
  if (request.method == 'GET'):
    name = request.GET.get('name')
    index = request.GET.get('index')
    searchType = request.GET.get('searchType')
  # if search type is genre
  elif (request.method == 'POST'):
    name = request.POST['genre']
    index = 0
    searchType = "genre"

  results = spotifyrec.getRecs(name, index, searchType)
  # load appropriate template based on search type
  if (searchType == "track"):
    template = loader.get_template('trackrec.html')
  elif (searchType == "artist"):
    template = loader.get_template('artistrec.html')
  else:
    template = loader.get_template('genrerec.html')

  # store all metadata of tracks in recResults
  tracks = []
  artists = []
  trackArts = []
  for result in results:
    tracks.append(result[0])
    artists.append(result[1])
    trackArts.append(result[2])
  recResults = zip(tracks, artists, trackArts)
  genreSeeds = spotifyrec.getGenreSeeds()["genres"]

  context = {
    'name': name,
    'recResults': recResults,
    'genreSeeds': genreSeeds
  }
  return HttpResponse(template.render(context, request))