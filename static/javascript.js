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
  socket.emit("round start")
})

$("#content").on("submit", "#getBid", function(e){
  e.preventDefault()
  let bid = $('input.bid').val()
  $("#getBid").remove()
  console.log(bid)
  socket.emit("receive bid", bid, socket.id)
})

socket.on("deal hand", function(hand) {
  let shownHand = showHand(hand)
  $('#content').html(shownHand)
  socket.emit("request bid")
})

socket.on("make bid field", function(){
  let bidField = getBidField()
  $('#content').append(bidField)
})

socket.on("get next bid", function(){
  socket.emit("request bid")
})

// This is the next function to work on
socket.on("begin play", function(){
  $("#content").append("Its your turn to play a card")
})

function getTrump(hand){
  let trump = hand["trump"]
  let trumpValue = trump[0]
  let trumpSuit = trump[1]
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
    let index = 0
    let value = card
    let suit = hand[card]
    let color
    if (suit == "&clubsuit;" || suit == "&spadesuit;"){
      color = "black"
    }
    else{
      color = "red"
    }
    handArray+=('<div class="'+color+' card id='+index+'">\
                <div class="top">'+value+' '+suit+'</div>\
                <h1>'+suit+'</h1>\
                <div class="bottom">'+value+' '+suit+'</div>\
                </div>')
    index += 1
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
  delete hand["trump"]
  let handArray = getHandArray(hand)
  let showHand ='hand:'+handArray+'<br><br>'+'trump card:'+trumpCard+'<br><br>'
  return showHand
}
