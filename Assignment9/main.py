from fix_parser import FixParser
from order import Order, OrderState
from risk_engine import RiskEngine
from logger import Logger

fix = FixParser()
risk = RiskEngine()
log = Logger()

# raw = "8=FIX.4.2|35=D|55=AAPL|54=1|38=500|40=2|10=128"
raw = "8=FIX.4.2|35=D|55=AAPL|44=50|54=1|38=500|40=2|10=128"
msg = fix.parse(raw)
order = Order(symbol=msg["55"], qty=int(msg["38"]), side=msg["54"], price=msg['44'])
log.log("OrderCreated", msg)

try:
    risk.check(order)
    order.transition(OrderState.ACKED)
    risk.update_position(order)
    order.transition(OrderState.FILLED)
    log.log("OrderFilled", {"symbol": order.symbol, "qty": order.qty})
except ValueError as e:
    order.transition(OrderState.REJECTED)
    log.log("OrderRejected", {"reason": str(e)})

log.save()