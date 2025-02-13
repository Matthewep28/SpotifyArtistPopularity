# SpotifyArtistPopularity
Description
Analyzed Spotify and US Billboard 100 data using python to explore music trends, focusing on international artists, collaborations, and genre relevance. Using Spotify and Wikidata APIs, I examined how artist origin and song features influenced chart success. Linear and logarithmic regression analyses showed that popularity trends were more artist-driven than genre or regional factors. Key findings included signs of Latin America emerging as a growing market, a sharp decline in genre diversity since 1995, and a significant drop in the average song duration on the charts with the advent and growth of Spotify.

Index
1. 'Perez Spoify Artist Popularity Capstone.pdf' - Final presentation of Capstone done in Tabaleu. *Annotated*
2. 'Perez 16.2 Python Analysis' - Directory of all signigcant python files created for this project, inlcuidng APIs for data retrival, graphs, and data cleaning.

   
        a. 'Amount_Of_Songs_To_Popularity_Score_Graph.py' - Linear Regression of an artists' number of songs on Billboard100 to Spotify Popularity Score
        b. 'Billboard100_Avg_Stay_BNW.py' - Box and Whisker plot to show average duration a song will stay on the Billboard100
        c. 'Genre_History_Graph.py' - Line Graph showing what percent a genre make of total Billboard 100 songs by year, since 1975 
        d. 'International_Markets_To_Popularity_Score.py' - Linear Regression of number international markets an artist will appear in the Spotify Daily              50 to Spotify Popularity Score
        e. 'Number_Of_Featured_Artists_OverTime.py' - Line graph of number of songs on Billboard 100 since 1990 that feature multiple artists
        f. 'Number_Of_Unique_Songs_By_Artist.py' - Counts the number of unique songs an Artist has had on the billboard 100 (to be used in a linear                   regression model later)
        g. 'Parsed_Artist_Names.py' - Code that parses artists names so that songs with mutliple artists can ID each unique artist
        h. 'Regional_Growth_AreaChart.py' - Area Chart of the regional makeup of artists' origins featured on Billboard 100 
        i. 'Regional_Growth_PieChart.py' - Pie Chart showing the regional makeup of artists of the Billboard 100 in 2005 vs 2021
        j. 'Regional_Growth_Rate_BarGraph.py' - Bar Graph showing the growth rate regions made between 2005 and 2021
        k. 'SpotiftyApi_Template.py' - Template of how I called the Spotify API to populate my datasets with additional information on artists and genres
        l. 'Spotify_Avg_Stay_BNW.py' - Box and Whisker plot to show average duration a song will stay on the Spotify Daily 50 (US)
        m. 'Top_10_Hits_to_Popularity_Score_Graph.py' - Linear Regression of an artists' number of songs that reached the Billboard100's top 10 to                    Spotify Popularity Score
        n. 'Top_Foreign_Countries.py' - Bar Graph showing which countries Internatinal Artists orginated the most between 2015 - 2021
        o. 'Weeks_On_BillBoard100_to_Popularity_Score_Graph.py' - Counts the number of weeks an artist was on Billboard 100 between all of their songs 
        p. 'WikidataAPI_Artist_Origin.py' - Using Wikidata API to find the origin/birthplace of artists


