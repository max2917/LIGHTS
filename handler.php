<?php

if (isset($_GET['mode']) and isset($_GET['red']) and isset($_GET['green']) and isset($_GET['blue'])) {
	send_color($_GET['mode'], $_GET['red'], $_GET['green'], $_GET['blue']);
}
else {
	send_color("error", 0, 1, 0);
	echo("PHP socket error\n");
}

function send_color($mode, $red, $green, $blue) {
	// UPDATE THIS IP IF THE SERVER MOVED OR CHANGED
	$server = "192.168.1.140";
	$fp = fsockopen($server, 10250, $errno, $errstr, 30);


	if (!$fp) { echo"$errstr ($errno)<br />\n"; }
	else {
		fwrite($fp, $mode . "," . $red . "," . $green . "," . $blue); // prepare packet
		fclose($fp); // send packet
	}
}

?>
