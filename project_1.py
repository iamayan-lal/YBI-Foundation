import pandas as pd

def load_data(file_path):
    """Loads election data from a CSV file."""
    return pd.read_csv(file_path)

def calculate_total_votes(df):
    """Calculates total votes per party."""
    return df.groupby('Party')['Votes'].sum().reset_index()

def get_winning_party(df):
    """Identifies the winning party in each constituency."""
    return df.loc[df.groupby('Constituency')['Votes'].idxmax(), ['Constituency', 'Party']]

def determine_overall_winner(df):
    """Determines the overall election winner."""
    total_votes = calculate_total_votes(df)
    return total_votes.loc[total_votes['Votes'].idxmax(), 'Party']

def calculate_vote_share(df):
    """Calculates vote share percentages."""
    total_votes = df['Votes'].sum()
    df['Vote Share (%)'] = (df['Votes'] / total_votes) * 100
    return df[['Candidate', 'Votes', 'Vote Share (%)']]

def close_contest(df):
    """Identifies close contests where the vote margin is less than 5%."""
    df_sorted = df.sort_values(by=['Constituency', 'Votes'], ascending=[True, False])
    df_sorted['Vote Margin'] = df_sorted.groupby('Constituency')['Votes'].diff()
    close_contests = df_sorted[df_sorted['Vote Margin'] < (df_sorted['Votes'] * 0.05)]
    return close_contests[['Constituency', 'Candidate', 'Votes', 'Vote Margin']]

def main():
    file_path = 'election_results.csv'  # Replace with your file path
    df = load_data(file_path)
    
    total_votes = calculate_total_votes(df)
    winning_parties = get_winning_party(df)
    overall_winner = determine_overall_winner(df)
    vote_share_df = calculate_vote_share(df)
    close_contests = close_contest(df)
    
    print('Total Votes per Party:\n', total_votes)
    print('\nWinning Party in Each Constituency:\n', winning_parties)
    print(f'\nOverall Election Winner: {overall_winner}')
    print('\nVote Share:\n', vote_share_df)
    print('\nClose Contests:\n', close_contests)

if __name__ == "__main__":
    main()
