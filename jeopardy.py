import pandas as pd
import random
df = pd.read_csv('jeopardy.csv')
columns = ['Show Number', 'Air Date', 'Round', 'Category', 'Value', 'Question', 'Answer']
df.columns = columns
df.dropna(inplace=True)
df.drop(index=df[df['Value'] == 'None'].index, inplace=True)
key_words = ["King", "England"]
df['Value'] = df['Value'].str.strip('$').str.replace(',', '').astype(float)
df3 = df.copy()

# find questions with key words
def find_question(df, key_words):
    # lowercase both keywords and data frame(df)
    for i, j in enumerate(key_words):
        key_words[i] = j.lower()
    df1 = df['Question'].str.lower()
    # create new columns for each key word with values True if key word is in df['Question'] and 'False' if not
    for j in key_words:
        df[j] = df1.apply(lambda x: True if j in x else 'False')
    # only those rows where all key words much True will survive drop method
    for j in key_words:
        df.drop(index=df[df[j] == 'False'].index, inplace=True)

    return df.reset_index(drop=True)
key_words_df = find_question(df, key_words)

# calculate mean on 'value' column
def mean_calculate(df):
    df['Value'] = df['Value'].astype(float)

    return df['Value'].mean()

# search unique answers
def unique_answers(df):
    return(df['Answer'].unique())

# compare frequency of 'computer' word in decades
def compare_19_20(df):
    #select all questions from 1990 to 1999
    df_19_years = df['Air Date'].str.extract(r'(\s*199\d{1})')
    df_19_years.dropna(inplace=True)
    index_19 = df_19_years.index
    df_19 = df.loc[df.index.intersection(index_19), :]

    # select all questions from 2000 to 2010
    df_20_years = df['Air Date'].str.extract(r'(\s*200\d{1})')
    df_20_years.dropna(inplace=True)
    index_20 = df_20_years.index
    df_20 = df.loc[df.index.intersection(index_20), :]

    # find 'computer' in 19
    computer_find_19_questions = df_19['Question'].str.extract(r'(computer)')
    computer_find_19_questions.dropna(inplace=True)
    computer_index_19 = computer_find_19_questions.index
    computer_count_19_df = df.loc[df.index.intersection(computer_index_19), :].reset_index(drop=True)

    # find 'computer' in 20
    computer_find_20_questions = df_20['Question'].str.extract(r'(computer)')
    computer_find_20_questions.dropna(inplace=True)
    computer_index_20 = computer_find_20_questions.index
    computer_count_20_df = df.loc[df.index.intersection(computer_index_20), :].reset_index(drop=True)
    return( computer_count_19_df, computer_count_20_df)

# look for category - game mode dependency
def Jeopardy_single_double(df):
    df_jeopardy = df.groupby(['Round', 'Category']).count()
    round_I = df_jeopardy.loc[('Jeopardy!')]
    #print(round_I.sort_values(['Question']).to_string())
    round_II = df_jeopardy.loc[('Double Jeopardy!')]
    #print(round_II.sort_values(['Question']).to_string())

# the game
def play_game(df):
    n = random.randint(0, len(df))
    print(df.loc[n, 'Question'])
    answer = input('Type your answer here ')
    if answer == df.loc[n, 'Answer']:
        print('You right \n Victory')
    else:
        print('It is wrong answer, the right answer is ', df.loc[n, 'Answer'])