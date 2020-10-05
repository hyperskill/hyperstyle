class ClassWithMembers {
    private static final int LIGHT_SPEED = 3 * 100_000_000;
    private static final double PI = 3.1415;

    private final String msg;
    private final int cost = 10;
    ClassWithMembers(String msg) {
        this.msg = msg;
    }
    public String getMsg() {
        return msg;
    }

    public int getCost() {
        return cost;
    }

    public static void main(String[] args) {
        ClassWithMembers instance = new ClassWithMembers("Hello");
        System.out.println(instance.getMsg());
        System.out.println(instance.getCost());
    }
}
