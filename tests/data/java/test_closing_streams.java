import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;

class TryWithResourcesExample {
    private static final String FILE_NAME = "test.java";

    public static void main(String[] args) {
        InputStream in = null;
        try {
            in = new FileInputStream(FILE_NAME);
            System.out.println(in.read());
        } catch (IOException e) {
            System.out.println(e.getMessage());
        } finally {
            try {
                if (in != null) {
                    in.close();
                }
            } catch (IOException ignored) {
                // ignored
            }
        }

        // better use try-with-resources
        try (InputStream in2 = new FileInputStream(FILE_NAME)) {
            System.out.println(in2.read());
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }

        try {
            InputStream in3 = new FileInputStream(FILE_NAME);
            System.out.println(in3.read());
        } catch (IOException e) {
            System.out.print(e.getMessage());
            // it will be good to check closing
        }
    }
}
