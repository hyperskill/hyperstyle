class NestedBlocksExample {
    public static void main(String[] args) {
        int a = 10;
        {
            a = 20;
            System.out.println(a);
        }
        switch (a) {
            case 0:
                x = 1;
                break;
            case 1:
                // Never OK, statement outside block
                System.out.println("Hello 1");
            {
                x = 2;
                break;
            }
            case 2: {
                // OK if allowInSwitchCase is true
                System.out.println("Hello 2");
                x = 3;
                break;
            }
            default: {
                System.out.println("Unknown case");
                break;
            }
        }
    }
}

