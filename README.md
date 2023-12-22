# ada-2023-project-adacalypse

## Repository organisation

📁 *code* contains our main python notebook **P3_notebook.ipynb** as well as python code files with auxiliary or reusable logic.

📁 *data* contains primary data sources as well as intermediate results. More details about each file's usage can be read in the folder's README.md. The motivation for each source can be read below.

## Modern Times: Rise of Technology in Cinema

Find our website here : [https://adacalypse.github.io/modern-times-ADA/](https://link-url-here.org](https://adacalypse.github.io/modern-times-ADA/)

### Abstract
Cinema is a form of art that has blossomed in the 20th century and has nowadays become a major medium and a reflection of our society and values. In this project, we are interested in exploring and analyzing how technological evolution shaped the movie industry. This evolution can be characterized by events such as the invention of sound and color film, nuclear power, various modes of transport, the space race, computers, and the rise of the internet. We believe that we should observe a two-fold impact of technology on our dataset: one is on the technology used to produce the movies in itself, thus impacting actor careers, film genres, and popular opinion; the other is technology itself as a narrative theme appearing in plot summaries. We seek to measure, through a statistical and data-centered lens, this cultural evolution.


### Research questions 
- **Lost movies:** Lost films are movies of which there is no surviving print. We want to study how the digitalization of films has reduced the amount of lost films. Were some actors completely forgotten after the loss of the film they starred in? 
- **Remakes:** Which stories are so popular that they were remade over and over with the help of new technologies and opportunities?
- **Introduction of sound and color:** To what degree did the introduction of sound and color change the relevance of actors? Were some silent-era actors pushed out of the medium due to new challenges of speaking lines? How fast was the transition from silent to sound, from monochrome to color, and why? 
- **Technological development:** We seek to measure time-wise correlation between historical technological advances and the proportion of films related to that technology. Which movies and time periods were particularly influential? What are some of the main technological themes per each decade? 
- **Sentiment analysis:** 
    - **Tech in real life:** How have people's opinions changed with regard to certain technologies, such as CGI and VFX? Are certain techniques favoured in certain genres? Which movies were seen as visual marvels in the past and are now looked back on in horror? 
    - **Tech in movies:** How are technologies written about in movies? Which technologies are seen as good, or bad? How does this break down per genre?


### Methods
- **Lost movies and remakes:** Time trend visualization. We find the concerned actors and evaluate their careers. We computed top ten lost movies (by lost actor count) and top ten most remade films.
- **Introduction of sound and color:** Visualization of decrease in silent (and similarly black-and-white) films across years, as well as the difference in number of movies of concerned actors in silent and non-silent films. Death and retirement are taken into account as confounders with exact matching.  
- **Technological development:** We employ [Autophrase](https://github.com/shangjingbo1226/AutoPhrase) to extract high quality keyphrases from the movie plot summaries, and record those with the highest TF-IDF score, where a document is a decade's worth of plot summaries. We seek out the most influential movies by finding the highest-revenue movies in the year where the phrases appear for the first time. Then, for every available country, we measure the Maximum Information Coefficient between technology adoption in the HCCTA dataset and number of movies with the relevant technology present in the plot summaries every year to see how closely narrative trends follow technological trends. 
    - **MIC(X,Y):** The maximum information coefficient, computed with [MINEPY](https://github.com/minepy/mictools), is the mutual information (expected KL-divergence between joint distribution and product of marginal distributions) scaled down by the minimum number of bins used for discretization. 
    - **TF-IDF:** The product of term-frequency (count) and log-inverse document frequency (proportion of documents in which a term appears).
- **Sentiment analysis:**
    - **Tech in real life:** A pretrained [BERT model](https://huggingface.co/finiteautomata/bertweet-base-sentiment-analysis) is used for sentiment analysis on reviews about tech-related films. Keyword identification is be done with the help of OpenAI API. To analyze general opinion change on old movies, we take advantage of the review_type of RottenTomates (rotten or fresh).
    - **Tech in movies:** For this we need to identify which movies are tech-related. We start by filtering the genres. We also group together all words present in all summaries (after preprocessing) and we use OpenAi API (text-davinci-003 model) to identify which words are tech-related with 2 consecutives prompts. This corpus of tech-related words are used as a count metric to identify how many tech-related words each plot summary has. This metric helps filtering movies where technology elements are not present enough for a sentiment analysis. 


### Proposed additional datasets
- **[Lost Movie Wikibase](https://en.wikipedia.org/wiki/List_of_lost_films):** (<1Mb) List of most relevant US lost movies. This lists 107 movies along with their director, release year, cast, and historical notes. From this list, 48 are also listed in our movie data. It is only a small sample but as it lists prominent known films, it could still be of a certain relevance. 
- **[HCCTA](https://www.nber.org/research/data/historical-cross-country-technology-adoption-hccta-dataset):** (1.6 Mb) A dataset for the analysis of technology adoption patterns over the last 250 years. The missing values are encoded as full-stops. The data is mostly from large western countries. Examples of technologies include industrial robots (count), railway line length (km), mobile phones owned (count), private cars (count).
- **[RottenTomatoes](https://www.kaggle.com/datasets/stefanoleone992/rotten-tomatoes-movies-and-critic-reviews-dataset/data?select=rotten_tomatoes_critic_reviews.csv):** rotten_tomatoes_critic_reviews (214 Mo) and rotten_tomatoes_movies (16.3 Mo) were merged on id to link the reviews with movie names and release year. Dataset contains movie reviews from the RottenTomatoes website.
- **[Wikipedia](https://fr.wikipedia.org):** (<1Mb) Additional movie release date information, for the purposes of augmenting the data.
- **[BoxOfficeMojo](https://www.boxofficemojo.com/):** (<1Mb) Additional box office information, for the purposes of augmenting the data.


### Organization within team
Work was highly collaborative (and effective!), so it is difficult to exactly attribute work to specific individuals, but here is an approximation of the task distribution:

<table class="tg" style="table-layout: fixed; width: 342px">
<colgroup>
<col style="width: 16px">
<col style="width: 180px">
</colgroup>
<thead>
  <tr>
    <th class="tg-0lax">Teammate</th>
    <th class="tg-0lax">Contributions</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td class="tg-0lax">Amine </td>
    <td class="tg-0lax"> (1) Web scraping to recover missing information <br> (2) Plot summaries preprocessing  <br> (3) ChatGPT API prompting for tech-word identification <br> (4) Targeted Sentiment analysis implementation and interpretation for reviews and plot summaries  </td>
  </tr>
  <tr>
    <td class="tg-0lax">Lena </td>
    <td class="tg-0lax"> (1) Lost movie, Chaplin GIFs and remake analysis <br> (2) Web site creation <br> (3) Elaboration and pre-writing of datastory for the website </td>
  </tr>
  <tr>
    <td class="tg-0lax">Olivia</td>
    <td class="tg-0lax"> (1) Silent and sound analysis <br> (2) Actor career "survival" analysis <br> (3) Interactive plot expert <br> (4) Help for the interpretation of sentiment analysis </td>
  </tr>
  <tr>
    <td class="tg-0lax">Orfeas:</td>
    <td class="tg-0lax"> (1) Loading and initial pre-processing of the data <br> (2) Missing and duplicate plot summary analysis <br> (3) Keyphrase extraction and TF-IDF scoring <br> (4) Geographical visualisation of tech-event correlation </td>
  </tr>
  <tr>
    <td class="tg-0lax">Oscar </td>
    <td class="tg-0lax"> (1) Technology related keyword search <br> (2) Technology event search <br> (3) Parallelization analysis of tech-event and their reflection in movies </td>
  </tr>  
</tbody>
</table>

