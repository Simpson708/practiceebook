from flask import Flask, render_template, request
import yfinance as yf

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    data = None
    error = None

    if request.method == "POST":
        ticker = request.form.get("ticker").upper()

        try:
            stock = yf.Ticker(ticker)
            info = stock.history(period="1mo")

            if info.empty:
                error = "Ticker not found. Try another symbol."
            else:
                current_price = info["Close"].iloc[-1]
                prev_price = info["Close"].iloc[-2]
                percent_change = round(((current_price - prev_price) / prev_price) * 100, 2)

                data = {
                    "ticker": ticker,
                    "current_price": round(current_price, 2),
                    "percent_change": percent_change,
                    "chart": info["Close"].to_list(),
                    "dates": info.index.strftime('%Y-%m-%d').to_list()
                }

        except Exception as e:
            error = "Error fetching data."

    return render_template("index.html", data=data, error=error)

if __name__ == '__main__':
    app.run(debug=True)
