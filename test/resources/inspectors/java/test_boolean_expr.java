import java.util.Scanner;

class BooleanExpressions {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        int a = scanner.nextInt();
        int b = scanner.nextInt();
        int c = scanner.nextInt();
        int d = scanner.nextInt();

        if (a > b) { // ok
            System.out.println("a > b");
        }

        if (a > b && a > b) { // duplicated
            System.out.println("a > b again");
        }

        if (a > b && a < d) {
            System.out.println("b < a < d");
        }

        if (a > b && true) { // should be simplified
            System.out.println("a > b > c");
        }

        process(a, b, c, d);
    }

    private static void process(int a, int b, int c, int d) {
        boolean enabled = false;
        if (a > b && b < c && c > d || c < a && enabled) {
            System.out.println("Too complex");
        }

        for (int i = 0; i < 10; i++) {
            System.out.println(getValue(i));
        }
    }

    private static boolean getValue(int i) {
        if (i < 1) {
            return true;
        } else {
            return false;
        }
    }
}
