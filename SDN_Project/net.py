from mininet.net import Mininet
from mininet.node import OVSSwitch, RemoteController
from mininet.cli import CLI
from mininet.link import TCLink

def create_topology():
    net = Mininet(controller=RemoteController, link=TCLink)

    net.addController('c1', controller=RemoteController, ip='127.0.0.1', port=6633)

    # Create switches with dpID
    switch1 = net.addSwitch('s1', cls=OVSSwitch, dpid='1')
    switch2 = net.addSwitch('s2', cls=OVSSwitch, dpid='2')
    switch3 = net.addSwitch('s3', cls=OVSSwitch, dpid='3')
    switch4 = net.addSwitch('s4', cls=OVSSwitch, dpid='4')
    switch5 = net.addSwitch('s5', cls=OVSSwitch, dpid='5')
    switch6 = net.addSwitch('s6', cls=OVSSwitch, dpid='6')
    switch7 = net.addSwitch('s7', cls=OVSSwitch, dpid='7')
    switch8 = net.addSwitch('s8', cls=OVSSwitch, dpid='8')


 


    # Create hosts
    host1 = net.addHost('h1', ip='10.0.0.1/24', defaultRoute='via 10.0.0.100')
    host2 = net.addHost('h2', ip='10.0.0.2/24', defaultRoute='via 10.0.0.200')
    host3 = net.addHost('h3', ip='10.0.0.3/24', defaultRoute='via 10.0.0.100')
    host4 = net.addHost('h4', ip='10.0.0.4/24', defaultRoute='via 10.0.0.200')
    host5 = net.addHost('h5', ip='10.0.0.5/24', defaultRoute='via 10.0.0.200')
    host6 = net.addHost('h6', ip='10.0.0.6/24', defaultRoute='via 10.0.0.100')
    host7 = net.addHost('h7', ip='10.0.0.7/24', defaultRoute='via 10.0.0.200')
    host8 = net.addHost('h8', ip='10.0.0.8/24', defaultRoute='via 10.0.0.200')

    # Connect switches
    net.addLink(switch1, switch3, cls=TCLink, bw=1000, delay='1ms')
    net.addLink(switch1, switch8, cls=TCLink, bw=1000, delay='1ms')
    net.addLink(switch3, switch4, cls=TCLink, bw=1000, delay='1ms')
    net.addLink(switch3, switch6, cls=TCLink, bw=1000, delay='1ms')
    net.addLink(switch3, switch8, cls=TCLink, bw=1000, delay='1ms')
    net.addLink(switch4, switch7, cls=TCLink, bw=1000, delay='1ms')
    net.addLink(switch5, switch7, cls=TCLink, bw=1000, delay='1ms')
    net.addLink(switch5, switch2, cls=TCLink, bw=1000, delay='1ms')
    net.addLink(switch5, switch4, cls=TCLink, bw=1000, delay='1ms')
    net.addLink(switch6, switch8, cls=TCLink, bw=1000, delay='1ms')
    net.addLink(switch6, switch5, cls=TCLink, bw=1000, delay='1ms')
    net.addLink(switch8, switch7, cls=TCLink, bw=1000, delay='1ms')
    net.addLink(switch2, switch7, cls=TCLink, bw=1000, delay='1ms')
    net.addLink(switch2, switch4, cls=TCLink, bw=1000, delay='1ms')


    # Connect hosts to switches
    net.addLink(host1, switch1, cls=TCLink, bw=1000, delay='1ms')
    net.addLink(host2, switch2, cls=TCLink, bw=1000, delay='1ms')
    net.addLink(host3, switch3, cls=TCLink, bw=1000, delay='1ms')
    net.addLink(host4, switch4, cls=TCLink, bw=1000, delay='1ms')
    net.addLink(host5, switch5, cls=TCLink, bw=1000, delay='1ms')
    net.addLink(host6, switch6, cls=TCLink, bw=1000, delay='1ms')
    net.addLink(host7, switch7, cls=TCLink, bw=1000, delay='1ms')
    net.addLink(host8, switch8, cls=TCLink, bw=1000, delay='1ms')

    # Start the network
    net.start()

    # Enable ICMP on hosts for ping
    for host in net.hosts:
        host.cmd('sysctl -w net.ipv4.icmp_echo_ignore_all=0')

    # Enter the Mininet command line interface
    CLI(net)

    # Stop the network
    net.stop()

if __name__ == '__main__':
    create_topology()
