package com.gmail.brauckmann.lukas;

import net.java.games.input.Component;
import net.java.games.input.Controller;
import net.java.games.input.ControllerEnvironment;

/**
 * Class representing a connection to a Gamepad/Controller.
 * 
 * @author Lukas
 * 
 */
public class Gamepad extends Thread {
	/**
	 * Controller.
	 */
	private Controller controller = null;
	/**
	 * Client to send commands.
	 */
	private GamepadClient client;
	/**
	 * Flag for running.
	 */
	private boolean running = true;

	/**
	 * Initialize.
	 * 
	 * @param client
	 *            Client.
	 */
	public Gamepad(GamepadClient client) {
		super();
		this.client = client;
		setup();
	}

	/**
	 * Setup the connection to the controller.
	 */
	private void setup() {
		// Get all available controllers.
		Controller[] ca = ControllerEnvironment.getDefaultEnvironment()
				.getControllers();

		// Search for correct controller.
		for (int i = 0; i < ca.length && controller == null; i++) {
			if (ca[i].getType() == Controller.Type.STICK) {
				controller = ca[i];
			}
		}
		if (controller == null) {
			// Could not find a controller.
			System.out.println("Found no controller!");
			running = false;
		} else {
			// Connected to controller.
			System.out.println("Connected to: " + controller.getName());
		}
	}

	@Override
	public void run() {
		if (running)
			// Start client.
			client.start();
		boolean hover = false;
		while (running) {
			controller.poll();
			Component[] components = controller.getComponents();
			boolean moving = false;
			// Move values.
			float x = 0;
			float y = 0;
			float z = 0;
			float rz = 0;

			// Parse values from the controller.
			try {
				for (int i = 0; i < components.length; i++) {
					if (components[i].getName().equals("Base 3")) {
						// Emergency.
						if (components[i].getPollData() == 1.0f) {
							client.sendCommand('@');
							System.out.println("Emergency");
							Thread.sleep(2000);
							continue;
						}
					} else if (components[i].getName().equals("Thumb 2")) {
						// Land.
						if (components[i].getPollData() == 1.0f) {
							client.sendCommand('11');
							continue;
						}
					} else if (components[i].getName().equals("Trigger")) {
						// Takeoff.
						if (components[i].getPollData() == 1.0f) {
							client.sendCommand('12');
							continue;
						}
					} else if (components[i].getName().equals("Base 4")) {
						// Enable/disable user mode.
						if (components[i].getPollData() == 1.0f) {
							System.out.println("User mod");
							client.sendCommand('0');
							client.sendCommand('5');
							Thread.sleep(500);
							continue;
						}
					} else {
						if (components[i].getName().equals("x")) {
							if (Math.abs(components[i].getPollData()) > 0.1) {
								client.sendCommand('3');
								moving = true;
							}else if (Math.abs(components[i].getPollData()) < -0.1) {
								client.sendCommand('4');
								moving = true;
							}
						}
						if (components[i].getName().equals("y")) {
							if (Math.abs(components[i].getPollData()) < -0.1) {
								client.sendCommand('2');
								moving = true;
							}
						}

						if (!moving) 
							client.sendCommand('5');
					}
				}
			} catch (InterruptedException e) {

			}

		}
	}
}
