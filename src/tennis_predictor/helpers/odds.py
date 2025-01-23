import pandas as pd

def _abbreviate_name(firstname: str, n_chars: int = 1) -> str:
    """Lee Sin -> L.S."""
    firstnames = firstname.split(' ')
    initials = [firstnames[0][:n_chars]] + [s[0] for s in firstnames[1:] if len(s) > 0]
    return '.'.join(initials) + '.'

def make_shortname(df: pd.DataFrame) -> pd.DataFrame:
    """Add a column of unique shortNames for players. Used to join dataframes "players" and "odds".
        'Danilo', 'Acosta' => 'Acosta Dan.'
        'Dario', 'Acosta' => 'Acosta Dar.'
        'Diego', 'Acosta' => 'Acosta Di.'
    """
    # First pass with 1 char
    n_chars = 1
    df['shortName'] = (
        df['lastName'].str.title()
        + ' ' 
        + df['firstName'].apply(_abbreviate_name, args=[n_chars])
    )
    # Check duplicates
    df_count = df.groupby('shortName')['id'].count()
    df_duplicate_shortnames = df_count[df_count > 1]

    # As long as there are duplicates, make longer shortnames for the duplicates
    while df_duplicate_shortnames.shape[0] > 0:
        # Some players can have the same names, stop at 10 chars.
        if n_chars > 10:
            break
        n_chars += 1
        df2 = df.merge(df_duplicate_shortnames, on='shortName', how='inner', suffixes=['', '_y'])
        df2 = df2.drop(columns=['id_y'])
        df2['shortName'] = (
            df2['lastName'].str.title()
            + ' ' 
            + df2['firstName'].apply(_abbreviate_name, args=[n_chars])
        )

        # Apply changes
        df = df.merge(df2[['id', 'shortName']], on='id', how='left', suffixes=['', '_y'])
        df['shortName'] = df['shortName_y'].fillna(df['shortName'])
        df = df.drop(columns=['shortName_y'])

        # Check duplicates
        df_count = df.groupby('shortName')['id'].count()
        df_duplicate_shortnames = df_count[df_count > 1]

    return df