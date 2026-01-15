def safe_unique(df, col):
    if col in df.columns:
        return df[col].dropna().astype(str).nunique()
    return 0
