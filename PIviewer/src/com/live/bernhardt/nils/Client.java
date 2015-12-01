package com.live.bernhardt.nils;


import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.Socket;
import java.net.UnknownHostException;

/**
 * Client for the connection to the server.
 * 
 * @author Nils Bernhardt
 *
 */
public class Client extends Thread {
	/**
	 * host ip
	 */
	private final String host;
	/**
	 * host port
	 */
	private final int port;
	/**
	 * panel for displaying
	 */
	private final UpdateableMap panel;
	/**
	 * reconnecting after connection loss
	 */
	private boolean reconnect = true;
	/**
	 * frame of the application
	 */
	private final UpdateableTitle frame;

	/**
	 * 
	 * @param frame
	 *            application frame
	 * @param panel
	 *            mappanel
	 * @param host
	 *            ip
	 * @param port
	 *            port
	 */
	public Client(UpdateableTitle frame, UpdateableMap panel, String host, int port) {
		this.panel = panel;
		this.host = host;
		this.port = port;
		this.frame = frame;
	}

	/**
	 * stops the reconnection
	 */
	public void halt() {
		reconnect = false;
	}

	@Override
	public void run() {
		while (reconnect) {
			try {
				frame.updateTitle("Connecting to: " + host);
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
					InputStream in = socket.getInputStream();
					frame.updateTitle("Connected to: " + host);
					BufferedReader reader = new BufferedReader(
							new InputStreamReader(in));
					String data = reader.readLine();
					int width = Integer.parseInt(data);
					byte[] values = new byte[width * width];
					int read = in.read(values);
					int index = 0;
					while (read != -1) {
						index += read;
						if(index==values.length){
							panel.updateMap(values);
							index = 0;
						}
						read = in.read(values, index, values.length-index);
					}
					in.close();
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
