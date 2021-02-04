
public class QQMain {

    public static void main(String[] args) {
        System.out.println("SADASD");
    }
    public static void f() {
        System.out.println("ASDS");
    }
}
class Application {

    String name;

    public void run(String[] args) {
        System.out.println(name);

        for (String arg : args) {
            System.out.println(arg);
        }
    }
}
