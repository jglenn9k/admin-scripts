<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>DNS Tools</title>
<style type="text/css">
table, td, th {border:1px solid black;}
td {text-align:right;}
</style>
</head>
<body>
<?php

function linuxUptime() {
  $ut = strtok( exec( "cat /proc/uptime" ), "." );
  $days = sprintf( "%2d", ($ut/(3600*24)) );
  $hours = sprintf( "%2d", ( ($ut % (3600*24)) / 3600) );
  $min = sprintf( "%2d", ($ut % (3600*24) % 3600)/60  );
  $sec = sprintf( "%2d", ($ut % (3600*24) % 3600)%60  );
  return array( $days, $hours, $min, $sec );
}

$ut = linuxUptime();

$ua = get_browser();

?>
<p>You are on server <?php echo php_uname('n');?>
</p>
<p>Your IP address is <?php echo $_SERVER["REMOTE_ADDR"];?>
</p>
<p>Your host name is <?php echo gethostbyaddr($_SERVER["REMOTE_ADDR"]);?>
</p>
<p>Your browser is <?php echo $ua->parent;?>
</p>
<p>Your operating system is <?php echo $ua->platform;?>
</p>
<p>Server uptime is <?php echo "$ut[0] days, $ut[1] hours, $ut[2] minutes, $ut[3] seconds."; ?>
</p>
<table border="1">
<tr><th>Tool</th><th>Host Name</th></tr>
<form name="ping" action="/cgi-bin/ping" method="get">
<tr><td><input type="submit" value="Ping" /></td>
<td><input type="text" name="ip" /></td></tr>
</form>
<form name="whois" action="/cgi-bin/whois" method="get">
<tr><td><input type="submit" value="Who Is" /></td>
<td><input type="text" name="ip" /></td></tr>
</form>
<form name="tracert" action="/cgi-bin/traceroute" method="get">
<tr><td><input type="submit" value="Trace Route" /></td>
<td><input type="text" name="ip" /></td></tr>
</form>
<form name="dig" action="/cgi-bin/dig" method="get">
<tr><td><input type="submit" value="DNS record lookup" /></td>
<td><input type="text" name="ip" /></td>
<td>Type: <select name="type">
<option value="ANY">ANY</option>
<option value="A">A</option>
<option value="AAAA">AAAA</option>
<option value="CNAME">CNAME</option>
<option value="MX">MX</option>
<option value="NS">NS</option>
<option value="PTR">PTR</option>
<option value="SOA">SOA</option>
<option value="SPF">SPF</option>
<option value="SRV">SRV</option>
<option value="TXT">TXT</option>
<option value="DNSSEC">DNSSEC</option>
</select></td></tr>
</form>
<form name="revdns" action="/cgi-bin/reversedig" method="get">
<tr><td><input type="submit" value="Reverse DNS Lookup" /></td>
<td><input type="text" name="ip" /></td></tr>
</form>
<form name="smtp" action="/cgi-bin/smtp" method="get">
<tr><td><input type="submit" value="TCP/SMTP Port Test" /></td>
<td><input type="text" name="ip" /></td></tr>
</form>
</table>
<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-XXXXXXX-XX', 'example.com');
  ga('send', 'pageview');

</script>
<p>Questions? Want a feature? Send an email to <a href="mailto:<?php echo $_SERVER["SERVER_ADMIN"];?>"><?php echo $_SERVER["SERVER_ADMIN"];?></a>.
</body>
</html>
