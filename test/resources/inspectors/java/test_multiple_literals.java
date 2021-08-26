class Main {
    public static void main(String[] args) {
        // ok
        String shortRareLiteral1 = "12";
        String shortRareLiteral2 = "12";
        String shortRareLiteral3 = "12";

        // ok
        String longRareLiteral1 = "123";
        String longRareLiteral2 = "123";
        String longRareLiteral3 = "123";

        // ok
        String shortFrequentLiteral1 = "34";
        String shortFrequentLiteral2 = "34";
        String shortFrequentLiteral3 = "34";
        String shortFrequentLiteral4 = "34";

        // warning
        String longFrequentLiteral1 = "456";
        String longFrequentLiteral2 = "456";
        String longFrequentLiteral3 = "456";
        String longFrequentLiteral4 = "456";

        System.out.println(
            shortRareLiteral1 + shortRareLiteral2 + shortRareLiteral3 +
            longRareLiteral1 + longRareLiteral2 + longRareLiteral3 +
            shortFrequentLiteral1 + shortFrequentLiteral2 + shortFrequentLiteral3 + shortFrequentLiteral4 +
            longFrequentLiteral1 + longFrequentLiteral2 + longFrequentLiteral3 + longFrequentLiteral4
        );
    }
}
