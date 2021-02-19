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

function getTrump(hand){
  let trumpValue = Object.keys(hand)[0]
  let trumpSuit = hand[trumpValue]
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
  return trumpCard
}

function getHandArray(hand){
  let handArray = ""
  console.log(hand)
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
  }
  return handArray
}

function getBidField(){
  let bidField = "<form action='' id='getBid' method='POST'>\
                  <input type='text' placeholder='Input your bid' class='bid'>\
                  <input type='submit' value='Submit'>"
  return bidField
}

function showHand(hand){
  console.log(hand)
  let trumpCard = getTrump(hand)
  delete hand[Object.keys(hand)[0]];
  let handArray = getHandArray(hand)
  let bidField = getBidField()
  let showHand ='hand:'+handArray+'<br>'+bidField+'<br>'+'trump card:'+trumpCard
  return showHand
}

// TODO: Still need to figure how how input is going to work.
// TODO: Eventually gonna have to refactor this document cause its getting big

socket.on("deal hand", function(hand) {
  let shownHand = showHand(hand)
  $('#content').html(shownHand)
})