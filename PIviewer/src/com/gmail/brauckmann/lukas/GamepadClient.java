package com.gmail.brauckmann.lukas;

import java.io.BufferedWriter;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.net.Socket;
import java.net.UnknownHostException;

/**
 * Client for the connection to the server.
 * 
 * @author Lukas
 *
 */
public class GamepadClient extends Thread {

	BufferedWriter out;
	
	Socket socket = null;
	/**
	 * Host ip.
	 */
	private final String host;
	/**
	 * Host port.
	 */
	private final int port;
	/**
	 * Reconnecting after connection loss.
	 */
	private boolean reconnect = true;
	/**
	 * Flag for running.
	 */
	private boolean running = false;

	/**
	 * 
	 * @param host
	 *            Ip.
	 * @param port
	 *            Port.
	 */
	public GamepadClient(String host, int port) {
		this.host = host;
		this.port = port;
	}

	/**
	 * Stop the reconnection.
	 */
	public void halt() {
		reconnect = false;
		running = false;
	}

	/**
	 * Update command string.
	 * 
	 * @param c
	 *            New command.
	 */
	public void sendCommand(int c) {
		if (running) {
			try {
				out.write(c);
				out.flush();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
	}
	
	public void sendValues(float x, float y, float z, float rz){
		if (running) {
			try {
				int ix = (int) ((x+1) * 10);
				int iy = (int) ((y+1) * 10);
				int iz = (int) ((z+1) * 10);
				int irz = (int) ((rz+1) * 10);
				out.write(ix);
				out.write(iy);
				out.write(iz);
				out.write(irz);
				out.flush();
				System.out.println(ix + ", " + iy + ", " + iz + ", " + irz);
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
	}

	@Override
	public void run() {
		while (reconnect) {
			try {
				while (socket == null && reconnect) {
					try {
						// Connect socket to host.
						socket = new Socket(host, port);
						out = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
						running = true;
					} catch (Exception e) {
						synchronized (this) {
							try {
								// Wait and try to connect again.
								this.wait(1000);
							} catch (InterruptedException e1) {

							}
						}
					}
				}
				if (reconnect) {
					while (running) {

					}
					// Close socket.
					out.close();
					socket.close();
					System.out.println("Close");
				}
			} catch (UnknownHostException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
	}
}
