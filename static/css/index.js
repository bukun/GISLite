
    $(document).ready(function(){
var speed = 50; //数字越大速度越慢
var tab = document.getElementById("demo");
var tab1 = document.getElementById("demo1");
var tab2 = document.getElementById("demo2");
tab2.innerHTML = tab1.innerHTML;
function Marquee() {
if (tab2.offsetWidth - tab.scrollLeft <= 0)
tab.scrollLeft -= tab1.offsetWidth
else {
tab.scrollLeft++;
}
}
var MyMar = setInterval(Marquee, speed);
tab.onmouseover = function () {
clearInterval(MyMar)
};
tab.onmouseout = function () {
MyMar = setInterval(Marquee, speed)
};
        });

