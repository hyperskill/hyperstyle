import java.util.Scanner;

class Main {
    private static final String YES = "YES";
    private static final String NO = "NO";

    public static void main(String[] args) {
        printArmy();
        checkTriangle();
        checkQueens();
        calculator();
    }

    private static void printArmy() {  // CC is 10
        Scanner scanner = new Scanner(System.in);
        int p = scanner.nextInt();
        if (p < 1) {
            System.out.println("no army");
        } else if (p < 5) {
            System.out.println("few");
        } else if (p < 10) {
            System.out.println("several");
        } else if (p < 20) {
            System.out.println("pack");
        } else if (p < 50) {
            System.out.println("lots");
        } else if (p < 100) {
            System.out.println("horde");
        } else if (p < 250) {
            System.out.println("throng");
        } else if (p < 500) {
            System.out.println("swarm");
        } else if (p < 1000) {
            System.out.println("zounds");
        } else {
            System.out.println("legion");
        }
    }

    private static void checkTriangle() { // CC is 4
        Scanner scanner = new Scanner(System.in);

        int a = scanner.nextInt();
        int b = scanner.nextInt();
        int c = scanner.nextInt();

        if (a + b > c && b + c > a && c + a > b) {
            System.out.println(YES);
        } else {
            System.out.println(NO);
        }
    }

    private static void checkQueens() { // CC is 4
        Scanner scanner = new Scanner(System.in);

        int num1 = scanner.nextInt();
        int num2 = scanner.nextInt();
        int num3 = scanner.nextInt();
        int num4 = scanner.nextInt();

        if (num1 == num3) {
            System.out.println(YES);
        } else if (num2 == num4) {
            System.out.println(YES);
        } else if (Math.abs(num1 - num3) == Math.abs(num2 - num4)) {
            System.out.println(NO);
        } else {
            System.out.println(NO);
        }
    }

    private static void calculator() { // CC is 3
        Scanner scanner = new Scanner(System.in);

        final String[] line = scanner.nextLine().split("\\s+");

        final long a = Long.parseLong(line[0]);
        final char op = line[1].charAt(0);
        final long b = Long.parseLong(line[2]);

        switch (op) {
            case '+':
                System.out.println(a + b);
                break;
            case '-':
                System.out.println(a - b);
                break;
            case '*':
                System.out.println(a * b);
                break;
            case '/':
                if (b == 0) {
                    System.out.println("Division by 0!");
                } else {
                    System.out.println(a / b);
                }
                break;
            default:
                System.out.println("Unknown operator");
        }
    }
}
