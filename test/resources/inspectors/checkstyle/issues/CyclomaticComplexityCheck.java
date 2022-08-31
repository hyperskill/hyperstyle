class ComplexBooleanExpression {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        int a = scanner.nextInt();
        int b = scanner.nextInt();
        int c = scanner.nextInt();
        int d = scanner.nextInt();

        if (a > b) {
            if (a > c) {
                if (a > d) {
                    System.out.println("'a' is the largest");
                }
            }
        }

        if (b > a) {
            if (b > c) {
                if (b > d) {
                    System.out.println("'b' is the largest");
                }
            }
        }

        if (c > a) {
            if (c > b) {
                if (c > d) {
                    System.out.println("'c' is the largest");
                }
            }
        }

        if (d > a) {
            if (d > b) {
                if (d > c) {
                    System.out.println("'d' is the largest");
                }
            }
        }
    }
}
