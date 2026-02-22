#include <stdio.h>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <signal.h>

#pragma comment(lib, "ws2_32.lib")

SOCKET sock;

void stop_sniffer(int sig) {
    printf("\nStopping sniffer safely...\n");
    closesocket(sock);
    WSACleanup();
    exit(0);
}

int main() {
    WSADATA wsa;
    char buffer[65536];

    signal(SIGINT, stop_sniffer);

    printf("C Packet Sniffer Running...\n");

    WSAStartup(MAKEWORD(2,2), &wsa);

    sock = socket(AF_INET, SOCK_RAW, IPPROTO_IP);

    if(sock == INVALID_SOCKET) {
        printf("Socket creation failed\n");
        return 1;
    }

    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = 0;
    addr.sin_addr.s_addr = inet_addr("127.0.0.1");

    bind(sock, (struct sockaddr *)&addr, sizeof(addr));

    int opt = 1;
    ioctlsocket(sock, SIO_RCVALL, (u_long *)&opt);

    while(1) {
        int data_size = recv(sock, buffer, sizeof(buffer), 0);
        if(data_size > 0) {
            printf("Packet captured: %d bytes\n", data_size);
        }
    }

    return 0;
}