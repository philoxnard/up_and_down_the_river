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


// TODO: Clean up this monster function, its huge. 
// TODO: Still need to figure how how input is going to work.

socket.on("deal hand", function(hand) {
  console.log(hand)
  let trumpValue = Object.keys(hand)[0]
  let trumpSuit = hand[trumpValue]
  delete hand[trumpValue]
  let handArray = ""
  if (trumpSuit == "&clubsuit;" || trumpSuit == "&spadesuit;"){
    trumpColor = "black"
  }
  else{
    trumpColor = "red"
  }
  trumpCard = ('<div class="'+trumpColor+' card">\
              <div class="top">'+trumpValue+' '+trumpSuit+'</div>\
              <h1>'+trumpSuit+'</h1>\
              <div class="bottom">'+trumpValue+' '+trumpSuit+'</div>\
              </div>')
  for (var card in hand) {
    let value = card
    let suit = hand[card]
    let color
    if (suit == "&clubsuit;" || suit == "&spadesuit;"){
      color = "black"
    }
    else{
      color = "red"
    }
    handArray+=('<div class="'+color+' card">\
                <div class="top">'+value+' '+suit+'</div>\
                <h1>'+suit+'</h1>\
                <div class="bottom">'+value+' '+suit+'</div>\
                </div>')
  let bidField = "<form>\
                  <input type='text'\
                  placeholder='Input your bid'>\
                  <input type='submit'\
                  value='Submit'>"
  $('#content').html(handArray+'<br>'+bidField+'<br>'+trumpCard)
  }
})