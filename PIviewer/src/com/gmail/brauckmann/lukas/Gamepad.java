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
		Controller[] ca = ControllerEnvironment.getDefaultEnvironment().getControllers();

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
		boolean move = false;
		while (running) {
			controller.poll();
			Component[] components = controller.getComponents();
			// Move values.
			float x = 0;
			float y = 0;
			float z = 0;
			float rz = 0;

			// Parse values from the controller.
			for (int i = 0; i < components.length; i++) {
				if (components[i].getName().equals("Base 3")) {
					// Emergency.
					client.setCmd("10");
				} else if (components[i].getName().equals("Thumb 2")) {
					// Land.
					client.setCmd("7");
				} else if (components[i].getName().equals("Trigger")) {
					// Takeoff.
					client.setCmd("9");
				} else if (components[i].getName().equals("Base 4")) {
					// Enable/disable user mode.
					client.setCmd("0");
				} else if (components[i].getName().equals("x")) {
					if (Math.abs(components[i].getPollData()) > 0.01) {
						x = components[i].getPollData();
						move = true;
					}
				} else if (components[i].getName().equals("y")) {
					if (Math.abs(components[i].getPollData()) > 0.01) {
						y = components[i].getPollData();
						move = true;
					}
				} else if (components[i].getName().equals("z")) {
					if (Math.abs(components[i].getPollData()) > 0.01) {
						z = components[i].getPollData();
						move = true;
					}
				} else if (components[i].getName().equals("rz")) {
					if (Math.abs(components[i].getPollData()) > 0.01) {
						rz = components[i].getPollData();
						move = true;
					}
				}
				if (move) {
					// Create move command string.
					String cmd = "6.";
					cmd += String.valueOf(x) + ",";
					cmd += String.valueOf(y) + ",";
					cmd += String.valueOf(-z) + ",";
					cmd += String.valueOf(rz);
					client.setCmd(cmd);
				} else
					// Hover.
					client.setCmd("5");
			}
		}
	}
}
