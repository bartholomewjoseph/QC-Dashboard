def calculate_pregnancy_metrics(df):
    for col in ["c_alive", "c_dead", "agg_dead_miscarrage"]:
        if col not in df.columns:
            df[col] = 0

    df["c_count"] = df["c_alive"] + df["c_dead"]
    df["p_count"] = df["c_count"] + df["agg_dead_miscarrage"]

    return {
        "alive": int(df["c_alive"].sum()),
        "dead": int(df["c_dead"].sum()),
        "miscarriage": int(df["agg_dead_miscarrage"].sum()),
        "total": int(df["p_count"].sum())
    }
