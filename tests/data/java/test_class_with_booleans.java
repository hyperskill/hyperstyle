class ClassWithBooleans {
    private boolean enabled = true;
    private boolean isTyped = true;
    private boolean count = false;
    private boolean correct = true;
    private int isValid = 1;

    public boolean getEnabledqqq21() {
        return enabled;
    }

    public boolean isTyped() {
        return isTyped;
    }

    public boolean getCount() {
        return count;
    }

    public boolean isEnabled() {
        return enabled;
    }

    public boolean isCount() {
        return count;
    }

    public boolean isCorrect() {
        return correct;
    }

    public int getIsValid() {
        return isValid;
    }


    public static void main(String[] args) {
        ClassWithBooleans object = new ClassWithBooleans();
        System.out.println(object.isTyped());
    }
}
