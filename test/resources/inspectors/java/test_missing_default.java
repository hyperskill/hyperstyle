import java.util.Scanner;

class HelloWorld {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int x = 1;
        int y = scanner.nextInt();
        switch (x) {
            case 0:
                y = 1;
                break;
        }
        System.out.println(x);
        System.out.println(y);
    }
}
