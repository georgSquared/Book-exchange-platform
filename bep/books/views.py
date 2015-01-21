from django.template import RequestContext
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect
from user_entry.models import UserProfile
from user_entry.models import User
from books.models import Book
from django.core.urlresolvers import reverse_lazy
import urllib
import urllib2
from xml.dom import minidom
from geopy.geocoders import Nominatim
from google_distance_matrix.core import DM
from django.db import models
from django.http import HttpResponse

def approve(request):
	if request.method=='GET':
		title = request.GET['title4']
		book = Book.objects.get(title=title,owner=request.user)
		book.permission=True
		book.save()
	
		return HttpResponseRedirect("/")


def cancelreservation(request):
	if request.method=='GET':
		title = request.GET['title3']
		book = Book.objects.get(title=title,borrower=request.user)
		user = User.objects.get(username=book.borrower)
		owner = User.objects.get(username=book.owner)
		profile=user.profile
		profile2=owner.profile
		profile2.points-=1
		profile.points+=1
		profile.books_borrowed-=1
		profile.save()
		book.available=True
		book.borrower=""
		book.save()
	
		return HttpResponseRedirect("/")



def selectuser(request):
	if request.method=='GET':
		
		
		current_user = request.user
		profile = current_user.profile
		if profile.points >= 1 :
			title = request.GET['title']
			owner2 = request.GET['owner']
			owner_user = User.objects.get(username=owner2)
			profile.points-=1
			profile2=owner_user.profile
			profile2.books_borrowed+=1
			profile2.points+=1
			profile2.save()
			profile.save()
			book = Book.objects.get(title=title,owner=owner_user)
			book.borrower=current_user.username
			book.available=False
			book.save()
			return HttpResponseRedirect("/")
		else:
			return render(request, 'books/no_points.html', context_instance=RequestContext(request))

	


def makeavailable(request):

	if request.method=='GET':

		title2 = request.GET['title2']
		book2 = Book.objects.get(title=title2,owner=request.user)
		borrower_user = User.objects.get(username=book2.borrower)
		owner = User.objects.get(username=book2.owner)
		profile=borrower_user.profile
		profile.points+=1
		profile.save()
		profile2=owner.profile
		profile2.books_borrowed-=1
		profile2.save()
		book2.available=True
		book2.permission=False
		book2.borrower=""
		book2.save()
	
		return HttpResponseRedirect("/")



def search(request):
    x=0
    if request.method=='GET':
        query={'q':request.GET['q']}
        BASE_URL = "http://www.goodreads.com/"
        DEFAULT_PAGE_SIZE = 20
        titles=[]
        pictures=[]
        authors=[]
        key = "BqXOOHL6Om2KJbNWS2fig"
        secret = "n4rmxnjm1htOv5NO09WxweSZw1tLgYY5kdEdmLGFI"
        url="https://www.goodreads.com/search.xml?key=BqXOOHL6Om2KJbNWS2fig&"
        data = urllib.urlencode(query)
        req = urllib2.Request(url,data)
        response = urllib2.urlopen(req)
        xmldoc = minidom.parse(response)

        for element in xmldoc.getElementsByTagName('title'):
            x+=1
            if x >3 :     #posa vivlia tha emfanizei
                break
            titles.append(element.firstChild.nodeValue) #titloi vivliwn
        x=0
        for element in xmldoc.getElementsByTagName('image_url'):
            x+=1
            if x >3 :
                break
            pictures.append(element.firstChild.nodeValue) #eikones vivliwn

        x=0
        for element in xmldoc.getElementsByTagName('name'):
            x+=1
            if x >3 :
                break
            authors.append(element.firstChild.nodeValue) #eikones vivliwn
        
        #This is how to unify results to send to template
        results = [{'title': i[0], 'image': i[1], 'author': i[2]} for i in zip(titles, pictures, authors)]

        return render(request, 'books/bookresults.html', {'results': results}, context_instance=RequestContext(request))


def add(request):
	if request.method=="GET":
		title = request.GET['title']
		image = request.GET['image']
		author = request.GET['author']

		current_user = request.user
		book_exists = False

		#Check if the owner who has asked to add a book already owns it(in our local database) and inform him accordigly.
		#If he does not, instantiate it and increase his availabe books
		exists = Book.objects.filter(title=title, image_url=image, author=author, owner=current_user).exists()
		if exists:
			book_exists = True
		else:
			book = Book(title=title, image_url=image, author=author, owner=current_user)
			book.save()
			profile = current_user.profile
			profile.books_available+=1
			profile.save()


		return render(request, 'books/addbook.html', {'title': title, 'image': image, 'author': author, 'book_exists': book_exists}, context_instance=RequestContext(request))


def find(request):
	if request.method=="GET":
		title = request.GET['title']
		image = request.GET['image']
		author = request.GET['author']

		usernames = []
		addresses = []
		availability = []
		api_key="AIzaSyBC0Eh8gIKo3eE48lyR_n1nq2oRdTfS19I"
		current_user = request.user
		current_profile = UserProfile.objects.get(user_id=current_user.id)
		
		book_exists = True
		
		geolocator = Nominatim()
		result_coords = []
		distances = []

		if (current_profile.address is not None) and (current_profile.address != ""):

			#Get usernames and addresses of users that posses the book, if it exists in our local database.
			#If it doesnt exist, an appropriate message is given in the template
			exists = Book.objects.filter(title=title, image_url=image, author=author).exists()
			if exists:
				bookresults = Book.objects.filter(title=title, image_url=image, author=author)
				for book in bookresults:
					user = User.objects.get(id=book.owner_id)
					profile = UserProfile.objects.get(user_id=book.owner_id)
					availability.append(book.available)
					usernames.append(user.username)
					if (profile.address is not None) and (profile.address!='') :
						addresses.append(profile.address)
					else:
						addresses.append("Unspecified Location")
				

				#Retrieve latitude and longitude from addresses
				for address in addresses:
					if address!= "Unspecified Location":
						location = geolocator.geocode(address)
						lat = str(location.latitude)
						lng = str(location.longitude)

						owner_coords = lat + ', ' + lng


					else:
						#If location is unspecified, assign dummy coords(these are somewhere in the Arctic Ocean)
						owner_coords = '84.408434, 44.991876'

					result_coords.append(owner_coords)
				
				#Instansiate a distance matrix object and get distances between the user and the owners of the book
				distance_matrix = DM(api_key)
				distance_matrix.make_request(str(current_profile.address), result_coords, mode="walking")
				distance_values = distance_matrix.get_distance_values()
				
				#distance_values returns a dictionary of dictionaries, so this is the way the extract the correct values
				for origin in distance_values:
					for destination in distance_values[origin]:
						if (distance_values[origin][destination] != "ZERO_RESULTS"):
							distances.append(distance_values[origin][destination])
						else:
							distances.append("Unspecified")




			
			else:
				book_exists = False

			results = [{'username': i[0], 'distance': i[1], 'available': i[2]} for i in sorted(zip(usernames, distances, availability), key=lambda i: i[1])]
			
			return render(request, 'books/findbook.html', {'results': results, 'book_exists': book_exists, 'title': title}, context_instance=RequestContext(request))

		else:
			return render(request, 'books/noaddress.html', context_instance = RequestContext(request))