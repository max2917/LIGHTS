
// Send XMLHttpRequest to update light strip via php
// Input: param in format "mode=someMode&red=int&green=int&blue=int"
function request(param) {

    // Append to param which devices
    let desk = document.getElementById("desk").checked;
    let doctorWho = document.getElementById("doctorWho").checked;
    let pc = document.getElementById("pc").checked;
    let window = document.getElementById("window").checked;

    param = param+"&desk="+desk+"&doctorWho="+doctorWho+"&pc="+pc+"&window="+window;
    console.log("javascript: ", param);

	var xhr = new XMLHttpRequest();
	xhr.open("GET", "handler.php?"+param, true);
	xhr.send();
};

// Set entire light strip to a static color
// Inputs: R, G, B as 0...255
function static(r, g, b) {

    // Hide animation speed slider because a static option is selected
    var t = document.getElementById("animationSpeedSlider");
    if (!t.classList.contains("hide")) {
        t.classList.add("hide");
    }
	
	updateSlider(r, g, b)
    
    // Send request
	request("mode=static"+"&red="+r+"&green="+g+"&blue="+b);
};
function updateSlider(r, g, b) {
    // Dynamically update the state of the sliders before sending
	let hSlider	= document.getElementById("hSlide");    // Get sliders
	let sSlider	= document.getElementById("sSlide");
	let vSlider	= document.getElementById("vSlide");
	let HSV = RGBtoHSV(r, g, b);                        // Convert values to HSV
	hSlider.value = `${HSV.h}`;                         // Set new slier positions
	sSlider.value = `${HSV.s}`;
	vSlider.value = `${HSV.v}`;
	
    // Calculate adjusted RGB for SV slider gradients to preserve 100% S and V
    let adjRGB = HSVtoRGB(HSV.h, 1, 1);
	sSlider.style.background = `linear-gradient(to right, white, rgb(${adjRGB.r}, ${adjRGB.g}, ${adjRGB.b}))`;
    vSlider.style.background = `linear-gradient(to right, black, rgb(${adjRGB.r}, ${adjRGB.g}, ${adjRGB.b}))`;

    // white panel with S controlled transparency
    // black panel with V controlled transparency
	// NOTE: hSlider.style must be updated to be equal to the buttonHeight
    //  variable in style.css
    let lightness = 50+(sSlider.value/2);   // S and V adjusted to prevent full wash/blackout of slider colors
    let brightness = 50+(vSlider.value/2);
    hSlider.style.boxShadow  = `inset 0 150px 0 0 rgba(255, 255, 255, ${(1-(lightness/100))}), inset 0 150px 0 0 rgba(0, 0, 0, ${(1-(brightness/100))})`;
    sSlider.style.boxShadow  = `inset 0 150px 0 0 rgba(255, 255, 255, ${(1-(lightness/100))}), inset 0 150px 0 0 rgba(0, 0, 0, ${(1-(brightness/100))})`;
    vSlider.style.boxShadow  = `inset 0 150px 0 0 rgba(255, 255, 255, ${(1-(lightness/100))}), inset 0 150px 0 0 rgba(0, 0, 0, ${(1-(brightness/100))})`;
}

// Set light strip to some animated mode
function animate(mode) {

    // Show animation speed slider because an animation is selected
    var speedSlider = document.getElementById("animationSpeedSlider");
    if (speedSlider.classList.contains("hide")) {
        speedSlider.classList.remove("hide");
    }

    if (isNaN(mode)) {
        // Send request with empty values for green, and blue with speed value in red
        request("mode="+mode+"&red="+speedSlider.value+"&green=0&blue=0");
    } else {
        request("mode=speed"+"&red="+mode+"&green=0&blue=0");
    }

	console.log("ANIMATE\t", mode);
	
};

gradientLeftState = false;
gradientRightState = false;
gradientBarState = true;
gradientLeftColor = { r: 0, g: 0, b: 255 };
gradientRightColor = { r: 255, g: 0, b: 255 };

// Set light strip to some gradient animation mode
function sendGradient() {
    requestString = "mode=gradient"+"&red="+gradientLeftColor.r+"/"+gradientLeftColor.g+"/"+gradientLeftColor.b+"&green="+gradientRightColor.r+"/"+gradientRightColor.g+"/"+gradientRightColor.b+"&blue="
    if (gradientBarState) { requestString += "1" }
    else { requestString += "0"}
    console.log(requestString);
    request(requestString);
}
function gradientBAR() {
    let BAR = document.getElementById("gradientBAR");
    let BARPREVIEW = document.getElementById("gradientPREVIEW");
    if (gradientBarState == true) {
        BAR.style.background = `#000`;
        BAR.style.color = `rgb(250, 250, 250)`;
        gradientBarState = false;
        updateGradientPreview();
    }
    else {
        BAR.style.background = `rgb(250, 250, 250)`;
        BAR.style.color = `#111111`;
        gradientBarState = true;
        updateGradientPreview();
    }
}
function gradientLEFTclicked(rgb) {
    if (typeof rgb !== 'undefined') { gradientLeftColor = rgb; }
    let LEFT = document.getElementById("gradientLEFT");
    if (gradientLeftState == false) {
        LEFT.style.boxShadow = `0px 0px 20px rgb(0, 255, 255)`;
        gradientLeftState = true;
    }
    else {
        LEFT.style.boxShadow = `0px 0px 0px rgba(0, 0, 0, 0)`;
        gradientLeftState = false;
    }

    // Update button color
    LEFT.style.background = `
        linear-gradient(
            to bottom,
            rgb(250, 250, 250),
            rgb(250, 250, 250) 90%,
            rgba(0, 0, 0, 0) 90%
        ),
        linear-gradient(
            to right,
            rgb(${gradientLeftColor.r}, ${gradientLeftColor.g}, ${gradientLeftColor.b}),
            rgb(${gradientLeftColor.r}, ${gradientLeftColor.g}, ${gradientLeftColor.b}) 100%
        )
    `;
}
function gradientRIGHTclicked(rgb) {
    if (typeof rgb !== 'undefined') { gradientRightColor = rgb; }
    let RIGHT = document.getElementById("gradientRIGHT");
    if (gradientRightState == false) {
        RIGHT.style.boxShadow = `0px 0px 20px rgb(0, 255, 255)`;
        gradientRightState = true;
    }
    else {
        RIGHT.style.boxShadow = `0px 0px 0px rgba(0, 0, 0, 0)`;
        gradientRightState = false;
    }

    // Update button color
    RIGHT.style.background = `
        linear-gradient(
            to bottom,
            rgb(250, 250, 250),
            rgb(250, 250, 250) 90%,
            rgba(0, 0, 0, 0) 90%
        ),
        linear-gradient(
            to right,
            rgb(${parseInt(gradientRightColor.r, 10)}, ${parseInt(gradientRightColor.g, 10)}, ${parseInt(gradientRightColor.b, 19)}),
            rgb(${parseInt(gradientRightColor.r, 10)}, ${parseInt(gradientRightColor.g, 10)}, ${parseInt(gradientRightColor.b, 19)}) 100%
        )
    `;
}
function updateLEFTbutton(rgb) {
    let LEFT = document.getElementById("gradientLEFT");
    if (typeof rgb !== 'undefined') { gradientLeftColor = rgb; }
    // Update button color
    LEFT.style.background = `
        linear-gradient(
            to bottom,
            rgb(250, 250, 250),
            rgb(250, 250, 250) 90%,
            rgba(0, 0, 0, 0) 90%
        ),
        linear-gradient(
            to right,
            rgb(${parseInt(gradientLeftColor.r, 10)}, ${parseInt(gradientLeftColor.g, 10)}, ${parseInt(gradientLeftColor.b, 19)}),
            rgb(${parseInt(gradientLeftColor.r, 10)}, ${parseInt(gradientLeftColor.g, 10)}, ${parseInt(gradientLeftColor.b, 19)}) 100%
        )
    `;
    updateSlider(rgb.r, rgb.g, rgb.b);
    updateGradientPreview();
}
function updateRIGHTbutton(rgb) {
    let RIGHT = document.getElementById("gradientRIGHT");
    if (typeof rgb !== 'undefined') { gradientRightColor = rgb; }
    // Update button color
    RIGHT.style.background = `
        linear-gradient(
            to bottom,
            rgb(250, 250, 250),
            rgb(250, 250, 250) 90%,
            rgba(0, 0, 0, 0) 90%
        ),
        linear-gradient(
            to right,
            rgb(${parseInt(gradientRightColor.r, 10)}, ${parseInt(gradientRightColor.g, 10)}, ${parseInt(gradientRightColor.b, 19)}),
            rgb(${parseInt(gradientRightColor.r, 10)}, ${parseInt(gradientRightColor.g, 10)}, ${parseInt(gradientRightColor.b, 19)}) 100%
        )
    `;
    updateSlider(rgb.r, rgb.g, rgb.b);
    updateGradientPreview();
}
function updateGradientPreview() {
    let PREVIEW = document.getElementById("gradientPREVIEW");
    if (gradientBarState == true) {
        PREVIEW.style.background = `
            linear-gradient(
                to right,
                rgba(0, 0, 0, 0) 33.3%,
                rgba(255, 255, 255, 1) 33.3%,
                rgba(255, 255, 255, 1) 66.6%,
                rgba(0, 0, 0, 0) 66.6%
            ),
            linear-gradient(
                to right,
                rgb(${parseInt(gradientLeftColor.r, 10)}, ${parseInt(gradientLeftColor.g, 10)}, ${parseInt(gradientLeftColor.b, 19)}),
                rgb(${parseInt(gradientRightColor.r, 10)}, ${parseInt(gradientRightColor.g, 10)}, ${parseInt(gradientRightColor.b, 19)}) 100%
            )
        `;
    }
    else {
        PREVIEW.style.background = `
            linear-gradient(
                to right,
                rgb(${parseInt(gradientLeftColor.r, 10)}, ${parseInt(gradientLeftColor.g, 10)}, ${parseInt(gradientLeftColor.b, 19)}),
                rgb(${parseInt(gradientRightColor.r, 10)}, ${parseInt(gradientRightColor.g, 10)}, ${parseInt(gradientRightColor.b, 19)}) 100%
            )
        `;
    }
    sendGradient();
}

// Update light strip based on slider states
function sliderUpdate(h, s, v) {
    // Convert HSV input to RGB then call static to set color
    //  unless sliders are being used to set gradients
	let rgb = HSVtoRGB(h, (s/100), (v/100));
    if (gradientLeftState == false && gradientRightState == false) {
        static(rgb.r, rgb.g, rgb.b);
    }
    else {
        if (gradientLeftState == true) { updateLEFTbutton(rgb); }
        if (gradientRightState == true) { updateRIGHTbutton(rgb); }
        //sendGradient();
    }
};

// Convert HSV inputs to RGB
// Inputs: h [0, 360], s, v [0, 1]
// Output: r, g, b [0, 255]
function HSVtoRGB(h, s, v) {
	let f = (n, k = (n+h/60)%6) => v - v*s*Math.max(Math.min(k, 4-k, 1), 0);
	return { r: 255*f(5), g: 255*f(3), b: 255*f(1) }
};

// Covert RGB inputs to HSV
function RGBtoHSV(r, g, b) {
    let rabs, gabs, babs, rr, gg, bb, h, s, v, diff, diffc, percentRoundFn;
    rabs = r / 255;
    gabs = g / 255;
    babs = b / 255;
    v = Math.max(rabs, gabs, babs),
    diff = v - Math.min(rabs, gabs, babs);
    diffc = c => (v - c) / 6 / diff + 1 / 2;
    percentRoundFn = num => Math.round(num * 100) / 100;
    if (diff == 0) {
        h = s = 0;
    } else {
        s = diff / v;
        rr = diffc(rabs);
        gg = diffc(gabs);
        bb = diffc(babs);

        if (rabs === v) {
            h = bb - gg;
        } else if (gabs === v) {
            h = (1 / 3) + rr - bb;
        } else if (babs === v) {
            h = (2 / 3) + gg - rr;
        }
        if (h < 0) {
            h += 1;
        }else if (h > 1) {
            h -= 1;
        }
    }
    return {
        h: Math.round(h * 360),
        s: percentRoundFn(s * 100),
        v: percentRoundFn(v * 100)
    };
};
