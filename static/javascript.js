var socket = io.connect('http://' + document.domain + ':' + location.port);

// Listens for the submit event for a player joining the game
// Instantiates the player, then creates a button to start the game
$('#content').on("submit", "#getPlayer", function(e) {
  e.preventDefault()
  let user_name = $( 'input.name' ).val()
  console.log(socket.id)
  socket.emit('new user', user_name, socket.id)
  $('#info').html('<form action="" id="start">\
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
  console.log(index)
  socket.emit("play card", index, socket.id)
  $("#info").html("")
})

// When someone clicks the "continue" button after a trick is done, this will 
// bounce info back to the server, which will then determine whether to continue to
// the next trick, or to start a new round.
$("#content").on("submit", "#continue", function(e){
  e.preventDefault()
  $("#info").html("")
  socket.emit("continue")
})

// Takes each player's hand and displays it to each respective client
// Also shows the trump card to each client
socket.on("deal hand", function(hand) {
  let trumpCard = getTrump(hand)
  delete hand["trump"]
  let shownHand = showHand(hand)
  $("#info").html("")
  $('#hand').html(shownHand)
  $("#trump").html("Trump card is: "+trumpCard)
  $("#trick").html("")
  socket.emit("request bid")
})

// Displays a text field where the player may input their bid
// only displays to whoever's turn it is
socket.on("make bid field", function(){
  let bidField = getBidField()
  $('#info').append(bidField)
})

// Quick bounce from server to client back to server
// Passes the bid to whoever is next in line
socket.on("get next bid", function(){
  socket.emit("request bid")
})

// Function to display a table with all the player's bids. Generated and updated
// After each player submits their bid
// TODO: Will likely need to pass index along in the bids obj and do this the 
//        same way that I did the showHand function to get it in the right order
socket.on("show bidTable", function(bids){ 
  let bidTable = "<table>\
                    <tr>\
                      <th>Player</th>\
                      <th>Bid</th>\
                    </tr>"
  for (bid in bids){
    let player = bids[bid]
    bidTable += " <tr>\
                    <td>"+player+"</td>\
                    <td>"+bid+"</td>\
                  </tr>"
  }
  $("#bidTable").html(bidTable+"</table>")
})

// After playing a card, this updates the client's view to what cards are still in
// their hand. 
socket.on("update hand", function(hand){
  let handArray = getHandArray(hand)
  let shownHand = 'hand:'+handArray
  $("#hand").html(shownHand)
})

// Appends a simple string indicating whose turn it is
// Only appears for whoever's turn it is
socket.on("your turn", function(){
  $("#info").html("Its your turn to play a card")
})

// Shows the current trick to everybody
socket.on("show trick", function(trick){
  console.log("trying to show trick")
  let trickArray = ""
  for (let name in trick){
    let color
    let value = trick[name][0]
    let suit = trick[name][1]
    if (suit == "&clubsuit;" || suit == "&spadesuit;"){
      color = "black"
    }
    else{
      color = "red"
    }
    trickArray += (name+'\'s card:\
                    <div class="'+color+' hand card">\
                    <div class="top">'+value+' '+suit+'</div>\
                    <h1>'+suit+'</h1>\
                    <div class="bottom">'+value+' '+suit+'</div>\
                    </div>')
  }
  $("#trick").html(trickArray)
})

// Function that gets called when a trick has ended
// Generates a button that allows the users to proceed to the next trick
socket.on("end trick", function(msg){
  $("#info").html("The trick has ended. "+msg)
  $("#info").append('<form action="" id="continue">\
                      <input type="submit" value="Continue">\
                    </form>')
})

socket.on("update trick table", function(tricks){
  let trickTable = "<table>\
                    <tr>\
                      <th>Player</th>\
                      <th>Tricks Won</th>\
                    </tr>"
  for (trick in tricks){
    let player = tricks[trick]
    trickTable += " <tr>\
                    <td>"+player+"</td>\
                    <td>"+trick+"</td>\
                  </tr>"
  }
  $("#trickTable").html(trickTable+"</table>")  
})

// Simple bounce function if the continue button gets clicked at the end
// of a round. Bounces back to the round start server function
socket.on("restart round", function(){
  $("#bidTable").html("")
  $("#trickTable").html("")
  socket.emit("round start")
})

// Function called when going between tricks within the same round
// Clears out the current trick display on the table, clears the info section
// Then, bounces back to server to allow play to continue
socket.on("next trick", function(){
  $("#info").html("")
  $("#trick").html("")
  socket.emit("new trick")
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
  for (let index = 0; index<Object.keys(hand).length; index++) {
    var cardInfo = hand[index]
    let value = cardInfo[0]
    let suit = cardInfo[1]
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
  let handArray = getHandArray(hand)
  let showHand ='hand:'+handArray
  return showHand
}
