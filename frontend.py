import pandas as pd
import numpy as np
import pandas as pd
import numpy as np
import plotly.express as px
from dash import Dash,Input, Output, html, dcc
import nltk
from textblob import TextBlob
import sqlite3
import threading
import waitress

conn = sqlite3.connect('data/reddit.db')
c = conn.cursor()

# import data
df = pd.read_sql_query("SELECT * FROM submissions", conn)
df['creation_date'] = pd.to_datetime(df['timestamp'], unit='s')
df['update_time'] = pd.to_datetime(df['update_time'], unit='s')
df.set_index('creation_date', inplace=True)
df.drop('timestamp', axis=1, inplace=True)
df.sort_index(inplace=True)

# Setting the stopwords
nltk.download("stopwords")
stops = set(nltk.corpus.stopwords.words("english"))
stops_additionals = {"’", "“", "”", "n't", "'s", "'m", "'re", "'ve", "'ll", "'d", "''", "'","’t","’re","’m","’s", '’ s', '’ ve', '’ ll', '’ d', '’ m', '’ re', '’ t', '’ nt', '’ ve', '’ ll', '’ d', '’ m', '’ re', '’ t', '’ nt', '’ ve', '’ ll', '’ d', '’ m', '’ re', '’ t', '’ nt', '’ ve', '’ ll', '’ d', '’ m', '’ re', '’ t', '’ nt', '’ ve', '’ ll', '’ d', '’ m', '’ re', '’ t', '’ nt', '’ ve', '’ ll', '’ d', '’ m', '’ re', '’ t', '’ nt', '’ ve', '’ ll', '’ d', '’ m', '’ re', '’ t', '’ nt', '’ ve', '’ ll', '’ d', '’ m', '’ re', '’ t', '’ nt', 'ca n\'t', 'don ’ t','need','whats','oh','found'}
stops.update(stops_additionals)

# Setting date range
min_date = df.index.min()
max_date = df.index.max()

# Dash app
app = Dash(__name__)
app.layout = html.Div([
    html.Div(children = [
        html.H1(children = "Analysis of Reddit Submissions"),
        html.P(children="Data from the 'new' posts of the 50 most popular subreddits. collection date: 05-22-2023 - Present"),
        html.P(children = "The dataset is updated every 2 hours."),
        html.H2(children = "Optimal time to post"),
        html.P(children = "Select resolution:"),
        dcc.RadioItems(id='resolution', options={'hour':"By hour", "day_name":"By day", "month_name":"By month", "year":"By year"}, 
                                                          inline=True, 
                                                          value='hour',
                                                          className='element')
                                                          
    ]),
    html.Div( children = [
        dcc.DatePickerRange(id='date-range-1', 
                            start_date=min_date, 
                            end_date=max_date,
                            min_date_allowed=min_date,
                            max_date_allowed=max_date,
        )
    ], className=('element')),
    dcc.Graph(id='bar-graph'),
    html.H2(children = "How long should your title be ?"),
        html.Div( children = [
        dcc.DatePickerRange(id='date-range-2', 
                            start_date=min_date, 
                            end_date=max_date,
                            min_date_allowed=min_date,
                            max_date_allowed=max_date,
        )
    ], className=('element')),
    dcc.Graph(id='nlp-graph'),
    html.H2(children = "Trendy words"),
        html.Div( children = [
        dcc.DatePickerRange(id='date-range-3', 
                            start_date=min_date, 
                            end_date=max_date,
                            min_date_allowed=min_date,
                            max_date_allowed=max_date,
        ),
    ], className=('element')),
    html.P(children = "Note: Due to hardware limitation these are determined from a smaller subset of the data (~5%)"),
    html.P(children = "Please be patient as it may take a while to load"),
    dcc.Graph(id='word-graph'),
    html.H4(children = "This dashboard and the underlying data collection tool are available on my github"),
    html.A(href="https://github.com/Inner-daydream/esiea-uofm-python", children="https://github.com/Inner-daydream/esiea-uofm-python"),
    html.H4("the dataset is available at the following link:"),
    html.A(href="https://files.lucasquitman.fr/share/5wPigSHx", children="https://files.lucasquitman.fr/share/5wPigSHx")
], className='container')

@app.callback(
    Output('bar-graph', 'figure'),
    Input('date-range-1', 'start_date'),
    Input('date-range-1', 'end_date'),
    Input('resolution', 'value')
)

def update_bar_graph(start_date, end_date, resolution):
    if start_date is not None and end_date is not None:
        data = df.loc[start_date:end_date]
        resolution = getattr(data.index, resolution)
        if callable(resolution):
            resolution = resolution()
        data = data.groupby([resolution]).score.mean().round(0)
        fig = px.bar(data, x=data.index, 
                     y="score", 
                     title=f"Average post score within timeframe", 
                     color_continuous_scale=px.colors.sequential.Redor,
                     color="score",
                    )
        fig.update_layout(xaxis_title="", 
                          yaxis_title="Average post score",
                        ) 
        fig.update_xaxes(tickvals=resolution.unique().tolist(), tickmode='array', overwrite=True, ticktext=resolution.unique().tolist())
        fig.update_traces(hovertemplate="Average score: %{y}")
        return fig
    

@app.callback(
    Output('nlp-graph', 'figure'),
    Input('date-range-2', 'start_date'),
    Input('date-range-2', 'end_date'),
)
def nlp_graph(start_date, end_date):
    data = df.loc[start_date:end_date]
    data['title_length'] = [len(title.split()) for title in df['title']]
    data = data.groupby('title_length').score.mean().round(0).reset_index()
    fig = px.bar(data,x='title_length', y='score', title='Relationship between the number of words in a title and its score')
    fig.update_layout(xaxis_title="Number of words in a title", yaxis_title="Score")
    fig.update_traces(hovertemplate="Number of words: %{x}<br>Score: %{y}")
    return fig

@app.callback(
    Output('word-graph', 'figure'),
    Input('date-range-3', 'start_date'),
    Input('date-range-3', 'end_date'),
)
def word_frequency(start_date, end_date):
    # Selecting a sample of 5% of the data
    data = df.drop(df.sample(len(df)-int((len(df)*0.05))).index).reset_index()
    data= data.query('creation_date > @start_date and creation_date < @end_date')

    
    all_titles = [title +'\n' for title in data["title"]]

    # Set the titles as a TextBlob
    all_titles_str = ' '.join(all_titles)
    all_titles_blob = TextBlob(all_titles_str)

    # only keep nouns
    nouns = all_titles_blob.noun_phrases
    # get frequency of nouns
    nouns_freq = nltk.FreqDist(nouns).items()

    global_words = [item for item in nouns_freq if (item[0] not in stops) and  (' ' not in item[0])]

    # Sorting the values in a descending order
    global_sorted_items = sorted(global_words, key=lambda x: x[1], reverse=True)
    data = pd.DataFrame(data=global_sorted_items[:20], columns=["word", "frequency"])
    fig = px.bar(data_frame=data, x="frequency", y="word", title="Most frequent words in titles", orientation='h')
    # show all ticks
    fig.update_layout(yaxis=dict(
        tickmode='linear',
    ))

    return fig

def run(port):
    webapp = threading.Thread(target=lambda: waitress.serve(app.server, port=port))
    webapp.daemon = True
    webapp.start()



