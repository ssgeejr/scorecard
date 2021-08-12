package com.north.scorecard.tethysui;

import java.util.ArrayList;

public class TestEngine {

	TopTenList ttl = new TopTenList();
	
	public TestEngine() {
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
