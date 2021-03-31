class SwitchExample {
    private static final String UNKNOWN = "Unknown";

    public static void main(String[] args) {
        switchWithDefault(10);
        switchWithoutDefault(20);
        switchWithShiftedDefault(30);
        switchFallthrough(50);
    }

    private static void switchWithDefault(int n) {
        switch (n) {
            case 10:
                System.out.println(n + 1);
                break;
            case 20:
                System.out.println(n + 2);
                break;
            default:
                System.out.println(UNKNOWN);
        }
    }

    private static void switchWithoutDefault(int n) {
        switch (n) {
            case 20:
                System.out.println(n + 1);
                break;
            case 30:
                System.out.println(n + 2);
                break;
        }
    }

    private static void switchWithShiftedDefault(int n) {
        switch (n) {
            default:
                System.out.println(UNKNOWN);
                break;
            case 30:
                System.out.println(n + 1);
                break;
            case 40:
                System.out.println(n + 2);
                break;
        }
    }

    private static void switchFallthrough(int n) {
        switch (n) {
            case 50:
            case 60:
                System.out.println(n + 1);
            case 70:
                System.out.println(n + 2);
                break;
            default:
                break;
        }
    }
}
