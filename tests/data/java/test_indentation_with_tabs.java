import java.util.Arrays;
import java.util.List;

class Indentation {

    public static void main(String[] args) {
	int a = 10;
	int b = 20;

	System.out.println(a + b);

	var words = List.of(
		"Hello",
		"How is it going?",
		"Let's program!"
	);

	var numbers = Arrays.asList(
		100,
		200,
		300
	);

	invokeMethod(words, numbers);
    }

    private static void invokeMethod(List<String> words,
				     List<Integer> numbers) {

	System.out.println(words);
	System.out.println(numbers);
    }
}
