package com.north.scorecard.tethysui;

public class ScorecardMonth {
	private String name = "?????";
	private String dt = "0000";
	private int netTotal =0;
	private int netNew = 0;
	private int netClosed = 0;
	private int crtiTotal = 0;
	private int critNew = 0;
	private int critClosed = 0;
	private int highTotal = 0;
	private int highNew = 0;
	private int highClosed = 0;
	private int medTotal = 0;
	private int medNew = 0;
	private int medClosed = 0;
	private int lowTotal =0;
	private int lowNew = 0;
	private int lowClosed = 0;
		
	public ScorecardMonth() {}
	public ScorecardMonth(String _name, String _dt) {
		name = _name;
		dt = _dt;
	}


	public String getName() {
		return name;
	}


	public String getDt() {
		return dt;
	}


	public int getNetTotal() {
		return netTotal;
	}


	public int getNetNew() {
		return netNew;
	}


	public int getNetClosed() {
		return netClosed;
	}


	public int getCrtiTotal() {
		return crtiTotal;
	}


	public int getCritNew() {
		return critNew;
	}


	public int getCritClosed() {
		return critClosed;
	}


	public int getHighTotal() {
		return highTotal;
	}


	public int getHighNew() {
		return highNew;
	}


	public int getHighClosed() {
		return highClosed;
	}


	public int getMedTotal() {
		return medTotal;
	}


	public int getMedNew() {
		return medNew;
	}


	public int getMedClosed() {
		return medClosed;
	}


	public int getLowTotal() {
		return lowTotal;
	}


	public int getLowNew() {
		return lowNew;
	}


	public int getLowClosed() {
		return lowClosed;
	}


	public void setName(String name) {
		this.name = name;
	}


	public void setDt(String dt) {
		this.dt = dt;
	}


	public void setNetTotal(int netTotal) {
		this.netTotal = netTotal;
	}


	public void setNetNew(int netNew) {
		this.netNew = netNew;
	}


	public void setNetClosed(int netClosed) {
		this.netClosed = netClosed;
	}


	public void setCrtiTotal(int crtiTotal) {
		this.crtiTotal = crtiTotal;
	}


	public void setCritNew(int critNew) {
		this.critNew = critNew;
	}


	public void setCritClosed(int critClosed) {
		this.critClosed = critClosed;
	}


	public void setHighTotal(int highTotal) {
		this.highTotal = highTotal;
	}


	public void setHighNew(int highNew) {
		this.highNew = highNew;
	}


	public void setHighClosed(int highClosed) {
		this.highClosed = highClosed;
	}


	public void setMedTotal(int medTotal) {
		this.medTotal = medTotal;
	}


	public void setMedNew(int medNew) {
		this.medNew = medNew;
	}


	public void setMedClosed(int medClosed) {
		this.medClosed = medClosed;
	}


	public void setLowTotal(int lowTotal) {
		this.lowTotal = lowTotal;
	}


	public void setLowNew(int lowNew) {
		this.lowNew = lowNew;
	}


	public void setLowClosed(int lowClosed) {
		this.lowClosed = lowClosed;
	}

}
