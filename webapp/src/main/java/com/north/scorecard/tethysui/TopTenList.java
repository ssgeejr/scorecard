package com.north.scorecard.tethysui;

import java.util.ArrayList;
//add(int index, E element)
public class TopTenList{
	private ArrayList<TopTenItem> critical = new ArrayList<TopTenItem>();
	private ArrayList<TopTenItem> high = new ArrayList<TopTenItem>();
	private ArrayList<TopTenItem> medium = new ArrayList<TopTenItem>();
	private ArrayList<TopTenItem> low = new ArrayList<TopTenItem>();
	public void addCriticalItem(TopTenItem tti) {
		critical.add(tti);
	}
	public void addHighItem(TopTenItem tti) {
		high.add(tti);
	}
	public void addMediumItem(TopTenItem tti) {
		medium.add(tti);
	}
	public void addLowItem(TopTenItem tti) {
		low.add(tti);
	}
	public ArrayList<TopTenItem> getCritcalList(){return critical;}
	public ArrayList<TopTenItem> getHighList(){return high;}
	public ArrayList<TopTenItem> getMediumList(){return medium;}
	public ArrayList<TopTenItem> getLowList(){return low;}
	
}
