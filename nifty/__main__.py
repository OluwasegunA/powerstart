from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.requests import Request
from starlette.routing import Route
import uvicorn
from datetime import datetime
from extension.__extensions__ import validateSymbol
from extension.__extensions__ import validateYear
from extension.__extensions__ import getData
from extension.__extensions__ import getDate
from extension.__extensions__ import getData
from extension.__extensions__ import isValidDate
from extension.__extensions__ import filteredStock

stocks = getData()

async def price_data(request: Request) -> JSONResponse:
    """
    Return price data for the requested symbol
    """
    symbol = request.path_params['symbol']
    year = request.query_params.get('year', None)
    
    if not validateSymbol(symbol) :
        return JSONResponse({'error': 'Invalid character provided in symbol'}, status_code=400)
    
    year = validateYear(year)
    result = filteredStock(stocks, symbol=symbol, year=year)
    
    result = sorted(result, key = getDate)
    
    return JSONResponse(result)



async def add_data(request: Request):
    try:
        
        symbol = request.path_params['symbol']
        
        if not validateSymbol(symbol) :
            return JSONResponse({'error': 'Invalid character provided in symbol'}, status_code=400)
        
        payload = await request.json()

        for data in payload:
            date = data.get('date')
            close = data.get('close')  
            high = data.get('high')
            open = data.get('open')  
            low = data.get('low')

            if not (symbol and date and close and high and open and low):
                return JSONResponse({'error': 'Invalid payload. Ensure all required fields are provided.'}, status_code=400)

            if not isValidDate(date):
                return JSONResponse({'error': 'Invalid date format. Use DD/MM/YYYY.'}, status_code=400)
            
            if any(item == data for item in stocks):
                return JSONResponse({'error': 'Duplicate stock price data'}, status_code=409)
            
            symbol = symbol.upper()
            
            stock = {
                'Symbol': symbol,
                'date': date,
                'close': close,
                'low': low,
                'open': open,
                'high': high
            }
            
            dataDate = datetime.strptime(date, '%d/%m/%Y')
            stock['date'] = dataDate.strftime('%Y-%m-%d')
            
            stocks.append(stock)
                    
        return JSONResponse({'message': 'Data added successfully.', 'data': stock}, status_code=201)
    except Exception as e:
        return JSONResponse({'error': str(e)}, status_code=500)


# URL routes
app = Starlette(debug=True, routes=[
    Route('/nifty/stocks/{symbol}', price_data),
    Route('/nifty/stocks/{symbol}', add_data, methods=["POST"])
])


def main() -> None:
    """
    start the server
    """
    uvicorn.run(app, host='0.0.0.0', port=8888)
    
# Entry point
main()
