from src.models.alerts.alert import Alert
from src.common.database import Database

Database.initialize()
alert_needing_update = Alert.find_need_update()

for alert in alert_needing_update:
    alert.load_item_price()
    alert.send_if_price_reached()
