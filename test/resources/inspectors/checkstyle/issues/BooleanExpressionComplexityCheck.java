class ComplexBooleanExpression {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        int a = scanner.nextInt();
        int b = scanner.nextInt();
        int c = scanner.nextInt();
        int d = scanner.nextInt();

        if (a > b && a > b && a > c && a > d) {
            System.out.println("'a' is the largest");
        }
    }
}
