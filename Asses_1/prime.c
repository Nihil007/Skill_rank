#include <stdio.h>

int main() {
    int num,i,prime=1;

    scanf("%d", &num);

    if (num <= 1) {
        prime = 0;
    } else {
        for (i=2; i<= num/2;i++) {
            if(num%i==0) {
                prime= 0;
                break;
            }
        }
    }

    if (prime)
        printf("%d prime\n", num);
    else
        printf("%d not prime\n", num);

    return 0;
}
