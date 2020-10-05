class ThreadDemo {

    public static void main(String[] args) {
        Thread t = new Thread(() -> System.out.println("Hello!"));
        t.run();
    }
}
