var socket = io.connect('http://' + document.domain + ':' + location.port);

$('#content').on("submit", "#getPlayer", function(e) {
  e.preventDefault()
  let user_name = $( 'input.name' ).val()
  console.log(socket.id)
  socket.emit('new user', user_name, socket.id)
  $('#content').html('<form action="" id="start">\
                        <input type="submit" value="Start the game">\
                      </form>')  
})

$("#content").on("submit", "#start", function(e){
  e.preventDefault()
  $('#content').html("placeholder")
  socket.emit("game start")
})

$("#content").on("submit", "#getBid", function(e){
  e.preventDefault()
  let bid = $('input.bid').val()
  console.log(bid)
  socket.emit("receive bid", bid, socket.id)
})

socket.on('player_added', function(players) {
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
                    <input type='submit' value='Submit'>\
                  </form>"
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
// TODO: BUG FIX: Sometimes the cards don't display in the right place, no idea why

socket.on("deal hand", function(hand) {
  let shownHand = showHand(hand)
  $('#content').html(shownHand)
})