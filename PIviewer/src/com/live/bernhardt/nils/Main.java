package com.live.bernhardt.nils;

import java.awt.BorderLayout;
import java.awt.EventQueue;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

import javax.swing.JFrame;
import javax.swing.JOptionPane;

import com.gmail.brauckmann.lukas.Gamepad;
import com.gmail.brauckmann.lukas.GamepadClient;

/**
 * Creates a window and starts a thread for connection.
 * 
 * @author Nils Bernhardt
 *
 */
public class Main {
	/**
	 * application frame
	 */
	private Frame frame;

	/**
	 * Launch the application.
	 */
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					Main window = new Main();
					window.frame.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}

	/**
	 * Create the application.
	 */
	public Main() {
		initialize();
	}

	/**
	 * Initialize the contents of the frame.
	 */
	private void initialize() {
		frame = new Frame();
		frame.setBounds(0, 0, 1000, 500);
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.setResizable(false);

		MapPanel panel = new MapPanel(frame);
		frame.getContentPane().add(panel, BorderLayout.CENTER);

		String ip = null;
		while (ip == null) {
			ip = JOptionPane.showInputDialog("Enter IP", loadDefaultIP());
		}
		storeDefaultIP(ip);
		//new Client(frame, panel, ip, 8888).start();
		new Gamepad(new GamepadClient(ip, 8000)).start();
	}

	/**
	 * filename for the stored ip.
	 */
	private final String filename = "ip.dat";

	/**
	 * Stores the ip
	 * 
	 * @param ip
	 *            to store
	 */
	private void storeDefaultIP(String ip) {
		File file = new File(filename);
		try {
			BufferedWriter writer = new BufferedWriter(new FileWriter(file));
			writer.write(ip);
			writer.close();
		} catch (IOException e) {
		}
	}

	/**
	 * Loads the ip. empty if no ip is stored
	 * 
	 * @return ip
	 */
	private String loadDefaultIP() {
		File file = new File(filename);
		if (!file.exists())
			return "";

		try {
			BufferedReader reader = new BufferedReader(new FileReader(file));
			String ip = reader.readLine();
			reader.close();
			return ip;
		} catch (IOException e) {
			return "";
		}

	}

}
