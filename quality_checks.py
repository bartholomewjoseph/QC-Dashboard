def duplicate_households(df):
    if "unique_code" not in df.columns:
        return set()
    return set(df[df["unique_code"].duplicated(keep=False)]["unique_code"].dropna())


def pregnancy_mismatch(df):
    required = [
        "c_alive", "c_dead",
        "agg_child_still_alive",
        "agg_child_alive_death"
    ]
    if not all(c in df.columns for c in required):
        return df.iloc[0:0]

    return df[
        (df["c_alive"] != df["agg_child_still_alive"]) |
        (df["c_dead"] != df["agg_child_alive_death"])
    ]
