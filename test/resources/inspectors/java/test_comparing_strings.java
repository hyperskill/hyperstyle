import java.util.Scanner;

class ComparingStrings {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String line = scanner.nextLine();

        System.out.println(line == "Hello");
        System.out.println(line.equalsIgnoreCase("Hello, World"));
        System.out.println(line.equals("World"));
    }
}
