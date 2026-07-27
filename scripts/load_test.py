import requests
import time
import concurrent.futures

BASE_URL = "http://127.0.0.1:8000/api/v1"


def test_screener(req_id):
    start = time.time()
    res = requests.get(f"{BASE_URL}/screener?min_roe=15")
    duration = time.time() - start
    return req_id, res.status_code, duration


def test_profile(ticker):
    start = time.time()
    res = requests.get(f"{BASE_URL}/companies/{ticker}")
    duration = time.time() - start
    return ticker, res.status_code, duration


def run_tests():
    print("\n🚀 --- 1. Testing 10 Concurrent Screener Queries ---")
    screener_start = time.time()

    # Simulating 10 users requesting at the exact same time
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(test_screener, range(10)))

    screener_total = time.time() - screener_start

    for r in results:
        status_icon = "✅" if r[1] == 200 else "❌"
        print(f"Request {r[0]+1}: {status_icon} Status {r[1]} | Time: {r[2]:.4f}s")

    print(f"\n🎯 >>> Total time for 10 concurrent requests: {screener_total:.4f}s")
    if screener_total < 10:
        print("✅ PASS: Completed within 10 seconds target!")
    else:
        print("❌ FAIL: Took longer than 10 seconds.")

    print("\n🚀 --- 2. Testing Company Profile Load Times ---")
    tickers = ["TCS", "RELIANCE", "INFY", "HDFCBANK", "ABB"]

    for ticker in tickers:
        t, status, duration = test_profile(ticker)
        status_icon = "✅" if status == 200 else "❌"
        print(
            f"Profile {ticker}: {status_icon} Status {status} | Time: {duration:.4f}s"
        )
        if duration > 3:
            print(f"   ⚠️ WARNING: {ticker} took longer than 3 seconds target!")


if __name__ == "__main__":
    run_tests()
