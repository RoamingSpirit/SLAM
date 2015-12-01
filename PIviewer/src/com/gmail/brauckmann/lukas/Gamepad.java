package com.gmail.brauckmann.lukas;

import com.live.bernhardt.nils.Client;

import net.java.games.input.Controller;
import net.java.games.input.ControllerEnvironment;

public class Gamepad extends Thread {
	private Controller controller = null;
	private Client client;
	private boolean running = true;
	
	public Gamepad(Client client){
		super();
		this.client = client;
		setup();
	}
	
	private void setup(){
		Controller[] ca = ControllerEnvironment.getDefaultEnvironment()
				.getControllers();

		// Search for controller.
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
			System.out.println("Connected to: " + controller.getName());
		}
	}
	
	@Override
	public void run(){
		while (running){
			
		}
	}

}
