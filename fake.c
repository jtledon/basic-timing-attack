#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

int main() {
    srand(time(NULL));
    int rnd = (rand() % 20) + 1;
    if (rnd == 10) {
        printf("success: %d\n", rnd);
    } else {
        printf("fail: %d\n", rnd);
    }
    sleep(rnd % 3);
    return 0;
}
