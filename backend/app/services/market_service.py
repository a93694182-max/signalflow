from datetime import datetime

import yfinance as yf
from fastapi import HTTPException, status


SYMBOL_NAMES = {
    "^KS11": "KOSPI",
    "^KQ11": "KOSDAQ",
    "KRW=X": "원/달러 환율",
    "BTC-USD": "비트코인",
    "GC=F": "금 선물",
    "CL=F": "WTI 원유",
}


ALLOWED_PERIODS = {
    "5d",
    "1mo",
    "3mo",
    "6mo",
    "1y",
    "2y",
    "5y",
}

ALLOWED_INTERVALS = {
    "1d",
    "1wk",
    "1mo",
}



def get_market_price(symbol: str) -> dict:
    ticker = yf.Ticker(symbol)

    try:
        history = ticker.history(period="5d", interval="1d")
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="시장 데이터를 가져오는 중 오류가 발생했습니다.",
        ) from exc

    if history.empty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{symbol} 시장 데이터를 찾을 수 없습니다.",
        )

    closes = history["Close"].dropna()

    if closes.empty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{symbol} 종가 데이터를 찾을 수 없습니다.",
        )

    price = float(closes.iloc[-1])

    if len(closes) >= 2:
        previous_close = float(closes.iloc[-2])
    else:
        previous_close = price

    change = price - previous_close
    change_percent = (
        change / previous_close * 100
        if previous_close != 0
        else 0.0
    )

    market_time_value = closes.index[-1]
    market_time = market_time_value.to_pydatetime()

    return {
        "symbol": symbol,
        "name": SYMBOL_NAMES.get(symbol, symbol),
        "price": round(price, 2),
        "previous_close": round(previous_close, 2),
        "change": round(change, 2),
        "change_percent": round(change_percent, 2),
        "currency": ticker.fast_info.get("currency"),
        "market_time": market_time,
    }


def get_market_dashboard() -> dict:
    symbols = list(SYMBOL_NAMES.keys())

    markets = []

    for symbol in symbols:
        try:
            market = get_market_price(symbol)
            markets.append(market)
        except HTTPException:
            continue

    if not markets:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="시장 데이터를 가져오지 못했습니다.",
        )

    return {
        "markets": markets,
    }




def get_market_history(
    symbol: str,
    period: str = "1mo",
    interval: str = "1d",
) -> dict:
    if period not in ALLOWED_PERIODS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"지원하지 않는 period입니다: {period}",
        )

    if interval not in ALLOWED_INTERVALS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"지원하지 않는 interval입니다: {interval}",
        )

    ticker = yf.Ticker(symbol)

    try:
        history = ticker.history(
            period=period,
            interval=interval,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="시장 히스토리를 가져오는 중 오류가 발생했습니다.",
        ) from exc

    if history.empty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{symbol} 히스토리 데이터를 찾을 수 없습니다.",
        )

    points = []

    for index, row in history.iterrows():
        points.append(
            {
                "time": index.to_pydatetime(),
                "open": round(float(row["Open"]), 2),
                "high": round(float(row["High"]), 2),
                "low": round(float(row["Low"]), 2),
                "close": round(float(row["Close"]), 2),
                "volume": int(row["Volume"]),
            }
        )

    return {
        "symbol": symbol,
        "name": SYMBOL_NAMES.get(symbol, symbol),
        "period": period,
        "interval": interval,
        "points": points,
    }

