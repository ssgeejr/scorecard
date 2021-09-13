package com.north.scorecard.tethysui;

import java.util.ArrayList;
import java.sql.*;
import javax.sql.DataSource;

//For Date Navigation 
import java.time.LocalDate;

public class TestEngine {
	private Connection conn = null;
	TopTenList ttl = new TopTenList();
	
	public TestEngine() {
		ScorecardData scorecard = new ScorecardData();
		LocalDate xdate = LocalDate.now(); // 2015-11-24
		ScorecardMonth scm = null;
//		for(int x = 0; x < 12; x++) {
//########### ALPHA (1) ###########			
			String dt = setMonthValue(xdate.getMonthValue()) + setYearValue(xdate.getYear());
			String month = xdate.getMonth().toString().substring(0,3) + " " + setYearValue(xdate.getYear());
			System.out.println(dt);
			scorecard.setAlpha(fetchData(month,dt));
			System.out.println("SCM.MONTH: " + scorecard.getAlpha().getName());
			xdate = xdate.minusMonths(1);
			//--------------------------------------------------
//########### BETA (2) ###########	
			dt = setMonthValue(xdate.getMonthValue()) + setYearValue(xdate.getYear());
			month = xdate.getMonth().toString().substring(0,3) + " " + setYearValue(xdate.getYear());
			System.out.println(dt);
			scorecard.setBeta(fetchData(month,dt));
			System.out.println("SCM.MONTH: " + scorecard.getBeta().getName());
			xdate = xdate.minusMonths(1);			
//########### GAMMA (3) ###########		
			dt = setMonthValue(xdate.getMonthValue()) + setYearValue(xdate.getYear());
			month = xdate.getMonth().toString().substring(0,3) + " " + setYearValue(xdate.getYear());
			System.out.println(dt);
			scorecard.setGamma(fetchData(month,dt));
			System.out.println("SCM.MONTH: " + scorecard.getGamma().getName());
			xdate = xdate.minusMonths(1);
//########### DELTA (4) ###########		
			dt = setMonthValue(xdate.getMonthValue()) + setYearValue(xdate.getYear());
			month = xdate.getMonth().toString().substring(0,3) + " " + setYearValue(xdate.getYear());
			System.out.println(dt);
			scorecard.setDelta(fetchData(month,dt));
			System.out.println("SCM.MONTH: " + scorecard.getDelta().getName());
			xdate = xdate.minusMonths(1);
//########### EPSILON (5) ###########		
			dt = setMonthValue(xdate.getMonthValue()) + setYearValue(xdate.getYear());
			month = xdate.getMonth().toString().substring(0,3) + " " + setYearValue(xdate.getYear());
			System.out.println(dt);
			scorecard.setEpsilon(fetchData(month,dt));
			System.out.println("SCM.MONTH: " + scorecard.getEpsilon().getName());
			xdate = xdate.minusMonths(1);
//########### ZETA (6) ###########		
			dt = setMonthValue(xdate.getMonthValue()) + setYearValue(xdate.getYear());
			month = xdate.getMonth().toString().substring(0,3) + " " + setYearValue(xdate.getYear());
			System.out.println(dt);
			scorecard.setZeta(fetchData(month,dt));
			System.out.println("SCM.MONTH: " + scorecard.getZeta().getName());
			xdate = xdate.minusMonths(1);
//########### ETA (7) ###########		
			dt = setMonthValue(xdate.getMonthValue()) + setYearValue(xdate.getYear());
			month = xdate.getMonth().toString().substring(0,3) + " " + setYearValue(xdate.getYear());
			System.out.println(dt);
			scorecard.setEta(fetchData(month,dt));
			System.out.println("SCM.MONTH: " + scorecard.getEta().getName());
			xdate = xdate.minusMonths(1);
//########### THETA (8) ###########		
			dt = setMonthValue(xdate.getMonthValue()) + setYearValue(xdate.getYear());
			month = xdate.getMonth().toString().substring(0,3) + " " + setYearValue(xdate.getYear());
			System.out.println(dt);
			scorecard.setTheta(fetchData(month,dt));
			System.out.println("SCM.MONTH: " + scorecard.getTheta().getName());
			xdate = xdate.minusMonths(1);
//########### IOTA (9) ###########		
			dt = setMonthValue(xdate.getMonthValue()) + setYearValue(xdate.getYear());
			month = xdate.getMonth().toString().substring(0,3) + " " + setYearValue(xdate.getYear());
			System.out.println(dt);
			scorecard.setIota(fetchData(month,dt));
			System.out.println("SCM.MONTH: " + scorecard.getIota().getName());
			xdate = xdate.minusMonths(1);
//########### KAPPA (10) ###########		
			dt = setMonthValue(xdate.getMonthValue()) + setYearValue(xdate.getYear());
			month = xdate.getMonth().toString().substring(0,3) + " " + setYearValue(xdate.getYear());
			System.out.println(dt);
			scorecard.setKappa(fetchData(month,dt));
			System.out.println("SCM.MONTH: " + scorecard.getKappa().getName());
			xdate = xdate.minusMonths(1);
//########### LAMBDA (11) ###########		
			dt = setMonthValue(xdate.getMonthValue()) + setYearValue(xdate.getYear());
			month = xdate.getMonth().toString().substring(0,3) + " " + setYearValue(xdate.getYear());
			System.out.println(dt);
			scorecard.setLambda(fetchData(month,dt));
			System.out.println("SCM.MONTH: " + scorecard.getLambda().getName());
			xdate = xdate.minusMonths(1);
//########### MU (12) ###########		
			dt = setMonthValue(xdate.getMonthValue()) + setYearValue(xdate.getYear());
			month = xdate.getMonth().toString().substring(0,3) + " " + setYearValue(xdate.getYear());
			System.out.println(dt);
			scorecard.setMu(fetchData(month,dt));
			System.out.println("SCM.MONTH: " + scorecard.getMu().getName());
	}
	
	public ScorecardMonth fetchData(String name, String dt) {
		return new ScorecardMonth(name, dt);
	}
	
	
	public String setMonthValue(int date) {
		return (date > 9)?date + "":"0" + date;
	}
	public String setYearValue(int year) {
		return (year + "").substring(2);
	}

	public void testMonthNavigation() {
		try {
			DataSource ds = null;
			conn = DriverManager.getConnection("jdbc:mysql://tethysdb/scorecard","scorecard","scorecard");
			System.out.println("Connection Successful [" + !conn.isClosed() + "]");
			
			
			
			
			
		}catch(Exception ex) {
			ex.printStackTrace();
		}finally {
			try {conn.close();}catch(Exception ce) {}
		}
	}
	
	public void testTopTen() {
		ttl.addCriticalItem(new TopTenItem(566,19,62758,"Microsoft XML Parser (MSXML) and XML Core Services Unsupported"));
		ttl.addCriticalItem(new TopTenItem(565,19,59196,"Adobe Flash Player Unsupported Version Detection"));
		ttl.addCriticalItem(new TopTenItem(422,14,137754,"Microsoft Windows 10 Version 1803 Unsupported Version Detection"));
		ttl.addCriticalItem(new TopTenItem(81,3,108797,"Unsupported Windows OS (remote)"));
		ttl.addCriticalItem(new TopTenItem(57,2,130913,"Security Updates for Microsoft Office Products (November 2019)"));
		ttl.addCriticalItem(new TopTenItem(43,1,122615,"Microsoft Windows 7 / Server 2008 R2 Unsupported Version Detecti"));
		ttl.addCriticalItem(new TopTenItem(43,1,147231,"KB5000851: Windows 7 and Windows Server 2008 R2 March 2021 Secur"));
		ttl.addCriticalItem(new TopTenItem(43,1,73756,"Microsoft SQL Server Unsupported Version Detection (remote check"));
		ttl.addCriticalItem(new TopTenItem(42,1,134942,"Microsoft Windows Type 1 Font Parsing Remote Code Execution Vuln"));
		ttl.addCriticalItem(new TopTenItem(42,1,142683,"KB4586805: Windows 7 and Windows Server 2008 R2 November 2020 Se"));
		
		
		ArrayList<TopTenItem> list = ttl.getCritcalList();
		for (TopTenItem i : list) {
			System.out.println("Count [" + i.getCount() + "] Pct [" + i.getPct() + "%] PluginID [" + i.getPluginid() + "] Name: [" + i.getName() + "]");
		}
		
		
	}

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		new TestEngine();
	}

}
