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
	private boolean running = true;
	/**
	 * Command string.
	 */
	private String cmd = "";

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
	 * @param cmd
	 *            New command.
	 */
	public void setCmd(String cmd) {
		this.cmd = cmd;
	}

	@Override
	public void run() {
		while (reconnect) {
			try {
				Socket socket = null;
				while (socket == null && reconnect) {
					try {
						// Connect socket to host.
						socket = new Socket(host, port);
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
					BufferedWriter out = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
					while (running) {
						// Send command string.
						out.write(cmd);
						cmd = "";
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
