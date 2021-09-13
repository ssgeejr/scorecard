<%@page import="java.sql.*, javax.sql.*, javax.naming.*, java.util.*"%>
<%@page import="com.north.scorecard.tethysui.*" %>
<%
	boolean fault = false;
	String ymval = "";
	TopTenList ttl = null;
	ArrayList<TopTenItem> items = null;
	TopTenItem item = null;
	
	try{
	    String month = request.getParameter("month").trim();
	    String year = request.getParameter("year").trim();
	    ymval = "Time Frame: " + month + "/" + year;
//		out.println("DTKEY: " + month + "/" + year  + "<br>");
	}catch(Exception ex){
		fault = true;
//		out.println(ex.toString());
	}
	//out.println("FAULT: " + fault + "<br>");
	try{
	DataEngine de = new DataEngine();
	ttl = de.fetchTopTenDataResults("0721");
	items = ttl.getCritcalList();
	System.out.println("ITEMS_SIZE: " + items.size());
	System.out.println("TTLSIZE: " + (ttl == null));
	fault = true;
	}catch(Exception ex){
		System.err.println("******************************************************");
		 ex.printStackTrace();
		 out.println("<hr> ERRRORRRRRRR </hr><br>");
		 out.println(ex.getMessage());
	}

%>


<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
<meta content="en-us" http-equiv="Content-Language" />
<meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
<title>Top 10 Issues by Risk</title>
<style type="text/css">
.auto-style1 {
	text-align: center;
}
.auto-style2 {
	text-align: right;
}
.auto-style3 {
	border-style: solid;
	border-width: 1px;
}
.auto-style4 {
	color: #FFFFFF;
}
.auto-style5 {
	text-align: left;
}
.st_c {
	width: 50px; text-align: center;
}
.st_p {
	width: 50px; text-align: center;
}
.st_i {
	width: 125px; text-align: center;
}
.st_n {
	text-align: left;
}
.st_sh{
	background-color: #0000FF; color: #FFFFFF
}
</style>
</head>

<body>
<form action="index.jsp" method="post">
<div align="center" >

<table style="width: 600pt">
	<tr>
		<td class="auto-style1"><strong>Top 10 Issues by Risk<br />
		<%= ymval %></strong></td>
	</tr>
	<tr>
		<td class="auto-style2"><select name="month" id="month">
		<option selected="selected" value="01">Jan</option>
		<option value="02">Feb</option>
		<option value="03">Mar</option>
		<option value="04">Apr</option>
		<option value="05">May</option>
		<option value="06">Jun</option>
		<option value="07">Jul</option>
		<option value="08">Aug</option>
		<option value="09">Sep</option>
		<option value="10">Oct</option>
		<option value="11">Nov</option>
		<option value="12">Dec</option>
		</select><select  name="year" id="year">
		<option selected="selected" value="21">2021</option>
		<option value="22">2022</option>
		<option value="23">2023</option>
		</select>
		<input type="image" src="s.png" border="0" alt="Submit" />
		</td>
	</tr>
	<tr>
		<td>
				<table style="width: 600pt">
			<tr>
				<td class="st_sh">CRITICAL</td>
			</tr>
			<tr>
				<td>
				<table class="auto-style3" style="width: 100%">
					<tr bgcolor="#008080">
						<td class="st_c"><strong>Count</strong></td>
						<td class="st_p"><strong>%</strong></td>
						<td class="st_i"><strong>Plugin-ID</strong></td>
						<td class="st_n"><strong>&nbsp;Vulnerability</strong></td>
					</tr>
					
					<% 
						items = ttl.getCritcalList();
					    item = items.get(0);
					%>
					
					<tr bgcolor="#FFFFCC">
						<td class="st_c">&nbsp; <%= item.getCount() %></td>
						<td class="st_p">&nbsp; <%= item.getPct() %>%</td>
						<td class="st_i">&nbsp; <%= item.getPluginid() %></td>
						<td class="st_n">&nbsp;<%= item.getName() %></td>
					</tr>
					<% 
					    item = items.get(1);
					%>
					
					<tr>
						<td class="st_c">&nbsp; <%= item.getCount() %></td>
						<td class="st_p">&nbsp; <%= item.getPct() %>%</td>
						<td class="st_i">&nbsp; <%= item.getPluginid() %></td>
						<td class="st_n">&nbsp;<%= item.getName() %></td>
					</tr>
					<% 
					    item = items.get(2);
					%>
					
					<tr bgcolor="#FFFFCC">
						<td class="st_c">&nbsp; <%= item.getCount() %></td>
						<td class="st_p">&nbsp; <%= item.getPct() %>%</td>
						<td class="st_i">&nbsp; <%= item.getPluginid() %></td>
						<td class="st_n">&nbsp;<%= item.getName() %></td>
					</tr>
					<% 
					    item = items.get(3);
					%>
					
					<tr>
						<td class="st_c">&nbsp; <%= item.getCount() %></td>
						<td class="st_p">&nbsp; <%= item.getPct() %>%</td>
						<td class="st_i">&nbsp; <%= item.getPluginid() %></td>
						<td class="st_n">&nbsp;<%= item.getName() %></td>
					</tr>
					<% 
					    item = items.get(4);
					%>
					
					<tr bgcolor="#FFFFCC">
						<td class="st_c">&nbsp; <%= item.getCount() %></td>
						<td class="st_p">&nbsp; <%= item.getPct() %>%</td>
						<td class="st_i">&nbsp; <%= item.getPluginid() %></td>
						<td class="st_n">&nbsp;<%= item.getName() %></td>
					</tr>
					<% 
					    item = items.get(5);
					%>
					
					<tr>
						<td class="st_c">&nbsp; <%= item.getCount() %></td>
						<td class="st_p">&nbsp; <%= item.getPct() %>%</td>
						<td class="st_i">&nbsp; <%= item.getPluginid() %></td>
						<td class="st_n">&nbsp;<%= item.getName() %></td>
					</tr>
						<% 
					    item = items.get(6);
					%>
					
					<tr bgcolor="#FFFFCC">
						<td class="st_c">&nbsp; <%= item.getCount() %></td>
						<td class="st_p">&nbsp; <%= item.getPct() %>%</td>
						<td class="st_i">&nbsp; <%= item.getPluginid() %></td>
						<td class="st_n">&nbsp;<%= item.getName() %></td>
					</tr>
					<% 
					    item = items.get(7);
					%>
					
					<tr>
						<td class="st_c">&nbsp; <%= item.getCount() %></td>
						<td class="st_p">&nbsp; <%= item.getPct() %>%</td>
						<td class="st_i">&nbsp; <%= item.getPluginid() %></td>
						<td class="st_n">&nbsp;<%= item.getName() %></td>
					</tr>
					<% 
					    item = items.get(8);
					%>
					
					<tr bgcolor="#FFFFCC">
						<td class="st_c">&nbsp; <%= item.getCount() %></td>
						<td class="st_p">&nbsp; <%= item.getPct() %>%</td>
						<td class="st_i">&nbsp; <%= item.getPluginid() %></td>
						<td class="st_n">&nbsp;<%= item.getName() %></td>
					</tr>
					<% 
					    item = items.get(9);
					%>
					
					<tr>
						<td class="st_c">&nbsp; <%= item.getCount() %></td>
						<td class="st_p">&nbsp; <%= item.getPct() %>%</td>
						<td class="st_i">&nbsp; <%= item.getPluginid() %></td>
						<td class="st_n">&nbsp;<%= item.getName() %></td>
					</tr>

				</table>
				</td>
			</tr>
		</table>

		</td>
	</tr>
	<tr>
		<td>
				<table style="width: 600pt">
			<tr>
				<td class="st_sh">HIGH</td>
			</tr>
			<tr>
				<td>
				<table class="auto-style3" style="width: 100%">
					<tr bgcolor="#008080">
						<td class="st_c"><strong>Count</strong></td>
						<td class="st_p"><strong>%</strong></td>
						<td class="st_i"><strong>Plugin-ID</strong></td>
						<td class="st_n"><strong>&nbsp;Vulnerability</strong></td>
					</tr>
					
					<% 
						items = ttl.getHighList();
					    item = items.get(0);
					%>
					
					<tr bgcolor="#FFFFCC">
						<td class="st_c">&nbsp; <%= item.getCount() %></td>
						<td class="st_p">&nbsp; <%= item.getPct() %>%</td>
						<td class="st_i">&nbsp; <%= item.getPluginid() %></td>
						<td class="st_n">&nbsp;<%= item.getName() %></td>
					</tr>
					<% 
					    item = items.get(1);
					%>
					
					<tr>
						<td class="st_c">&nbsp; <%= item.getCount() %></td>
						<td class="st_p">&nbsp; <%= item.getPct() %>%</td>
						<td class="st_i">&nbsp; <%= item.getPluginid() %></td>
						<td class="st_n">&nbsp;<%= item.getName() %></td>
					</tr>
					<% 
					    item = items.get(2);
					%>
					
					<tr bgcolor="#FFFFCC">
						<td class="st_c">&nbsp; <%= item.getCount() %></td>
						<td class="st_p">&nbsp; <%= item.getPct() %>%</td>
						<td class="st_i">&nbsp; <%= item.getPluginid() %></td>
						<td class="st_n">&nbsp;<%= item.getName() %></td>
					</tr>
					<% 
					    item = items.get(3);
					%>
					
					<tr>
						<td class="st_c">&nbsp; <%= item.getCount() %></td>
						<td class="st_p">&nbsp; <%= item.getPct() %>%</td>
						<td class="st_i">&nbsp; <%= item.getPluginid() %></td>
						<td class="st_n">&nbsp;<%= item.getName() %></td>
					</tr>
					<% 
					    item = items.get(4);
					%>
					
					<tr bgcolor="#FFFFCC">
						<td class="st_c">&nbsp; <%= item.getCount() %></td>
						<td class="st_p">&nbsp; <%= item.getPct() %>%</td>
						<td class="st_i">&nbsp; <%= item.getPluginid() %></td>
						<td class="st_n">&nbsp;<%= item.getName() %></td>
					</tr>
					<% 
					    item = items.get(5);
					%>
					
					<tr>
						<td class="st_c">&nbsp; <%= item.getCount() %></td>
						<td class="st_p">&nbsp; <%= item.getPct() %>%</td>
						<td class="st_i">&nbsp; <%= item.getPluginid() %></td>
						<td class="st_n">&nbsp;<%= item.getName() %></td>
					</tr>
						<% 
					    item = items.get(6);
					%>
					
					<tr bgcolor="#FFFFCC">
						<td class="st_c">&nbsp; <%= item.getCount() %></td>
						<td class="st_p">&nbsp; <%= item.getPct() %>%</td>
						<td class="st_i">&nbsp; <%= item.getPluginid() %></td>
						<td class="st_n">&nbsp;<%= item.getName() %></td>
					</tr>
					<% 
					    item = items.get(7);
					%>
					
					<tr>
						<td class="st_c">&nbsp; <%= item.getCount() %></td>
						<td class="st_p">&nbsp; <%= item.getPct() %>%</td>
						<td class="st_i">&nbsp; <%= item.getPluginid() %></td>
						<td class="st_n">&nbsp;<%= item.getName() %></td>
					</tr>
					<% 
					    item = items.get(8);
					%>
					
					<tr bgcolor="#FFFFCC">
						<td class="st_c">&nbsp; <%= item.getCount() %></td>
						<td class="st_p">&nbsp; <%= item.getPct() %>%</td>
						<td class="st_i">&nbsp; <%= item.getPluginid() %></td>
						<td class="st_n">&nbsp;<%= item.getName() %></td>
					</tr>
					<% 
					    item = items.get(9);
					%>
					
					<tr>
						<td class="st_c">&nbsp; <%= item.getCount() %></td>
						<td class="st_p">&nbsp; <%= item.getPct() %>%</td>
						<td class="st_i">&nbsp; <%= item.getPluginid() %></td>
						<td class="st_n">&nbsp;<%= item.getName() %></td>
					</tr>

				</table>
				</td>
			</tr>
		</table>

		</td>
	</tr>
	<tr>
		<td>
				<table style="width: 600pt">
			<tr>
				<td class="st_sh">MEDIUM</td>
			</tr>
			<tr>
				<td>
				<table class="auto-style3" style="width: 100%">
					<tr bgcolor="#008080">
						<td class="st_c"><strong>Count</strong></td>
						<td class="st_p"><strong>%</strong></td>
						<td class="st_i"><strong>Plugin-ID</strong></td>
						<td class="st_n"><strong>&nbsp;Vulnerability</strong></td>
					</tr>
					
					<% 
						items = ttl.getMediumList();
					    item = items.get(0);
					%>
					
					<tr bgcolor="#FFFFCC">
						<td class="st_c">&nbsp; <%= item.getCount() %></td>
						<td class="st_p">&nbsp; <%= item.getPct() %>%</td>
						<td class="st_i">&nbsp; <%= item.getPluginid() %></td>
						<td class="st_n">&nbsp;<%= item.getName() %></td>
					</tr>
					<% 
					    item = items.get(1);
					%>
					
					<tr>
						<td class="st_c">&nbsp; <%= item.getCount() %></td>
						<td class="st_p">&nbsp; <%= item.getPct() %>%</td>
						<td class="st_i">&nbsp; <%= item.getPluginid() %></td>
						<td class="st_n">&nbsp;<%= item.getName() %></td>
					</tr>
					<% 
					    item = items.get(2);
					%>
					
					<tr bgcolor="#FFFFCC">
						<td class="st_c">&nbsp; <%= item.getCount() %></td>
						<td class="st_p">&nbsp; <%= item.getPct() %>%</td>
						<td class="st_i">&nbsp; <%= item.getPluginid() %></td>
						<td class="st_n">&nbsp;<%= item.getName() %></td>
					</tr>
					<% 
					    item = items.get(3);
					%>
					
					<tr>
						<td class="st_c">&nbsp; <%= item.getCount() %></td>
						<td class="st_p">&nbsp; <%= item.getPct() %>%</td>
						<td class="st_i">&nbsp; <%= item.getPluginid() %></td>
						<td class="st_n">&nbsp;<%= item.getName() %></td>
					</tr>
					<% 
					    item = items.get(4);
					%>
					
					<tr bgcolor="#FFFFCC">
						<td class="st_c">&nbsp; <%= item.getCount() %></td>
						<td class="st_p">&nbsp; <%= item.getPct() %>%</td>
						<td class="st_i">&nbsp; <%= item.getPluginid() %></td>
						<td class="st_n">&nbsp;<%= item.getName() %></td>
					</tr>
					<% 
					    item = items.get(5);
					%>
					
					<tr>
						<td class="st_c">&nbsp; <%= item.getCount() %></td>
						<td class="st_p">&nbsp; <%= item.getPct() %>%</td>
						<td class="st_i">&nbsp; <%= item.getPluginid() %></td>
						<td class="st_n">&nbsp;<%= item.getName() %></td>
					</tr>
						<% 
					    item = items.get(6);
					%>
					
					<tr bgcolor="#FFFFCC">
						<td class="st_c">&nbsp; <%= item.getCount() %></td>
						<td class="st_p">&nbsp; <%= item.getPct() %>%</td>
						<td class="st_i">&nbsp; <%= item.getPluginid() %></td>
						<td class="st_n">&nbsp;<%= item.getName() %></td>
					</tr>
					<% 
					    item = items.get(7);
					%>
					
					<tr>
						<td class="st_c">&nbsp; <%= item.getCount() %></td>
						<td class="st_p">&nbsp; <%= item.getPct() %>%</td>
						<td class="st_i">&nbsp; <%= item.getPluginid() %></td>
						<td class="st_n">&nbsp;<%= item.getName() %></td>
					</tr>
					<% 
					    item = items.get(8);
					%>
					
					<tr bgcolor="#FFFFCC">
						<td class="st_c">&nbsp; <%= item.getCount() %></td>
						<td class="st_p">&nbsp; <%= item.getPct() %>%</td>
						<td class="st_i">&nbsp; <%= item.getPluginid() %></td>
						<td class="st_n">&nbsp;<%= item.getName() %></td>
					</tr>
					<% 
					    item = items.get(9);
					%>
					
					<tr>
						<td class="st_c">&nbsp; <%= item.getCount() %></td>
						<td class="st_p">&nbsp; <%= item.getPct() %>%</td>
						<td class="st_i">&nbsp; <%= item.getPluginid() %></td>
						<td class="st_n">&nbsp;<%= item.getName() %></td>
					</tr>

				</table>
				</td>
			</tr>
		</table>

		</td>
	</tr>
	<tr>
		<td>
				<table style="width: 600pt">
			<tr>
				<td class="st_sh">LOW</td>
			</tr>
			<tr>
				<td>
				<table class="auto-style3" style="width: 100%">
					<tr bgcolor="#008080">
						<td class="st_c"><strong>Count</strong></td>
						<td class="st_p"><strong>%</strong></td>
						<td class="st_i"><strong>Plugin-ID</strong></td>
						<td class="st_n"><strong>&nbsp;Vulnerability</strong></td>
					</tr>
					
					<% 
						items = ttl.getLowList();
					    item = items.get(0);
					%>
					
					<tr bgcolor="#FFFFCC">
						<td class="st_c">&nbsp; <%= item.getCount() %></td>
						<td class="st_p">&nbsp; <%= item.getPct() %>%</td>
						<td class="st_i">&nbsp; <%= item.getPluginid() %></td>
						<td class="st_n">&nbsp;<%= item.getName() %></td>
					</tr>
					<% 
					    item = items.get(1);
					%>
					
					<tr>
						<td class="st_c">&nbsp; <%= item.getCount() %></td>
						<td class="st_p">&nbsp; <%= item.getPct() %>%</td>
						<td class="st_i">&nbsp; <%= item.getPluginid() %></td>
						<td class="st_n">&nbsp;<%= item.getName() %></td>
					</tr>
					<% 
					    item = items.get(2);
					%>
					
					<tr bgcolor="#FFFFCC">
						<td class="st_c">&nbsp; <%= item.getCount() %></td>
						<td class="st_p">&nbsp; <%= item.getPct() %>%</td>
						<td class="st_i">&nbsp; <%= item.getPluginid() %></td>
						<td class="st_n">&nbsp;<%= item.getName() %></td>
					</tr>
					<% 
					    item = items.get(3);
					%>
					
					<tr>
						<td class="st_c">&nbsp; <%= item.getCount() %></td>
						<td class="st_p">&nbsp; <%= item.getPct() %>%</td>
						<td class="st_i">&nbsp; <%= item.getPluginid() %></td>
						<td class="st_n">&nbsp;<%= item.getName() %></td>
					</tr>
					<% 
					    item = items.get(4);
					%>
					
					<tr bgcolor="#FFFFCC">
						<td class="st_c">&nbsp; <%= item.getCount() %></td>
						<td class="st_p">&nbsp; <%= item.getPct() %>%</td>
						<td class="st_i">&nbsp; <%= item.getPluginid() %></td>
						<td class="st_n">&nbsp;<%= item.getName() %></td>
					</tr>
					<% 
					    item = items.get(5);
					%>
					
					<tr>
						<td class="st_c">&nbsp; <%= item.getCount() %></td>
						<td class="st_p">&nbsp; <%= item.getPct() %>%</td>
						<td class="st_i">&nbsp; <%= item.getPluginid() %></td>
						<td class="st_n">&nbsp;<%= item.getName() %></td>
					</tr>
						<% 
					    item = items.get(6);
					%>
					
					<tr bgcolor="#FFFFCC">
						<td class="st_c">&nbsp; <%= item.getCount() %></td>
						<td class="st_p">&nbsp; <%= item.getPct() %>%</td>
						<td class="st_i">&nbsp; <%= item.getPluginid() %></td>
						<td class="st_n">&nbsp;<%= item.getName() %></td>
					</tr>
					<% 
					    item = items.get(7);
					%>
					
					<tr>
						<td class="st_c">&nbsp; <%= item.getCount() %></td>
						<td class="st_p">&nbsp; <%= item.getPct() %>%</td>
						<td class="st_i">&nbsp; <%= item.getPluginid() %></td>
						<td class="st_n">&nbsp;<%= item.getName() %></td>
					</tr>
					<% 
					    item = items.get(8);
					%>
					
					<tr bgcolor="#FFFFCC">
						<td class="st_c">&nbsp; <%= item.getCount() %></td>
						<td class="st_p">&nbsp; <%= item.getPct() %>%</td>
						<td class="st_i">&nbsp; <%= item.getPluginid() %></td>
						<td class="st_n">&nbsp;<%= item.getName() %></td>
					</tr>
					<% 
					    item = items.get(9);
					%>
					
					<tr>
						<td class="st_c">&nbsp; <%= item.getCount() %></td>
						<td class="st_p">&nbsp; <%= item.getPct() %>%</td>
						<td class="st_i">&nbsp; <%= item.getPluginid() %></td>
						<td class="st_n">&nbsp;<%= item.getName() %></td>
					</tr>

				</table>
				</td>
			</tr>
		</table>

		</td>
	</tr>
	<tr>
		<td>&nbsp;</td>
	</tr>
	<tr>
		<td>&nbsp;</td>
	</tr>
	<tr>
		<td>&nbsp;</td>
	</tr>
</table>
</div>
</form>
</body>

</html>
