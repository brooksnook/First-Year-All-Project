import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class CabCompany {
    HashMap<String, Vehicle> vehicleMap = new HashMap<>();

    /**
     * Store the vehicles.
     * @param theVehicles The company's vehicles.
     */
    public CabCompany(ArrayList<Vehicle> theVehicles) {
        for(Vehicle vehicle : theVehicles) {
            vehicleMap.put(vehicle.getVehicleID(), vehicle);
        }
    }

    /**
     * Prints out the details of all the cab company's vehicles
     */
    public void listAllVehicles() {
        for(Vehicle vehicle : vehicleMap.values()) {
            System.out.println(vehicle);
        }
    }

    /**
     * Reads from a bookings file and adds bookings for all the vehicles
     * @param bookingsFilename Bookings file to read from
     * @throws IOException If it fails to read the booking file
     * @throws InvalidPathException If the file path is invalid
     * @throws IllegalArgumentException If there is an incorrect number of elements for a booking in the booking file
     */
    public void readBookings(String bookingsFilename) throws IOException, InvalidPathException, IllegalArgumentException {
        Path filePath = Paths.get(bookingsFilename);
        List<String> lines = Files.readAllLines(filePath);
        for (String line : lines) {
            String[] lineArray = line.trim().split(",");
            if (lineArray.length != 3) {
                throw new IllegalArgumentException("Invalid format for bookings file");
            }
            Booking booking = new Booking(lineArray[0], lineArray[1], lineArray[2]);
            vehicleMap.get(booking.vehicleId()).addBooking(booking);
        }
    }

    /**
     * Gets the takings for a vehicle in the cab company
     * @param id The vehicle ID for the vehicle you're trying to get the taking for
     * @return The specified vehicle's takings
     * @throws IllegalArgumentException If the vehicleID inputted is not valid
     */
    public int getTakingsForVehicle(String id) throws IllegalArgumentException {
        if(vehicleMap.containsKey(id)) {
            return vehicleMap.get(id).getTakings();
        } else {
            throw new IllegalArgumentException("Invalid vehicle ID");
        }
    }

    /**
     * Takings a file path for a report file and
     * @param reportFilename File path for the report file
     * @throws IOException If there is an error writing to the file
     * @throws InvalidPathException If there is an invalid file path inputted
     */
    public void writeReport(String reportFilename) throws IOException, InvalidPathException {
       Path reportFile = Paths.get(reportFilename);
       Files.writeString(reportFile, "Cab Company Report\n", StandardCharsets.UTF_8);
       int totalTakings = 0;
       for(Vehicle vehicle : vehicleMap.values()) {
           if(vehicle instanceof Cab cab) {
               String line = "Cab " + cab.getVehicleID() + " driven by " + cab.getDriver() + " had " + cab.getBookings().size() + " journeys and made £" + cab.getTakings() + "\n";
               Files.writeString(reportFile, line, StandardOpenOption.APPEND);
           } else if(vehicle instanceof Bus bus) {
               String line = "Bus " + bus.getVehicleID() + " had " + bus.getBookings().size() + " journeys and made £" + bus.getTakings() + "\n";
               Files.writeString(reportFile, line, StandardOpenOption.APPEND);
           }
           totalTakings += vehicle.getTakings();
       }
       Files.writeString(reportFile, "\nTotal takings for the day £" + totalTakings, StandardOpenOption.APPEND);
    }

    /**
     * Prints out all bookings to the console for all the cab company's vehicles
     */
    public void listAllBookings() {
        for(Vehicle vehicle : vehicleMap.values()) {
            for(Booking booking : vehicle.getBookings()) {
                System.out.println(booking);
            }
        }
    }
}
