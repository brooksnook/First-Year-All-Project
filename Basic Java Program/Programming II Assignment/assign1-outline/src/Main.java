import java.io.File;
import java.io.IOException;
import java.nio.file.*;
import java.util.*;

/**
 * A class containing the main method for the taxi company program.
 * There are several test methods that will display the results of
 * different parts of the program.
 */
public class Main
{
    /**
     * The main method for the cab company program.
     * Three arguments are required:
     * 1. The name of the file of vehicle details.
     * 2. The name of the file of bookings.
     * 3. The name of the file for the report.
     * @param args The program arguments.
     * @throws IOException If there is an error reading the files.
     */
    public static void main(String[] args)
            throws IOException
    {
        if(args.length != 3) {
            System.out.println(
                    "There should be three program arguments: " +
                            "the name of the vehicles file, " +
                            "the name of the bookings file and " +
                            "the name of the output file for the report.");
            System.exit(1);
        }
        else {
            System.out.printf("Using files: %s, %s and %s", args[0], args[1], args[2]);
            System.out.println();
        }
        String vehiclesFilename = args[0];
        String bookingsFilename = args[1];
        String reportFilename = args[2];

        // Read the vehicle details.
        ArrayList<Vehicle> theVehicles = new ArrayList<>() ;
        try {
            theVehicles = readVehicleDetails(vehiclesFilename);
        } catch (IOException e) {
            System.out.println("Error reading vehicles file");
            System.exit(1);
        } catch (IllegalArgumentException e) {
            System.out.println("Invalid file formatting for vehicles file");
            System.exit(1);
        }

        // TODO: Test the reading of the vehicle details.
        // for(Vehicle vehicle : theVehicles) {
        //     System.out.println(vehicle);
        // }

        CabCompany cabCompany = new CabCompany(theVehicles);
        // TODO: List the vehicles.
        cabCompany.listAllVehicles();

        // reading all bookings
        try {
            cabCompany.readBookings(bookingsFilename);
        } catch (InvalidPathException e) {
            System.out.println("Invalid bookings file");
            System.exit(1);
        } catch (IllegalArgumentException e) {
            System.out.println(e.getMessage());
            System.exit(1);
        }

        // TODO: Test the listing of the bookings.
        cabCompany.listAllBookings();

        // TODO: Test the calculation of the takings.
        for(Vehicle vehicle : theVehicles) {
            System.out.println(vehicle.getVehicleID() + " " + cabCompany.getTakingsForVehicle(vehicle.getVehicleID()));
        }

        // test
        // TODO: Test the writing of the report.
        try {
            cabCompany.writeReport(reportFilename);
        } catch (InvalidPathException e) {
            System.out.println("Invalid file path for report file");
            System.exit(1);
        }

        List<String> report = Files.readAllLines(Paths.get(reportFilename));
        for(String line : report) {
            System.out.println(line);
        }
    }

    /**
     * Decode the vehicle details and create a Vehicle object.
     * @param vehicleDetails The details of the vehicle.
     * @return The Vehicle object created from the details.
     * @throws IllegalArgumentException If there is an incorrect number of elements in one of the bookings
     */
    private static Vehicle decodeVehicleDetails(String vehicleDetails) throws IllegalArgumentException {
        String[] vehicleDetailArray = vehicleDetails.trim().split(",");
        Vehicle decodedVehicle = null;

        if(vehicleDetailArray.length != 4) {
            throw new IllegalArgumentException("Incorrect number of vehicle details");
        }

        if(vehicleDetailArray[0].equals("C")) {
            decodedVehicle = new Cab(vehicleDetailArray[1], Integer.parseInt(vehicleDetailArray[3]), vehicleDetailArray[2]);
        } else if(vehicleDetailArray[0].equals("B")) {
            ArrayList<String> route = new ArrayList<>(List.of(vehicleDetailArray[3].trim().split(":")));
            decodedVehicle = new Bus(vehicleDetailArray[1], Integer.parseInt(vehicleDetailArray[2]), route);
        }

        return decodedVehicle;
    }


    /**
     * Read the file of vehicle details.
     * DO NOT CHANGE THIS METHOD
     * @param vehiclesFilename The name of the file of vehicle details.
     * @throws IOException  If there is an error reading the file.
     */
    private static ArrayList<Vehicle> readVehicleDetails(String vehiclesFilename)
            throws IOException
    {
        Path filePath = Paths.get(vehiclesFilename);
        List<String> lines = Files.readAllLines(filePath);
        ArrayList<Vehicle> theVehicles = new ArrayList<>();
        for(String vehicleDetails : lines) {
            vehicleDetails = vehicleDetails.trim();
            Vehicle aVehicle = decodeVehicleDetails(vehicleDetails);
            if(aVehicle != null) {
                theVehicles.add(aVehicle);
            }
        }
        return theVehicles;
    }
}
