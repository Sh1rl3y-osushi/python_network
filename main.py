import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import uuid
import heapq
import random
import sys

from network_event import NetworkEventScheduler
from link import Link
from node import Node
from packet import Packet
from collections import defaultdict




if __name__ == "__main__":
    network_event_scheduler = NetworkEventScheduler(log_enabled=True,verbose=True)

    node1 = Node(1,"192.168.1.1",network_event_scheduler)
    node2 = Node(2,"192.168.1.2",network_event_scheduler)

    link_1to2 = Link(node1,node2,bandwidth=10000,delay=0.01,packet_loss=0.1,network_event_scheduler=network_event_scheduler)
    
    #network_event_scheduler.draw()
    header_size = 40
    payload_size = 120
    node1.set_traffic(destination="192.168.1.2",bitrate=1000,start_time=1,duration=10,burstiness=1,header_size=header_size,payload_size=payload_size)

    network_event_scheduler.run()

    network_event_scheduler.generate_summary(network_event_scheduler.packet_logs)

