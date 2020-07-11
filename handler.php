<?php

if (isset($_GET['mode']) and isset($_GET['red']) and isset($_GET['green']) and isset($_GET['blue'])) {
	send_color($_GET['mode'], $_GET['red'], $_GET['green'], $_GET['blue']);
}
elseif (isset($_GET['mode'])) {
	if     ($_GET['mode'] == "rainbow")			{ send_color("rainbow", "0", "0", "0"); }
	elseif ($_GET['mode'] == "pride")			{ send_color("pride", "0", "0", "0"); }
	elseif ($_GET['mode'] == "strobe")			{ send_color("strobe", "0", "0", "0"); }
	elseif ($_GET['mode'] == "rainbowChase")	{ send_color("rainbowChase", "0", "0", "0"); }
}
else {
	send_color("error", 0, 1, 0);
	echo("PHP socket error\n");
}

function send_color($mode, $red, $green, $blue) {
	// UPDATE THIS IP IF THE SERVER MOVED OR CHANGED
	$server = "192.168.0.168";
	$fp = fsockopen($server, 10250, $errno, $errstr, 30);


	if (!$fp) { echo"$errstr ($errno)<br />\n"; }
	else {
		fwrite($fp, $mode . "," . $red . "," . $green . "," . $blue); // prepare packet
		fclose($fp); // send packet
	}
}

?>
