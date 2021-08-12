package com.north.scorecard.tethysui;

public class TopTenItem {


	private int count = 0;
	private int pct = 0;
	private int pluginid = 0;
	private String name = "";
	
	public TopTenItem() {}
	public TopTenItem(int c, int p, int id, String n) {
		count = c;
		pct = p;
		pluginid = id;
		name = n;
	}
	
	public int getCount() {
		return count;
	}
	public int getPct() {
		return pct;
	}
	public int getPluginid() {
		return pluginid;
	}
	public String getName() {
		return name;
	}
	
	public void setCount(int count) {
		this.count = count;
	}
	public void setPct(int pct) {
		this.pct = pct;
	}
	public void setPluginid(int pluginid) {
		this.pluginid = pluginid;
	}
	public void setName(String name) {
		this.name = name;
	}
	
	
}
