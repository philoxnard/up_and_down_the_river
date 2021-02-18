var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on( 'connect', function() {
  var form = $('#getPlayer').on( 'submit', function( e ) {
    e.preventDefault()
    let user_name = $( 'input.name' ).val()
    console.log(socket.id)
    socket.emit('new user', user_name, socket.id)
    $('#content').html('<form id="start"><input type="submit" value="ready"/></form>')
  
  var start = $('#start').on('submit', function(){
    $('#content').html("placeholder")
    socket.emit("game start")
    })
  })
}) 

socket.on( 'player_added', function(players) {
  console.log(players)
})


socket.on("deal hand", function(hand) {
  console.log(hand)
  for (var card in hand) {
    let value = card
    let suit = hand[card]
    if (suit == "&clubsuit;" || suit == "&spadesuit;"){
      var color = "black"
    }
    else{
      var color = "red"
    }
    $('#content').html('<div class="'+color+' card">\
                        <div class="top">'+value+' '+suit+'</div>\
                        <h1>'+suit+'</h1>\
                        <div class="bottom">'+value+' '+suit+'</div>\
                        </div>')
  }
})