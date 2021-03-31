import java.util.Objects;

class Device {
    private String name;
    private String model;

    public boolean equals(Device device) {
        return Objects.equals(name, device.name)
                && Objects.equals(model, device.model);
    }
}
