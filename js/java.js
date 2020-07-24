
// Send XMLHttpRequest to update light strip via php
// Input: param in format "mode=someMode&red=int&green=int&blue=int"
function request(param) {
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
    
    // Send request
	request("mode=static"+"&red="+r+"&green="+g+"&blue="+b);
};

// Set light strip to some animated mode
function animate(mode) {

    // Show animation speed slider because an animation is selected
    var t = document.getElementById("animationSpeedSlider");
    if (t.classList.contains("hide")) {
        t.classList.remove("hide");
    }

    if (isNaN(mode)) {
        // Send request with empty values for red, green, and blue
        request("mode="+mode+"&red=0&green=0&blue=0");
    } else {
        request("mode=speed"+"&red="+mode+"&green=0&blue=0");
    }

	console.log("ANIMATE\t", mode);
	
};

// Update light strip based on slider states
function sliderUpdate(h, s, v) {
	// Convert HSV input to RGB then call static to set color
	let rgb = HSVtoRGB(h, (s/100), (v/100));
	static(rgb.r, rgb.g, rgb.b);
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
