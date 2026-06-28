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
from switch import Switch
from collections import defaultdict

if __name__ == "__main__":
    network_event_scheduler = NetworkEventScheduler(log_enabled=True,verbose=True,stp_verbose=True)

    node1 = Node("n1","00:1A:2B:3C:4D:5C",network_event_scheduler)
    node2 = Node("n2","00:1B:2C:3D:4E:5D",network_event_scheduler)
    #node3 = Node("n3","00:1B:2C:3D:4E:5E",network_event_scheduler)
    #node4 = Node("n4","00:1B:2C:3D:4E:5F",network_event_scheduler)

    switch1 = Switch("s1",network_event_scheduler)
    switch2 = Switch("s2",network_event_scheduler)
    switch3 = Switch("s3",network_event_scheduler)
    switch4 = Switch("s4",network_event_scheduler)




    link_n1_s1 = Link(node1,switch1,bandwidth=10000,delay=0.01,packet_loss=0,network_event_scheduler=network_event_scheduler)
    link_n2_s4 = Link(node2,switch4,bandwidth=10000,delay=0.01,packet_loss=0,network_event_scheduler=network_event_scheduler)
    link_s1_s2 = Link(switch2,switch1,bandwidth=10000,delay=0.01,packet_loss=0,network_event_scheduler=network_event_scheduler)
    link_s1_s3 = Link(switch1,switch3,bandwidth=10000,delay=0.01,packet_loss=0,network_event_scheduler=network_event_scheduler)
    link_s1_s4 = Link(switch1,switch4,bandwidth=10000,delay=0.01,packet_loss=0,network_event_scheduler=network_event_scheduler)
    link_s2_s3 = Link(switch2,switch3,bandwidth=10000,delay=0.01,packet_loss=0,network_event_scheduler=network_event_scheduler)
    link_s2_s4 = Link(switch2,switch4,bandwidth=10000,delay=0.01,packet_loss=0,network_event_scheduler=network_event_scheduler)
    link_s3_s4 = Link(switch3,switch4,bandwidth=10000,delay=0.01,packet_loss=0,network_event_scheduler=network_event_scheduler)

    node1.set_traffic(destination=node2.mac_address,bitrate=1000,start_time=1,duration=10,burstiness=1,header_size=40,payload_size=120)
    #node2.set_traffic(destination=node4.mac_address,bitrate=1000,start_time=1,duration=10,burstiness=1,header_size=40,payload_size=120)

    network_event_scheduler.draw()
    network_event_scheduler.run()
    
    switch1.print_link_states()
    switch2.print_link_states()
    switch3.print_link_states()
    switch4.print_link_states()

    switches = [switch1,switch2,switch3,switch4]
    network_event_scheduler.draw_with_link_states(switches)

    switch1.print_forwarding_table()
    switch2.print_forwarding_table()
    switch3.print_forwarding_table()
    switch4.print_forwarding_table()
    #network_event_scheduler.generate_summary(network_event_scheduler.packet_logs)
    #network_event_scheduler.generate_throughput_graph(network_event_scheduler.packet_logs)
    #network_event_scheduler.generate_delay_histogram(network_event_scheduler.packet_logs)


