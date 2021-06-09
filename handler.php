<?php

if (isset($_GET['mode']) and isset($_GET['red']) and isset($_GET['green']) and isset($_GET['blue']) and isset($_GET['desk']) and isset($_GET['doctorWho']) and isset($_GET['pc']) and isset($_GET['window'])) {
	send_color($_GET['mode'], $_GET['red'], $_GET['green'], $_GET['blue'], $_GET['desk'], $_GET['doctorWho'], $_GET['pc'], $_GET['window']);
}
else {
	send_color("error", 0, 1, 0, "true", "false", "false", "false");
	echo("PHP socket error\n");
}

function send_color($mode, $red, $green, $blue, $desk, $doctorWho, $pc, $window) {
	// UPDATE THESE IPS IF THE SERVERS MOVED OR CHANGED
	if ($desk == "true")		{ send_packet($mode, $red, $green, $blue, "192.168.1.140"); }
	if ($window == "true")		{ send_packet($mode, $red, $green, $blue, "192.168.1.141"); }
	if ($doctorWho == "true")	{ send_packet($mode, $red, $green, $blue, "192.168.1.142"); }
	if ($pc == "true")			{ send_packet($mode, $red, $green, $blue, "192.168.1.143"); }
}

function send_packet($mode, $red, $green, $blue, $address) {
	$server = "$address";
	$fp = fsockopen($server, 10250, $errno, $errstr, 30);

	if (!$fp) { echo"$errstr ($errno)<br />\n"; }
	else {
		fwrite($fp, $mode . "," . $red . "," . $green . "," . $blue); // prepare packet
		fclose($fp); // send packet
	}
}

?>
