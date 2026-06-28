from packet import Packet
import uuid


class BPDU(Packet):
    def __init__(self,source_mac,destination_mac,root_id,bridge_id,path_cost,network_event_scheduler):
        super().__init__(source_mac,destination_mac,header_size=20,payload_size=50,network_event_scheduler=network_event_scheduler)
        self.payload = {
            "root_id":root_id,
            "bridge_id":bridge_id,
            "path_cost":path_cost
        }

    def __str__(self):
        return f'BPDU(souce: {self.header["source_mac"]}, destination: {self.header["destination_mac"]}, root_id: {self.payload["root_id"]}, bridge_id: {self.payload["bridge_id"]}, path_cost: {self.payload["path_cost"]})'