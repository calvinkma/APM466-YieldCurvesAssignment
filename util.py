def get_date_like_column_names(df):
    columns = list(df)
    column_names = list(filter(lambda x: x.count("/") == 2, columns))
    return column_names