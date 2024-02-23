# Performance prediction of movies in India based on quantitative parameters

This is the course project for CS361: Machine Learning Course at IIT Guwahati, Jan-May 2024, under the guidance of Prof. Ashish Anand, Dept. of CSE, IIT Guwahati.

Through this project, we aim to predict the performance of any movie at a given time in the Indian audiences, using Machine Learning.

## UNDER CONSTRUCTION

This is project is not yet completed, and under continuous development.

Hence, one is advised to **NOT** run the project as of now.

## Dataset Creation

The dataset was created in the following way:

1. Movie `urls` were fetched from [imdb.com](https://www.imdb.com/) using [this](https://github.com/g-s01/indMov/blob/main/WebScraper/UrlsCreator.ipynb) notebook.
    1. The `urls` fetched can be seen [here](https://github.com/g-s01/indMov/blob/main/data/urls.txt)
2. From the `urls`, the data about a movie was fetched using [selenium](https://www.selenium.dev)
    and [Beautyful Soup](https://pypi.org/project/beautifulsoup4/), using [this](https://github.com/g-s01/indMov/blob/main/WebScraper/dataSetCreator.py) script.
     1. The dataset created can be viewed [here](https://github.com/g-s01/indMov/blob/main/data/data.csv)

# Credits

* Adittya Gupta
* [Gautam Sharma](https://g-s01.github.io/)
* Sparsh Mittal
* Yash Raj Singh
