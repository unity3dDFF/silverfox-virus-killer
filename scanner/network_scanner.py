"""Current network connection scanner.

Only an exact IP IOC is treated as confirmed.  Port matches are low-confidence
context and are never represented as a block that the program did not perform.
"""

from __future__ import annotations

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    psutil = None
    PSUTIL_AVAILABLE = False

from ioc import MaliciousDomains, MaliciousIPs, MaliciousPorts


class NetworkScanner:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.malicious_domains = MaliciousDomains()
        self.malicious_ips = MaliciousIPs()
        self.malicious_ports = MaliciousPorts()

    def scan(self):
        if not PSUTIL_AVAILABLE:
            return []
        results = []
        try:
            connections = psutil.net_connections(kind="inet")
        except (psutil.AccessDenied, OSError) as exc:
            if self.verbose:
                print(f"无法枚举网络连接: {exc}")
            return []
        for conn in connections:
            if not conn.raddr:
                continue
            result = self._classify(conn)
            if result:
                results.append(result)
        return results

    def _classify(self, conn):
        remote_ip, remote_port = conn.raddr.ip, conn.raddr.port
        base = {
            "type": "network", "local_address": self._address(conn.laddr),
            "remote_address": self._address(conn.raddr), "remote_ip": remote_ip,
            "remote_port": remote_port, "status": conn.status, "pid": conn.pid,
            "remediable": False, "action": "recommend_investigate",
        }
        if self.malicious_ips.is_malicious(remote_ip):
            return {**base, "severity": "critical", "confidence": "confirmed",
                    "detector": "known_remote_ip", "detail": f"远端 IP 命中已知 IOC: {remote_ip}"}
        if self.malicious_ports.is_malicious(remote_port):
            return {**base, "severity": "low", "confidence": "low",
                    "detector": "notable_remote_port",
                    "detail": f"连接使用银狐样本曾用端口 {remote_port}（端口本身不能定性）"}
        return None

    @staticmethod
    def _address(address):
        return f"{address.ip}:{address.port}" if address else "N/A"

    def is_suspicious_connection(self, conn):
        return bool(conn.raddr and self.malicious_ports.is_malicious(conn.raddr.port))

    def is_malicious_connection(self, conn):
        return bool(conn.raddr and self.malicious_ips.is_malicious(conn.raddr.ip))

    def is_malicious_domain(self, domain):
        return self.malicious_domains.is_malicious(domain)

    def get_connections_by_pid(self, pid):
        return [conn for conn in psutil.net_connections(kind="inet") if conn.pid == pid]

    def get_connections_by_status(self, status):
        return [conn for conn in psutil.net_connections(kind="inet") if conn.status == status]

    def get_established_connections(self):
        return self.get_connections_by_status("ESTABLISHED")

    def get_listening_connections(self):
        return self.get_connections_by_status("LISTEN")
