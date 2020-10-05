import java.util.List;

class ForLoopExample {

    public static void main(String[] args) {
        List<Integer> numbers = List.of(1, 2, 3, 4, 5);
        for (int n : numbers) {
            System.out.println(n);
        }

        for (int i = 0; i < numbers.size(); i++) {
            System.out.println(numbers.get(i));
        }

        for (int i = 0, j = 0, k = 0; i < 10; i++, j++, k++) {
            System.out.println(i + j + k);
        }
    }
}
