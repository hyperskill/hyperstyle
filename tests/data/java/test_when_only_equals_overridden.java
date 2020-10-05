import java.util.Objects;

class Person {

    private String firstName;
    private String lastName;
    private int age;

    // constructor, getters and setters

    @Override
    public boolean equals(Object other) {
        /* Check this and other refer to the same object */
        if (this == other) {
            return true;
        }

        /* Check other is Person and not null */
        if (!(other instanceof Person)) {
            return false;
        }

        Person person = (Person) other;

        /* Compare all required fields */
        return age == person.age &&
                Objects.equals(firstName, person.firstName) &&
                Objects.equals(lastName, person.lastName);
    }
}
