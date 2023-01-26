// var toDay = new Date().getTime();
// JS vs GG
// if(toDay>new Date("Dec 6, 2022 15:00:00").getTime() && toDay<new Date("Dec 6, 2022 19:30:00").getTime())
document.getElementById("data").innerHTML = '<table ><tr><td style="width: 110px; height: 110px;"><center><h1 id="day"></h1></center></td><td style="width: 110px; height: 110px;"><center><h1 id="hour"></h1></center></td><td style="width: 110px; height: 110px;"><center><h1 id="min"></h1></center></td><td style="width: 110px; height: 110px;"><center><h1 id="sec"></h1></center></td></tr></table>';


// Set the date we're counting down to
var countDownDate = new Date("Dec 6, 2022 15:00:00").getTime();
var todayis = new Date().getTime()
var count = 1;


// Update the count down every 1 second
if (todayis < new Date("Dec 6, 2022 15:00:00").getTime()) {
    var x = setInterval(function () {
        //today's date and time
        var now = new Date().getTime();

        if (now < new Date("Dec 6, 2022 15:00:00").getTime()) {

            document.getElementById("discription").innerHTML = "<h3>LPL 2022 Will Begin in</h3>";
            //distance between now and the count down date
            var distance = countDownDate - now;

            //time calculations for days, hours, minutes and seconds
            var days = Math.floor(distance / (1000 * 60 * 60 * 24));
            var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            var seconds = Math.floor((distance % (1000 * 60)) / 1000);

            // display the result in the element with id="countdown"
            document.getElementById("day").innerHTML = days + "d ";
            document.getElementById("hour").innerHTML = hours + "h ";
            document.getElementById("min").innerHTML = minutes + "m ";
            document.getElementById("sec").innerHTML = seconds + "s ";

        }

    }, 1000)

} else {
    if (todayis < new Date("Dec 23, 2022 19:30:00").getTime()) {
        document.getElementById("discription").innerHTML = "<br>";
        document.getElementById("data").innerHTML ="Updating...";

    } else {
        document.getElementById("discription").innerHTML = "<h3>LPL 2021 Champions</h3>";
        document.getElementById("data").innerHTML = '<h1>Jaffna Kings</h1>';
    }
}
