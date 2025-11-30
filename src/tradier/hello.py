import os, dotenv
from pathlib import Path

from lumiwealth_tradier import Tradier

dotenv.load_dotenv()

tradier_acct = os.getenv('tradier_acct')

tradier_token = os.getenv('tradier_token')

if not tradier_acct or not tradier_token:
    dotenv.load_dotenv(Path(__file__).parent / '.env')
    tradier_acct = tradier_acct or os.getenv('tradier_acct')
    tradier_token = tradier_token or os.getenv('tradier_token')

tradier = Tradier(tradier_acct, tradier_token, is_paper=True)

quotes_data = tradier.market.get_quotes(["AAPL", "MSFT", "SPY"])

print(quotes_data)

start_date="2025-10-31"
end_date="2025-11-11"

data = tradier.market.get_historical_quotes(
    symbol="AAPL",
    interval="daily",
    start_date=start_date,
    end_date=end_date
)

print(data.head())

timesales = tradier.market.get_timesales(
    "MSFT",
    interval=5,  # Can be 1, 5 or 15
    start_date=start_date,
    end_date=end_date,
    session_filter="all",  # Can be "all" or "open"
)

print(timesales.head())

chains = tradier.market.get_option_chains("DASH", expiration="2025-11-28", greeks=True)

print(chains.head())