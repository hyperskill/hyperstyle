import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

class Geek {

    private String type;
    private List<String> languages;
    private int experience;

    Geek(String type, List<String> languages, int experience) {
        this.type = type;
        this.languages = languages;
        this.experience = experience;
    }

    public static class GeekBuilder {

        private String type;
        private List<String> languages;
        private int experience;

        public GeekBuilder setType(String type) {
            this.type = type;
            return this;
        }

        public GeekBuilder setLanguages(List<String> languages) {
            this.languages = languages;
            return this;
        }

        public GeekBuilder setExperience(int experience) {
            this.experience = experience;
            return this;
        }

        public Geek build() {
            return new Geek(type, languages, experience);
        }
    }

    public String toString() {
        return "Type : " + type + "\n" +
                "Languages : " + languages + "\n" +
                "Experience : " + experience + " years";
    }
}

class TestDrive {
    public static void main(String[] args) {
        final Scanner scanner = new Scanner(System.in);
        final String geekName = scanner.nextLine();
        scanner.close();
        System.out.println("Geek " + geekName + " created.");

        Geek geek = new Geek.GeekBuilder()
                .setType("Admin")
                .setLanguages(new ArrayList<>() {{
                    add("Perl");
                    add("PowerShell");
                }})
                .setExperience(10)
                .build();

        System.out.println(geek);
    }
}
