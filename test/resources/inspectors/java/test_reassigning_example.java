class ReassigningExample {

    public static void main(String[] args) {
        for (int i = 0, j = 0; i < 10; i++, j++) {
            i++;
            System.out.println(sum(i, j));
        }
    }

    private static int sum(int a, int b) {
        a = 10;
        return a + b;
    }
}
