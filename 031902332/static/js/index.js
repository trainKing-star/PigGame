$(document).ready(function(){
    var $container = document.getElementById('container');
    var deck = Deck();
    deck.mount($container);
    deck.flip();
    deck.intro();

    background_index();

    setInterval(background_index, 154 * 1000);

    function background_index(){
        let playerc = $("#jplayer");
        if (playerc.data().jPlayer && playerc.data().jPlayer.internal.ready === true) {
            playerc.jPlayer("setMedia", {
                mp3: "static/background_index.mp3"
            }).jPlayer("play");//jPlayer("play") 用来自动播放
        }else {
            playerc.jPlayer({
                ready: function() {
                    $(this).jPlayer("setMedia", {
                        mp3: "static/background_index.mp3" //同上
                    }).jPlayer("play");//同上
                },
                swfPath: "node_modules/jPlayer/dist/jplayer/jquery.jplayer.swf",
                supplied: "mp3"  //acc属于M4A
            });
        }
    }
});