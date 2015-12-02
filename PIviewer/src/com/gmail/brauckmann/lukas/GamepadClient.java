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
	 * Host ip
	 */
	private final String host;
	/**
	 * Host port
	 */
	private final int port;
	/**
	 * Reconnecting after connection loss
	 */
	private boolean reconnect = true;
	
	private boolean running = true;
	
	private String cmd = "";

	/**
	 * 
	 * @param host
	 *            ip
	 * @param port
	 *            port
	 */
	public GamepadClient(String host, int port) {
		this.host = host;
		this.port = port;
	}

	/**
	 * stops the reconnection
	 */
	public void halt() {
		reconnect = false;
		running = false;
	}
	
	public void setCmd(String cmd){
		this.cmd = cmd;
	}

	@Override
	public void run() {
		while (reconnect) {
			try {
				Socket socket = null;
				while (socket == null && reconnect) {
					try {
						socket = new Socket(host, port);
					} catch (Exception e) {
						synchronized (this) {
							try {
								this.wait(1000);
							} catch (InterruptedException e1) {

							}
						}
					}
				}
				if (reconnect) {
					BufferedWriter out = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
					
					while (running){
						out.write(cmd);
						cmd = "";
					}
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
