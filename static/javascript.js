var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on( 'connect', function() {
  var form = $( 'form' ).on( 'submit', function( e ) {
    e.preventDefault()
    let user_name = $( 'input.name' ).val()
    socket.emit( 'my event', user_name)
    // $( 'form' ).replaceWith(
    //     <form action="" method="POST">
    //         <input type="submit" value="Click when all players are in the game"/>
    //     </form>
    //)
  } )
} )
