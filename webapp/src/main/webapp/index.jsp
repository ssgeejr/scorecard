<a href='<%@page import="java.sql.*, javax.sql.*, javax.naming.*"%>'></a>

<%
	boolean fault = false;
	String ymval = "";
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


if(!fault){


    DataSource ds = null;
    Connection conn = null;
    ResultSet result = null;
    Statement stmt = null;
    try{
        Context ctx = new InitialContext();
        ds = (DataSource)ctx.lookup("java:comp/env/jdbc/tethys");
        if (ds != null) {
            conn = ds.getConnection();
            Statement statement = conn.createStatement();
            String sql = "select riskid, total from scorecard where dtkey = '0721' order by riskid";
            ResultSet rs = statement.executeQuery(sql);
            while(rs.next()){
                out.println("RISKID: " + rs.getInt("riskid") + " TOTAL: " + rs.getInt("total") + "<br>");
            }
        }else{
            out.println("DATASOURCE WAS NULL...");
        }
    } catch (Exception e) {
        e.printStackTrace();
    }
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
				<td bgcolor="#0000FF" class="auto-style4">CRITICAL</td>
			</tr>
			<tr>
				<td>
				<table class="auto-style3" style="width: 100%">
					<tr bgcolor="#008080">
						<td style="width: 75px"><strong>Count</strong></td>
						<td style="width: 75px"><strong>%</strong></td>
						<td style="width: 75px"><strong>Plugin-ID</strong></td>
						<td style="width: *" class="auto-style5"><strong>&nbsp;Vulnerability</strong></td>
					</tr>
					<tr bgcolor="#FFFFCC">
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td>&nbsp;</td>
					</tr>
					<tr>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td>&nbsp;</td>
					</tr>
					<tr bgcolor="#FFFFCC">
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td>&nbsp;</td>
					</tr>
					<tr>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td>&nbsp;</td>
					</tr>
					<tr bgcolor="#FFFFCC">
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td>&nbsp;</td>
					</tr>
					<tr>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td>&nbsp;</td>
					</tr>
					<tr bgcolor="#FFFFCC">
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td>&nbsp;</td>
					</tr>
					<tr>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td>&nbsp;</td>
					</tr>
					<tr bgcolor="#FFFFCC">
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td>&nbsp;</td>
					</tr>
					<tr>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td>&nbsp;</td>
					</tr>
					<tr bgcolor="#FFFFCC">
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td>&nbsp;</td>
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
				<td bgcolor="#0000FF" class="auto-style4">HIGH</td>
			</tr>
			<tr>
				<td>
				<table class="auto-style3" style="width: 100%">
					<tr bgcolor="#008080">
						<td style="width: 75px"><strong>Count</strong></td>
						<td style="width: 75px"><strong>%</strong></td>
						<td style="width: 75px"><strong>Plugin-ID</strong></td>
						<td style="width: *" class="auto-style5"><strong>&nbsp;Vulnerability</strong></td>
					</tr>
					<tr bgcolor="#FFFFCC">
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td>&nbsp;</td>
					</tr>
					<tr>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td>&nbsp;</td>
					</tr>
					<tr bgcolor="#FFFFCC">
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td>&nbsp;</td>
					</tr>
					<tr>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td>&nbsp;</td>
					</tr>
					<tr bgcolor="#FFFFCC">
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td>&nbsp;</td>
					</tr>
					<tr>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td>&nbsp;</td>
					</tr>
					<tr bgcolor="#FFFFCC">
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td>&nbsp;</td>
					</tr>
					<tr>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td>&nbsp;</td>
					</tr>
					<tr bgcolor="#FFFFCC">
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td>&nbsp;</td>
					</tr>
					<tr>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td>&nbsp;</td>
					</tr>
					<tr bgcolor="#FFFFCC">
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td>&nbsp;</td>
					</tr>
				</table>
				</td>
			</tr>
		</table>
</td>
	</tr>
	<tr>
		<td>		<div align="center">
		<table style="width: 600pt">
			<tr>
				<td bgcolor="#0000FF" class="auto-style4">MEDIUM</td>
			</tr>
			<tr>
				<td>
				<table class="auto-style3" style="width: 100%">
					<tr bgcolor="#008080">
						<td style="width: 75px"><strong>Count</strong></td>
						<td style="width: 75px"><strong>%</strong></td>
						<td style="width: 75px"><strong>Plugin-ID</strong></td>
						<td style="width: *" class="auto-style5"><strong>&nbsp;Vulnerability</strong></td>
					</tr>
					<tr bgcolor="#FFFFCC">
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td>&nbsp;</td>
					</tr>
					<tr>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td>&nbsp;</td>
					</tr>
					<tr bgcolor="#FFFFCC">
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td>&nbsp;</td>
					</tr>
					<tr>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td>&nbsp;</td>
					</tr>
					<tr bgcolor="#FFFFCC">
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td>&nbsp;</td>
					</tr>
					<tr>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td>&nbsp;</td>
					</tr>
					<tr bgcolor="#FFFFCC">
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td>&nbsp;</td>
					</tr>
					<tr>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td>&nbsp;</td>
					</tr>
					<tr bgcolor="#FFFFCC">
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td>&nbsp;</td>
					</tr>
					<tr>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td>&nbsp;</td>
					</tr>
					<tr bgcolor="#FFFFCC">
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td>&nbsp;</td>
					</tr>
				</table>
				</td>
			</tr>
		</table>
		</div>
</td>
	</tr>
	<tr>
		<td >
		<div align="center">
		<table style="width: 600pt">
			<tr>
				<td bgcolor="#0000FF" class="auto-style4">LOW</td>
			</tr>
			<tr>
				<td>
				<table class="auto-style3" style="width: 100%">
					<tr bgcolor="#008080">
						<td style="width: 75px"><strong>Count</strong></td>
						<td style="width: 75px"><strong>%</strong></td>
						<td style="width: 75px"><strong>Plugin-ID</strong></td>
						<td style="width: *" class="auto-style5"><strong>&nbsp;Vulnerability</strong></td>
					</tr>
					<tr bgcolor="#FFFFCC">
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td>&nbsp;</td>
					</tr>
					<tr>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td>&nbsp;</td>
					</tr>
					<tr bgcolor="#FFFFCC">
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td>&nbsp;</td>
					</tr>
					<tr>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td>&nbsp;</td>
					</tr>
					<tr bgcolor="#FFFFCC">
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td>&nbsp;</td>
					</tr>
					<tr>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td>&nbsp;</td>
					</tr>
					<tr bgcolor="#FFFFCC">
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td>&nbsp;</td>
					</tr>
					<tr>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td>&nbsp;</td>
					</tr>
					<tr bgcolor="#FFFFCC">
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td>&nbsp;</td>
					</tr>
					<tr>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td>&nbsp;</td>
					</tr>
					<tr bgcolor="#FFFFCC">
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td style="width: 75px">&nbsp;</td>
						<td>&nbsp;</td>
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
