from alice_blue import *
from datetime import date
from datetime import time
import datetime
import time
import traceback
import math
import api



alice  =None
socket_opened = False
indexLtp = None
strangle = True
entry = datetime.datetime(int(input("entery year: ")),
                               int(input("entry month: ")),
                               int(input("entry date: ")),
                               int(input("entry hour: ")),
                               int(input("entry min: ")),
                               int(input("entry sec: ")))

def login():
    global alice
    access_tokenn = AliceBlue.login_and_get_access_token(username=api.user, password=api.pwd, twoFA=api.twofa,api_secret=api.secret,app_id=api.app)
    alice = AliceBlue(username=api.user, password=api.pwd, access_token=access_tokenn)
    alice = AliceBlue(username=api.user, password=api.pwd, access_token=access_tokenn, master_contracts_to_download=['NSE','NFO'])

    
    def event_handler_quote_update(message):
        try:
            print(message)
            global indexLtp
            indexLtp = message['ltp']
            
            
        except Exception as e:
            traceback.print_exc()

    def open_callback():
        global socket_opened
        socket_opened = True

    alice.start_websocket(subscribe_callback=event_handler_quote_update,
                        socket_open_callback=open_callback,
                        run_in_background=True)
    while(socket_opened==False):
        pass
    alice.subscribe(alice.get_instrument_by_symbol('NSE', 'Nifty Bank'), LiveFeedType.MARKET_DATA) 

def place_order (transaction_type,symbol):
   # qty = int(symbol.lot_size)
    res= alice.place_order(transaction_type = TransactionType.Sell,
                     instrument = symbol,
                     quantity = 100,
                     order_type = OrderType.Market,
                     product_type = ProductType.Delivery,
                     price = 0.0,
                     trigger_price = None,
                     stop_loss = None,
                     square_off = None,
                     trailing_sl = None,
                     is_amo = False)
    print(res)


if __name__ == '__main__':
    login()
    time.sleep(10)
    ATMStrike = math.ceil(indexLtp/100)*100
    print(f'ATMStrike : {ATMStrike}')
    awayFromATM = 0
if datetime.datetime.now() == entry:
    ce_strike = alice.get_instrument_for_fno(symbol = 'BANKNIFTY', expiry_date=datetime.date(2022, 3, 3), is_fut=False, strike=ATMStrike + awayFromATM, is_CE = True)
    pe_strike = alice.get_instrument_for_fno(symbol = 'BANKNIFTY', expiry_date=datetime.date(2022, 3, 3), is_fut=False, strike=ATMStrike - awayFromATM, is_CE = False)

    print(ce_strike, pe_strike)

    
    place_order(TransactionType.Sell,ce_strike )
    place_order(TransactionType.Sell,pe_strike )

       