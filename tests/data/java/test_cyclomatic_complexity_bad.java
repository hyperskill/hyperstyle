import java.util.*;

class Main {

    public static void main(String[] args) {
        System.out.print("Enter cells: ");
        String cells = new Scanner(System.in).nextLine();

        char[][] matrix = new char[3][3];
        char[] cel = cells.toCharArray();
        int k = 0;

        System.out.print("--------\n");
        for (int i = 0; i < 3; i++) {
            System.out.print("| ");
            for (int j = 0; j < 3; j++) {
                matrix[i][j] = cel[k++];
                System.out.print(matrix[i][j] + " ");
            }
            System.out.println("|");
        }

        System.out.print("----------\n");
        result(matrix);
    }

    public static int differenceXO(char[][] matrix) {
        int xs = 0;
        int os = 0;
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                if (matrix[i][j] == 'X') {
                    xs++;
                }
                if (matrix[i][j] == 'O') {
                    os++;
                }
            }
        }
        return Math.abs(xs - os);
    }

    public static void result(char[][] matrix) {
        String impossible = "Impossible";
        if (differenceXO(matrix) <= 1) {
            if (isOwin(matrix) && isXwin(matrix)) {
                System.out.println(impossible);
                return;
            }
            if (!isOwin(matrix) && !isXwin(matrix) && !isNotFinished(matrix)) {
                System.out.println("Draw");
                return;
            }
            if (isXwin(matrix)) {
                System.out.println("X wins");
                return;
            }
            if (isOwin(matrix)) {
                System.out.println("O wins");
            } else {
                System.out.println("Game not finished");
            }
        } else {
            System.out.println(impossible);
        }
    }

    public static boolean isOwin(char[][] matrix) {
        boolean isWin = false;
        int diag1 = 0;
        int diag2 = 0;

        for (int i = 0; i < 3; i++) {
            int x = 0;
            int y = 0;
            for (int j = 0; j < 3; j++) {
                if (i == j && matrix[i][j] == 'O') {
                    diag1++;
                }
                if (i + j == 2 && matrix[i][j] == 'O') {
                    diag2++;
                }
                if (matrix[i][j] == 'O') {
                    x++;
                    if (x == 3) {
                        isWin = true;
                    }
                }
                if (matrix[j][i] == 'O') {
                    y++;
                    if (y == 3) {
                        isWin = true;
                    }
                }
            }
        }
        if (diag1 == 3 || diag2 == 3) {
            isWin = true;
        }
        return isWin;
    }

    public static boolean isXwin(char[][] matrix) { // CC is 15
        boolean isWin = false;
        int diag1 = 0;
        int diag2 = 0;
        //check x win
        for (int i = 0; i < 3; i++) {
            int x = 0;
            int y = 0;
            for (int j = 0; j < 3; j++) {
                if (i == j && matrix[i][j] == 'X') {
                    diag1++;
                }
                if (i + j == 2 && matrix[i][j] == 'X') {
                    diag2++;
                }
                if (matrix[i][j] == 'X') {
                    x++;
                    if (x == 3) {
                        isWin = true;
                    }
                }
                if (matrix[j][i] == 'X') {
                    y++;
                    if (y == 3) {
                        isWin = true;
                    }
                }

            }
        }
        if (diag1 == 3 || diag2 == 3) {
            isWin = true;
        }

        // just a few additional lines to add complexity
        if (diag1 > diag2 && diag1 == 10) {
            System.out.println("HI");
        }
        return isWin;
    }

    public static boolean isNotFinished(char[][] matrix) {
        //check Finish
        boolean isItNotfinished = false;
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                if (matrix[i][j] == '_') {
                    isItNotfinished = true;
                }
            }
        }

        return isItNotfinished;
    }
}
