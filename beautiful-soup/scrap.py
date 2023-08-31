import re
import pandas as pd
import requests
from bs4 import BeautifulSoup


def extract(page):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
    url = f"https://www.airlinequality.com/airline-reviews/kenya-airways/page/{page}/"
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'lxml')
    return soup


review_list = []    

def transform(soup):
    articles = soup.find_all('article', itemprop="review")
    # print(articles[0])

    for article in articles:
        # Get date when article was published
        try:
            date_published = article.find('meta', itemprop="datePublished").get('content', '')
        except:
            date_published = 'NA'

        # Get summary title overview
        try:
            summary_title = article.find("h2", class_="text_header").text
        except:
            summary_title = 'NA'
            
        # Get country of origin
        try:
            countries = article.find("h3", class_="text_sub_header userStatusWrapper")
            country = re.search(r'\((.*?)\)', countries.text).group(1)
        except:
            country = 'NA'

        # Get trip verification details
        try:
            ver_status = article.find('div', class_='text_content', itemprop='reviewBody')
            ver_pattern = r'(Trip Verified|Not Verified)'
            verification_status = re.search(ver_pattern, ver_status.get_text(strip=True)).group()
        except:
            verification_status = 'NA'
            
        # Get trip reviews
        try:
            reviews = article.find('div', class_='text_content', itemprop='reviewBody').get_text(strip=True)
            ignore_strs = ["✅Trip Verified|", "Not Verified|"]
            for i in ignore_strs:
                if reviews.startswith(i):
                    reviews = reviews[len(i):].strip()
        except:
            reviews = 'NA'
            
            
        # Get clients rating (out of ten)  
        try:
            ratings = article.find('span', itemprop="ratingValue").get_text(strip=True)
        except:
            ratings = 'NA'

        # Get clients opinion about recommending the airlines
        try:
            recommendation = article.find('td', class_='review-rating-header recommended')\
                .find_next('td', class_="review-value").text
        except:
            recommendation = 'NA'
        
        
        general_dict = {
            'date_published': date_published,
            'summary_title': summary_title,
            'country': country,
            'trip_verified': verification_status,
            'review': reviews,
            'ratings_10': ratings,
            'recommend': recommendation
        }
        
        # print(general_dict)
        
        
        # Get details about aircraft, reason for travel,cabin and route  
        class_descriptive = ['aircraft', 'type_of_traveller', 'cabin_flown', 'route']
        details_dict = {}
        
        for i in class_descriptive:
            target_descriptions = article.find('td', {'class': f'review-rating-header {i}'})
            try:    
                next_td = target_descriptions.find_next('td', class_='review-value') if target_descriptions else 'NA'
                details_dict[i] = next_td.get_text(strip=True) if next_td else 'NA'
            except:
                pass
        
        # print(details_dict)


        # Get clients rating about specific issues
        class_stars = ['seat_comfort', 'cabin_staff_service', 'food_and_beverages', 'inflight_entertainment', 
                    'ground_service', 'wifi_and_connectivity', 'value_for_money']
        stars_dict = {}
        
        for i in class_stars:
            target_stars = article.find('td', class_=f'review-rating-header {i}')
            try:
                rating_td = target_stars.find_next('td', class_='review-rating-stars') if target_stars else 'NA'
                stars_dict[i] = len(rating_td.find_all('span', class_='star fill')) if rating_td else 'NA'
                
            except:
                pass
        # print(len(stars_dict))
        
        
        data = general_dict | details_dict | stars_dict
        review_list.append(data)
        
    return review_list


for i in range(1, 6):
    print(f'Scraping from page {i}')
    raw_data = extract(page=i)
    transform(raw_data)
    

df = pd.DataFrame(review_list)
print(df.head())
