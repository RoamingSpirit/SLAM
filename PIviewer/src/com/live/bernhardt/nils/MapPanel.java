package com.live.bernhardt.nils;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;

import javax.swing.JFrame;
import javax.swing.JPanel;

/**
 * JPanel for displaying a map represented by a byte array
 * 
 * @author Nils Bernhardt
 *
 */
@SuppressWarnings("serial")
public class MapPanel extends JPanel implements UpdateableMap {
	/**
	 * Current map,
	 */
	private byte[] map;
	/**
	 * width and height of the map
	 */
	private int size = 0;
	/**
	 * Jframe this panel is in.
	 */
	private final JFrame frame;

	/**
	 * 
	 * @param frame
	 *            motherpanel
	 */
	public MapPanel(JFrame frame) {
		this.frame = frame;
	}

	@Override
	public void paint(Graphics g) {
		if (map != null)
			synchronized (map) {
				for (int x = 0; x < size; x++)
					for (int y = 0; y < size; y++) {
						int value = map[x +y * size] & 0xFF;
						g.setColor(new Color(value, value, value));
						g.drawLine(x, y, x, y);
					}

			}
	}

	/* (non-Javadoc)
	 * @see UpdateableMap#updateMap(int[])
	 */
	@Override
	public void updateMap(byte[] map) {
		int size = 0;
		synchronized (map) {
			size = (int) Math.sqrt(map.length);
			this.map = map;
		}
		if (this.size != size) {
			frame.getContentPane().setPreferredSize(new Dimension(size, size));
			frame.pack();
		}
		this.size = size;
		repaint();
	}

}
