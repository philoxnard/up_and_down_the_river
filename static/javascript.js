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

// TODO: Emit to each player's individual room using that player.sid
socket.on( 'success', function(name) {
  console.log("console success")
  $('#content').html(name)
})