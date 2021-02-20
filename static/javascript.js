var socket = io.connect('http://' + document.domain + ':' + location.port);

// Listens for the submit event for a player joining the game
// Instantiates the player, then creates a button to start the game
$('#content').on("submit", "#getPlayer", function(e) {
  e.preventDefault()
  let user_name = $( 'input.name' ).val()
  console.log(socket.id)
  socket.emit('new user', user_name, socket.id)
  $('#content').html('<form action="" id="start">\
                        <input type="submit" value="Start the game">\
                      </form>')  
})

// Listens for the submit event to start the game
// Sets game state to bidding and starts the game round
$("#content").on("submit", "#start", function(e){
  e.preventDefault()
  socket.emit("round start")
})

// Listens for the player's bid and sends it to server
// Only appears on screen for whoever's turn it is
$("#content").on("submit", "#getBid", function(e){
  e.preventDefault()
  let bid = $('input.bid').val()
  $("#getBid").remove()
  console.log(bid)
  socket.emit("receive bid", bid, socket.id)
})

// Listens for clicks on cards in the player's hand
// Only activates if it is the current player's turn, and if game state is "playing"
// Takes the clicked card and sends it through the game.play_card method
$("#content").on("click", ".hand", function(){
  let index = $(this).attr("id");
  socket.emit("play card", index, socket.id)
})

// Takes each player's hand and displays it to each respective client
// Also shows the trump card to each client
socket.on("deal hand", function(hand) {
  let shownHand = showHand(hand)
  $('#content').html(shownHand)
  socket.emit("request bid")
})

// Displays a text field where the player may input their bid
// only displays to whoever's turn it is
socket.on("make bid field", function(){
  let bidField = getBidField()
  $('#content').append(bidField)
})

// Quick bounce from server to client back to server
// Passes the bid to whoever is next in line
socket.on("get next bid", function(){
  socket.emit("request bid")
})

// After playing a card, this updates the client's view to what cards are still in
// their hand. 
socket.on("update hand", function(hand){
  let handArray = getHandArray(hand)
  let shownHand ='hand:'+handArray
  $("#content").html(shownHand)
  // TODO: Alter both this code here and the general code on how a hand is displayed
  // TODO: to make it so that updating the hand only replaces a hand div that's inside
  // TODO: the content div. There should be a hand div, a trump div, and maybe
  // TODO: a bid div, as well as some other informational divs to add in there later
  // TODO: like name, score, whose turn it is, what everyone else has bid so far.
})

// Appends a simple string indicating whose turn it is
// Only appears for whoever's turn it is
socket.on("your turn", function(){
  $("#content").append("Its your turn to play a card")
})

// Function to receive the trump from the server.
// The trump card is sent as part of each player's hand so its data can be extracted
// Takes the player's hand object as an argument
// Returns a string of html that displays a card
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

// Function to receive the hand from the server
// The trump card gets removed before this card is called, so the remaineder
// of the hand is ready to be unpacked.
// Takes the player's hand object as an argument
// Returns a string of html that displays all the user's cards
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
    handArray+=('<div class="'+color+' hand card" id="'+index+'">\
                <div class="top">'+value+' '+suit+'</div>\
                <h1>'+suit+'</h1>\
                <div class="bottom">'+value+' '+suit+'</div>\
                </div>')
    index += 1
  }
  return handArray
}

// A function for creating the input field where a player will place their bid
// Returns a string of html that creates a submission field
function getBidField(){
  let bidField = "<form action='' id='getBid' method='POST'>\
                    <input type='text' placeholder='Input your bid' class='bid'>\
                    <input type='submit' value='Submit'>\
                  </form>"
  return bidField
}

// Function for executing the logic of how a player's hand is received from the server
// Takes the player's hand object as an argument
// Determines the trump card
// Removes the trump card from the hand object
// Converts the hand object into a long html string
// Returns a string of html that includes the player hand and the trump card
function showHand(hand){
  console.log(hand)
  let trumpCard = getTrump(hand)
  delete hand["trump"]
  let handArray = getHandArray(hand)
  let showHand ='hand:'+handArray+'<br><br>'+'trump card:'+trumpCard+'<br><br>'
  return showHand
}
