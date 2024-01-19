import nmap
import socket
import networkx as nx
import matplotlib.pyplot as plt
import subprocess
import csv

# Function to get a valid IP address from the user
def get_valid_ip_address():
    while True:
        ip_or_hostname = input("Please enter the target IP address or hostname: ")
        try:
            ip_address = socket.gethostbyname(ip_or_hostname)
            return ip_address
        except socket.error:
            print("Invalid IP address or hostname. Please try again.")


# Function to perform a simple port scan using socket
def simple_port_scan(ip_addr, start_port, end_port):
    
    open_ports = []  # List to store open ports
    try:
        # Loop through the specified range of ports and attempt to connect
        for port in range(start_port, end_port + 1):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(5)
                result = s.connect_ex((ip_addr, port))
                if result == 0:
                    print(f"The port {port} is open")
                    open_ports.append(port)
        # Display the result of the port scan
        if open_ports:
            print("Open Ports:", open_ports)
        else:
            print("No open ports found in the specified range.")
    except ValueError:
        print("Invalid port range. Please enter a valid range.")

# set port range yhaa se port range set kro




def user_based_scan(target):
    try:
        # Create an nmap scanner object
        nm = nmap.PortScanner()

        # Perform a service version detection scan
        nm.scan(hosts=target, arguments='-p 1-1000 -sV')  # Customize the arguments based on your project needs

        # Display the results of the user-based scan
        for host in nm.all_hosts():
            print(f"Host: {host}")
            for proto in nm[host].all_protocols():
                print(f"Protocol: {proto}")
                ports = nm[host][proto].keys()
                for port in ports:
                    print(f"Port: {port}\tState: {nm[host][proto][port]['state']}\tService: {nm[host][proto][port]['name']}")
    except nmap.PortScannerError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Function to perform a targeted scan using nmap

def scan_target(target):
    try:
        # Create a scanner object
        scanner = nmap.PortScanner()

        # Perform a basic scan on the target
        scanner.scan(target, arguments='-p 1-1000')

        # Print scan results
        for host in scanner.all_hosts():
            print('Host : %s (%s)' % (host, scanner[host].hostname()))
            print('State : %s' % scanner[host].state())

            # Print open ports and services
            for proto in scanner[host].all_protocols():
                print('Protocol : %s' % proto)
                ports = list(scanner[host][proto].keys())
                ports.sort()
                for port in ports:
                    print('Port : %s\tState : %s' % (port, scanner[host][proto][port]['state']))
                    print('Service : %s' % scanner[host][proto][port]['name'])
    except nmap.PortScannerError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Function to perform an aggressive scan using nmap
def nmap_aggressive_scan(target):
    try:
        # Create an nmap scanner object
        nm = nmap.PortScanner()

        # Perform an aggressive scan using the -A option
        nm.scan(hosts=target, arguments='-A')

        # Display the results of the aggressive scan
        for host in nm.all_hosts():
            print(f"Host: {host}")
            for proto in nm[host].all_protocols():
                print(f"Protocol: {proto}")
                ports = nm[host][proto].keys()
                for port in ports:
                    print(f"Port: {port}\tState: {nm[host][proto][port]['state']}\tService: {nm[host][proto][port]['name']}")
    except nmap.PortScannerError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Function to perform network scanning using Nmap
def scan_network():
    result = subprocess.run(['nmap', '-sn', '192.168.18.0/24'], capture_output=True)
    output = result.stdout.decode('utf-8')
    return output

# Function to parse the scanning results and build the network topology
def build_topology(scan_output):
    devices = []

    lines = scan_output.split('\n')
    for line in lines:
        if 'Nmap scan report for' in line:
            device = line.split(' ')[4]
            devices.append(device)

    return devices

# Function to visualize and save the network topology as a graph
def visualize_topology(devices):
    G = nx.connected_watts_strogatz_graph(len(devices), k=4, p=0.2)  # Adjust k and p as needed

    node_labels = {i: device for i, device in enumerate(devices)}

    pos = nx.spring_layout(G, k=0.1)
    plt.figure(figsize=(10, 10))
    nx.draw(G, pos, with_labels=True, labels=node_labels, node_color='lightblue', node_size=600, font_size=7)
    nx.draw_networkx_edges(G, pos, width=2.0, alpha=0.5)
    plt.savefig('network_topology.png')

    plt.show()
    plt.close()

    # Save devices data to CSV
    save_devices_to_csv(devices)

def save_devices_to_csv(devices):
    with open('devices_data.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Device'])
        for device in devices:
            csv_writer.writerow([device])

# Main function to orchestrate the network scanning and topology building process
def main():
    while True:
        print("Select an option:")
        print("1. Service Version Detection (nmap)")
        print("2. Basic Port Scan (socket)")
        print("3. Specify Address Scan (nmap)")
        print("4. Aggressive Scan")
        print("5. Network Topology Scan")
        print("6. Exit")
        
        choice = input("Enter your choice (1/2/3/4/5/6): ")

        if choice == '1':
            # User chooses service version detection
            user_based_scan_target = get_valid_ip_address()
            user_based_scan(user_based_scan_target)

        elif choice == '2':
            # User chooses basic port scan
            ip_addr = get_valid_ip_address()
            print("The IP you entered is:", ip_addr)
            port_range = input("Enter the range of ports you want to scan (e.g., 1-1024): ")
            start_port, end_port = map(int, port_range.split('-'))
            simple_port_scan(ip_addr, start_port, end_port)

        elif choice == '3':
            # User chooses to scan a specific address
            specific_scan_target = get_valid_ip_address()
            scan_target(specific_scan_target)

        elif choice == '4':
            # User chooses Aggressive scan
            aggressive_scan_target = get_valid_ip_address()
            nmap_aggressive_scan(aggressive_scan_target)

        elif choice == '5':
            # User chooses Network Topology Scan
            scan_output = scan_network()
            devices = build_topology(scan_output)
            visualize_topology(devices)

        elif choice == '6':
            # User chooses to exit the program
            print("Exiting the program. Goodbye!")
            break

        else:
            # Invalid choice
            print("Invalid choice. Please enter 1, 2, 3, 4, 5, or 6.")

main()