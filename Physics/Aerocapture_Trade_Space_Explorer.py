"""This file is intended to create the aerocapture trade space specifically for Mars for different entry velocities,
different lift to drag ratios, different flight path angles, spacecraft mass, nose radius and cross sectional area values.
It uses python multiprocessing to run multiple simulations at once because as you can imagine there are many cases to run.
This script utilizes the Aerocapture Mission Analysis Tool from here: https://github.com/athulpg007/AMAT. This script is 
intended to be run on a cloud virtual machine because of the number of possible combinations, but you could also use it
to search a particular region of the trade space quickly if you already know for instance your cross sectional area or 
your spacecraft mass for instance. Or however you want to use it! It can be set up to email you if it fails."""

from multiprocessing import Pool, Manager
import time
import numpy as np
from AMAT.planet import Planet
from AMAT.vehicle import Vehicle

# Because adding all possible celestial bodies with an atmosphere as defined by AMAT would take ~8 times longer,
# we will stick to modeling Mars aerocapture only at this time
planet = Planet("MARS")

vinf_kms_array = np.linspace( 0.0,   30.0,  11)

#
LD_array       = np.linspace( 0.0,    1.0 , 6)
num_LD = len(LD_array)
v0_kms_array    = np.zeros(len(vinf_kms_array))
v0_kms_array[:] = np.sqrt(1.0*(vinf_kms_array[:]*1E3)**2.0 +\
                          2*np.ones(len(vinf_kms_array))*\
                          planet.GM/(planet.RP+150.0*1.0E3))/1.0E3
num_v0 = len(v0_kms_array)

# Initialize some of the output arrays
overShootLimit_array = np.zeros((num_v0, num_LD))
exitflag_os_array = np.zeros((num_v0, num_LD))
underShootLimit_array = np.zeros((num_v0, num_LD))
exitflag_us_array = np.zeros((num_v0, num_LD))

# Create array to store theoretical corridor width values
TCW_array = np.zeros((num_v0, num_LD))

# Define initial flight path angles to test
init_EFPA = [-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15]

# Create the function to determine corridor width. This function gets run in parallel using multiprocessing
def simulate_parallel(args, result_queue):

    mass, ballisticcoeff, crosssecarea, noseradius = args
    for i in range(num_v0):
        for j in range(num_LD):
            for k in init_EFPA:
                try:

                    planet.loadAtmosphereModel('../atmdata/Mars/mars-gram-avg.dat', 0, 1, 2, 3)

                    # Define entry interface as just below the skip altitude (i.e. edge of the atmosphere
                    EI = (planet.h_skip-1)/1000

                    vehicle = Vehicle('Apollo', mass, ballisticcoeff, LD_array[j], crosssecarea, 0.0, noseradius, planet)
                    vehicle.setInitialState(EI, 0.0, 0.0, v0_kms_array[i], 0.0, k, 0.0, 0.0)

                    # Modify these values if you want to model
                    # vehicle.setMaxRollRate(30.0)
                    # vehicle.setEquilibriumGlideParams(75.0, 3.0, 18.9, 120.0, 101, -500.0)
                    # vehicle.setDragEntryPhaseParams(6.0, 80.0, 101, -300.0)

                    # Set the target orbit parameters.
                    vehicle.setTargetOrbitParams(200.0, 2000.0, 50.0)
                    vehicle.setSolverParams(1E-6)

                    # Find overshoot limit
                    overShootLimit, exitflag_os = vehicle.findOverShootLimit(2400.0, 0.1, -80.0, -4.0, 1E-10, 400.0)
                    overShootLimit_array[i, j] = overShootLimit
                    exitflag_os_array[i, j] = exitflag_os

                    # Find undershoot limit
                    underShootLimit, exitflag_us = vehicle.findUnderShootLimit(2400.0, 0.1, -80.0, -4.0, 1E-10, 400.0)
                    underShootLimit_array[i, j] = underShootLimit
                    exitflag_us_array[i, j] = exitflag_us

                    # Calculate TCW
                    TCW_array[i, j] = overShootLimit - underShootLimit
                    # Process the result and put it in the queue
                    result_queue.put((vinf_kms_array[i],LD_array[j], overShootLimit, exitflag_os, underShootLimit, exitflag_us))
                    # Clear vehicle instance from memory
                    del vehicle
                    print(str(num_v0 * num_LD) +
                          ": Arrival V_infty: " + str(vinf_kms_array[i]) + " km/s" +
                          ", L/D: " + str(LD_array[j]) +
                          " OSL: " + str(overShootLimit_array[i, j]) +
                          " USL: " + str(underShootLimit_array[i, j]) +
                          ", TCW: " + str(TCW_array[i, j]) +
                          " EFOS: " + str(exitflag_os_array[i, j]) +
                          " EFUS: " + str(exitflag_us_array[i, j]))
                except Exception as e:
                    # If an exception occurs, send an email notification
                    subject = "Error in Simulation Script"
                    body = f"An error occurred in the simulation script:\n\n{str(e)}"
                    send_email(subject, body)

# Create a function to email you if the simulation fails
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
def send_email(subject, body):
    # Email configuration
    sender_email = "your_email@gmail.com"
    receiver_email = "recipient_email@gmail.com"
    password = "your_email_password"

    # Create the email message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Attach the body of the email
    message.attach(MIMEText(body, "plain"))

    try:
        # Connect to the SMTP server
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            # Login to the email account
            server.login(sender_email, password)
            # Send the email
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email notification sent successfully.")
    except Exception as e:
        print(f"Error sending email notification: {e}")

if __name__ == "__main__":

    # Set the maximum number of parallel jobs
    batch_size = 15
    manager = Manager()
    result_queue = manager.Queue()

    # Define which parameters to test and at what values
    mass_values = [1,5,10,50,100,250,500,750,1000,1500,2000,2500,5000,10000,25000,50000,100000]     # kgs
    noseradius_values = [0.01, 0.025,0.05,0.1,0.5,1,2,5]                                            # meters
    ballisticcoeff_values = np.linspace(1, 400.0, 6)                                                # kg/m^2
    crosssecarea_values = [0.01, 0.05, 0.1, 0.5, 1, 5, 10, 50]                                      # m^2

    # Generator for generating processes dynamically
    def generate_processes():
        for mass in mass_values:
            for ballisticcoeff in ballisticcoeff_values:
                for crosssecarea in crosssecarea_values:
                    for noseradius in noseradius_values:
                        yield (mass, ballisticcoeff, crosssecarea, noseradius)

    try:
        while True:
            processes = [next(generate_processes()) for _ in range(batch_size)]
            print([next(generate_processes()) for _ in range(batch_size)])
            # Run the batch of processes

            with Pool(processes=batch_size) as pool:
                pool.starmap(simulate_parallel, [(args, result_queue) for args in processes])

            # Check for completed processes
            while not result_queue.empty():
                result = result_queue.get()
                # Process the result, e.g., store it or print it
                # print(result)

            time.sleep(1)  # Adjust as needed to control the rate of checking for completed processes

    except KeyboardInterrupt:
        print("Process interrupted. Exiting.")
