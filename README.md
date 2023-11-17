# ada-2023-project-adacalypse
## Modern Times: Rise of Technology in Cinema


### Abstract
Cinema is a form of art that has blossomed in the 20th century and has nowadays become a major medium and a reflection of our society and values. In this project, we are interested in exploring and analyzing how technological evolution shaped the movie industry. This evolution can be characterized by events such as the inclusion of sound and color, the invention and use of atomic bombs, the space race and moon landing, and the rise of the internet and social media. We believe that we should observe a two-fold impact of technology on our dataset: one is on the technology used to produce the movies in itself, thus impacting actor careers and film genres; the other is technology itself as a narrative theme appearing in plot summaries. We seek to measure, through a statistical and data-centered lens, this cultural evolution. Alternatives ideas: 


### Research questions 
- **Lost movies:** Lost films are movies of which there is no surviving print. We want to study how the digitalization of films has reduced the amount of lost films. Were some actors completely forgotten after the loss of the film they starred in? 
- **Introduction of sound and color:** To what degree did the introduction of sound and color change the relevance of actors? Were some silent-era actors pushed out of the medium due to new challenges of speaking lines? How fast was the transition from silent to sound, from monochrome to color, and why? 
- **Historical events parallelisation:** We seek time-wise correlation between historical technological advances and related films. Which movies and time periods were particularly influential? What are some of the main technological themes per each decade?
- **Sentiment analysis:** 
    - **Tech in real life:** How have film genres diversified and grown with advancements in video editing and special effects? Given these advancements, has the public become more picky about CGI? Which movies were seen as visual marvels in the past and are now looked back on in horror? 
    - **Tech in movies:** In the second part, we want to investigate the sentiment on technology related elements present in the movie.


### Alternatives ideas
**Themes:** War and Feminism were also considered as alternative thematics, as they both have a great narrative and real impact on the movie industry. 
**Research question:** Explore narrative around technology: is it seen as good for humanity, bad, or somewhere in-between. For this moral analysis we could use eMFDscore on related movies. 


### Methods
- **Lost movies:** Time and country trend visualization. We find the concerned actors and evaluate their careers.
- **Introduction of sound and color:** Visualization of decrease in silent (and similarly black-and-white) films across years, as well as of the difference in number of movies of concerned actors in silent and non-silent films. Death and retirement will be taken into account as confounders.  
- **Historical events parallelisation:** We measure the Maximum Information Coefficient between technology adoption in the HCCTA dataset and term frequency in the plot summaries every year to see how closely narrative trends follow technological trends. Then we perform the same analysis grouped by film genre. We seek out the most influential movies by finding the earliest and highest-revenue movie whose plot contains a technological keyword. Finally, we employ Autophrase to extract keyphrases with high term-frequency inverse-document-frequency TF-IDF score per decade, and visualize the results with word-clouds.
    - **MIC(X,Y):** The mutual information (expected KL-divergence between joint distribution and product of marginal distributions) scaled down by the minimum number of bins used for discretization.
    - **TF-IDF:** The product of term-frequency (count) and log-inverse document frequency (proportion of documents in which a term appears).
- **Sentiment analysis:**
    - **Tech in real life:** TextBlob and Vader are used for sentiment analysis on reviews about technology. Keyword identification will be done with the help of OpenAI API. To analyze general opinion change on old movies, we take advantage of the review_type of RottenTomates (rotten or fresh).
    - **Tech in movies:** For this we need to identify which movies are tech-related. We start by filtering the genres. We also group together all words present in all summaries (after preprocessing) and we use OpenAi API to identify which words are tech-related with 2 consecutives prompts. This corpus of tech-related words are used as a count metric to identify how many tech-related words each plot summary has. This metric helps filtering movies where technology elements are not present enough for a sentiment analysis. 


### Proposed additional datasets
- **[Lost Movie Wikibase](https://en.wikipedia.org/wiki/List_of_lost_films):** (<1Mb) List of most relevant US lost movies. This lists 107 movies along with their director, release year, cast, and historical notes. From this list, 48 are also listed in our movie data. It is only a small sample but as it lists prominent known films, it could still be of a certain relevance. 
- **[HCCTA](https://www.nber.org/research/data/historical-cross-country-technology-adoption-hccta-dataset):** (1.6 Mb) A dataset for the analysis of technology adoption patterns over the last 250 years. The missing values are encoded as full-stops. The data is mostly from large western countries. Examples of technologies include industrial robots (count), railway line length (km), mobile phones owned (count), private cars (count).
- **[IMDB Ratings](https://developer.imdb.com/non-commercial-datasets/):** (70 Mb) Dataset that contains ratings of films (0-10) and the number of votes. Each film has an ‘imdb_id’ that has been mapped to ‘wikipedia_id’.
- **[RottenTomatoes](https://www.kaggle.com/datasets/stefanoleone992/rotten-tomatoes-movies-and-critic-reviews-dataset/data?select=rotten_tomatoes_critic_reviews.csv):** rotten_tomatoes_critic_reviews (214 Mo) and rotten_tomatoes_movies (16.3 Mo) were merged on id to link the reviews with movie names and release year. Dataset contains movie reviews from the RottenTomatoes website.
- **[Wikipedia](https://fr.wikipedia.org):** Complete release date information. For this data, as well as the next entry, web scraping was performed by checking the html script based on the wikipedia and imdb IDs.
- **[BoxOfficeMojo](https://www.boxofficemojo.com/):** Complete the box office information


### Proposed timeline 
We modularised and ordered the different tasks in time to enable a flexible and efficient organization. The modules are the following:
1. Further Analysis of Data
    - Sentiment analysis of summaries of movies related to technologyof reviews of movies related to technology
    - Extract phrases using Autophrase in order to make word clouds related to technology 
    - Historical event parallelization 
        - Choice of relevant keywords (see results of b)
        - Find mutual information/maximum information coefficient between technology events and keywords related to these event in the plot summaries
    - Lost Movies Analysis
        - Lost actors: find the old forgotten pop stars
        - Identify the most popular remakes
    - Remakes: identify how movies were remade as time and technology develops
2. Website
    - Narrative
    - Structure
        - Text
        - Visualisation
3. Code fusion and cleaning
4. README writing



