import java.util.ArrayList;
import java.util.HashSet;

class Main {

    public static void main(String[] args) {
        ArrayList<String> words = new ArrayList<>();

        words.add("first");
        words.add("second");
        words.add("third");

        System.out.println(words);

        HashSet<Integer> uniqueNumbers = new HashSet<>();

        uniqueNumbers.add(1);
        uniqueNumbers.add(2);
        uniqueNumbers.add(3);

        System.out.println(uniqueNumbers);
    }
}
