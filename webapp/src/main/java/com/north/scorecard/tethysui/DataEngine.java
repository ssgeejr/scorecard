package com.north.scorecard.tethysui;

import java.sql.*;
import java.util.ArrayList;

import javax.sql.*;
import javax.naming.*;

public class DataEngine {
	private Connection conn = null;
	
	public DataEngine() throws Exception{
//        Context ctx = new InitialContext();
//        ds = (DataSource)ctx.lookup("java:comp/env/jdbc/tethys");		
	}
	
	public DataEngine(boolean testmode) throws Exception{
		try {
		
			System.out.println("HELLO-WORLD");
//			conn = DriverManager.getConnection("jdbc:mysql://tethys/scorecard","scorecard","scorecard");
//			System.out.println("Connection IsClosed: " + conn.isClosed());
			fetchTopTenDataResults("0721");
		}finally {
			try {conn.close();}catch(Exception ce) {}
		}
	}
	
	public TopTenList fetchTopTenDataResults(String dt) throws Exception{
		TopTenList ttl = new TopTenList();
		try {
			
			Context ctx = new InitialContext();
			DataSource ds = (DataSource)ctx.lookup("java:comp/env/jdbc/tethys");
			if (ds == null) {
			 conn = DriverManager.getConnection("jdbc:mysql://tethysdb/scorecard","scorecard","scorecard");
			}else {
				System.out.println("CONTEXT CONNECTION SUCCESSFULLY LOADED ... ");
				conn = ds.getConnection();
			}
			System.out.println("Connection IsClosed: " + conn.isClosed());
		
			String query = "select" 
			+" a.pluginid as pid,"
			+" a.riskid as rid,"
			+" total,"
			+" pct,"
			+" b.vulname as name"
			+" from" 
			+" carddata a, plugin b"
			+" where" 
			+" a.riskid = ?"
			+" and a.dtkey = ?"
			+" and a.pluginid = b.pluginid"
			+" order by" 
			+" a.riskid, total desc";
			PreparedStatement psdata = conn.prepareStatement(query);
			System.out.println(query);
			
			psdata.setInt(1, 0);
			psdata.setString(2, "0721");
			ResultSet rs = psdata.executeQuery();
			
			int counter = 0;
			System.out.println("*************************** CRITICAL ***************************");
			while(rs.next()) {
				ttl.addCriticalItem(new TopTenItem(rs.getInt("total"), rs.getInt("pct"), rs.getInt("pid"),rs.getString("name")));
				counter++;
//				System.out.println("COUNTER: " + counter);
				if(counter == 10)break;
			}
//			ArrayList<TopTenItem> list = ttl.getCritcalList();
//			for (TopTenItem i : list) {
//				System.out.println("Count [" + i.getCount() + "] Pct [" + i.getPct() + "%] PluginID [" + i.getPluginid() + "] Name: [" + i.getName() + "]");
//			}
			
			psdata.setInt(1, 1);
			psdata.setString(2, dt);
			rs = psdata.executeQuery();
			System.out.println("*************************** HIGH ***************************");
			counter = 0;
			while(rs.next()) {
				ttl.addHighItem(new TopTenItem(rs.getInt("total"), rs.getInt("pct"), rs.getInt("pid"),rs.getString("name")));
				counter++;
//				System.out.println("COUNTER: " + counter);
				if(counter == 10)break;
			}
			
//			list = ttl.getHighList();
//			for (TopTenItem i : list) {
//				System.out.println("Count [" + i.getCount() + "] Pct [" + i.getPct() + "%] PluginID [" + i.getPluginid() + "] Name: [" + i.getName() + "]");
//			}
			psdata.setInt(1, 2);
			psdata.setString(2, "0721");
			rs = psdata.executeQuery();
			counter = 0;
			System.out.println("*************************** MEDIUM ***************************");
			while(rs.next()) {
				ttl.addMediumItem(new TopTenItem(rs.getInt("total"), rs.getInt("pct"), rs.getInt("pid"),rs.getString("name")));
				counter++;
//				System.out.println("COUNTER: " + counter);
				if(counter == 10)break;
			}
//			list = ttl.getMediumList();
//			for (TopTenItem i : list) {
//				System.out.println("Count [" + i.getCount() + "] Pct [" + i.getPct() + "%] PluginID [" + i.getPluginid() + "] Name: [" + i.getName() + "]");
//			}
			psdata.setInt(1, 3);
			psdata.setString(2, "0721");
			rs = psdata.executeQuery();
			counter = 0;
			System.out.println("*************************** LOW ***************************");
			
			while(rs.next()) {
				ttl.addLowItem(new TopTenItem(rs.getInt("total"), rs.getInt("pct"), rs.getInt("pid"),rs.getString("name")));
				counter++;
//				System.out.println("COUNTER: " + counter);
				if(counter == 10)break;
			}
//			list = ttl.getLowList();
//			for (TopTenItem i : list) {
//				System.out.println("Count [" + i.getCount() + "] Pct [" + i.getPct() + "%] PluginID [" + i.getPluginid() + "] Name: [" + i.getName() + "]");
//			}
			
		}finally {
			try {conn.close();}catch(Exception ce) {}
		}

		return ttl;
	}
	
	public static void main (String[] args) {
		try {
//			new DataEngine(true);
			
			
			DataEngine de = new DataEngine();
			de.fetchTopTenDataResults("0721");
			
			
		}catch(Exception ex) {
			ex.printStackTrace();
		}
	}
	
	
	
	
}
