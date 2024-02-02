from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.requests import Request
from starlette.routing import Route
import uvicorn
import csv
from datetime import datetime


async def price_data(request: Request) -> JSONResponse:
    """
    Return price data for the requested symbol
    """
    symbol = request.path_params['symbol']
    year = request.query_params.get('year', None)
    
    if not validateSymbol(symbol) :
        return JSONResponse({'error': 'Invalid character provided in symbol'}, status_code=400)
    
    year = validateYear(year)
    
    res = getData(symbol=symbol, year=year)
    
    res = sorted(res, key = getDate)
    
    return JSONResponse(res)


# Todo: Service level logic. To be Refactored into a separate file    
def getDate(obj):
    return datetime.strptime(obj['date'], '%d/%m/%Y')

def getData(symbol, year) -> []:
    res = []
    
    with open('data/nifty50_all.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            
            if(row['Symbol'].lower() == symbol):
                row = {k.lower(): v for k, v in row.items()}
                row.pop('symbol', None)
                dataDate = datetime.strptime(row['date'], '%Y-%m-%d')
                formattedDate = dataDate.strftime('%d/%m/%Y')
                
                if (year is not None):
                    if year == dataDate.year  :
                        row['date'] = formattedDate
                        res.append(row)
                        
                else :
                    row['date'] = formattedDate
                    res.append(row)
    
    return res

def validateSymbol(sym) -> bool:
    allowed_characters = set("&abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_ ")

    for char in sym:
        if char not in allowed_characters:
            return False
        
    return True

def validateYear(yr) -> int:
    if yr is not None:
        try:
            yr = int(yr)
            if not (1000 <= yr <= 9999):
                raise ValueError('Year is not a four digit integer')
            return yr
        except ValueError as e:
            return JSONResponse({'error': str(e)}, status_code=400)

# URL routes
app = Starlette(debug=True, routes=[
    Route('/nifty/stocks/{symbol}', price_data)
])


def main() -> None:
    """
    start the server
    """
    uvicorn.run(app, host='0.0.0.0', port=8888)
    
# Entry point
main()
