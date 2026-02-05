#include <stdio.h>
#include <string.h>
#include <netdb.h>
#include <arpa/inet.h>

int main() {
    char url[256];
    printf("Enter a URL: ");
    scanf("%255s", url);

    if (strncmp(url, "http://", 7) == 0) memmove(url, url+7, strlen(url));
    if (strncmp(url, "https://", 8) == 0) memmove(url, url+8, strlen(url));
    if (strncmp(url, "www.", 4) == 0) memmove(url, url+4, strlen(url));

    struct hostent *host = gethostbyname(url);
    if (host == NULL) {
        printf("Could not resolve the domain\n");
        return 1;
    }

    struct in_addr **addr_list = (struct in_addr **) host->h_addr_list;
    printf("IP Address of %s: %s\n", url, inet_ntoa(*addr_list[0]));
    return 0;
}
// How to run: gcc Resolve-IP.c -o Resolve-IP ./Resolve-IP
