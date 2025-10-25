# Required libraries
import json
import requests as re
from io import BytesIO
import textwrap as tw
import customtkinter as ctk
from PIL import Image, ImageTk


# Variables to make things easier
body = '#f2f2f7'
option_color = '#007aff'
url = ''
api = 'apiKey=6ff68bb78238495aa13017d62e6eceae'
count = False
sort = True
txt_coll = '#1c1c1e'
txt_col = '#8e8e93'
font = 'Lucida Handwriting'


# Function to set up the url based on what the user selected, send a request to that url, loop through the request and create frames to store each article
def get_news():
    for widget in bottom_frame.winfo_children():
        widget.destroy()

    global url, count, sort

    # Initialise the beginning of the url
    url = 'https://newsapi.org/v2/'

    # Check if we are getting every news article
    if news_type_option.get().lower() == 'everything':
        count = False
        url = url + 'everything?'
        sort = True
    else:
        count = True
        sort = False
        url += 'top-headlines?'

    # Add topics
    url += f'q={que_option.get().lower()}&'

    # Add a language
    url += f'lang={lang_option.get().lower()}&'

    # Check if to add a country
    if count:
        url += f'country={country_option.get().lower()}&'

    # Check if we can sort
    if sort:
        url += f'sortBy={sort_option.get().lower()}&'

    url += api

    # For debugging
    print(url)

    # Send a request to the constructed url
    try:
        n = re.get(url)
        new = json.dumps(n.json(), indent=4)     # Just to get a better view of the json
        news = n.json()


        # Get the number of articles gotten
        res = ctk.CTkLabel(bottom_frame, text=f"{news['totalResults']} Total Articles ", font=(font, 15, 'bold'), text_color=txt_coll)
        res.pack(pady=5)

        # Check if the response has an article
        if "articles" not in news or len(news["articles"]) == 0:
            ctk.CTkLabel(bottom_frame, text="No articles found.", font=(font, 18, 'bold')).pack(pady=10)
            return

        # Loop through the response to get required information
        for n in range(len(news['articles'])):

            # Assign information to variables
            author = news['articles'][n]['author']
            image_url = news['articles'][n]['urlToImage']
            article_title = news['articles'][n]['title']
            content = news['articles'][n]['description']

            # Create a frame for each article
            news_frame = ctk.CTkFrame(bottom_frame, fg_color="#ffffff", height=550, corner_radius=20)
            news_frame.pack(padx=10, pady=5, fill='x')
            news_frame.pack_propagate(False)

            info_frame = ctk.CTkFrame(news_frame, fg_color="transparent")
            info_frame.pack(anchor='nw')
            info_frame.pack_propagate(True)

            # Check if an author was gotten
            if author:
                author_lab = ctk.CTkLabel(info_frame, text=tw.fill(author, width=20), font=(font, 20, 'bold'), text_color='black')
                author_lab.pack(side='right', padx=(30, 5), pady=5)
            else:
                author_label = ctk.CTkLabel(info_frame, text='No Author', font=(font, 18, 'bold'), text_color='black').pack(anchor='e', side='right', padx=(90, 5), pady=10)


            # Get the image af each article
            try:
                img = re.get(image_url)
                article_image = Image.open(BytesIO(img.content))
                image_ctk = ctk.CTkImage(light_image=article_image, dark_image=article_image, size=(400, 350))
                image_label = ctk.CTkLabel(info_frame, text='', image=image_ctk, corner_radius=50)
                image_label.pack(side='left', padx=0, pady=15)
            except:
                img = re.get('https://eagle-sensors.com/wp-content/uploads/unavailable-image.jpg')
                article_image = Image.open(BytesIO(img.content))
                image_ctk = ctk.CTkImage(light_image=article_image, dark_image=article_image, size=(400, 350))
                image_label = ctk.CTkLabel(info_frame, text='', image=image_ctk, corner_radius=50)
                image_label.pack(anchor='nw', padx=0, pady=15)

            # Get the title
            ctk.CTkLabel(news_frame, text=tw.fill(article_title, width=65), font=('Helvetica', 17, 'bold'), text_color=txt_coll).pack()

            # Check for and Get Contents
            if not content:
                content = 'No content available.'
            ctk.CTkLabel(news_frame, text=tw.fill(content, width=85), font=('Verdana', 16), text_color=txt_coll).pack(pady=5)

    except re.exceptions.ConnectionError:
        print('Make sure you have an Internet Connection')



# Function to get what is available
def check_choice(choice):
    if news_type_option.get().lower() == 'everything':
        country_option.configure(values=other)
        country_option.set('none')

        sort_option.configure(values=sort_by)
        sort_option.set('Relevance')
    else:
        country_option.configure(values=country)
        country_option.set('us')

        sort_option.configure(values=other)
        sort_option.set('none')
    print(country_option.get())

root = ctk.CTk()
root.title('Briefly')
root.resizable(False, False)
root.iconbitmap('newspaper.ico')
root.geometry('780x500')
ctk.set_default_color_theme("dark-blue")


# User Options
news_type = ['Everything', 'Top-Headlines']
country = ['ae', 'ar', 'at', 'ca', 'ch', 'fr', 'jp', 'ng', 'us']
other = ['none']
lang = ['en']
que = ['news', 'politics', 'economy', 'technology', 'sports', 'health', 'science', 'education', 'entertainment', 'business', 'environment', 'weather', 'travel', 'tesla']
sort_by = ['Relevance', 'Popularity']

top_frame = ctk.CTkFrame(root, fg_color=body, height=60, corner_radius=0)
top_frame.pack(side='top', fill='x')


title = ctk.CTkLabel(top_frame, text='Briefly News ', font=(font, 40, 'bold'), width=60, text_color=txt_coll)
title.grid(row=0, sticky='w', padx=10, pady=10, columnspan=2)

getnews = ctk.CTkButton(top_frame, text='Get News', command=get_news, fg_color=option_color, corner_radius=5, hover_color='#4ca1ff')
getnews.grid(row=0, column=4, padx=10, pady=10)


bottom_frame = ctk.CTkScrollableFrame(root, fg_color=body, height=400, corner_radius=0)
bottom_frame.pack(side='top', fill='x')
# bottom_frame.pack_propagate(False)

typ = ctk.CTkLabel(top_frame, text='Type: ', text_color=txt_col, font=(font, 13, 'bold'))
typ.grid(column=0, row=1, sticky='w', padx=5)
news_type_option = ctk.CTkOptionMenu(top_frame, values=news_type, width=10, corner_radius=5, fg_color=option_color, command=check_choice)
news_type_option.grid(column=0, row=1, padx=(45, 0), pady=20)

c = ctk.CTkLabel(top_frame, text='Country: ', text_color=txt_col, font=(font, 13, 'bold'))
c.grid(column=1, row=1, sticky='w', padx=5)
country_option = ctk.CTkOptionMenu(top_frame, values=other, width=10, corner_radius=5, fg_color=option_color)
country_option.grid(column=1, row=1, padx=(75, 0), pady=20)

l = ctk.CTkLabel(top_frame, text='Language: ', text_color=txt_col, font=(font, 13, 'bold'))
l.grid(column=2, row=1, sticky='w', padx=5)
lang_option = ctk.CTkOptionMenu(top_frame, values=lang, width=10, corner_radius=5, fg_color=option_color)
lang_option.grid(column=2, row=1, padx=(95, 0), pady=20)

q = ctk.CTkLabel(top_frame, text='Topics: ', text_color=txt_col, font=(font, 13, 'bold'))
q.grid(column=3, row=1, sticky='w', padx=5)
que_option = ctk.CTkOptionMenu(top_frame, values=que, width=10, fg_color=option_color)
que_option.grid(column=3, row=1, padx=(65, 0), pady=20)

s = ctk.CTkLabel(top_frame, text='Sort: ', text_color=txt_col, font=(font, 13, 'bold'))
s.grid(column=4, row=1, sticky='w', padx=5)
sort_option = ctk.CTkOptionMenu(top_frame, values=sort_by, width=10, fg_color=option_color)
sort_option.grid(column=4, row=1, padx=(50, 15), pady=20)


root.mainloop()