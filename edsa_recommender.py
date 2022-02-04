"""

    Streamlit webserver-based Recommender Engine.

    Author: Explore Data Science Academy.

    Note:
    ---------------------------------------------------------------------
    Please follow the instructions provided within the README.md file
    located within the root of this repository for guidance on how to use
    this script correctly.

    NB: !! Do not remove/modify the code delimited by dashes !!

    This application is intended to be partly marked in an automated manner.
    Altering delimited code may result in a mark of 0.
    ---------------------------------------------------------------------

    Description: This file is used to launch a minimal streamlit web
	application. You are expected to extend certain aspects of this script
    and its dependencies as part of your predict project.

	For further help with the Streamlit framework, see:

	https://docs.streamlit.io/en/latest/

"""
# Streamlit dependencies
import streamlit as st
import streamlit.components.v1 as components

# Data handling dependencies
import pandas as pd
import numpy as np
import sweetviz as sv

# Custom Libraries
from utils.load import local_css
from utils.data_loader import load_movie_titles
from utils.api import fetch_poster, fetch_runtime ,fetch_imdbrating, fetch_plot, fetch_genre
from recommenders.collaborative_based import collab_model
from recommenders.content_based import content_model
from source import (sweet , slides)

#Api modules
import requests

    #------------------------------------------------------------------------#
    #---------------------------Data Loading---------------------------------#
    #------------------------------------------------------------------------#

title_list = load_movie_titles('../unsupervised_data/unsupervised_movie_data/movies.csv')
movies = pd.read_csv('../unsupervised_data/unsupervised_movie_data/movies.csv')
links = pd.read_csv('resources/data/movies_link.csv')

    #------------------------------------------------------------------------#
    #----------------------------Functions-----------------------------------#
    #------------------------------------------------------------------------#

def st_display_sweetviz(report_html,width=1000,height=500):
	report_file = codecs.open(report_html,'r')
	page = report_file.read()
	components.html(page,width=width,height=height,scrolling=True)

    #------------------------------------------------------------------------#    
    #--------------------------App declaration-------------------------------#
    #------------------------------------------------------------------------#

def main():
    
    st.sidebar.image("https://i.imgur.com/fXhhwGw.png")
    # DO NOT REMOVE the 'Recommender System' option below, however,
    # you are welcome to add more options to enrich your app.
    page_options = ["Recommender System","Recommend with Poster","SweetViz","EDA","Business Solutions","Slides","Meet the Team"]

    # -------------------------------------------------------------------
    # ----------- !! THIS CODE MUST NOT BE ALTERED !! -------------------
    # -------------------------------------------------------------------
    page_selection = st.sidebar.selectbox("Choose Option", page_options)
    if page_selection == "Recommender System":
        # Header contents
        st.write('# Movie Recommender Engine')
        st.write('### EXPLORE Data Science Academy Unsupervised Predict')
        st.image('resources/imgs/Image_header.png',use_column_width=True)
        # Recommender System algorithm selection
        sys = st.radio("Select an algorithm",
                        ('Content Based Filtering',
                        'Collaborative Based Filtering'))

        # User-based preferences
        st.write('### Enter Your Three Favorite Movies')
        movie_1 = st.selectbox('Fisrt Option',title_list[14930:15200])
        movie_2 = st.selectbox('Second Option',title_list[25055:25255])
        movie_3 = st.selectbox('Third Option',title_list[21100:21200])
        fav_movies = [movie_1,movie_2,movie_3]

        # Perform top-10 movie recommendation generation
        if sys == 'Content Based Filtering':
            if st.button("Recommend"):
                st.subheader('')
                try:
                    with st.spinner('Crunching the numbers...'):
                        top_recommendations = content_model(movie_list=fav_movies,
                                                            top_n=10)
                    st.title("We think you'll like:")
                    for i,j in enumerate(top_recommendations):
                        st.subheader(str(i+1)+'. '+j)
                except:
                    
                    st.error("Oops! Looks like this algorithm does't work.\
                              We'll need to fix it!")


        if sys == 'Collaborative Based Filtering':
            if st.button("Recommend"):
                try:
                    with st.spinner('Crunching the numbers...'):
                        top_recommendations = collab_model(movie_list=fav_movies,
                                                           top_n=10)
                    st.title("We think you'll like:")
                    for i,j in enumerate(top_recommendations):
                        st.subheader(str(i+1)+'. '+j)
                except:
                    st.error("Oops! Looks like this algorithm does't work.\
                              We'll need to fix it!")

    # -----------------------------------------------------------------------#
    # -------------------SAFE FOR ALTERING/EXTENSION ------------------------#
    # -----------------------------------------------------------------------#

    if page_selection == "Recommend with Poster":
        # Header contents
        st.image('resources/imgs/heading.png')
        st.markdown("<h2 style='text-align: center; color: black;'>EXPLORE Data Science Academy Unsupervised Predict</h2>", unsafe_allow_html=True)
        st.image('resources/imgs/Image_header.png',use_column_width=True)
        # Recommender System algorithm selection
        sys = st.radio("Select an algorithm",
                       ('Content Based Filtering',
                        'Collaborative Based Filtering'))

        # User-based preferences
        st.write('### Enter Your Three Favorite Movies')
        movie_1 = st.selectbox('Fisrt Option',title_list[14930:15200])
        movie_2 = st.selectbox('Second Option',title_list[25055:25255])
        movie_3 = st.selectbox('Third Option',title_list[21100:21200])
        fav_movies = [movie_1,movie_2,movie_3]

        # Perform top-10 movie recommendation generation
        if sys == 'Content Based Filtering':
            if st.button("Recommend"):

                try:
                    with st.spinner('Crunching the numbers...'):
                        top_recommendations = content_model(movie_list=fav_movies,
                                                            top_n=10)
                    st.title("We think you'll like:")
                    with st.container():
                        for i,j in enumerate(top_recommendations):
                            col1, col2, = st.columns(2)
                            with col1:
                                temp_id = links.loc[links['title'] == j].movieId.values[0]
                                id = str(links.loc[links['movieId']== temp_id].imdbId.values[0])                                
                                st.image(fetch_poster('tt'+id.zfill(7)))
                            with col2:
                                st.subheader(str(i+1)+'. '+j)
                                id = str(links.loc[links['movieId']== temp_id].imdbId.values[0])
                                st.write('Plot: ' + fetch_plot('tt'+id.zfill(7)))
                                st.write('Genre: ' + fetch_genre('tt'+id.zfill(7)))
                                st.write('Rating: ' + fetch_imdbrating('tt'+id.zfill(7) )+ '/10')
                                st.write('Runtime: ' + fetch_runtime('tt'+id.zfill(7)))
                            
                            
                except:
                    st.error("Oops! Looks like this algorithm does't work.\
                              We'll need to fix it!")
                        
        if sys == 'Collaborative Based Filtering':
            if st.button("Recommend"):
                try:
                    with st.spinner('Crunching the numbers...'):
                        top_recommendations = collab_model(movie_list=fav_movies,
                                                           top_n=10)
                    st.title("We think you'll like:")
                    with st.container():
                        for i,j in enumerate(top_recommendations):
                            col1, col2, = st.columns(2)
                            with col1:
                                temp_id = links.loc[links['title'] == j].movieId.values[0]
                                id = str(links.loc[links['movieId']== temp_id].imdbId.values[0])                                
                                st.image(fetch_poster('tt'+id.zfill(7)))
                            with col2:
                                st.subheader(str(i+1)+'. '+j)
                                id = str(links.loc[links['movieId']== temp_id].imdbId.values[0])
                                st.write('Plot: ' + fetch_plot('tt'+id.zfill(7)))
                                st.write('Genre: ' + fetch_genre('tt'+id.zfill(7)))
                                st.write('Rating: ' + fetch_imdbrating('tt'+id.zfill(7) )+ '/10')
                                st.write('Runtime: ' + fetch_runtime('tt'+id.zfill(7)))
                except:
                    st.error("Oops! Looks like this algorithm does't work.\
                              We'll need to fix it!")
    
    #------------------------------------------------------------------------#
    #                         Sweetviz report                                #
    #------------------------------------------------------------------------#

    if page_selection == "SweetViz":
        st.image('resources/imgs/sweetviz.png',use_column_width=True)
        st.markdown('Sweetviz is an open-source Python library that helps generate beautiful, highly detailed visualizations to Exploratory Data Analysis with a single line of code. It also generates a summarised report and can help create interactive dashboards as well.')
        ds = st.radio("Choose the data source", ("movies data", "ratings data"))
        if ds == "movies data":
            data_file = 'resources/data/movies.csv'
        else:
            data_file = 'resources/data/ratings.csv'
        if data_file is not None:
            df1 = pd.read_csv(data_file)
            st.dataframe(df1.head())
            if st.button("Generate Sweetviz Report"):
                report = sv.analyze(df1)
                report.show_html()
                st_display_sweetviz("SWEETVIZ_REPORT.html")

        pass

    #------------------------------------------------------------------------#
    #                               Slides                                   #
    #------------------------------------------------------------------------#

    if page_selection == "Slides":
        st.markdown(slides,unsafe_allow_html=True)

    #------------------------------------------------------------------------#
    #                               EDA                                      #
    #------------------------------------------------------------------------#   
        
    if page_selection == "EDA":
        
        st.markdown("<h1 style='text-align: center; color: black;'>Exploratory Data Analysis</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: black;'>Exploratory Data Analysis refers to the critical process of performing initial investigations on data so as to discover patterns,to spot anomalies,to test hypothesis and to check assumptions with the help of summary statistics and graphical representations.</h3>", unsafe_allow_html=True)
        if st.checkbox('Why show Eda??'):
            st.subheader('r/dataisbeautiful subscriber rank per year')
            st.image('resources/imgs/reddit.png',use_column_width=True)
        eda_select = st.selectbox('Select a Visual to inspect ',('Rating Distribution','Top review count','Average Rating by Count of Rating', 'Ratings per Year'))
        if eda_select == "Rating Distribution":
            st.image("resources/imgs/donut_ratings.png",use_column_width=True)
            st.write("Most movies where scored with a rating of 4 stars with 26.6%. Indicating that most users have not had to be subjected films like BALLISTIC: ECKS VS. SEVER which is the lowest rated film of all time on Rotten Tomatoes")
            st.image('resources/imgs/worst.png')

        #Movies Realese before and after 1995
        if eda_select == "Top review count":
                st.image("resources/imgs/top_8.png",use_column_width=True)
                st.markdown("<h3 style='text-align: center; color: black;'>Fig 1. User 72315 has rated an extreme number of movies relative to other users. For EDA purposes, this user is removed to make interpretation easier.</h3>", unsafe_allow_html=True)
                st.image("resources/imgs/top_fixed.png",use_column_width=True)
                st.markdown("<h3 style='text-align: center; color: black;'>With the outlier removed, the risk of the data being biased is lessened</h3>", unsafe_allow_html=True)
        
        #Distributins of user ratings for movies in the past 25 years
        if eda_select == "Average Rating by Count of Rating":
                st.image("resources/imgs/mean_ratings.png",use_column_width=True)
                st.write("There doesn't seem to be a relationship, as the number of ratings and how a user rates a movie do not show any correlation.")
                st.image("resources/imgs/mean_ratings2.png",use_column_width=True)
                st.write("With the outlier removed, the risk of the data being biased is lessened")

        if eda_select == "Ratings per Year":
            st.image("resources/imgs/movies_year.png",use_column_width=True)
            st.markdown("<h3 style='text-align: center; color: black;'>Possible reason for the decline in rating's around the 2000's is the economic crash in America during 2008.</h3>", unsafe_allow_html=True)
            
        pass

    #------------------------------------------------------------------------#
    #                         Business Solutions                             #
    #------------------------------------------------------------------------# 

    if page_selection == "Business Solutions":
        st.markdown("<h1 style='text-align: center; color: black;'>Business Solutions</h1>", unsafe_allow_html=True)
        st.write("The internet is a go-to space for businesses seeking to access the global marketplace. Nowadays, there is a preference among shoppers to make purchases online from the comfort of their own homes.Now more than ever it really pays to know your customer, and thanks to Recommender Systems now you can")
        st.write("Recommender Systems can assess multiple parameters to create solutions unique to the business needs. It's an effective system when expanding your business (35% of all sales on Amazon are attributed to the recommender). It ensures businesses are better equiped to provide their customers with their desired products and services, boosting business and income")
        
        
        st.markdown("<h2 style='text-align: center; color: black;'>Content Based Filtering</h2>", unsafe_allow_html=True)
        st.write("")
        col1, col2 = st.columns(2)
        with col1:
            st.image('resources/imgs/content3.png',use_column_width=True)
        with col2:
            st.write('')
            st.markdown("<p style='text-align: center; color: black;'>Content-based filtering uses item features to recommend other items similar to what the user likes, based on their previous actions or explicit feedback.Content-based filtering makes recommendations by using keywords and attributes assigned to objects in a database (e.g., items in an online marketplace) and matching them to a user profile creating some form of feature matrix. The user profile is created based on data derived from a user’s actions, such as purchases, ratings (likes and dislikes), downloads, items searched for on a website and/or placed in a cart, and clicks on product links. An example of a feature matrix:</p>", unsafe_allow_html=True)
        

        st.markdown("<h2 style='text-align: center; color: black;'>Collaborative Filtering</h2>", unsafe_allow_html=True)
        st.write("")
        col1, col2 = st.columns(2)
        with col1:
            st.image('resources/imgs/collab2.png',use_column_width=True)
        with col2:
            st.markdown("<p style='text-align: center; color: black;'>Collaborative filtering uses algorithms to filter data from user reviews to make personalized recommendations for users with similar preferences. This is the hallmark for Recommender Systems, Giving greater insights into what users/customers are interested</p>", unsafe_allow_html=True)

    #------------------------------------------------------------------------#
    #                              Meet the Team                             #
    #------------------------------------------------------------------------# 
    if page_selection == "Meet the Team":
        st.markdown("<h1 style='text-align: center; color: black;'>Meet the Team</h1>", unsafe_allow_html=True)
        st.image('resources/imgs/team.png',use_column_width=True)
        st.markdown("<h2 style='text-align: center; color: black;'>Contact Info</h2>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("<p style='text-align: center; color: black;'>Drikus De Wet</p>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: black;'>jchdewet@gmail.com</p>", unsafe_allow_html=True)
        with col2:
            st.markdown("<p style='text-align: center; color: black;'>Euphrasia Mampuru</p>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: black;'>euphrasiacm@gmail.com</p>", unsafe_allow_html=True)

        with col3:
            st.markdown("<p style='text-align: center; color: black;'>Macdaline Mathye</p>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: black;'>mathyemacdaline@gmail.com</p>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<p style='text-align: center; color: black;'>Gabriel Maja</p>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: black;'>gabemaja10@gmail.com</p>", unsafe_allow_html=True)

        with col2:
            st.markdown("<p style='text-align: center; color: black;'>Robert Mackintosh</p>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: black;'>robertmack101@gmail.com</p>", unsafe_allow_html=True)

    #------------------------------------------------------------------------# 

if __name__ == '__main__':
    main()
