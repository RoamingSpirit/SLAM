package com.live.bernhardt.nils;
import javax.swing.JFrame;


public class Frame extends JFrame implements UpdateableTitle {

	/**
	 * 
	 */
	private static final long serialVersionUID = 6675268979334983402L;

	@Override
	public void updateTitle(String text) {
		this.setTitle(text);
	}

}
