import time
from datetime import datetime
import cta_analytics.scraper as cas
db = cas.mongo_wrapper(server='192.168.1.120')
route_list = [2, 6, 55, 146, 136, 36, 148]
stop_list = [4862, 1427, 14019, 5037, 10575, 15193]
for j in range(25 * 60):
    print 'fired ' + datetime.now().isoformat()
    try:
        bus_res = cas.get_buses_on_route(route_list)
        print 'got bus'
        db.add_bus_locations(bus_res)
        print 'saved bus'
        pred_res = cas.get_predictions(stop_list)
        print 'got predictions'
        db.add_stop_prediction(pred_res)
        print 'saved predictions'
    except Exception as e:
        print e
        print 'there was an error'

    time.sleep(60)
