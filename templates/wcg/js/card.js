var pcd = [0, 0, 0, 0, 0, 0, 0, 0];
var pcard = 0;
var a = 0, b = 0, d = 0, blood = 0;
var skip=false;
function show(x) {
    if (x != 0) document.getElementById("c" + x.toString()).style = "transform:scaleX(1.1) scaleY(1.1); -webkit-transform:scaleX(1.1) scaleY(1.1); -moz-transform:scaleX(1.1) scaleY(1.1); animation-duration: .5s; animation-timing-function: ease;";
    else {
        document.getElementById("c1").style = "transform:scaleX(1) scaleY(1); -webkit-transform:scaleX(1) scaleY(1); -moz-transform:scaleX(1) scaleY(1);";
        document.getElementById("c2").style = "transform:scaleX(1) scaleY(1); -webkit-transform:scaleX(1) scaleY(1); -moz-transform:scaleX(1) scaleY(1);";
        document.getElementById("c3").style = "transform:scaleX(1) scaleY(1); -webkit-transform:scaleX(1) scaleY(1); -moz-transform:scaleX(1) scaleY(1);";
        document.getElementById("c4").style = "transform:scaleX(1) scaleY(1); -webkit-transform:scaleX(1) scaleY(1); -moz-transform:scaleX(1) scaleY(1);";
        document.getElementById("c5").style = "transform:scaleX(1) scaleY(1); -webkit-transform:scaleX(1) scaleY(1); -moz-transform:scaleX(1) scaleY(1);";
        document.getElementById("c6").style = "transform:scaleX(1) scaleY(1); -webkit-transform:scaleX(1) scaleY(1); -moz-transform:scaleX(1) scaleY(1);";
    }
    var tmp;
    if (x == 0) tmp = "img/0.png";
    if (x == 1) tmp = document.getElementById('c1').src;
    if (x == 2) tmp = document.getElementById('c2').src;
    if (x == 3) tmp = document.getElementById('c3').src;
    if (x == 4) tmp = document.getElementById('c4').src;
    if (x == 5) tmp = document.getElementById('c5').src;
    if (x == 6) tmp = document.getElementById('c6').src;
    document.getElementById('big').src = tmp;
    bigger(3, 2);
}
function bigger(h, w) { //大屏显示由小变大特效
    if (h >= 453) return;
    document.getElementById('big').height = h;
    document.getElementById('big').width = w;
    setTimeout(function () {
        bigger(h + 6, w + 4);
    }, 2);
}
function insert(i, n) { //在玩家手牌第i个的位置插入第n张卡牌
    if(n==0){
        document.getElementById('c'+i.toString()).className="non";
        setTimeout(function(){
            document.getElementById('c'+i.toString()).src="img/0.png";
        },500);
        return;
    }
    document.getElementById('c'+i.toString()).className="new";
    setTimeout(function(){document.getElementById("c"+i.toString()).style.opacity="1.0";},500);
    document.getElementById('c'+i.toString()).src = "img/" + ("" + n) + ".png";
}
function update(){
    if(skip==true){
        document.getElementById('waiting').style.display = 'block';
        return;
    }
    document.getElementById('waiting').style.display = 'none';
    for(var i=1;i<=6;i++){
        insert(i,pcd[i]);
    }
    document.getElementById('a').innerHTML = a;
    document.getElementById('b').innerHTML = b;
    document.getElementById('d').innerHTML = d;
    document.getElementById('bl').innerHTML = blood;
}

