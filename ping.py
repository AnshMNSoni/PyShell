import socket
import os
import time
import struct
import select
import platform
import subprocess
from rich.console import Console
from rich.text import Text

console = Console()

ICMP_ECHO_REQUEST = 8

def checksum(source_string):
    countTo = (len(source_string) // 2) * 2
    sum = 0
    count = 0

    while count < countTo:
        thisVal = source_string[count + 1] * 256 + source_string[count]
        sum = sum + thisVal
        sum = sum & 0xffffffff
        count += 2

    if countTo < len(source_string):
        sum += source_string[-1]
        sum = sum & 0xffffffff

    sum = (sum >> 16) + (sum & 0xffff)
    sum += (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff
    answer = (answer >> 8) | ((answer << 8) & 0xff00)
    return answer

def create_packet(id, sequence):
    header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, 0, id, sequence)
    data = struct.pack('d', time.time())
    chksum = checksum(header + data)
    header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, socket.htons(chksum), id, sequence)
    return header + data

def receive_one_ping(sock, id, timeout):
    time_left = timeout
    while True:
        start_select = time.time()
        ready = select.select([sock], [], [], time_left)
        duration_select = time.time() - start_select
        if ready[0] == []:  # Timeout
            return None, 0

        time_received = time.time()
        rec_packet, addr = sock.recvfrom(1024)
        icmp_header = rec_packet[20:28]
        type, code, checksum_rcv, packet_id, sequence = struct.unpack('bbHHh', icmp_header)

        if packet_id == id:
            bytes_in_double = struct.calcsize('d')
            time_sent = struct.unpack('d', rec_packet[28:28 + bytes_in_double])[0]
            rtt = (time_received - time_sent) * 1000
            return addr[0], rtt

        time_left = time_left - duration_select
        if time_left <= 0:
            return None, 0

def send_one_ping(sock, dest_addr, id, sequence):
    packet = create_packet(id, sequence)
    sock.sendto(packet, (dest_addr, 1))

def do_one_ping(dest_addr, timeout, id, sequence):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp"))
    except PermissionError:
        raise PermissionError("Root privileges required to send ICMP packets.")

    send_one_ping(sock, dest_addr, id, sequence)
    addr, rtt = receive_one_ping(sock, id, timeout)
    sock.close()
    return addr, rtt

def system_ping(host, count=4, interval=1, timeout=1):
    system = platform.system()
    if system == "Windows":
        cmd = ["ping", "-n", str(count), "-w", str(int(timeout * 1000)), host]
    else:
        cmd = ["ping", "-c", str(count), "-i", str(interval), "-W", str(int(timeout)), host]

    try:
        with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True) as proc:
            for line in proc.stdout:
                console.print(line.rstrip())
    except Exception as e:
        console.print(f"[bold red]Ping failed:[/bold red] {e}")

def ping(host, count=4, timeout=1, interval=1):
    try:
        dest_addr = socket.gethostbyname(host)
    except socket.gaierror:
        console.print(f"[bold red]ping: unknown host {host}[/bold red]")
        return

    console.print(f"[bold green]PING[/bold green] {host} ({dest_addr}) 56(84) bytes of data.")

    id = os.getpid() & 0xFFFF
    sent_packets = 0
    received_packets = 0
    rtt_min = None
    rtt_max = None
    rtt_sum = 0.0

    try:
        for seq in range(count):
            addr, rtt = do_one_ping(dest_addr, timeout, id, seq)
            sent_packets += 1

            if addr:
                received_packets += 1
                rtt_sum += rtt
                rtt_min = rtt if rtt_min is None else min(rtt_min, rtt)
                rtt_max = rtt if rtt_max is None else max(rtt_max, rtt)
                msg = Text(f"56 bytes from {addr}: icmp_seq={seq} ttl=64 time={rtt:.2f} ms")
                msg.stylize("green")
                console.print(msg)
            else:
                msg = Text(f"Request timeout for icmp_seq {seq}")
                msg.stylize("yellow")
                console.print(msg)

            if seq < count - 1:
                time.sleep(interval)

        if received_packets == 0:
            console.print("[bold red]No packets received. Falling back to system ping.[/bold red]")
            system_ping(host, count, interval, timeout)
            return

    except PermissionError as e:
        console.print(f"[bold red]{e}[/bold red]")
        console.print("[bold yellow]Falling back to system ping.[/bold yellow]")
        system_ping(host, count, interval, timeout)
        return

    lost_packets = sent_packets - received_packets
    loss = (lost_packets / sent_packets) * 100
    console.print(f"\n--- {host} ping statistics ---")
    console.print(f"[bold]{sent_packets} packets transmitted, {received_packets} received, {loss:.0f}% packet loss[/bold]")
    if received_packets > 0:
        avg_rtt = rtt_sum / received_packets
        console.print(f"[bold]rtt min/avg/max = {rtt_min:.3f}/{avg_rtt:.3f}/{rtt_max:.3f} ms[/bold]")