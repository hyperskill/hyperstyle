import java.util.*;

public class Main {
    public static void main(String[] args) {
        // write your code here
        Scanner scanner = new Scanner(System.in);
        int heightBus = scanner.nextInt();
        int bridges = scanner.nextInt();
        scanner.nextLine();
        String heightBridges = scanner.nextLine();
        String[] heightsList = heightBridges.split(" ");
        String willNotCrash = "Will not crash";
        String willCrash = "";

        for (int i = 0; i < bridges; i++) {
            if (heightBus >= Integer.parseInt(heightsList[i])) {
                willCrash = "Will crash on bridge " + (i + 1);
                break;
            }
        }

        if ("".equals(willCrash)) {
            System.out.println(willNotCrash);
        } else {
            System.out.println(willCrash);
        }
    }
}
