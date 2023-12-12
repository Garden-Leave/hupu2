from prometheus_client import Gauge, Counter, start_http_server
import time


c1 = Counter('request_total', 'total request handled',['pod','node','code'])
g1 = Gauge('request_latency', 'latency per request')

if __name__=='__main__':
    start_http_server(9090)
    for a in range(100):
        c1.labels('pod1','node1').inc(1)
        time.sleep(3)



