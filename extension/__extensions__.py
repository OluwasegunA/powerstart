from starlette.responses import JSONResponse
import csv
from datetime import datetime

def getDate(obj):
    return datetime.strptime(obj['date'], '%d/%m/%Y')

def isValidDate(date):
    try:
        datetime.strptime(date, '%d/%m/%Y')
        return True
    except ValueError:
        return False


def getData() -> []:
    data = []
    with open('data/nifty50_all.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

def filteredStock(stocks, symbol, year) -> []:
   res = []
   for row in stocks:
      if row.get('Symbol').lower() == symbol :
         row = {k.lower(): v for k, v in row.items()}
         row.pop('symbol', None)
         dataDate = datetime.strptime(row['date'], '%Y-%m-%d')
         formattedDate = dataDate.strftime('%d/%m/%Y')
                  
         if year is not None :
            if year == dataDate.year  :
               row['date'] = formattedDate
               res.append(row)
                           
         else :
            row['date'] = formattedDate
            res.append(row)
        
   return res

def validateSymbol(sym) -> bool:
    allowed_characters = set("&abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_ ")
    
    if any(char not in allowed_characters for char in sym):
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
