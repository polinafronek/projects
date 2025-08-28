import csv
import re
import time
from collections import defaultdict
import sys
import requests
from bs4 import BeautifulSoup
import datetime

class Movies:
    def __init__(self, path_to_the_file):
        self.path_to_the_file =  path_to_the_file
        self.movies = []

        with open(path_to_the_file, "r", encoding="utf-8") as file_in:
            for line in file_in:
                line = line.strip()
                current_array = []
                first_comma = line.index(",")
                current_array.append(line[:first_comma])
                for i, item in enumerate(line):
                    if item == ",":
                        latest_comma = i
                    
                current_array.append(line[first_comma + 1 : latest_comma])
                current_array.append(line[latest_comma +1:])
                self.movies.append(current_array)

        self.movies = self.movies[:1000]
                                     
    def dist_by_release(self):
        years = []
        for line in self.movies[1:]:
            title = line[1].strip("'").strip('"')
            year = title.split()[-1]
            year = year.strip("(").strip(")")
            
            if year.isalpha():
                years.append("the year is not specified")
            else:
                years.append(year)

        release_years = {}
        for year in years:
            if year not in release_years.keys():
                release_years[year] = 1
            else:
                release_years[year] += 1

        release_years = dict(sorted(release_years.items(), key = lambda item: -item[1]))
        return release_years
    
    def dist_by_genres(self):
        array_with_genres = [line[-1].strip().split("|") for line in self.movies[1:]]
        genres = {}

        for array in array_with_genres:
            for genre in array:
                if genre not in genres.keys():
                    genres[genre] = 1
                else:
                    genres[genre] += 1

        genres = dict(sorted(genres.items(), key=lambda item : -item[1]))

        return genres
    
    def most_genres(self, n):
        movies = {}

        for movie in self.movies[1:]:
            movies[movie[1]] = len(movie[-1].split("|"))
        
        movies = dict(sorted(movies.items(), key=lambda item: -item[1])[:n])
        return movies
    
class Ratings:

    def __init__(self, path_to_the_file):
        self.ratings = []

        with open(path_to_the_file, "r", encoding="utf-8") as file_in:
            next(file_in)
            for line in file_in:
                self.ratings.append(line.split(","))

        
        self.Movies.ratings = self.ratings[:1000]

    class Movies:
        def __init__(self):
            movies = Movies("movies.csv")
            self.inf_from_Movies = movies.movies[:1000]
            
        def dist_by_year(self):
            years = []
            for line in self.ratings:
                dt_object = datetime.datetime.fromtimestamp(int(line[-1].strip("\n")))
                year = dt_object.year
                years.append(year) 

            ratings_by_year = {}
            for year in years:
                if year not in ratings_by_year.keys():
                    ratings_by_year[year] = 1
                else:
                    ratings_by_year[year] += 1

            ratings_by_year = dict(sorted(ratings_by_year.items(), key=lambda item: item[0]))

            return ratings_by_year
        
        def dist_by_rating(self):
            ratings_distribution = {}

            for line in self.ratings:
                mark = line[2]
                if mark not in ratings_distribution.keys():
                    ratings_distribution[mark] = 1
                else:
                    ratings_distribution[mark] += 1

            ratings_distribution = dict(sorted(ratings_distribution.items(), key=lambda item : item[0]))
            return ratings_distribution

        def top_by_num_of_ratings(self, n):
            ratings_for_movieId = {}

            for line in self.ratings:
                if line[1] not in ratings_for_movieId.keys():
                    ratings_for_movieId[line[1]] = [float(line[2])]
                else:
                    ratings_for_movieId[line[1]] += [float(line[2])]

            top_movies = {}
            
            for line in self.inf_from_Movies[1:]:
                if line[0] not in ratings_for_movieId.keys():
                    marks = []
                else:
                    marks = ratings_for_movieId[line[0]]
                top_movies[line[1]] = marks

            top_movies = dict(sorted(top_movies.items(), key=lambda item: -len(item[1]))[:n])
            return top_movies
        
        def top_by_ratings(self, n, metric="average"):
            num_of_ratings = self.top_by_num_of_ratings(len(self.inf_from_Movies)) 
            top_movies = {}
            if metric == "average":
                for movies in num_of_ratings:
                    if len(num_of_ratings[movies]) == 0:
                        top_movies[movies] = 0
                    else:
                        top_movies[movies] = round(sum(num_of_ratings[movies]) / len(num_of_ratings[movies]), 2)
            elif metric == "median":
                for movies in num_of_ratings:
                    sorted_marks = sorted(num_of_ratings[movies])
                    if len(sorted_marks) == 0: 
                        top_movies[movies] = 0.0
                    elif len(sorted_marks) == 1:
                        top_movies[movies] = sorted_marks[0]
                    else:
                        if len(sorted_marks) % 2 == 0:
                            top_movies[movies] = round((sorted_marks[len(sorted_marks) // 2 - 1] + sorted_marks[len(sorted_marks) // 2]) / 2, 2)
                        else:
                            top_movies[movies] = round(sorted_marks[len(sorted_marks) // 2], 2)
            else:
                raise ValueError("Incorrect metric")

            top_movies = dict(sorted(top_movies.items(), key=lambda item: -item[1])[:n])
            
            return top_movies
        
        def top_controversial(self, n):
            num_of_ratings = self.top_by_num_of_ratings(len(self.inf_from_Movies))
            top_movies = {}
            for movies in num_of_ratings:
                if len(num_of_ratings[movies]) < 2:
                    top_movies[movies] = 0.0
                else:
                    mean = sum(num_of_ratings[movies]) / len(num_of_ratings[movies])
                    squared_mean = [(x - mean) ** 2 for x in num_of_ratings[movies]]
                    top_movies[movies] = round(sum(squared_mean) / len(squared_mean),2)

            top_movies = dict(sorted(top_movies.items(), key=lambda item: item[1], reverse = True)[:n])
            return top_movies
        
    class User(Movies):

        def dist_user_by_marks(self):
            self.user_by_marks = {}
            for line in self.ratings[1:]:
                user = line[0]
                if user not in self.user_by_marks.keys():
                    self.user_by_marks[user] = [line[2]]
                else:
                    self.user_by_marks[user] += [line[2]]

            dist_marks_by_users = [(user, len(marks)) for user, marks in self.user_by_marks.items()]
            dist_user_by_marks = {}

            for tuple in dist_marks_by_users:
                counts = tuple[1]
                if counts not in dist_user_by_marks.keys():
                    dist_user_by_marks[counts] = 1
                else:
                    dist_user_by_marks[counts] += 1

            return dist_user_by_marks
        
        def dist_user_by_mean(self, metric="average"):
            ratings_by_user = {}
            if metric == "average":
                for user, ratings in self.user_by_marks.items():
                    if len(ratings) == 0:
                        ratings_by_user[user] = 0.0
                    elif len(ratings) == 1:
                        ratings_by_user[user] = float(ratings)
                    else:
                        ratings = [float(x) for x in ratings]
                        ratings_by_user[user] = round(sum(ratings) / len(ratings), 2)
            elif metric == "median":
                for user, ratings in self.user_by_marks.items():
                    sorted_ratings = sorted(ratings)
                    if len(sorted_ratings) == 0:
                        ratings_by_user[user] = 0.0
                    elif len(sorted_ratings) == 1:
                        ratings_by_user[user] = ratings
                    else:
                        if len(sorted_ratings) % 2 == 0:
                            ratings_by_user[user] = round((sorted_ratings[len(sorted_ratings) // 2 - 1] + sorted_ratings[len(sorted_ratings) // 2]) / 2, 2)
                        else:
                            ratings_by_user[user] = round(sorted_ratings(len(sorted_ratings) // 2), 2)
            else:
                raise ValueError("Incorrect metric")
            
            user_by_ratings = {}
            for user, digit in ratings_by_user.items():
                if digit not in user_by_ratings.keys():
                    user_by_ratings[digit] = 1
                else:
                    user_by_ratings[digit] += 1

            return user_by_ratings 
        
        def difference_in_ratings(self, n):
            difference_in_ratings = {}
            for user, ratings in self.user_by_marks.items():
                if len(ratings) < 2:
                    difference_in_ratings[user] = 0.0
                else:
                    ratings = [float(x) for x in ratings]
                    mean = sum(ratings) / len(ratings)
                    squared_mean = [(x - mean) ** 2 for x in ratings]
                    difference_in_ratings[user] = round(sum(squared_mean) / len(squared_mean), 2)

            difference_in_ratings = dict(sorted(difference_in_ratings.items(), key=lambda item: item[1], reverse = True)[:n])

            return difference_in_ratings

class Tags:
    def __init__(self, path_to_the_file):
        self.path_to_the_file = path_to_the_file
        self.tags = self._load_tags()
        
    def _load_tags(self):
        tags = []
        try:
            with open(self.path_to_the_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    tags.append({
                        'userId': int(row['userId']),
                        'movieId': int(row['movieId']),
                        'tag': row['tag'].strip(),
                        'timestamp': int(row['timestamp'])
                    })
        except Exception as e:
            print(f"Error loading tags: {e}")
        return tags
    
    def most_words(self, n):
        word_counts = {}
        for tag in self.tags:
            current_tag = tag['tag']
            word_count = len(current_tag.split())
            if current_tag not in word_counts or word_count > word_counts[current_tag]:
                word_counts[current_tag] = word_count
        return dict(sorted(word_counts.items(), key=lambda x: (-x[1], x[0]))[:n])
    
    def longest(self, n):
        tag_lengths = {tag['tag']: len(tag['tag']) for tag in self.tags}
        return sorted(tag_lengths.keys(), key=lambda x: (-tag_lengths[x], x))[:n]
    
    def most_words_and_longest(self, n):
        most_words = set(tag for tag, _ in self.most_words(n).items())
        longest = set(self.longest(n))
        return sorted(most_words & longest)
    
    def most_popular(self, n):
        tag_counts = defaultdict(int)
        for tag in self.tags:
            tag_counts[tag['tag']] += 1
        return dict(sorted(tag_counts.items(), key=lambda x: (-x[1], x[0]))[:n])
    
    def tags_with(self, word):
        word_lower = word.lower()
        unique_tags = set()
        for tag in self.tags:
            if word_lower in tag['tag'].lower():
                unique_tags.add(tag['tag'])
        return sorted(unique_tags)

class Links:

    def __init__(self, path_to_the_file):
        self.path_to_the_file = path_to_the_file
        self.links = self._load_links()  
        self.movie_id_to_imdb_id_map = {link['movieId']: link['imdbId'] for link in self.links}
        self.movie_data_cache = {}  
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9'
        })

    def _load_links(self):
        links_data = []
        max_links_to_load = 50 
        try:
            with open(self.path_to_the_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for i, row in enumerate(reader):
                    if i >= max_links_to_load: 
                        break 

                    if row.get('movieId') and row.get('imdbId'):
                        links_data.append({
                            'movieId': int(row['movieId']),
                            'imdbId': row['imdbId'].zfill(7),
                        })
        except FileNotFoundError:
            print(f"links.csv file not found at {self.path_to_the_file}")
        except Exception as e:
            print(f"Error loading links: {e}")
        
        return links_data

    def _parse_money(self, money_str):
        if not money_str:
            return 0
        money_str = re.sub(r'[^\d]', '', money_str.split('(')[0].strip())
        try:
            return int(money_str)
        except ValueError:
            return 0

    def _parse_runtime(self, runtime_str):
        if not runtime_str:
            return 0
        if isinstance(runtime_str, int):
            return runtime_str
        
        minutes = 0
        match_hours_minutes = re.search(r'(\d+)\s*h(?:our)?s?\s*(\d+)\s*min(?:ute)?s?', runtime_str, re.I)
        match_hours_only = re.search(r'(\d+)\s*h(?:our)?s?', runtime_str, re.I)
        match_minutes_only = re.search(r'(\d+)\s*min(?:ute)?s?', runtime_str, re.I)

        if match_hours_minutes:
            hours = int(match_hours_minutes.group(1))
            mins = int(match_hours_minutes.group(2))
            minutes = hours * 60 + mins
        elif match_hours_only: 
            hours = int(match_hours_only.group(1))
            minutes = hours * 60
        elif match_minutes_only: 
            mins = int(match_minutes_only.group(1))
            minutes = mins
        else: 
            try:
                cleaned_str = re.sub(r'[^\d]', '', runtime_str)
                if cleaned_str:
                    num_val = int(cleaned_str)
                    if 0 < num_val < 1000: 
                         minutes = num_val
            except ValueError:
                pass 
        return minutes

    def _scrape_imdb_data(self, imdb_id):
        if imdb_id in self.movie_data_cache:
            return self.movie_data_cache[imdb_id]

        url = f"https://www.imdb.com/title/tt{imdb_id}/"
        data = {
            'Title': None,
            'Director': [],
            'Budget': None,
            'Cumulative Worldwide Gross': None,
            'Runtime': None
        }

        print(f"Scraping: {url}")

        try:
            time.sleep(0.01)
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            title_tag_h1 = soup.find('h1', attrs={'data-testid': 'hero__pageTitle'})
            if title_tag_h1:
                title_span = title_tag_h1.find('span', class_='hero__primary-text')
                data['Title'] = title_span.get_text(strip=True) if title_span else title_tag_h1.get_text(strip=True)
            if not data['Title']:
                og_title_tag = soup.find('meta', property='og:title')
                if og_title_tag and og_title_tag.get('content'):
                    data['Title'] = og_title_tag['content'].replace(' - IMDb', '').strip()

            director_li = soup.find('li', attrs={'data-testid': 'title-pc-principal-credit'})
            if director_li:
                label_span = director_li.find('span', class_='ipc-metadata-list-item__label')
                if label_span and 'Director' in label_span.get_text(strip=True):
                    director_links = director_li.select('a[href*="/name/nm"]')
                    for el in director_links:
                        name = el.get_text(strip=True)
                        if name not in data['Director']:
                            data['Director'].append(name)

            budget_li = soup.find('li', attrs={'data-testid': 'title-boxoffice-budget'})
            if budget_li:
                value_span = budget_li.find('span', class_='ipc-metadata-list-item__list-content-item')
                if value_span:
                    data['Budget'] = self._parse_money(value_span.get_text(strip=True))

            gross_li = soup.find('li', attrs={'data-testid': 'title-boxoffice-cumulativeworldwidegross'})
            if gross_li:
                value_span = gross_li.find('span', class_='ipc-metadata-list-item__list-content-item')
                if value_span:
                    data['Cumulative Worldwide Gross'] = self._parse_money(value_span.get_text(strip=True))

            runtime_li = soup.find('li', attrs={'data-testid': 'title-techspec_runtime'})
            if runtime_li:
                runtime_span = runtime_li.find('div', class_='ipc-metadata-list-item__content-container')
                if runtime_span:
                    data['Runtime'] = self._parse_runtime(runtime_span.get_text(strip=True))

            if not data['Runtime']:
                details_section = soup.find('section', attrs={'data-testid': 'Details'})
                if details_section:
                    runtime_label = details_section.find(lambda tag: tag.name == 'span' and "Runtime" in tag.get_text(strip=True) and tag.find_parent('li', attrs={'data-testid':'title-details-runtime'}))
                    if runtime_label:
                        runtime_div = runtime_label.find_parent('li').find('div', class_='ipc-metadata-list-item__content-container')
                        if runtime_div:
                            data['Runtime'] = self._parse_runtime(runtime_div.get_text(strip=True))

            self.movie_data_cache[imdb_id] = data
            return data

        except requests.exceptions.RequestException as e:
            print(f"Request error for {imdb_id}: {e}")
        except Exception as e:
            print(f"Parsing error for {imdb_id}: {e}")

        self.movie_data_cache[imdb_id] = data
        return data


    def get_imdb(self, list_of_movies, list_of_fields):
        results = []
        valid_fields = ['Title', 'Director', 'Budget', 'Cumulative Worldwide Gross', 'Runtime']

        for movie_id in list_of_movies:
            imdb_id = self.movie_id_to_imdb_id_map.get(movie_id)
            current_row = [movie_id]

            if not imdb_id:
                print(f"No IMDB ID found for movieId {movie_id}.")
                current_row.extend([None] * len(list_of_fields))
                results.append(current_row)
                continue

            scraped_data = self._scrape_imdb_data(imdb_id)
            
            for field in list_of_fields:
                if field not in valid_fields:
                    print(f"{field}' is not a supported")
                    current_row.append(None)
                    continue
                
                value = scraped_data.get(field)
                if field == 'Director' and isinstance(value, list):
                    current_row.append(", ".join(value) if value else None) 
                else:
                    current_row.append(value)
            results.append(current_row)

        results.sort(key=lambda x: x[0], reverse=True)
        return results

    def top_directors(self, n):
        director_counts = defaultdict(int)
        for i, link_entry in enumerate(self.links):
            imdb_id = link_entry['imdbId']
            data = self._scrape_imdb_data(imdb_id)
            directors = data.get('Director') 
            if directors:
                for director_name in directors:
                    if director_name:
                        director_counts[director_name.strip()] += 1
        
        sorted_directors = sorted(director_counts.items(), key=lambda item: item[1], reverse=True)
        return dict(sorted_directors[:n])

    def most_expensive(self, n):
        movie_budgets = {}
        for i, link_entry in enumerate(self.links):
            imdb_id = link_entry['imdbId']
            data = self._scrape_imdb_data(imdb_id)
            
            title = data.get('Title')
            budget = data.get('Budget')

            if title and isinstance(budget, int) and budget > 0:
                movie_budgets[title] = budget
            elif title and budget is None: 
                pass 

        sorted_budgets = sorted(movie_budgets.items(), key=lambda item: item[1], reverse=True)
        return dict(sorted_budgets[:n])

    def most_profitable(self, n):
        movie_profits = {}
        for i, link_entry in enumerate(self.links):
            imdb_id = link_entry['imdbId']
            data = self._scrape_imdb_data(imdb_id)

            title = data.get('Title')
            budget = data.get('Budget') 
            gross = data.get('Cumulative Worldwide Gross')

            if title and isinstance(budget, int) and isinstance(gross, int) and gross > 0 :
                profit = gross - budget
                movie_profits[title] = profit
        
        sorted_profits = sorted(movie_profits.items(), key=lambda item: item[1], reverse=True)
        return dict(sorted_profits[:n])

    def longest(self, n):
        movie_runtimes = {}
        for i, link_entry in enumerate(self.links):
            imdb_id = link_entry['imdbId']
            data = self._scrape_imdb_data(imdb_id)

            title = data.get('Title')
            runtime_minutes = data.get('Runtime')

            if title and isinstance(runtime_minutes, int) and runtime_minutes > 0:
                movie_runtimes[title] = runtime_minutes
        
        sorted_runtimes = sorted(movie_runtimes.items(), key=lambda item: item[1], reverse=True)
        return dict(sorted_runtimes[:n])
    
    def top_cost_per_minute(self, n):
        cost_per_minute = {}
        
        for link_entry in self.links:
            imdb_id = link_entry['imdbId']
            data = self._scrape_imdb_data(imdb_id)
            
            title = data.get('Title')
            budget = data.get('Budget', 0)
            runtime = data.get('Runtime', 1)
            
            if title and isinstance(budget, (int, float)) and budget > 0 and \
            isinstance(runtime, (int, float)) and runtime > 0:
                cpm = round(budget / runtime, 2)
                cost_per_minute[title] = cpm
                
        return dict(sorted(cost_per_minute.items(), 
                        key=lambda item: item[1], 
                        reverse=True)[:n])


def main():
    try:
        function = sys.argv[1]
    
        movies = Movies("movies.csv")
        ratings = Ratings("ratings.csv")
        tags = Tags("tags.csv")
        links = Links("links.csv")

        if function == "movies":
            dist_by_release = movies.dist_by_release()
            dist_by_genres = movies.dist_by_genres()
            most_genres = movies.most_genres(100)

        elif function == "ratings":
            movies_in_ratings = ratings.Movies()
            dist_by_year = movies_in_ratings.dist_by_year()
            dist_by_rating = movies_in_ratings.dist_by_rating()
            top_by_num_of_ratings = movies_in_ratings.top_by_num_of_ratings(30)
            top_by_ratings = movies_in_ratings.top_by_ratings(100, metric = "average")
            top_controversial = movies_in_ratings.top_controversial(10)
            users = ratings.User()
            dist_user_by_marks = users.dist_user_by_marks()
            dist_user_by_mean = users.dist_user_by_mean()
            difference_in_ratings = users.difference_in_ratings(10)
        
        elif function == "tags":
            most_words = tags.most_words(10)
            longest_tag = tags.longest(10)
            most_popular =  tags.most_popular(10)
            tags_with = tags.tags_with("action")

        elif function == "links":
            top_directors = links.top_directors(10)
            most_expensive = links.most_expensive(10)
            most_profitable = links.most_profitable(10)
            longest_link = links.longest(10)
        else:
            print("This class doesn't exist")
            sys.exit()

    except IndexError:
        print("Inccorect number of arguments")
        sys.exit()
    except FileNotFoundError:
        print("File not found")
    except Exception as e:
        print(f"ERROR: {e}")

class Tests:
    @staticmethod
    def test_movies_class():
        movies = Movies('movies.csv')
        assert isinstance(movies.movies, list)
        assert isinstance(movies.movies[0], list)
        assert isinstance(movies.dist_by_release(), dict)
        assert isinstance(movies.dist_by_genres(), dict)
        assert len(movies.most_genres(10)) == 10
        
    @staticmethod
    def test_ratings_class():
        ratings = Ratings('ratings.csv')
        assert isinstance(ratings.ratings, list)
        assert isinstance(ratings.ratings[0], list)
        movies_ratings = ratings.Movies()
        assert isinstance(movies_ratings.dist_by_year(), dict)
        assert isinstance(movies_ratings.dist_by_rating(), dict)
        assert len(movies_ratings.top_by_num_of_ratings(10)) == 10
        
    @staticmethod
    def test_tags_class():
        tags = Tags('tags.csv')
        assert isinstance(tags.tags, list)
        assert isinstance(tags.tags[0], dict)
        assert isinstance(tags.most_words(10), dict)
        assert isinstance(tags.longest(10), list)
        assert len(tags.most_popular(10)) == 10
        assert isinstance(tags.tags_with("action"), list)
        
    @staticmethod
    def test_links_class():
        links = Links('links.csv')
        assert isinstance(links.links, list)
        assert isinstance(links.links[0], dict)
        assert isinstance(links.get_imdb([1, 2], ['Director']), list)
        assert isinstance(links.top_directors(10), dict)
        assert isinstance(links.most_expensive(10), dict)

    @staticmethod
    def test_movies_dist_by_release_sorted():
        movies = Movies('movies.csv')
        dist = movies.dist_by_release()
        values = list(dist.values())
        assert all(values[i] >= values[i+1] for i in range(len(values)-1)), "dist_by_release is not sorted correctly"

    @staticmethod
    def test_movies_dist_by_genres_sorted():
        movies = Movies('movies.csv')
        dist = movies.dist_by_genres()
        values = list(dist.values())
        assert all(values[i] >= values[i+1] for i in range(len(values)-1)), "dist_by_genres is not sorted correctly"

    @staticmethod
    def test_movies_most_genres_sorted():
        movies = Movies('movies.csv')
        top = movies.most_genres(100)
        values = list(top.values())
        assert all(values[i] >= values[i+1] for i in range(len(values)-1)), "most_genres is not sorted correctly"

    @staticmethod
    def test_ratings_dist_by_year_sorted():
        ratings = Ratings('ratings.csv')
        dist = ratings.Movies().dist_by_year()
        keys = list(dist.keys())
        assert all(keys[i] <= keys[i+1] for i in range(len(keys)-1)), "dist_by_year is not sorted correctly"

    @staticmethod
    def test_ratings_dist_by_rating_sorted():
        ratings = Ratings('ratings.csv')
        dist = ratings.Movies().dist_by_rating()
        keys = list(dist.keys())
        assert all(float(keys[i]) <= float(keys[i+1]) for i in range(len(keys)-1)), "dist_by_rating is not sorted correctly"

    @staticmethod
    def test_ratings_top_by_num_sorted():
        ratings = Ratings('ratings.csv')
        top = ratings.Movies().top_by_num_of_ratings(10)
        values = [len(v) for v in top.values()]
        assert all(values[i] >= values[i+1] for i in range(len(values)-1)), "top_by_num_of_ratings is not sorted correctly"

    @staticmethod
    def test_ratings_top_by_ratings_sorted():
        ratings = Ratings('ratings.csv')
        top = ratings.Movies().top_by_ratings(10)
        values = list(top.values())
        assert all(values[i] >= values[i+1] for i in range(len(values)-1)), "top_by_ratings is not sorted correctly"

    @staticmethod
    def test_ratings_top_controversial_sorted():
        ratings = Ratings('ratings.csv')
        top = ratings.Movies().top_controversial(10)
        values = list(top.values())
        assert all(values[i] >= values[i+1] for i in range(len(values)-1)), "top_controversial is not sorted correctly"

    @staticmethod
    def test_tags_most_words_sorted():
        tags = Tags('tags.csv')
        top = tags.most_words(10)
        values = list(top.values())
        assert all(values[i] >= values[i+1] for i in range(len(values)-1)), "most_words is not sorted correctly"
        
        items = list(top.items())
        for i in range(len(items)-1):
            if items[i][1] == items[i+1][1]:
                assert items[i][0] < items[i+1][0], "most_words not sorted by key when values equal"

    @staticmethod
    def test_tags_longest_sorted():
        tags = Tags('tags.csv')
        longest = tags.longest(10)
        lengths = [len(tag) for tag in longest]
        assert all(lengths[i] >= lengths[i+1] for i in range(len(lengths)-1)), "longest is not sorted correctly"
        
        for i in range(len(longest)-1):
            if len(longest[i]) == len(longest[i+1]):
                assert longest[i] < longest[i+1], "longest not sorted by tag text when lengths equal"

    @staticmethod
    def test_tags_most_popular_sorted():
        tags = Tags('tags.csv')
        top = tags.most_popular(10)
        values = list(top.values())
        assert all(values[i] >= values[i+1] for i in range(len(values)-1)), "most_popular is not sorted correctly"

        items = list(top.items())
        for i in range(len(items)-1):
            if items[i][1] == items[i+1][1]:
                assert items[i][0] < items[i+1][0], "most_popular not sorted by tag when counts equal"

    @staticmethod
    def test_links_top_directors_sorted():
        links = Links('links.csv')
        top = links.top_directors(10)
        values = list(top.values())
        assert all(values[i] >= values[i+1] for i in range(len(values)-1)), "top_directors is not sorted correctly"

    @staticmethod
    def test_links_most_expensive_sorted():
        links = Links('links.csv')
        top = links.most_expensive(10)
        values = list(top.values())
        assert all(values[i] >= values[i+1] for i in range(len(values)-1)), "most_expensive is not sorted correctly"

    @staticmethod
    def test_links_most_profitable_sorted():
        links = Links('links.csv')
        top = links.most_profitable(10)
        values = list(top.values())
        assert all(values[i] >= values[i+1] for i in range(len(values)-1)), "most_profitable is not sorted correctly"

    @staticmethod
    def test_links_longest_sorted():
        links = Links('links.csv')
        top = links.longest(10)
        values = list(top.values())
        assert all(values[i] >= values[i+1] for i in range(len(values)-1)), "longest is not sorted correctly"

    @staticmethod
    def test_links_top_cost_per_minute_sorted():
        links = Links('links.csv')
        top = links.top_cost_per_minute(10)
        values = list(top.values())
        assert all(values[i] >= values[i+1] for i in range(len(values)-1)), "top_cost_per_minute is not sorted correctly"


if __name__ == "__main__":
    Tests.test_movies_class()
    Tests.test_ratings_class()
    Tests.test_tags_class()
    Tests.test_links_class()
    Tests.test_movies_dist_by_release_sorted()
    Tests.test_movies_dist_by_genres_sorted()
    Tests.test_movies_most_genres_sorted()
    Tests.test_ratings_dist_by_year_sorted()
    Tests.test_ratings_dist_by_rating_sorted()
    Tests.test_ratings_top_by_num_sorted()
    Tests.test_ratings_top_by_ratings_sorted()
    Tests.test_ratings_top_controversial_sorted()
    Tests.test_tags_most_words_sorted()
    Tests.test_tags_longest_sorted()
    Tests.test_tags_most_popular_sorted()
    Tests.test_links_top_directors_sorted()
    Tests.test_links_most_expensive_sorted()
    Tests.test_links_most_profitable_sorted()
    Tests.test_links_longest_sorted()
    Tests.test_links_top_cost_per_minute_sorted()
    
    print("All tests passed!")
    main()
