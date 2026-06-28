from link import Link
from BPDU import BPDU

class Switch:
    def __init__(self,node_id,network_event_scheduler):
        self.network_event_scheduler = network_event_scheduler
        self.node_id = node_id
        self.links = []
        self.forwaring_table = {}
        self.link_states = {}
        self.root_id = node_id
        self.root_path_cost = 0
        self.is_root = True
        label = f'Switch {node_id}'
        self.network_event_scheduler.add_node(node_id,label)

    def add_link(self,link):
        if link not in self.links:
            self.links.append(link)
            self.link_states[link] = "initial"
            self.send_bpdu()
    
    def send_bpdu(self):
        for link in self.links:
            bpdu = BPDU(source_mac = "00:00:00:00:00:00",destination_mac = "FF:FF:FF:FF:FF:FF",root_id=self.root_id,bridge_id=self.node_id,path_cost=self.root_path_cost,network_event_scheduler=self.network_event_scheduler)
            link.enqueue_packet(bpdu,self)

    def update_forwarding_table(self,source_address,link):
        self.forwaring_table[source_address] = link

    def receive_packet(self,packet,receieved_link):
        if isinstance(packet,BPDU):
            self.network_event_scheduler.log_packet_info(packet,"received BPDU",self.node_id)
            self.process_bpdu(packet,receieved_link)
        else:
            if packet.arrival_time == -1:
                self.network_event_scheduler.log_packet_info(packet,"lost",self.node_id)
                return
            self.network_event_scheduler.log_packet_info(packet,"received",self.node_id)

            source_address = packet.header["source_mac"]
            self.update_forwarding_table(source_address,receieved_link) 
            self.forward_packet(packet,receieved_link)

    def process_bpdu(self,bpdu,receieved_link):
        new_root_id = bpdu.payload["root_id"]
        new_path_cost = bpdu.payload["path_cost"] + 1

        root_info_chanded = new_root_id != self.root_id or new_path_cost < self.root_path_cost

        if self.network_event_scheduler.stp_verbose:
            current_time = self.network_event_scheduler.current_time
            print(f"Time {current_time} - {self.node_id} processing BPDU: new_root_id={new_root_id}, current_root_id = {self.root_id} ,new_path_cost = {new_path_cost}, current_path_cost = {self.root_path_cost}, root_info_changed = {root_info_chanded}")
        
        if new_root_id < self.root_id or (new_root_id == self.root_id and new_path_cost < self.root_path_cost):
            self.root_id = new_root_id
            self.root_path_cost = new_path_cost
            self.is_root = False

        self.update_link_states(receieved_link,new_path_cost)

        if root_info_chanded:
            self.send_bpdu()
    
    def update_link_states(self,receieved_link,received_bpdu_path_cost):
        if self.is_root:
            for link in self.links:
                self.link_states[link] = "forwarding"
        else:
            best_path_cost = float("inf")
            best_link = None
            best_link_id = None

            for link in self.links:
                if self.is_link_between_switches(link):
                    link_path_cost = self.get_link_cost(link) + received_bpdu_path_cost
                    link_id = min(link.node_x.node_id,link.node_y.node_id)
                    if link_path_cost < best_path_cost or (link_path_cost == best_path_cost and link_id < best_link_id):
                        best_path_cost = link_path_cost
                        best_link = link
                        best_link_id = link_id
            
            for link in self.links:
                if link == best_link or not self.is_link_between_switches(link):
                    self.link_states[link] = "forwarding"
                else:
                    self.link_states[link] = "blocked"
    
            if self.network_event_scheduler.stp_verbose:
                print(f"{self.node_id} link states updated: {self.link_states}")
    
    def is_link_between_switches(self,link):
        return isinstance(link.node_x,Switch) and isinstance(link.node_y,Switch)
    
    def get_link_cost(self,link):
        min_cost = 0.0000001
        return max(min_cost,1.0 / link.bandwidth)



    def forward_packet(self,packet,receieved_link):
        destination_address = packet.header["destination_mac"]
        if destination_address in self.forwaring_table:
            link = self.forwaring_table[destination_address]
            if self.link_states[link] == "forwarding":
                self.network_event_scheduler.log_packet_info(packet,"forwarded",self.node_id)
                link.enqueue_packet(packet,self)
        else:
            for link in self.links:
                if link != receieved_link and self.link_states[link] == "forwarding":
                    self.network_event_scheduler.log_packet_info(packet,"broadcast",self.node_id)
                    link.enqueue_packet(packet,self)

    def print_forwarding_table(self):
        print(f"Switch {self.node_id} Forwarding Table:")
        for dest, link in self.forwaring_table.items():
            linked_node = link.node_x.node_id if link.node_x.node_id != self.node_id else link.node_y.node_id
            print(f" MAC Address {dest}: Link {linked_node}")
    
    def print_link_states(self):
        print(f"Switch {self.node_id} (root = {self.is_root}) link states")
        for link in self.links:
            state = self.link_states[link]
            connected_node = link.node_x if link.node_x != self else link.node_y
            print(f" - link {self.node_id} - {connected_node.node_id}: {state}")

    def __str__(self):
        connected_nodes = [link.node_x.node_id if self.node_id != link.node_x.node_id else link.node_y.node_id for link in self.links]
        connected_node_str = ', '.join(map(str,connected_nodes))
        return f"Switch {self.node_id} conntected to nodes: {connected_node_str}"
    