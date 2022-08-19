record Book(String title, String author, String isbn) { }

class OuterClass {
    class InnerClass {
        Book book = new Book("Title", "author", "isbn");
    }
}

class Main {
    public static void main(String[] args)
    {
        OuterClass.InnerClass a = new OuterClass.InnerClass();
        System.out.println((a.book));
    }
}
