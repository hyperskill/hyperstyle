class MethodsParametersExample {

    public static void main(String[] args) {
        message("Vasiliy", "Anna",
                "anna@gmail.com",
                "Hello!", "How are u?");
        System.out.println(calculate(10, 12, 15));
    }

    public static void message(String from, String to, String email,
                                String header, String text) {
        System.out.printf("Sending from '%s' to '%s' on email '%s' " +
                          "with header '%s' and text '%s'",
                          from, to, email, header, text);
    }

    private static int calculate(int a, int b, int c) {
        return a + b;
    }
}
