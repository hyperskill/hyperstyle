class MyClass {
    static final int log = 10; // OK
    static final int logger = 50; // OK
    static final int logMYSELF = 10; // violation
    static final int loggerMYSELF = 5; // violation
    static final int MYSELF = 100; // OK
    static final int myselfConstant = 1; // violation
    static final long serialVersionUID = 1L; // OK
    static final long thingCost = 400L; // violation
}
