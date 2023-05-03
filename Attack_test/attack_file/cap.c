#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
int main()
{
    sleep(5);
    setuid(0);
    printf("UID: %d\n", getuid());
    system("cat /etc/shadow | tail -n 3");
    return 0;
}
