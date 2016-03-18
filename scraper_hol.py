from bs4 import BeautifulSoup
#created externally for parsing and manipulating HTML
import urllib.request
#internal library for making requests
import shutil
#python standard library for working with files

base_link = "http://www.parliament.uk"
expenses_base = base_link + "/mps-lords-and-offices/members-allowances/house-of-lords/holallowances/hol-expenses04/"
expense_years = [
  "201415",
  "201314",
  "201213",
  "201112",
  "201011",
  "200102-to-200809"
]

#this function downloads the contents of eachlink with a month (which is an excel file) and puts it into the newly created docs with the name from the link
def download_sheet(doc_url):
	absolute_url = base_link + doc_url
	file_name = absolute_url.rsplit('/', 1)[-1]
	# we do this to create a name for each file
	#.rsplit is a method on a string in python. '/' is by what you split in this case. It brings back a list of items in between /. 
	# [-1] means that we get the last bit - it will be our file name
	with urllib.request.urlopen(absolute_url) as response, open(file_name, 'wb') as out_file:
		#with ..as..as is an easier way to do this operation, smth built-in python
		#urllib.request.urlopen(absolute_url) grabs the contents of the excel file.
		# open is standard python function that opens a given file on the computer or creates a new one with the given name if doesnt exist. 'wb' - just googled
		shutil.copyfileobj(response, out_file)
		#built-in function with a longer name - shutil.copyfileobj
		# this function takes the content of the response variable (which is stored in memory only and is the content of an excel file)
		#and puts it into the newly-created out-file variable (which exists physically on the computer)

#this little function grabs the content of the html files we provide, reads it (a urllib thing to get the html body) and parses into a special BS format
def getHTML(url):
	html_string = urllib.request.urlopen(url).read()
	# urllib.request.ulropen is a built-in method that grabs the content of all the html (it can any file type, like xlsx, image...) while .read only takes contents of the Body. 
	# This will return a string.
	return BeautifulSoup(html_string, 'html.parser')
	# BeautifulSoup parses the content to make it easier to work with - it creates its own type of data format similar to dictionary
	#'html.parser' is a built-in thing that you put after the name of the variable that contains a string with all contents.

#this function gets the parsed content of the HTML for each year link (see above), then BS finds all tags with a link inside 
#and within it gets links to each month (they alway follow 'href' like in a key value pair), then chooses only the ones that end in xlsx, and runds next function - download
def get_doc_links(url):
	html = getHTML(url)
	document_links = html.find_all('a', class_="document")
	# .find_all is a method from BeautifulSoup that finds exlusively all html tags, in this case <a class="document"></a>
	# the output will still be in the special BS format
	for link_tag in document_links:
		link = link_tag['href']
		#href is an attribute of an html element within a tag
		if link[-4:] == "xlsx": 
			download_sheet(link)

#this block creates links containing each year and rund get_doc_links function against them (each)
for year in expense_years:
	url = expenses_base + year
	get_doc_links(url)
