import socket
import os
import time
import struct
import select
import threading
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from rich.console import Console
from rich.text import Text

console = Console()
ICMP_ECHO_REQUEST = 8
ping_data = {"sequence": [], "rtt": []}
lock = threading.Lock()


def checksum(source_string):
    countTo = (len(source_string) // 2) * 2
    sum = 0
    count = 0
    while count < countTo:
        thisVal = source_string[count + 1] * 256 + source_string[count]
        sum += thisVal
        sum &= 0xffffffff
        count += 2
    if countTo < len(source_string):
        sum += source_string[-1]
        sum &= 0xffffffff
    sum = (sum >> 16) + (sum & 0xffff)
    sum += (sum >> 16)
    answer = ~sum
    answer &= 0xffff
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
        if ready[0] == []:
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
        time_left -= duration_select
        if time_left <= 0:
            return None, 0


def do_one_ping(dest_addr, timeout, id, sequence):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp"))
    except PermissionError:
        raise PermissionError("Root privileges required to send ICMP packets.")
    packet = create_packet(id, sequence)
    sock.sendto(packet, (dest_addr, 1))
    addr, rtt = receive_one_ping(sock, id, timeout)
    sock.close()
    return addr, rtt


def ping_loop(host, count, timeout, interval, id):
    dest_addr = socket.gethostbyname(host)
    for seq in range(count):
        try:
            addr, rtt = do_one_ping(dest_addr, timeout, id, seq)
        except PermissionError as e:
            console.print(f"[bold red]{e}[/bold red]")
            return
        with lock:
            ping_data["sequence"].append(seq)
            ping_data["rtt"].append(rtt if rtt else 0)
            if len(ping_data["sequence"]) > 10:
                ping_data["sequence"] = ping_data["sequence"][-10:]
                ping_data["rtt"] = ping_data["rtt"][-10:]
        if addr:
            msg = Text(f"Reply from {addr}: icmp_seq={seq} time={rtt:.2f} ms")
            msg.stylize("green")
        else:
            msg = Text(f"Request timeout for icmp_seq {seq}")
            msg.stylize("yellow")
        console.print(msg)
        time.sleep(interval)


def show_graph(host):
    fig, ax = plt.subplots()
    line, = ax.plot([], [], lw=2)
    ax.set_ylim(0, 200)
    ax.set_xlim(0, 10)
    ax.set_xlabel("Ping Sequence")
    ax.set_ylabel("RTT (ms)")
    ax.set_title(f"Live Ping RTT to {host}")
    ax.grid(True)

    def init():
        line.set_data([], [])
        return line,

    def update(frame):
        with lock:
            if ping_data["sequence"]:
                line.set_data(ping_data["sequence"], ping_data["rtt"])
                ax.set_xlim(ping_data["sequence"][0], ping_data["sequence"][-1] + 1)
                ax.set_ylim(0, max(ping_data["rtt"]) + 20)
        return line,

    ani = animation.FuncAnimation(fig, update, init_func=init, blit=True, interval=1000)
    plt.tight_layout()
    plt.show()


def ping(host, count=10, timeout=1, interval=1):
    try:
        socket.gethostbyname(host)
    except socket.gaierror:
        console.print(f"[bold red]ping: unknown host {host}[/bold red]")
        return

    console.print(f"[bold green]PING[/bold green] {host} ({socket.gethostbyname(host)}) 56(84) bytes of data.")
    id = os.getpid() & 0xFFFF

    # Start the ping loop in a background thread
    thread = threading.Thread(target=ping_loop, args=(host, count, timeout, interval, id), daemon=True)
    thread.start()

    # Show the live graph (main thread)
    show_graph(host)

