var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on( 'connect', function() {
  var form = $('#getPlayer').on( 'submit', function( e ) {
    e.preventDefault()
    let user_name = $( 'input.name' ).val()
    socket.emit('new user', user_name)
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

socket.on( 'success', function() {
  console.log("console success")
  $('#content').html("game has started, game.state set to bidding")
})