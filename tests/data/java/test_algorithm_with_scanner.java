import java.util.*;

class Main {
    public static void main(String[] args) {
        Scanner s = new Scanner(System.in);
        int length = s.nextInt();
        int[] nums = new int[length];
        for (int i = 0; i < length; i++) {
            nums[i] = s.nextInt();
        }
        int limit = s.nextInt();
        int sum = 0;
        for (int n : nums) {
            if (n > limit) {
                sum += n;
            }
        }
        System.out.println(sum);
    }
}
