import luigi, math, pickle
import pandas as pd

from sklearn.naive_bayes import MultinomialNB

class CleanDataTask(luigi.Task):
    """ Cleans the input CSV file by removing any rows without valid geo-coordinates.

        Output file should contain just the rows that have geo-coordinates and
        non-(0.0, 0.0) files.
    """
    tweet_file = luigi.Parameter()
    output_file = luigi.Parameter(default='clean_data.csv')

    def run(self):
        df = pd.read_csv(self.tweet_file, encoding='utf-8')
        df = df[df['tweet_coord'].notnull()]
        df = df[df['tweet_coord'] != '[0.0, 0.0]']
        df.to_csv(self.output_file, encoding='utf-8')


    def output(self):
        return luigi.LocalTarget(self.output_file)

class TrainingDataTask(luigi.Task):
    """ Extracts features/outcome variable in preparation for training a model.

        Output file should have columns corresponding to the training data:
        - y = airline_sentiment (coded as 0=negative, 1=neutral, 2=positive)
        - X = a one-hot coded column for each city in "cities.csv"
    """
    tweet_file = luigi.Parameter()
    cities_file = luigi.Parameter(default='cities.csv')
    output_file = luigi.Parameter(default='features.csv')

    def requires(self):
        return [CleanDataTask(self.tweet_file)]

    def run(self):
        df_tweets = pd.read_csv('clean_data.csv', encoding='utf-8')
        df_tweets["sentiment_code"] = df_tweets.airline_sentiment.astype("category")
        df_tweets['sentiment_code'] = df_tweets.sentiment_code.cat.codes

        df_cities = pd.read_csv(self.cities_file, encoding='utf-8')

        df_tweets['city'] = df_tweets['tweet_coord']
        df_tweets['city_coord'] = df_tweets['tweet_coord']
        for tweet_row_index, tweet_row in df_tweets.iterrows():
            tweet_lat = float(tweet_row.tweet_coord.split(',')[0][1:])
            tweet_lon = float(tweet_row.tweet_coord.split(',')[1][:-1])

            df = df_cities[df_cities['latitude'] < (tweet_lat + 2)]
            df = df[df['latitude'] > (tweet_lat - 2)]

            df = df[df['longitude'] < (tweet_lon + 2)]
            df = df[df['longitude'] > (tweet_lon - 2)]

            tweet_city = ''
            nearest_city_dist = float('inf')
            city_lat = 0
            city_lon = 0
            for city_row in df.itertuples():
                d = math.sqrt(math.pow(tweet_lat - city_row.latitude, 2) + math.pow(tweet_lon - city_row.longitude, 2))
                if d < nearest_city_dist:
                    nearest_city_dist = d
                    tweet_city = city_row.asciiname
                    city_lat = city_row.latitude
                    city_lon = city_row.longitude
            df_tweets.ix[tweet_row_index, 'city'] = tweet_city
            df_tweets.ix[tweet_row_index, 'city_coord'] = str(city_lat) + ', ' + str(city_lon)

        df_tweets = pd.concat([df_tweets.sentiment_code, df_tweets.city, pd.get_dummies(df_tweets['city'], prefix='city')], axis=1)
        df_tweets.to_csv(self.output_file, encoding='utf-8')


    def output(self):
        return luigi.LocalTarget(self.output_file)

class TrainModelTask(luigi.Task):
    """ Trains a classifier to predict negative, neutral, positive
        based only on the input city.

        Output file should be the pickle'd model.
    """
    tweet_file = luigi.Parameter()
    output_file = luigi.Parameter(default='model.pkl')

    def requires(self):
        return [TrainingDataTask(self.tweet_file)]

    def run(self):
        df_tweets = pd.read_csv('features.csv', encoding='utf-8')
        X = df_tweets.drop(['sentiment_code', 'city'], axis=1)
        y = df_tweets['sentiment_code']
        model = MultinomialNB().fit(X, y)
        pickle.dump(model, open(self.output_file, 'wb'))


    def output(self):
        return luigi.LocalTarget(self.output_file)

class ScoreTask(luigi.Task):
    """ Uses the scored model to compute the sentiment for each city.

        Output file should be a four column CSV with columns:
        - city name
        - negative probability
        - neutral probability
        - positive probability
    """
    tweet_file = luigi.Parameter(default='airline_tweets.csv')
    output_file = luigi.Parameter(default='scores.csv')

    def requires(self):
        return [TrainModelTask(self.tweet_file)]

    def run(self):
        loaded_model = pickle.load(open("model.pkl", 'rb'))
        df_tweets = pd.read_csv('features.csv', encoding='utf-8')
        df = pd.DataFrame(columns=['city', 'neg_probability', 'neutral_prob', 'positive_prob'])
        for row_index, row in df_tweets.iterrows():
            X = row.drop(['sentiment_code', 'city'])
            predictions = loaded_model.predict_proba(X.values.reshape(1, -1))[0]
            df.loc[len(df)] = [row[2], predictions[0], predictions[1], predictions[2]]
        df.sort_values(by=['city']).to_csv('scores.csv', encoding='utf-8', index=False)


if __name__ == "__main__":
    luigi.run(['ScoreTask', '--workers', '1', '--local-scheduler'])
