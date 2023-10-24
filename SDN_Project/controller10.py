import networkx as nx
import logging
import random
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.lib.packet import packet, ethernet, ipv4, udp, ether_types
from ryu.controller.handler import CONFIG_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.topology import event
from ryu.topology.api import get_all_switch, get_all_link
logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)

class SDNController(app_manager.RyuApp):

    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SDNController, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.topology_api_app = self
        self.topology_map = nx.Graph()  # Initialize the topology map
        self.switches = []
        self.links = []
        self.no_of_nodes = 0
        self.no_of_links = 0
        self.i=0
        self.src = 1
        self.dst = 5
        print("hi")
        LOG.info("SDN Controller initialized")




        

    @set_ev_cls([event.EventLinkAdd,event.EventLinkDelete])
    def get_topology_data(self, ev):
        
        switch_list = get_all_switch(self.topology_api_app)   
        switches=[switch.dp.id for switch in switch_list]
        self.switches = switch_list
        self.topology_map.add_nodes_from(switches)
        # print(switches)
        links_list = get_all_link(self.topology_api_app)
        links=[(link.src.dpid,link.dst.dpid,{'port':link.src.port_no}) for link in links_list]
        self.topology_map.add_edges_from(links)
        links = [(link.src.dpid, link.dst.dpid, {'port': link.src.port_no, 'weight': random.randint(1, 10)}) for link in links_list]
        self.topology_map.add_edges_from(links)
        self.links = links_list
        for link in links:
            weight = link[2]['weight']
            print(f"Weight: {weight}")

        # print ("**********List of links")
        # print (self.topology_map.edges())
        print(self.topology_map.nodes)
        print(len(links))
        if(len(links) == 28):
            self.run()
            

    def add_flow(self, datapath, priority, src_port, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        match = parser.OFPMatch(
                eth_src = self.src,
                eth_dst = self.dst,
                )
        mod = parser.OFPFlowMod(
            datapath=datapath,
            priority=priority,
            match=match,
            instructions=inst
        )
        datapath.send_msg(mod)
        # LOG.info("Flow rule installed on switch %s: Match=%s, Actions=%s", datapath.id, match, actions)

    def calculate_shortest_path(self, source, destination):
        try:
            shortest_path = nx.shortest_path(self.topology_map, source, destination)
            # LOG.info("Shortest path from %s to %s: %s", source, destination, shortest_path)
            return shortest_path
        except nx.NetworkXNoPath:
            # LOG.error("No path found from %s to %s", source, destination)
            return None

    def set_forwarding_rules(self, src, dst):
        print("hi")
        path = self.calculate_shortest_path(src, dst)
        if not path:
            return  # No path exists between source and destination
        print(path)
        print(",,,,,,,,,,,,,,,,,,,,,,,,")
        for i in range(len(path) - 1):
            print(len(path))
            print(i)
            src_dpid = path[i]
            dst_dpid = path[i+1]
            dst_port = self.topology_map[dst_dpid][src_dpid]['port']
            
            for swich in self.switches:
                if swich.dp.id == src_dpid:
                    ofproto = swich.dp.ofproto
                    datapath = swich.dp
                    actions = [swich.dp.ofproto_parser.OFPActionOutput(dst_port)]
                    ofproto = datapath.ofproto
                    parser = datapath.ofproto_parser

                    inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
                    match = parser.OFPMatch(
                            eth_src = src,
                            eth_dst = dst,
                            )
                    mod = parser.OFPFlowMod(
                        datapath=datapath,
                        priority=1,
                        match=match,
                        instructions=inst
                    )
                    datapath.send_msg(mod)

    def run(self ):
        self.set_forwarding_rules(self.src , self.dst)
        self.set_forwarding_rules(self.dst , self.src)

