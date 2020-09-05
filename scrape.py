import requests
from bs4 import BeautifulSoup

# function to sort list of dictionaries 
# from the smallest numbers of votes to the largest
def sort_stories_by_votes(lst):
	return sorted(lst, key=lambda item:item['votes'], reverse=True)

# function to select news with the number of votes 
# greater than or equal to 100
def create_custom(links, subs):
	lst=[]
	for index, item in enumerate(links):
		vote = subs[index].select('.score')
		# a record must have votes
		if len(vote):
			point = int(vote[0].getText().replace('points', ''))
			if point > 99:
				title = links[index].getText()
				href = links[index].get('href', None)
			
				lst.append({'title' : title, 'link' : href, 'votes' : point})
	return sort_stories_by_votes(lst)

# function to form https request and get links and subs for a page
def get_links_and_subs_for_page(page_number):
	https = 'https://news.ycombinator.com/news'
	if page_number > 1:
		https +='?p=' + str(page_number)
	res = requests.get(https)
	if not res.status_code == 200:
		raise Exception(f"Error with opening page {page_number}")
	bs = BeautifulSoup(res.text, 'html.parser')
	# in select : argument '.smth' means class, '#smth' means id
	# on the last page itemlist is empty
	if not bs.select('.itemlist')[0].getText().replace('\n', ''):
		raise Exception(f"Page {page_number} doesn\'t have any news!")
	links = bs.select('.storylink')
	subs =  bs.select('.subtext')
	return links, subs

def main():
	try:
		mega_links, mega_subs = get_links_and_subs_for_page(1)
		print(f"Page 1 was read!")
		page_num = 2
		while True:
			links, subs = get_links_and_subs_for_page(page_num)
			mega_links += links
			mega_subs += subs
			print(f"Page {page_num} was read!")
			page_num += 1
	except Exception as err:
		print(err)
	finally:
		hn = create_custom(mega_links, mega_subs)
		with open('result.txt', 'w', encoding='utf-8') as file:
			for dict_record in hn:
				for key, value in dict_record.items():
					file.write(f"{key} : {value} \n")
				file.write(f"\n")
		print(f"Number of news = {len(hn)}")

if __name__ == '__main__':
	main()
