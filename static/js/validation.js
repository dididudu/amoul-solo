//<script>
function selectionne(id) {
  for (var i = 0; i < 81; i++) {
    var id2 = "d"+i;
    document.getElementById(id2).className = "";
  }
  document.getElementById(id).className = "selected";
}

function update(id) {
  for (var i = 1; i < 10; i++) {
    var id2 = ""+i;
    document.getElementById(id2).innerHTML = ""+i;
    document.getElementById(id2).className = "";
    if (id == id2) {
      document.getElementById(id2).innerHTML = "<b>"+i+"</b>";
      document.getElementById(id2).className = "selected";
    }
  }
  for (var j = 0; j < 81; j++) {
    var id3 = "d"+j;
    var id4 = "v"+j;
    if (document.getElementById(id3).className == "selected") {
      if (id == '0') {
        document.getElementById(id3).innerHTML = "";
        document.getElementById(id4).value = "0";
      } else {
        document.getElementById(id3).innerHTML = id;
        document.getElementById(id4).value = id;
      }
    }
  }
  for (var k = 1; k < 10; k++) {
    var c = "c"+k;
    var s = calc(k);
    //document.getElementById(c).innerHTML = s;
    //document.getElementById(c).className = "selected";
  }
}

function calc(i) {
  var cpt = 0;
  var s1 = "<b>"+i+"</b>";
  var s2 = ""+i;
  for (var j = 0; j < 81; j++) {
    var id = "d"+j;
    var c = document.getElementById(id).innerHTML;
    if (c == s1 || c == s2) {
      cpt = cpt + 1;
    }
  }
  return cpt;
}

function hide(id) {
  var id1 = id + "p";
  var id2 = id + "m";

  document.getElementById(id1).className = "visible";
  document.getElementById(id2).className = "hidden";

  document.getElementById(id).className = "hidden";
}

function show(id) {
  var id1 = id + "p";
  var id2 = id + "m";

  document.getElementById(id1).className = "hidden";
  document.getElementById(id2).className = "visible";

  document.getElementById(id).className = "visible";
}

function zip(id) {
  var z = "";
  for (var j = 0; j < 81; j++) {
    var id2 = "d"+j;
    var v = document.getElementById(id2).innerHTML;
    if (v == '<i>&nbsp;</i>') {
      z = z + '0';
    } else if (v == '<b>1</b>') {
      z = z + '1';
    } else if (v == '<b>2</b>') {
      z = z + '2';
    } else if (v == '<b>3</b>') {
      z = z + '3';
    } else if (v == '<b>4</b>') {
      z = z + '4';
    } else if (v == '<b>5</b>') {
      z = z + '5';
    } else if (v == '<b>6</b>') {
      z = z + '6';
    } else if (v == '<b>7</b>') {
      z = z + '7';
    } else if (v == '<b>8</b>') {
      z = z + '8';
    } else if (v == '<b>9</b>') {
      z = z + '9';
    } else {
      z = z + v;
    }
  }
  document.getElementById(id).innerHTML = z;
}
//-->
