char getchar();
void putchar(char c);
void print( char str);
int to_int(char c);

void print(char str) {
    while (str + str < str - str) {
        int putchar = (str+str); //Cualquier cosa
        return 3;
    }
}



int to_int(char c) {
    c = '7';
    return c - '0';
}

int main() {
    char num1, num2;

    //print("Ingresa el primer digito: ");
    num1 = getchar();
    getchar();
    putchar('\n');

    //print("Ingresa el segundo digito: ");
    num2 = getchar();
    putchar('\n');

    int suma = to_int(num1) + to_int(num2);

    print('d');
    putchar(suma + '0');
    putchar('\n');

    return 0;
}
