# Import the necessary packages
import yfinance as yf
import telepot
from timeloop import Timeloop
from datetime import timedelta


# Information regarding the telegram bot
TELE_BOT_HANDLE = "CaiStockAlertBot"
TELE_HTTP_TOKEN = "6613311512:AAF4s2Pn7B0Nggs5_V2pAbhmvwpTWMZENsE"
RECIEVER_ID = 1364159898

# Create the information of the stock and the alert price
stock_watchlist = {
    "ADM" : 150,
    "HUM" : 1350,
    "JNJ" : 1140
}


# This function will take in the stock ticker and return information regarding the price of the stock
def getStockPrice(ticker, interval = "15m"):
    """
    ================================ INPUTS =================================
    ticker: The stock ticker symbol
    interval: The duration in between in which the stock price data is returned
    ================================ OUTPUTS ================================
    stock_price: (current price, previous price)
    """

    #Get the stock price at that day
    stock_price = yf.download(tickers=ticker, period='1d', interval=interval)
    
    return (stock_price.iloc[-1]['Close'], stock_price.iloc[-2]['Close'])



# This function will craft the message for the telegram bot
def generateMessage(ticker, stock_price, target_price):
    """
    ================================ INPUTS =================================
    ticker: The stock ticker symbol
    stock_price: The closing price of the stock
    target_price: The hit price that I want to be alerted for
    ================================ OUTPUTS ================================
    message: The crafted message to be sent on telegram
    """

    # Crafting the message
    message = f"{ticker}\n${round(stock_price,2)}\nHave hit the set threshold level of ${round(target_price,2)}"

    return message


# This function will send the message with the telegram cahtbot
def sendMessage(message):
    """
    ================================ INPUTS =================================
    message: The crafted message to be sent on telegram
    """

    # Create an instance of the telegram bot
    bot = telepot.Bot(TELE_HTTP_TOKEN)

    # Sending the message
    bot.sendMessage(RECIEVER_ID,message)



# Create the main logic for checking the price
def checkStock(stock_watchlist):

    # Iterate through all the stocks of interest
    for ticker, target_price in stock_watchlist.items():

        # Get the current and previous price
        current_price, previous_price = getStockPrice(ticker)

        # Check if it is a send condition
        if (current_price <= target_price) or (previous_price > target_price):
            
            # Send the message
            message = generateMessage(ticker, current_price, target_price)
            sendMessage(message)


# Create the time loop object
tl = Timeloop()

@tl.job(interval=timedelta(seconds=900))
def runCheck():
    checkStock(stock_watchlist)



# run the main file 
if __name__ == "__main__":
   tl.start(block=True)