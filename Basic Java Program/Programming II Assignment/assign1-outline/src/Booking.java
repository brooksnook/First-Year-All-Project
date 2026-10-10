public record Booking(String vehicleId, String pickup, String finalDestination) {
    @Override
    public String toString() {
        return "Vehicle: " + vehicleId + " from " + pickup + " to " + finalDestination;
    }
}
