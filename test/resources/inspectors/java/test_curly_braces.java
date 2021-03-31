import java.util.Scanner;

class HelloWorld {
    public static void main(String[] args) {
        for (int i = 0; i < args[0].length(); i++)
            System.out.println("Hello World!");

        Scanner scanner = new Scanner(System.in);
        int num = scanner.nextInt();
        int counter = 0;

        switch (num) {
            case 1:
                counter++;
                break; // OK
            case 6:
                counter += 10;
                break; // OK
            default:
                counter = 100;
                break; // OK
        }

        for (int i = 0; i < 10; i++) System.out.println(i);

        System.out.println(counter);
    }
}
