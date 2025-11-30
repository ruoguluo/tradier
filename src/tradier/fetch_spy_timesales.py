import os, dotenv, csv
from datetime import datetime, timedelta
from pathlib import Path
from lumiwealth_tradier import Tradier

def main():
    dotenv.load_dotenv()
    tradier_acct = os.getenv("tradier_acct")
    tradier_token = os.getenv("tradier_token")
    if not tradier_acct or not tradier_token:
        dotenv.load_dotenv(Path(__file__).parent / ".env")
        tradier_acct = tradier_acct or os.getenv("tradier_acct")
        tradier_token = tradier_token or os.getenv("tradier_token")
    tradier = Tradier(tradier_acct, tradier_token, is_paper=True)
    start_date="2025-10-31"
    end_date="2025-11-29"
    data = tradier.market.get_timesales(
        "SPY",
        interval=5,
        start_date=start_date,
        end_date=end_date,
        session_filter="all",
    )
    out_dir = Path("data")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "spy_timesales.csv"
    if hasattr(data, "to_csv"):
        df = data
        if "datetime" not in getattr(df, "columns", []):
            df = df.reset_index()
        df["symbol"] = "SPY"
        cols = ["symbol", "datetime"] + [c for c in ["price", "open", "high", "low", "close", "volume", "vwap"] if c in df.columns]
        df[cols].to_csv(out_path, index=False)
    else:
        rows = []
        if isinstance(data, dict):
            rows = data.get("series") or data.get("bars") or []
        elif isinstance(data, list):
            rows = data
        with out_path.open("w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["symbol", "datetime", "price", "open", "high", "low", "close", "volume", "vwap"])
            for r in rows:
                w.writerow([
                    "SPY",
                    r.get("datetime") or r.get("time"),
                    r.get("price"),
                    r.get("open"),
                    r.get("high"),
                    r.get("low"),
                    r.get("close"),
                    r.get("volume"),
                    r.get("vwap"),
                ])
    print(str(out_path))

if __name__ == "__main__":
    main()