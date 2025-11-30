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
    end_date = datetime.now()
    start_date = end_date - timedelta(days=10)
    tradier = Tradier(tradier_acct, tradier_token, is_paper=True)

    start_date="2025-10-31"
    end_date="2025-11-11"

    data = tradier.market.get_historical_quotes(
        "SPY",
        interval="daily",
        start_date=start_date,
        end_date=end_date,
        session_filter="all",
    )
    out_dir = Path("data")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "spy_daily.csv"
    if hasattr(data, "to_csv"):
        df = data
        cols = [c for c in ["open", "high", "low", "close", "volume"] if c in df.columns]
        if "date" in getattr(df, "columns", []):
            df = df.set_index("date")
        df[cols].to_csv(out_path, index=True, index_label="date")
    else:
        days = []
        if isinstance(data, dict):
            history = data.get("history") if isinstance(data.get("history"), dict) else data
            if isinstance(history, dict):
                days = history.get("day") or history.get("bars") or []
            elif isinstance(history, list):
                days = history
        elif isinstance(data, list):
            days = data
        with out_path.open("w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["date", "open", "high", "low", "close", "volume"])
            for d in days:
                w.writerow([
                    d.get("date"),
                    d.get("open"),
                    d.get("high"),
                    d.get("low"),
                    d.get("close"),
                    d.get("volume"),
                ])
    print(str(out_path))

if __name__ == "__main__":
    main()